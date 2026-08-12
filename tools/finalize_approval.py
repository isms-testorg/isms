#!/usr/bin/env python3
"""Finalize document approval metadata after an authorized review.

The workflow supplies pull-request reviews and members of the configured
approver team. This script only changes documents that are already `in_review`.
It never decides whether a review is sufficient by itself.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path

import yaml

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
LANGS = ("en", "de")


def flatten_pages(value: object) -> list[dict]:
    if not isinstance(value, list):
        return []
    if value and all(isinstance(item, list) for item in value):
        return [item for page in value for item in page if isinstance(item, dict)]
    return [item for item in value if isinstance(item, dict)]


def approved_approver(reviews: list[dict], members: list[dict], author: str) -> str | None:
    team_logins = {m.get("login") for m in members if m.get("login")}
    latest: dict[str, dict] = {}
    for review in reviews:
        login = (review.get("user") or {}).get("login")
        if login and login != author:
            latest[login] = review
    for login, review in latest.items():
        if login in team_logins and review.get("state") == "APPROVED":
            return login
    return None


def add_months(start: dt.date, months: int) -> dt.date:
    month = start.month - 1 + months
    year, month = start.year + month // 12, month % 12 + 1
    import calendar
    return dt.date(year, month, min(start.day, calendar.monthrange(year, month)[1]))


def finalize_documents(root: Path, approved_on: dt.date) -> list[Path]:
    paths = sorted(
        path for lang in LANGS for path in (root / "docs" / lang).rglob("*.md")
        if path.name.lower() != "readme.md"
    )
    if not paths:
        raise ValueError("no ISMS documents found")

    updates: list[tuple[Path, str, str]] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        if not match:
            raise ValueError(f"{path}: missing frontmatter")
        meta = yaml.safe_load(match.group(1)) or {}
        status = meta.get("status")
        if status == "approved":
            if meta.get("approved_on") and meta.get("next_review"):
                continue
            raise ValueError(f"{path}: approved document has incomplete approval dates")
        if status != "in_review":
            raise ValueError(f"{path}: expected status in_review, found {status!r}")
        cycle = meta.get("review_cycle_months")
        if not isinstance(cycle, int) or cycle <= 0:
            raise ValueError(f"{path}: invalid review_cycle_months")
        next_review = add_months(approved_on, cycle).isoformat()
        replacement = re.sub(r"(?m)^status: in_review$", "status: approved", match.group(1))
        replacement = re.sub(r"(?m)^approved_on:\s*$", f"approved_on: {approved_on.isoformat()}", replacement)
        replacement = re.sub(r"(?m)^next_review:\s*$", f"next_review: {next_review}", replacement)
        updates.append((path, text, FRONTMATTER_RE.sub(f"---\n{replacement}---\n", text, count=1)))

    for path, _, updated in updates:
        path.write_text(updated, encoding="utf-8")
    return [path for path, _, _ in updates]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reviews", type=Path, required=True)
    parser.add_argument("--team-members", type=Path, required=True)
    parser.add_argument("--author", required=True)
    parser.add_argument("--approved-on", required=True)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()

    reviews = flatten_pages(json.loads(args.reviews.read_text(encoding="utf-8")))
    members = flatten_pages(json.loads(args.team_members.read_text(encoding="utf-8")))
    approver = approved_approver(reviews, members, args.author)
    if not approver:
        print("No approved review from an eligible approver; nothing to do.")
        return 0
    try:
        approved_on = dt.date.fromisoformat(args.approved_on[:10])
        changed = finalize_documents(args.root, approved_on)
    except (ValueError, TypeError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"Approved by @{approver}; updated {len(changed)} document(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
