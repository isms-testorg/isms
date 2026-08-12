---
id: ctx-scope
title: ISMS Scope Statement
lang: en
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 12
classification: internal
controls: [A.5.1]
---

# ISMS Scope Statement

This document is part of the information security management system of dev-test. It is maintained under version control; the signed git history and the release packs are its change record.

## 1. Purpose

This statement defines the boundaries and intended outcomes of the fictional demonstration ISMS for dev-test. It supports consistent application of information-security policies and provides the context for risk treatment, objectives, controls, and documented information. It does not represent certification or proof of operating effectiveness.

## 2. Scope

The ISMS covers dev-test's distributed employees and contractors and the activities performed for software development, source-code management, release management, customer-data processing, and operation of supporting SaaS and cloud services. It includes the GitHub organization and repositories, CI/CD pipelines, identity provider, endpoint devices, cloud hosting, SaaS suppliers, secret storage, backup services, and this version-controlled ISMS repository.

The boundary includes home-office working arrangements and the locations from which authorized personnel work, together with relevant supplier interfaces and cloud regions selected by dev-test. Physical data-centre operations, supplier internal processes, and customer systems outside dev-test's control are excluded; their security is addressed through contractual, due-diligence, and shared-responsibility requirements. The ISMS applies to information in electronic form and relevant supporting records, regardless of where they are processed within the stated boundary.

## 3. Roles and responsibilities

The managing director provides direction and approves the scope. The CTO provides technical governance, the engineering lead owns secure development and release practices, the IT lead manages identities, endpoints, backups, and service dependencies, and the ISMS owner maintains the ISMS, coordinates risk and compliance activities, and reports status. All employees and contractors follow applicable requirements and report suspected events. Owners of outsourced services remain accountable for dev-test decisions even where implementation is delegated.

## 4. Requirements

The scope is implemented against ISO/IEC 27001:2022 and the applicable Annex A reference controls, GDPR/DSGVO obligations, customer contracts, supplier commitments, and applicable commercial and legal record-retention requirements. Confidentiality, integrity, and availability are managed through risk-based controls, documented responsibilities, least privilege, secure change practices, resilience measures, and protection of personal and customer information.

## 5. Exceptions

Exceptions require a documented risk-based rationale, named owner, compensating measures where appropriate, an expiry or review date, and approval by the responsible management role and the ISMS owner. Legal, contractual, privacy, and security obligations may not be waived by an operational exception. Exclusions from the scope are limited to the boundaries stated above and are reviewed when activities, systems, suppliers, or locations change.

## 6. Monitoring and compliance

The ISMS owner monitors objectives, risks, incidents, control implementation, document reviews, supplier dependencies, and audit or assessment actions using the repository registers and approved records. Management reviews significant results and overdue actions. Nonconformities are recorded and treated through the established corrective-action process. All records are fictional demonstration data; generated pipeline evidence remains the responsibility of the repository automation and is not implied by this statement.

## 7. References

Key references are ISO/IEC 27001:2022 clauses 4.3, 4.4, 5.2, 6.1, and 7.5; the dev-test risk register, Statement of Applicability, asset-group register, objectives register, interested-parties register, and approved policies and procedures. Applicable privacy and contractual requirements are interpreted for the relevant processing and service relationship.

## 8. Related Annex A controls

- **A.5.1** Policies for information security
