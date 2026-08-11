#!/usr/bin/env python3
"""Commit files through the GitHub GraphQL API so the commit is signed.

Branch protection on main requires signed commits. A workflow that pushes with
`git push` produces an unsigned commit and would be rejected, so the usual
answer is to weaken the rule for bots. That puts a hole in exactly the chain of
custody this repository exists to prove.

`createCommitOnBranch` avoids the trade: GitHub creates the commit server side
and signs it with its own key, so the branch protection rule can stay on and
every commit in the history verifies.

Usage:
  tools/commit_via_api.py --branch isms/evidence-2026-08 \\
      --message "chore(evidence): GitHub configuration snapshot 2026-08" \\
      evidence/github/2026-08/members.json ...
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys


def gh_json(args: list[str], stdin: str | None = None) -> dict:
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, input=stdin)
    if proc.returncode != 0:
        raise SystemExit(f"gh {' '.join(args[:2])} failed: {proc.stderr.strip()}")
    return json.loads(proc.stdout or "{}")


def run(args: list[str]) -> str:
    proc = subprocess.run(args, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"{' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


MUTATION = """
mutation($input: CreateCommitOnBranchInput!) {
  createCommitOnBranch(input: $input) {
    commit { oid url }
  }
}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", required=True, help="branch to create and commit on")
    parser.add_argument("--message", required=True)
    parser.add_argument("--base", default="main", help="branch to fork from (default main)")
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY"))
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    if not args.repo:
        print("ERROR: pass --repo owner/name or set GITHUB_REPOSITORY", file=sys.stderr)
        return 2

    additions = []
    for path in args.files:
        if not os.path.isfile(path):
            print(f"ERROR: {path} is not a file", file=sys.stderr)
            return 2
        with open(path, "rb") as fh:
            additions.append({
                "path": os.path.relpath(path).replace(os.sep, "/"),
                "contents": base64.b64encode(fh.read()).decode("ascii"),
            })

    base_sha = run(["git", "rev-parse", args.base])

    # Create the branch if it is not there yet; reuse it if a previous run made
    # it, so a re-run updates the same pull request instead of piling up new ones.
    existing = subprocess.run(
        ["gh", "api", f"repos/{args.repo}/git/ref/heads/{args.branch}"],
        capture_output=True, text=True)
    if existing.returncode == 0:
        head_oid = json.loads(existing.stdout)["object"]["sha"]
        print(f"branch {args.branch} exists at {head_oid[:12]}")
    else:
        gh_json(["api", f"repos/{args.repo}/git/refs",
                 "-f", f"ref=refs/heads/{args.branch}", "-f", f"sha={base_sha}"])
        head_oid = base_sha
        print(f"created branch {args.branch} at {head_oid[:12]}")

    subject, _, body = args.message.partition("\n\n")
    variables = {
        "input": {
            "branch": {
                "repositoryNameWithOwner": args.repo,
                "branchName": args.branch,
            },
            "message": {"headline": subject, "body": body or ""},
            "fileChanges": {"additions": additions},
            "expectedHeadOid": head_oid,
        }
    }

    # --input reads the whole GraphQL body from stdin; the nested `input`
    # object cannot be expressed with -f key=value pairs.
    result = gh_json(
        ["api", "graphql", "--input", "-"],
        stdin=json.dumps({"query": MUTATION, "variables": variables}),
    )
    commit = (result.get("data") or {}).get("createCommitOnBranch", {}).get("commit")
    if not commit:
        print(json.dumps(result, indent=2), file=sys.stderr)
        return 1
    print(f"signed commit {commit['oid'][:12]} with {len(additions)} file(s): {commit['url']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
