---
id: proc-incident-response
title: Incident Response Procedure
lang: en
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 12
classification: internal
controls: [A.5.25, A.5.26, A.5.27, A.5.28]
---

# Incident Response Procedure

This document is part of the information security management system of dev-test. It is maintained under version control; the signed git history and the release packs are its change record.

## 1. Purpose

This procedure provides a controlled response to suspected or confirmed information-security events so that dev-test limits harm, restores trustworthy service, fulfils notification duties, and learns from incidents.

## 2. Scope

It covers events involving source code, customer data, credentials and secrets, endpoints, GitHub, CI/CD, cloud and SaaS services, identity, backups, the ISMS repository, and suppliers. It applies during detection, triage, containment, eradication, recovery, communication, and evidence preservation.

## 3. Roles and responsibilities

Anyone who notices an event reports it immediately to the IT lead or ISMS owner through the approved internal channel. The IT lead coordinates technical containment; the engineering lead handles repositories, builds, and releases; the CTO directs material technical decisions; the ISMS owner maintains the incident record and compliance assessment; and the managing director authorises material business or customer communications. Legal or privacy advice is obtained for personal-data events. The incident lead assigns tasks and keeps decision authority clear.

## 4. Requirements

The reporter records time, source, affected service, observed facts, and safe contact details. The incident lead assigns severity, distinguishes event from incident, preserves relevant logs and volatile evidence where feasible, and opens an incident record. The team contains the threat, rotates exposed credentials, isolates systems, preserves availability where safe, investigates scope and root cause, eradicates malicious access, and recovers from trusted versions or backups. Communications are factual, need-to-know, and approved before release. The ISMS owner assesses GDPR/DSGVO, contractual, supplier, and law-enforcement obligations and coordinates deadlines with the managing director and advisers. Closure requires impact, timeline, evidence, actions, residual risk, affected parties, and lessons learned. Inputs are alerts, reports, logs, access history, backup status, and supplier notices. Outputs are the incident record, preserved evidence, recovery confirmation, notifications where required, and corrective actions.

## 5. Exceptions

Emergency containment may proceed without prior approval when delay would increase harm, provided the incident lead records the decision and informs the CTO and ISMS owner as soon as possible. Evidence must not be altered unnecessarily. If a required notification deadline or customer commitment is at risk, the managing director is escalated immediately.

## 6. Monitoring and compliance

The ISMS owner reviews incident severity decisions, response times, containment, notification decisions, evidence completeness, recovery tests, and recurring causes after each incident and at least quarterly. Significant incidents trigger corrective action and management review. The procedure is exercised periodically and reviewed annually or after a material incident, legal change, or platform change.

## 7. References

ISO/IEC 27001:2022 clauses 7.5, 8.1, 8.2 and 10.2; the incident-management, access-control, backup, privacy, supplier, and communication policies; the GDPR/DSGVO and customer-contract requirements; and controls A.5.25–A.5.28 listed below.

## 8. Related Annex A controls

- **A.5.25** Assessment and decision on information security events
- **A.5.26** Response to information security incidents
- **A.5.27** Learning from information security incidents
- **A.5.28** Collection of evidence
