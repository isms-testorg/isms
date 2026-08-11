# Working on the ISMS

Read `README.md` first for the layout and the setup checklist.

## Before you start

```bash
pip install pyyaml
make check
```

`make check` must be clean of errors before you open a pull request. Warnings
are the known backlog; do not add to it.

## Changing a policy

1. Edit **both** language versions. `make check` fails if the `version` or the
   `controls` list drifts between them.
2. Bump `version` in the frontmatter of both:
   - **patch** — typo, formatting, a clearer sentence with the same meaning
   - **minor** — new requirement, changed scope, new control mapped
   - **major** — the policy now says something materially different
3. If the change was reviewed and approved, set `status: approved`, `approver`,
   `approved_on`, and `next_review` to exactly `approved_on` plus
   `review_cycle_months`. The check does that arithmetic and will reject a
   mismatch.
4. Fill in the pull request template honestly. It is the change record.

Editorial-only changes do not need `approved_on` moved. A change of meaning
does — that is a new approval.

## Adding a document

Add an entry to `DOCUMENTS` in `tools/scaffold.py`, then:

```bash
make scaffold
```

Both language files appear with correct frontmatter. Never create them by hand;
the scaffold is what keeps the two languages in step.

## Adding or changing a risk

Edit `data/risks.yml`. The checker enforces the parts people forget:

- an owner and at least one asset group from `data/assets.yml`
- likelihood and impact as integers 1 to 5, inherent and residual
- at least one Annex A control when `treatment: modify`
- that control must not be excluded in `data/soa.yml`
- a due date while the status is `open` or `in_treatment`, and it must not have
  passed
- `accepted_by` when accepting a risk whose residual score is above the
  acceptance threshold in `meta.acceptance`

## Deciding applicability

Edit `data/soa.yml`. Each control needs `applicable: true` or `false`.

Excluding a control requires `justification_en` **and** `justification_de`.
"Not relevant" is not a justification an auditor accepts; state the fact that
makes it inapplicable, for example "the organisation operates no industrial
control systems".

Only these keys are allowed in an entry:

```
id  applicable  status  implementation_note_en  implementation_note_de
justification_en  justification_de
```

Anything else is rejected, because documents, risks and evidence link
themselves to controls from their own files.

## Evidence

Automated evidence lands in `evidence/github/YYYY-MM/` via the monthly
workflow. Do not edit those files; they are a snapshot of what the API returned.

For manual evidence: put the file in `evidence/`, then add an entry to
`data/evidence-index.yml`. An unindexed file is a warning, and an indexed path
that matches nothing is an error.

Never commit evidence containing credentials, personal data, or secret scanning
alert details. The pack goes to external auditors.

## Commits

Signed, always. `git log --show-signature` should show every commit verified.
Conventional prefixes, scope is the area touched:

```
feat(policy): add remote working requirements to acceptable use
fix(soa): correct A.8.23 applicability, web filtering does apply
chore(evidence): GitHub configuration snapshot 2026-08
docs(readme): explain the derived link tables
```

## Releasing

```bash
git tag -s v1.0.0 -m "ISMS release 1.0.0"
git push origin v1.0.0
```

The tag must be signed. The release workflow runs `check_isms.py --strict`,
which fails on any warning, so a release pack never contains an undecided
control, an unjustified exclusion, a draft document or a `TODO`.
