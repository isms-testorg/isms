---
id: pol-operations-security
title: Operations Security Policy
lang: en
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 12
classification: internal
controls: [A.5.37, A.8.6, A.8.7, A.8.8, A.8.9, A.8.13, A.8.15, A.8.16, A.8.17, A.8.19, A.8.32, A.8.34]
---

# Operations Security Policy

This document is part of the information security management system of dev-test. It is maintained under version control; the signed git history and the release packs are its change record.

## 1. Purpose

This policy establishes minimum, risk-based requirements for dev-test’s distributed software engineering and cloud-supported operations. It supports the confidentiality, integrity, and availability of information and is fictional demonstration content only.

## 2. Scope

It applies to employees, contractors, managers, repositories, CI/CD, endpoints, cloud and SaaS services, customer data, secrets, documentation, and the ISMS repository within the defined dev-test scope. Supplier-managed components are covered through contracts and assurance.

## 3. Roles and responsibilities

The managing director approves this policy and accepts escalated risk. The CTO provides technical direction; the engineering lead applies requirements in development and release work; the IT lead operates identity, endpoints, and services; the ISMS owner maintains the ISMS, coordinates reviews, and reports issues. All users follow the policy and report deviations.

## 4. Requirements

Operational systems use approved baselines, change control, vulnerability remediation, malware protection, backups, logging, monitoring, and synchronised time. Capacity and availability are reviewed for critical services. Software installation is restricted to authorised personnel and trusted sources. Logs are protected from alteration and retained according to the obligations register. Changes are tested and approved before release; audit testing uses controlled access and protects production information.

## 5. Exceptions

A documented exception requires a business reason, affected information or controls, risk assessment, compensating safeguards, owner, expiry date, and approval by the policy owner and managing director. Security or legal obligations may not be waived; expired exceptions are closed or re-approved.

## 6. Monitoring and compliance

The ISMS owner samples records and tracks objectives, incidents, risks, access reviews, supplier checks, and corrective actions. Control owners provide evidence when requested. Material nonconformity is escalated to the CTO and managing director. This policy is reviewed by 2027-08-12 or earlier after material change, incident, legal change, or major service change.

## 7. References

ISO/IEC 27001:2022 clauses 4–10; the dev-test ISMS context and risk register; applicable procedures; the Statement of Applicability; GDPR/DSGVO, customer contracts, and the obligations register. The policy owner maintains the policy and ensures that applicable controls are reflected in procedures, registers, and training. Records are controlled in the ISMS repository and contain no fabricated operational evidence.

## 8. Related Annex A controls

- **A.5.37** Documented operating procedures
- **A.8.6** Capacity management
- **A.8.7** Protection against malware
- **A.8.8** Management of technical vulnerabilities
- **A.8.9** Configuration management
- **A.8.13** Information backup
- **A.8.15** Logging
- **A.8.16** Monitoring activities
- **A.8.17** Clock synchronization
- **A.8.19** Installation of software on operational systems
- **A.8.32** Change management
- **A.8.34** Protection of information systems during audit testing
