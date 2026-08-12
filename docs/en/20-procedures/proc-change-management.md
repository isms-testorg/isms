---
id: proc-change-management
title: Change Management Procedure
lang: en
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 24
classification: internal
controls: []
---

# Change Management Procedure

This document is part of the information security management system of dev-test. It is maintained under version control; the signed git history and the release packs are its change record.

## 1. Purpose

This procedure keeps changes to code, infrastructure, cloud configuration, CI/CD, identity, SaaS integrations, security controls, and ISMS content authorised, tested, traceable, and reversible.

## 2. Scope

It applies to planned, emergency, standard, and supplier-performed changes affecting dev-test systems, customer-data processing, releases, or ISMS documents. Routine developer work remains subject to repository review and CI checks; production-impacting changes require the additional approval described here.

## 3. Roles and responsibilities

The requester describes the change and its risk. The engineering lead approves code and release changes; the IT lead approves identity, endpoint, infrastructure, and service changes; the CTO approves material technical or security risk; and the ISMS owner checks ISMS-document changes and records. The managing director approves changes with material business, legal, customer, or residual security impact.

## 4. Requirements

Each change has an issue, pull request, or approved service record stating purpose, scope, affected assets, security and privacy impact, dependencies, implementation plan, test evidence, rollback plan, owner, and requested timing. Changes use peer review, protected branches, automated checks, and separation between author and approver where practicable. Before deployment, the responsible lead confirms testing and approval. After deployment, the owner verifies expected behaviour, monitoring, backups, and customer impact and records the result. Failed changes are rolled back or contained and escalated. Emergency changes may be implemented to protect confidentiality, integrity, availability, or safety, but require retrospective review and approval within two business days. Outputs are the approved record, updated configuration or document, deployment history, test result, and lessons learned.

## 5. Exceptions

An emergency or urgent change may bypass normal scheduling only when delay creates greater risk. The responsible lead records the reason, scope, compensating controls, and approver. A change must not bypass security testing, access restrictions, or legal and contractual obligations without explicit CTO and, where material, managing-director approval.

## 6. Monitoring and compliance

The ISMS owner samples changes quarterly for approval, peer review, test evidence, rollback readiness, segregation, and closure. The engineering and IT leads monitor failed changes, emergency changes, rollback rate, and overdue post-implementation reviews. Exceptions and repeated failures become corrective actions. This procedure is reviewed every 24 months or after a major platform, release, or governance change.

## 7. References

ISO/IEC 27001:2022 clauses 6.3, 7.5, 8.1 and 8.2; the secure-development, operations, access-control, and documented-information policies; repository pull requests and CI/CD records; configuration records; and the nonconformity and corrective-action procedure.

## 8. Related Annex A controls

None directly. This document satisfies a requirement from clauses 4 to 10 of the standard.
