---
id: pol-network-security
title: Network and Information Transfer Security Policy
lang: en
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 12
classification: internal
controls: [A.5.14, A.8.11, A.8.12, A.8.20, A.8.21, A.8.22, A.8.23]
---

# Network and Information Transfer Security Policy

This document is part of the information security management system of dev-test. It is maintained under version control; the signed git history and the release packs are its change record.

## 1. Purpose

This policy establishes minimum, risk-based requirements for dev-test’s distributed software engineering and cloud-supported operations. It supports the confidentiality, integrity, and availability of information and is fictional demonstration content only.

## 2. Scope

It applies to employees, contractors, managers, repositories, CI/CD, endpoints, cloud and SaaS services, customer data, secrets, documentation, and the ISMS repository within the defined dev-test scope. Supplier-managed components are covered through contracts and assurance.

## 3. Roles and responsibilities

The managing director approves this policy and accepts escalated risk. The CTO provides technical direction; the engineering lead applies requirements in development and release work; the IT lead operates identity, endpoints, and services; the ISMS owner maintains the ISMS, coordinates reviews, and reports issues. All users follow the policy and report deviations.

## 4. Requirements

Information transfers use approved channels, recipient verification, and classification-based safeguards. Public interfaces are minimised; cloud networks, repositories, CI/CD runners, and administrative paths are separated where practical. Network services use secure configurations and encryption. Restricted or personal data is masked in non-production contexts and monitored for inappropriate disclosure. Web filtering and endpoint protections reduce malicious or unauthorised access; exceptions are documented.

## 5. Exceptions

A documented exception requires a business reason, affected information or controls, risk assessment, compensating safeguards, owner, expiry date, and approval by the policy owner and managing director. Security or legal obligations may not be waived; expired exceptions are closed or re-approved.

## 6. Monitoring and compliance

The ISMS owner samples records and tracks objectives, incidents, risks, access reviews, supplier checks, and corrective actions. Control owners provide evidence when requested. Material nonconformity is escalated to the CTO and managing director. This policy is reviewed by 2027-08-12 or earlier after material change, incident, legal change, or major service change.

## 7. References

ISO/IEC 27001:2022 clauses 4–10; the dev-test ISMS context and risk register; applicable procedures; the Statement of Applicability; GDPR/DSGVO, customer contracts, and the obligations register. The policy owner maintains the policy and ensures that applicable controls are reflected in procedures, registers, and training. Records are controlled in the ISMS repository and contain no fabricated operational evidence.

## 8. Related Annex A controls

- **A.5.14** Information transfer
- **A.8.11** Data masking
- **A.8.12** Data leakage prevention
- **A.8.20** Networks security
- **A.8.21** Security of network services
- **A.8.22** Segregation of networks
- **A.8.23** Web filtering
