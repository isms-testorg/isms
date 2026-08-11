#!/usr/bin/env python3
"""Collect operational evidence from the GitHub organisation.

Writes evidence/github/<YYYY-MM>/*.json. Each file records what was asked for,
what came back, and what could not be read, because "the token could not see
this" is itself evidence an auditor needs rather than a silent gap.

Only configuration and counts are stored. No alert descriptions, no secret
values, no file paths from secret scanning: the evidence must be safe to hand
to an external auditor.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys

from isms import EVIDENCE, ROOT


def gh(path: str, paginate: bool = True) -> tuple[object, str | None]:
    """Call the GitHub API. Returns (data, error). Never raises on HTTP errors."""
    cmd = ["gh", "api", path]
    if paginate:
        cmd += ["--paginate", "--slurp"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        message = (proc.stderr or "").strip().splitlines()
        return None, (message[-1] if message else f"exit {proc.returncode}")
    try:
        data = json.loads(proc.stdout or "null")
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc}"
    # --slurp wraps each page in a list; flatten when the pages are lists.
    if paginate and isinstance(data, list) and data and all(isinstance(p, list) for p in data):
        data = [item for page in data for item in page]
    return data, None


def envelope(kind: str, org: str) -> dict:
    return {
        "evidence_kind": kind,
        "organisation": org,
        "collected_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "collected_by": os.environ.get("GITHUB_WORKFLOW", "manual run"),
        "source": "GitHub REST API",
        "unavailable": [],
    }


def collect_members(org: str) -> dict:
    out = envelope("organisation members, roles and two factor authentication", org)

    admins, err = gh(f"orgs/{org}/members?role=admin&per_page=100")
    if err:
        out["unavailable"].append({"what": "admin members", "reason": err})
        admins = []
    members, err = gh(f"orgs/{org}/members?role=member&per_page=100")
    if err:
        out["unavailable"].append({"what": "regular members", "reason": err})
        members = []

    # Only organisation owners may read this. A 403 here is a finding in its
    # own right: it means nobody is able to evidence 2FA coverage.
    no_2fa, err = gh(f"orgs/{org}/members?filter=2fa_disabled&per_page=100")
    if err:
        out["unavailable"].append({
            "what": "members without two factor authentication",
            "reason": err,
            "note": "requires an organisation owner token with read:org",
        })
        no_2fa = None

    admin_logins = sorted(u["login"] for u in admins or [])
    member_logins = sorted(u["login"] for u in members or [])
    out["admins"] = admin_logins
    out["members"] = member_logins
    out["total"] = len(admin_logins) + len(member_logins)
    if no_2fa is not None:
        logins = sorted(u["login"] for u in no_2fa)
        out["without_2fa"] = logins
        out["without_2fa_count"] = len(logins)
        out["2fa_coverage_percent"] = (
            round(100 * (out["total"] - len(logins)) / out["total"], 1) if out["total"] else None
        )

    outside, err = gh(f"orgs/{org}/outside_collaborators?per_page=100")
    if err:
        out["unavailable"].append({"what": "outside collaborators", "reason": err})
    else:
        out["outside_collaborators"] = sorted(u["login"] for u in outside or [])

    settings, err = gh(f"orgs/{org}", paginate=False)
    if err:
        out["unavailable"].append({"what": "organisation settings", "reason": err})
    else:
        out["settings"] = {
            key: settings.get(key) for key in (
                "two_factor_requirement_enabled",
                "members_can_create_public_repositories",
                "default_repository_permission",
                "web_commit_signoff_required",
            )
        }
    return out


def collect_repos(org: str) -> tuple[dict, list[dict]]:
    out = envelope("repository inventory and visibility", org)
    repos, err = gh(f"orgs/{org}/repos?per_page=100&type=all")
    if err:
        out["unavailable"].append({"what": "repositories", "reason": err})
        return out, []
    out["repositories"] = [
        {
            "name": r["name"],
            "visibility": r.get("visibility"),
            "archived": r.get("archived"),
            "default_branch": r.get("default_branch"),
            "pushed_at": r.get("pushed_at"),
            "has_issues": r.get("has_issues"),
        }
        for r in sorted(repos, key=lambda r: r["name"])
    ]
    out["count"] = len(out["repositories"])
    out["private_count"] = sum(1 for r in out["repositories"] if r["visibility"] != "public")
    return out, repos


def collect_branch_protection(org: str, repos: list[dict]) -> dict:
    out = envelope("default branch protection and required reviews", org)
    results = []
    for repo in sorted(repos, key=lambda r: r["name"]):
        if repo.get("archived"):
            continue
        name, branch = repo["name"], repo.get("default_branch")
        if not branch:
            results.append({"repository": name, "protected": False, "reason": "no default branch"})
            continue
        data, err = gh(f"repos/{org}/{name}/branches/{branch}/protection", paginate=False)
        if err:
            # 404 from this endpoint means the branch is simply unprotected.
            results.append({
                "repository": name, "branch": branch, "protected": False,
                "reason": "no protection rule" if "404" in err else err,
            })
            continue
        reviews = data.get("required_pull_request_reviews") or {}
        results.append({
            "repository": name,
            "branch": branch,
            "protected": True,
            "required_approving_review_count": reviews.get("required_approving_review_count", 0),
            "require_code_owner_reviews": reviews.get("require_code_owner_reviews", False),
            "dismiss_stale_reviews": reviews.get("dismiss_stale_reviews", False),
            "required_signatures": bool((data.get("required_signatures") or {}).get("enabled")),
            "required_status_checks": [
                c for c in ((data.get("required_status_checks") or {}).get("contexts") or [])
            ],
            "enforce_admins": bool((data.get("enforce_admins") or {}).get("enabled")),
            "allow_force_pushes": bool((data.get("allow_force_pushes") or {}).get("enabled")),
        })
    out["branches"] = results
    out["protected_count"] = sum(1 for r in results if r.get("protected"))
    out["unprotected"] = [r["repository"] for r in results if not r.get("protected")]
    return out


def collect_alerts(org: str, repos: list[dict]) -> dict:
    out = envelope("open vulnerability and secret scanning alerts", org)
    today = dt.date.today()
    per_repo = []

    for repo in sorted(repos, key=lambda r: r["name"]):
        if repo.get("archived"):
            continue
        name = repo["name"]
        entry = {"repository": name}

        alerts, err = gh(f"repos/{org}/{name}/dependabot/alerts?state=open&per_page=100")
        if err:
            entry["dependabot"] = {"unavailable": err}
        else:
            by_severity: dict[str, int] = {}
            oldest_days = 0
            for alert in alerts or []:
                severity = ((alert.get("security_advisory") or {}).get("severity") or "unknown")
                by_severity[severity] = by_severity.get(severity, 0) + 1
                created = (alert.get("created_at") or "")[:10]
                try:
                    oldest_days = max(oldest_days, (today - dt.date.fromisoformat(created)).days)
                except ValueError:
                    pass
            entry["dependabot"] = {
                "open": len(alerts or []),
                "by_severity": by_severity,
                "oldest_open_days": oldest_days,
            }

        # Counts only. Secret scanning alert bodies point straight at where a
        # live credential is, which must not land in an auditor's evidence pack.
        secrets, err = gh(f"repos/{org}/{name}/secret-scanning/alerts?state=open&per_page=100")
        if err:
            entry["secret_scanning"] = {"unavailable": err}
        else:
            entry["secret_scanning"] = {"open": len(secrets or [])}

        per_repo.append(entry)

    out["repositories"] = per_repo
    out["dependabot_open_total"] = sum(
        r["dependabot"].get("open", 0) for r in per_repo if "open" in r["dependabot"])
    out["secret_scanning_open_total"] = sum(
        r["secret_scanning"].get("open", 0) for r in per_repo if "open" in r["secret_scanning"])
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--org", default=os.environ.get("ISMS_ORG"),
                        help="GitHub organisation; defaults to $ISMS_ORG")
    parser.add_argument("--month", default=dt.date.today().strftime("%Y-%m"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.org:
        print("ERROR: no organisation given, pass --org or set ISMS_ORG", file=sys.stderr)
        return 2

    outdir = os.path.join(EVIDENCE, "github", args.month)
    members = collect_members(args.org)
    repos_doc, repos = collect_repos(args.org)
    files = {
        "members.json": members,
        "repos.json": repos_doc,
        "branch_protection.json": collect_branch_protection(args.org, repos),
        "alerts.json": collect_alerts(args.org, repos),
    }

    problems = sum(len(doc["unavailable"]) for doc in files.values())
    if args.dry_run:
        print(json.dumps(files, indent=2, default=str))
        return 0

    os.makedirs(outdir, exist_ok=True)
    for name, doc in files.items():
        path = os.path.join(outdir, name)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=2, sort_keys=True, default=str)
            fh.write("\n")
        print(f"wrote {os.path.relpath(path, ROOT)}")

    if problems:
        print(f"\n{problems} item(s) could not be read; see the 'unavailable' lists. "
              f"This usually means the token lacks organisation scope.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
