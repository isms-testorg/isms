#!/usr/bin/env python3
"""Open, update and close GitHub issues for documents whose review is due.

Clause 7.5.3 wants documented information to be reviewed and kept suitable.
Proving that in an audit means showing that reviews were triggered, tracked and
closed, which is exactly what an issue per overdue document gives you.

Idempotent: one open issue per document, matched on a marker in the body rather
than the title, so retitling an issue does not spawn a duplicate.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys

from isms import LANGS, add_months, as_date, load_docs

LABEL = "isms:review-due"
MARKER = "<!-- isms-review-doc:{doc_id} -->"
MARKER_RE = re.compile(r"<!--\s*isms-review-doc:([\w.-]+?)\s*-->")


def gh(args: list[str], check: bool = True) -> str:
    proc = subprocess.run(["gh", *args], capture_output=True, text=True)
    if check and proc.returncode != 0:
        raise SystemExit(f"gh {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def ensure_label() -> None:
    gh(["label", "create", LABEL, "--color", "B60205",
        "--description", "ISMS document review is due", "--force"], check=False)


def open_issues() -> dict[str, dict]:
    """{doc_id: issue} for open review issues, keyed by the body marker."""
    raw = gh(["issue", "list", "--label", LABEL, "--state", "open",
              "--limit", "200", "--json", "number,title,body"])
    out = {}
    for issue in json.loads(raw or "[]"):
        match = MARKER_RE.search(issue.get("body") or "")
        if match:
            out[match.group(1)] = issue
    return out


def due_documents(docs: dict, today: dt.date, horizon: int,
                  include_drafts: bool) -> dict[str, dict]:
    """Documents needing attention, with why."""
    due = {}
    for doc_id, doc in docs["en"].items():
        meta = doc["meta"] or {}
        if meta.get("status") == "retired":
            continue
        next_review = as_date(meta.get("next_review"))
        approved_on = as_date(meta.get("approved_on"))

        if meta.get("status") == "draft":
            # A draft that never gets approved is the quiet way an ISMS dies,
            # but while the ISMS is being written every document is a draft and
            # an issue for each one is pure noise. `make check` already lists
            # them, so this is opt in.
            if not include_drafts:
                continue
            reason = "still in draft and never approved"
            days = None
        elif next_review is None:
            reason = "approved but no next_review date is set"
            days = None
        else:
            days = (next_review - today).days
            if days < 0:
                reason = f"review overdue by {-days} days (was due {next_review.isoformat()})"
            elif days <= horizon:
                reason = f"review due in {days} days, on {next_review.isoformat()}"
            else:
                continue

        due[doc_id] = {
            "reason": reason,
            "days": days,
            "owner": str(meta.get("owner") or "").lstrip("@"),
            "title": meta.get("title", doc_id),
            "version": meta.get("version"),
            "next_review": next_review,
            "cycle": meta.get("review_cycle_months"),
            "paths": [docs[lang][doc_id]["relpath"] for lang in LANGS if doc_id in docs[lang]],
            "suggested": (add_months(today, meta["review_cycle_months"]).isoformat()
                          if isinstance(meta.get("review_cycle_months"), int) else "?"),
            "approved_on": approved_on,
        }
    return due


def body_for(doc_id: str, info: dict) -> str:
    files = "\n".join(f"- `{p}`" for p in info["paths"])
    return f"""{MARKER.format(doc_id=doc_id)}

**{info['title']}** (version {info['version']}) {info['reason']}.

Files to review, in **both** languages:

{files}

To close this issue, open a pull request that either confirms the document is
still correct or changes it, and in both language versions:

1. bump `version` in the frontmatter (patch for editorial, minor or major for a
   real change of meaning),
2. set `approved_on` to the date of approval,
3. set `next_review` to `approved_on` plus `review_cycle_months`
   ({info['cycle']} months, so roughly `{info['suggested']}`),
4. set `status: approved` and name the `approver`.

`make check` will reject the pull request if those dates do not line up. This
issue closes itself on the next scheduled run once the document is no longer
due.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--horizon-days", type=int, default=30,
                        help="how far ahead to warn (default 30)")
    parser.add_argument("--today", help="override today's date (YYYY-MM-DD)")
    parser.add_argument("--include-drafts", action="store_true",
                        help="also raise issues for documents never approved")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    today = as_date(args.today) or dt.date.today()
    docs = load_docs()
    due = due_documents(docs, today, args.horizon_days, args.include_drafts)

    if args.dry_run:
        for doc_id, info in sorted(due.items()):
            print(f"{doc_id}: {info['reason']} (owner {info['owner'] or 'unassigned'})")
        print(f"\n{len(due)} document(s) would have an open review issue")
        return 0

    ensure_label()
    existing = open_issues()

    created = updated = closed = 0
    for doc_id, info in sorted(due.items()):
        title = f"[review] {info['title']}"
        body = body_for(doc_id, info)
        if doc_id in existing:
            number = str(existing[doc_id]["number"])
            gh(["issue", "edit", number, "--title", title, "--body", body])
            updated += 1
        else:
            cmd = ["issue", "create", "--title", title, "--body", body, "--label", LABEL]
            if info["owner"] and not info["owner"].startswith("TODO"):
                cmd += ["--assignee", info["owner"]]
            print(gh(cmd).strip())
            created += 1

    for doc_id, issue in existing.items():
        if doc_id not in due:
            gh(["issue", "close", str(issue["number"]), "--comment",
                "Document is no longer due for review. Closed automatically."])
            closed += 1

    print(f"{created} created, {updated} updated, {closed} closed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
