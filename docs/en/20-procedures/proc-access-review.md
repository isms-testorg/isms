---
id: proc-access-review
title: Access Review Procedure
lang: en
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 12
classification: internal
controls: []
---

# Access Review Procedure

This document is part of the information security management system of dev-test. It is maintained under version control; the signed git history and the release packs are its change record.

## 1. Purpose

This procedure ensures that access to GitHub, repositories, CI/CD, cloud services, SaaS platforms, the identity provider, secret storage, backups, endpoints, and the ISMS repository remains appropriate for the person’s role and current business need.

## 2. Scope

It applies to employees, contractors, service accounts, privileged accounts, and external support access within the dev-test ISMS scope. It covers joiner, mover, and leaver changes and the scheduled review of logical and physical access where dev-test controls the decision.

## 3. Roles and responsibilities

The IT lead operates the identity-provider and endpoint review and coordinates evidence. The engineering lead reviews repository, branch, deployment, and CI/CD permissions. The ISMS owner coordinates the review, checks completeness, records findings, and escalates overdue actions. The managing director approves acceptance of material residual access risk; the CTO approves engineering exceptions. Managers confirm business need for their team members, and every reviewer must be independent of the access change being reviewed where practicable.

## 4. Requirements

Access owners provide current membership and privilege exports at least quarterly and when a role, contract, or supplier relationship changes. Reviewers compare each entry with the role, employment or contract status, least-privilege need, MFA state, recent use, and approved exceptions. Unneeded access is removed promptly; excessive privilege is reduced; dormant accounts are disabled; and privileged or service-account ownership is recorded. Joiner access is approved before provisioning, mover access is re-approved after the change, and leaver access is revoked on or before the end of access need. Inputs are access exports, personnel and supplier status, role assignments, ticket or pull-request approvals, and prior findings. Outputs are the signed review record, remediation actions, updated memberships, and escalation decisions. The ISMS owner obtains managing-director approval for closure of material findings.

## 5. Exceptions

Temporary access may be granted only for a defined purpose, named owner, expiry date, and approval. If immediate removal would interrupt a critical release or investigation, the IT lead or engineering lead may defer it briefly, document the reason and compensating measure, and notify the ISMS owner. No exception may override legal, contractual, or security requirements; unresolved high-risk access is escalated to the managing director.

## 6. Monitoring and compliance

The ISMS owner tracks completion, overdue actions, privileged-access exceptions, leaver revocation timeliness, and MFA coverage. Quarterly records are sampled against source exports and GitHub history; failures create a nonconformity or corrective action. Results are reported in management review and retained in the ISMS repository. The procedure is reviewed on its next-review date or after a material identity, platform, or regulatory change.

## 7. References

ISO/IEC 27001:2022 clauses 5.3, 7.5, 8.1, 8.2 and 8.3; the access-control policy; personnel and supplier records; identity-provider, GitHub, CI/CD, cloud, SaaS, endpoint, secret-storage, backup, and ISMS-repository records; and the nonconformity and corrective-action procedure.

## 8. Related Annex A controls

None directly. This document satisfies a requirement from clauses 4 to 10 of the standard.
