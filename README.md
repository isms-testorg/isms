# ISMS — dev-test

Information Security Management System per **ISO/IEC 27001:2022**, kept as code
and versioned in git. Bilingual (German and English). The repository is the
single source of truth: policies, the risk register, the Statement of
Applicability and the collected evidence all live here, and every change goes
through a signed, reviewed pull request.

## Why a repository instead of a document management system

Three things an auditor asks for that git answers directly:

- **Who approved this, and when.** The merge commit and the required review
  from `CODEOWNERS` — approver cannot be the author.
- **What changed since the last version.** The diff.
- **Prove nobody altered it afterwards.** Commit signatures, verified end to
  end by `tools/verify_chain.sh` and shipped inside every release pack.

## Layout

```
data/            the machine readable layer, single source of truth
  controls/annex-a-2022.yml   93 Annex A controls, bilingual titles (reference)
  soa.yml                     Statement of Applicability decisions
  risks.yml                   risk register, scenarios linked to asset groups
  assets.yml                  asset groups (A.5.9)
  objectives.yml              clause 6.2 objectives and their measurement
  interested-parties.yml      clause 4.2
  evidence-index.yml          what evidence exists and how current it is
docs/en/ docs/de/  authored prose, one file per document, mirrored per language
  00-context/      clause 4 scope, context, roles
  10-policies/     topic policies covering all four Annex A themes
  20-procedures/   clauses 6.3, 7.5, 9.2, 9.3, 10.1 and operational procedures
evidence/github/YYYY-MM/       machine collected evidence, written by CI
tools/           the automation, plain Python plus PyYAML
build/           generated output, never committed
```

### What is derived and never stored twice

The Statement of Applicability does **not** record which document implements a
control, which risks relate to it, or which evidence covers it. All three are
read from the other files at render time:

| Link | Lives in |
|---|---|
| control → document | the `controls:` frontmatter of the document |
| control → risk | the `controls:` list in `data/risks.yml` |
| control → evidence | the `controls:` list in `data/evidence-index.yml` |

One place to update, so the two copies can never disagree. `check_isms.py`
rejects any attempt to add those keys back into `soa.yml`.

## Daily use

```bash
make check     # validate everything; run this before opening a pull request
make render    # generate SoA, risk register, coverage report into build/
make pdf       # needs pandoc + xelatex
make pack      # full release pack with checksums
make verify    # verify the signature chain
make scaffold  # create skeletons for newly declared documents
```

Only dependency is PyYAML (`pip install pyyaml`). Pandoc and XeLaTeX are needed
for `make pdf` and `make pack` only; CI installs them for releases.

## Document frontmatter

Every file under `docs/` carries this block. `make check` enforces it.

```yaml
---
id: pol-access-control        # must equal the filename, and match across languages
title: Access Control Policy
lang: en                      # must match the directory
version: 1.2.0                # MAJOR.MINOR.PATCH, identical in both languages
owner: "@handle"              # accountable for accuracy and review readiness
review_cycle_months: 12
classification: internal      # public | internal | confidential | restricted
controls: [A.5.15, A.8.2]     # must be identical in both languages
---
```

Approval metadata is pipeline-owned. A changed document is shown as `in_review`
in its pull-request preview. After a required independent CODEOWNER approval and
merge, the release pipeline derives `approved`, the approver, the merge date,
and the next-review date. The document owner is accountable for the content;
the approver is the GitHub reviewer, so neither is hand-entered in frontmatter.

## Automation

| Workflow | Trigger | What it does |
|---|---|---|
| `validate` | every PR and push to main | Runs consistency checks, marks changed documents `in_review` in the preview, renders the pack, uploads an artifact. Required status check. |
| `review-due` | Mondays 06:00 UTC | Opens an owner-routed issue for each document within 30 days of its review date and closes it once reviewed. |
| `evidence-collect` | 1st of the month 03:00 UTC | Snapshots the GitHub organisation's security configuration into `evidence/github/YYYY-MM/`, opens a PR. |
| `release` | signed tag `v*` | Strict validation, PDF and DOCX in both languages, signature chain report, checksums, provenance attestation, GitHub Release. |

## Setup checklist

Not yet done. Work through this before relying on the automation.

**1. Signing keys.** Every contributor, once per machine:

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

Then add the same public key to GitHub **as a signing key** (separate from the
authentication key): Settings → SSH and GPG keys → New SSH key → type
"Signing Key". Without that step GitHub shows commits as Unverified and the
release chain report fails.

**2. Team and owners.** Confirm the organisation teams in `.github/CODEOWNERS`,
`data/*.yml` and the document frontmatter use real GitHub team handles.

**3. Branch protection.** With the team in place:

```bash
gh api -X PUT repos/isms-testorg/ISMS-Automation/branches/main/protection \
  --input - <<'JSON'
{
  "required_status_checks": { "strict": true, "contexts": ["validate"] },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "require_code_owner_reviews": true,
    "dismiss_stale_reviews": true
  },
  "required_signatures": true,
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON
```

`required_signatures` is the one that turns the chain of custody from a
convention into a rule.

**4. Organisation token.** `evidence-collect` needs to read organisation
members and their 2FA state, which the default `GITHUB_TOKEN` cannot do.
Create a fine-grained PAT owned by an organisation owner, grant it access to
all repositories that should be collected, and add it as the
`ISMS_ORG_TOKEN` repository secret. The PAT needs:

- **Organisation permissions:** `Members: read`.
- **Repository permissions:** `Metadata: read`, `Administration: read`,
  `Dependabot alerts: read`, and `Secret scanning alerts: read`.

For a classic PAT, use the equivalent `read:org` scope and make sure the token
owner is an organisation owner. Without the repository permissions, the
workflow can still collect members and repositories, but branch protection,
Dependabot alerts, and secret-scanning alerts are recorded as unavailable.
Without the token, the workflow still runs and records exactly what it could
not read.

The separate **Settings → Actions → General → Workflow permissions** option
**Allow GitHub Actions to create and approve pull requests** must also be
enabled for the evidence workflow to open its pull request. This is independent
of the PAT permissions above.

**5. Fill in the content.** `make check` reports incomplete applicability,
evidence and placeholder content as the real backlog. A release cannot be
tagged until those findings are gone — `release` runs `check_isms.py --strict`,
which fails on any warning, then verifies derived approval state through
GitHub's review history.

## Known limitations

- **Organisation audit log** is GitHub Enterprise Cloud only. On Team plan
  that evidence has to be collected manually.
- **Evidence freshness** is derived from the `YYYY-MM` directory name, not file
  timestamps, because a fresh clone resets every mtime to checkout time.
- **Manual evidence** has no automatic staleness check unless it is filed under
  a `YYYY-MM` directory.
