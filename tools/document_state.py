#!/usr/bin/env python3
"""Derive document lifecycle metadata from GitHub and git history.

Document source files deliberately contain only stable metadata.  A pull
request is in review because GitHub says it is; an approved document version
is one merged through an approved pull request.  Keeping those facts out of
frontmatter prevents authors and bots from forging or accidentally invalidating
the approval record.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys

from isms import ROOT, add_months, load_docs


def run(*args: str) -> str:
    return subprocess.run(args, cwd=ROOT, check=True, capture_output=True,
                          text=True).stdout


def gh_json(path: str) -> object:
    return json.loads(run("gh", "api", path) or "null")


def document_paths(docs: dict, doc_id: str) -> list[str]:
    return [docs[lang][doc_id]["relpath"] for lang in ("en", "de") if doc_id in docs[lang]]


def changed_document_ids(docs: dict, base: str, head: str) -> set[str]:
    changed = set(run("git", "diff", "--name-only", base, head).splitlines())
    return {doc_id for doc_id in docs["en"] if changed.intersection(document_paths(docs, doc_id))}


def review_state(doc: dict) -> dict:
    return {
        "status": "in_review",
        "owner": doc["meta"]["owner"],
        "review_cycle_months": doc["meta"]["review_cycle_months"],
    }


def approval_state(doc: dict, pr: dict, reviews: list[dict]) -> dict:
    head = (pr.get("head") or {}).get("sha")
    author = ((pr.get("user") or {}).get("login") or "").lower()
    owner = str(doc["meta"]["owner"]).lstrip("@").lower()
    latest = {}
    for review in sorted(reviews, key=lambda r: r.get("submitted_at") or ""):
        login = ((review.get("user") or {}).get("login") or "").lower()
        if review.get("commit_id") == head and login != author:
            latest[login] = review
    approvals = [r for r in latest.values() if r.get("state") == "APPROVED"]
    if "/" not in owner:
        approvals = [r for r in approvals
                     if ((r.get("user") or {}).get("login") or "").lower() != owner]
    if not approvals:
        raise ValueError(f"PR #{pr.get('number')} has no valid final-head approval")
    approved = dt.datetime.fromisoformat(pr["merged_at"].replace("Z", "+00:00")).date()
    approver = max(approvals, key=lambda r: r.get("submitted_at") or "")["user"]["login"]
    return {
        "status": "approved",
        "owner": doc["meta"]["owner"],
        "approver": f"@{approver}",
        "approved_on": approved.isoformat(),
        "next_review": add_months(approved, doc["meta"]["review_cycle_months"]).isoformat(),
        "review_cycle_months": doc["meta"]["review_cycle_months"],
        "pull_request": pr["number"],
        "approved_revision": head,
    }


def merged_pr_for_commit(repository: str, commit: str) -> dict:
    prs = gh_json(f"repos/{repository}/commits/{commit}/pulls")
    merged = [pr for pr in prs if pr.get("merged_at")]
    if not merged:
        raise ValueError(f"commit {commit[:12]} is not associated with a merged pull request")
    return merged[0]


def release_states(docs: dict, repository: str) -> dict:
    states, pull_requests, reviews_by_pr = {}, {}, {}
    for doc_id, doc in docs["en"].items():
        commit = run("git", "log", "-1", "--format=%H", "--", *document_paths(docs, doc_id)).strip()
        if not commit:
            raise ValueError(f"{doc_id}: no commit found")
        pr = pull_requests.get(commit)
        if pr is None:
            pr = merged_pr_for_commit(repository, commit)
            pull_requests[commit] = pr
        reviews = reviews_by_pr.get(pr["number"])
        if reviews is None:
            reviews = gh_json(f"repos/{repository}/pulls/{pr['number']}/reviews")
            reviews_by_pr[pr["number"]] = reviews
        states[doc_id] = approval_state(doc, pr, reviews)
    return states


def write(path: str, mode: str, documents: dict) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"mode": mode, "documents": documents}, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(f"document lifecycle: {len(documents)} document(s) in {mode} mode")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write("## Document lifecycle\n\n")
            fh.write("| Document | Status | Owner | Approver | Approved | Next review |\n")
            fh.write("|---|---|---|---|---|---|\n")
            for doc_id, state in sorted(documents.items()):
                fh.write(f"| {doc_id} | {state.get('status', '')} | {state.get('owner', '')} | "
                         f"{state.get('approver', '')} | {state.get('approved_on', '')} | "
                         f"{state.get('next_review', '')} |\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--pr", action="store_true", help="mark documents changed between two refs in review")
    mode.add_argument("--release", action="store_true", help="derive approved state for every document")
    parser.add_argument("--base", help="base ref for --pr")
    parser.add_argument("--head", help="head ref for --pr")
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY"),
                        help="owner/name; required for --release")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    docs = load_docs()
    try:
        if args.pr:
            if not args.base or not args.head:
                parser.error("--pr requires --base and --head")
            states = {doc_id: review_state(docs["en"][doc_id])
                      for doc_id in changed_document_ids(docs, args.base, args.head)}
            write(args.out, "pr", states)
        else:
            if not args.repository:
                parser.error("--release requires --repository or GITHUB_REPOSITORY")
            write(args.out, "release", release_states(docs, args.repository))
    except (subprocess.CalledProcessError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
