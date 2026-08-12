---
id: pol-secure-development
title: Secure Development Policy
lang: en
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 12
classification: internal
controls: [A.8.4, A.8.25, A.8.26, A.8.27, A.8.28, A.8.29, A.8.30, A.8.31, A.8.33]
---

# Secure Development Policy

This document is part of the information security management system of dev-test. It is maintained under version control; the signed git history and the release packs are its change record.

## 1. Purpose

This policy establishes minimum, risk-based requirements for dev-test’s distributed software engineering and cloud-supported operations. It supports the confidentiality, integrity, and availability of information and is fictional demonstration content only.

## 2. Scope

It applies to employees, contractors, managers, repositories, CI/CD, endpoints, cloud and SaaS services, customer data, secrets, documentation, and the ISMS repository within the defined dev-test scope. Supplier-managed components are covered through contracts and assurance.

## 3. Roles and responsibilities

The managing director approves this policy and accepts escalated risk. The CTO provides technical direction; the engineering lead applies requirements in development and release work; the IT lead operates identity, endpoints, and services; the ISMS owner maintains the ISMS, coordinates reviews, and reports issues. All users follow the policy and report deviations.

## 4. Requirements

Security is integrated into the software life cycle from requirements through maintenance. Security and privacy requirements, threat considerations, approved architecture, secure coding, dependency review, peer review, automated checks, and acceptance testing are recorded. Development, test, and production access and data are separated. Test data is synthetic or minimised and protected. Outsourced development follows the same requirements, repository controls, review gates, and vulnerability remediation expectations.

## 5. Exceptions

A documented exception requires a business reason, affected information or controls, risk assessment, compensating safeguards, owner, expiry date, and approval by the policy owner and managing director. Security or legal obligations may not be waived; expired exceptions are closed or re-approved.

## 6. Monitoring and compliance

The ISMS owner samples records and tracks objectives, incidents, risks, access reviews, supplier checks, and corrective actions. Control owners provide evidence when requested. Material nonconformity is escalated to the CTO and managing director. This policy is reviewed by 2027-08-12 or earlier after material change, incident, legal change, or major service change.

## 7. References

ISO/IEC 27001:2022 clauses 4–10; the dev-test ISMS context and risk register; applicable procedures; the Statement of Applicability; GDPR/DSGVO, customer contracts, and the obligations register. The policy owner maintains the policy and ensures that applicable controls are reflected in procedures, registers, and training. Records are controlled in the ISMS repository and contain no fabricated operational evidence.

## 8. Related Annex A controls

- **A.8.4** Access to source code
- **A.8.25** Secure development life cycle
- **A.8.26** Application security requirements
- **A.8.27** Secure system architecture and engineering principles
- **A.8.28** Secure coding
- **A.8.29** Security testing in development and acceptance
- **A.8.30** Outsourced development
- **A.8.31** Separation of development, test and production environments
- **A.8.33** Test information
