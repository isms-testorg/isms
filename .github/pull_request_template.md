<!--
This PR is the change record for the ISMS. It is auditable evidence, so fill
it in properly. The merge commit plus the approving review is what proves the
change was authorised by someone other than the author.
-->

## What changes

<!-- One or two sentences. Which documents, data or controls does this touch? -->

## Reason for the change

- [ ] Scheduled periodic review
- [ ] Risk assessment result / new or changed risk
- [ ] Incident or nonconformity follow-up (link the issue)
- [ ] Internal or external audit finding
- [ ] Change in legal, regulatory or contractual requirements
- [ ] New or changed system, supplier or process
- [ ] Editorial only (no change of meaning)

Related issue:

## ISMS impact

- Annex A controls affected:
- Risks affected (`data/risks.yml` ids):
- Statement of Applicability changed: yes / no
- Version bumped in frontmatter: yes / no / not applicable
- Both language versions updated (DE **and** EN): yes / no

## Checklist

- [ ] `make check` passes locally
- [ ] `version`, `owner` and `review_cycle_months` in the frontmatter are correct
- [ ] Required independent CODEOWNER approval will be obtained before merge
- [ ] Commits are signed (`git log --show-signature`)
- [ ] Editorial-only changes did not bump the major or minor version
