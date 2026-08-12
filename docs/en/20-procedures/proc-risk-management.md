---
id: proc-risk-management
title: Risk Management Procedure
lang: en
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 12
classification: internal
controls: []
---

# Risk Management Procedure

This document is part of the information security management system of dev-test. It is maintained under version control; the signed git history and the release packs are its change record.

## 1. Purpose

This procedure provides a repeatable method for identifying, analysing, treating, accepting, monitoring, and communicating information-security risks within dev-test.

## 2. Scope

It covers source code, customer data, secrets, endpoints, identity, GitHub and CI/CD, cloud and SaaS services, backups, personnel, documentation, suppliers, home-office working, and supporting infrastructure. It applies to strategic, operational, project, supplier, privacy, legal, and continuity risks.

## 3. Roles and responsibilities

The ISMS owner maintains the methodology, risk register, review calendar, and reporting. Asset and process owners identify scenarios and propose treatments. The CTO owns engineering and technical risk decisions; the IT lead owns identity, endpoint, service, and backup risks; the engineering lead owns development and release risks. The managing director accepts risks above delegated tolerance and ensures resources. The ISMS owner coordinates review but does not silently accept a risk on behalf of its owner.

## 4. Requirements

At least annually and after material change, incident, supplier change, or new processing, owners identify assets, threats, vulnerabilities, existing controls, consequences, and affected obligations. They score likelihood and impact from 1 to 5 using the existing hybrid method; the register records the resulting risk score and rationale. Treatment is avoid, reduce, share, or accept, with owner, due date, applicable controls, bilingual plan, and target residual likelihood and impact. Controls are selected from the existing Annex A reference and legal or contractual requirements. The owner reviews treatment progress and rescoring after implementation. Inputs are asset groups, context, interested parties, incidents, audits, changes, supplier information, and threat information. Outputs are the updated risk register, treatment decisions, objective inputs, SoA inputs, and escalations.

## 5. Exceptions

Risk acceptance requires a named risk owner and approval at the level defined by the risk rating; material or high residual risk requires managing-director approval. Temporary treatment may be used only with an expiry date and compensating measure. If scoring information is uncertain, the owner records the conservative assumption and schedules reassessment rather than treating uncertainty as low risk.

## 6. Monitoring and compliance

The ISMS owner checks quarterly for stale assessments, missing owners, overdue treatments, invalid scores, unsupported controls, and residual risk above tolerance. Changes to likelihood, impact, assets, obligations, or controls are recorded with the reason. Significant risks are reported to management review; overdue or ineffective treatment triggers corrective action. The procedure is reviewed annually or after a material change to scope, methodology, obligations, or risk appetite.

## 7. References

ISO/IEC 27001:2022 clauses 6.1.2, 6.1.3, 8.1 and 8.2; the existing hybrid 1–5 risk methodology; asset, SoA, objective, incident, supplier, audit, and corrective-action records; and applicable GDPR/DSGVO and customer-contract requirements.

## 8. Related Annex A controls

None directly. This document satisfies a requirement from clauses 4 to 10 of the standard.
