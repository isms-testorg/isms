---
id: ctx-roles
title: Information Security Roles and Responsibilities
lang: en
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 12
classification: internal
controls: [A.5.2, A.5.3, A.5.4]
---

# Information Security Roles and Responsibilities

This document is part of the information security management system of dev-test. It is maintained under version control; the signed git history and the release packs are its change record.

## 1. Purpose

This document defines information-security authority, accountability, and segregation of duties for dev-test's fictional demonstration ISMS. It ensures that decisions are assigned to named roles and that important activities receive independent review where practical.

## 2. Scope

It applies to all employees and contractors, the ISMS repository, information assets, software-development and release activities, customer-data processing, supporting SaaS and cloud services, and the GitHub teams and repositories used within the ISMS boundary.

## 3. Roles and responsibilities

The managing director (@isms-testorg/dev-managing-director) approves the ISMS scope, policies, objectives, risk acceptance at management level, resources, and management-review outcomes. The CTO (@isms-testorg/dev-cto) sets technical direction and ensures security is integrated into architecture and engineering decisions. The engineering lead (@isms-testorg/dev-engineering-lead) owns secure development, code review, branch protection, dependency remediation, and release controls. The IT lead (@isms-testorg/dev-it-lead) owns identity and endpoint administration, access reviews, backup coordination, and supplier-service dependencies. The ISMS owner (@isms-testorg/dev-isms-owner) maintains documented information, coordinates risk treatment, monitors objectives and compliance, prepares reviews, and escalates gaps.

A document owner is accountable for the document's accuracy, bilingual consistency, and review readiness. An author proposes a change through a pull request and may be the owner or another contributor. An approver is a member of the required CODEOWNER team who independently approves the final pull-request revision; GitHub and the pipeline record that approval. Owners and authors do not self-approve.

Information and service owners define protection needs and approve access. Contributors follow policies, protect credentials and devices, and report events. Independent review is required for approvals, access recertification, risk acceptance, internal audit, and corrective-action closure where the organization can provide a suitably independent reviewer.

## 4. Requirements

Role assignments are recorded in approved documents and repository permissions. Least privilege, dual review, and separation between request, approval, implementation, and verification are applied to privileged access, production changes, releases, risk acceptance, and evidence review. A person must not approve their own access, risk acceptance, or corrective action closure. Where staffing prevents full separation, the ISMS owner records the limitation and a compensating review.

## 5. Exceptions

Temporary delegation requires a named delegate, defined authority, start and end dates, and notification to affected owners. Conflicts of interest and unavailable approvers are escalated to the managing director and ISMS owner. Delegation does not transfer ultimate management accountability or remove legal, contractual, privacy, or security duties.

## 6. Monitoring and compliance

The ISMS owner reviews role assignments, repository permissions, segregation-of-duties exceptions, training status, and overdue responsibilities at least annually and after material change. Managers monitor performance through objectives, access reviews, incidents, audits, and management review. Deviations are recorded, risk-assessed, assigned, and tracked to closure. This fictional document does not assert actual operating effectiveness or certification.

## 7. References

References include ISO/IEC 27001:2022 clauses 5.3, 5.4, 7.2, 7.3, and 9.3; the scope statement; access-control, secure-development, change-management, incident, audit, and corrective-action procedures; repository team permissions; and the objectives and risk registers.

## 8. Related Annex A controls

- **A.5.2** Information security roles and responsibilities
- **A.5.3** Segregation of duties
- **A.5.4** Management responsibilities
