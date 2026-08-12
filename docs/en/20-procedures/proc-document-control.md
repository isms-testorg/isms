---
id: proc-document-control
title: Control of Documented Information
lang: en
version: 0.1.0
owner: "@isms-testorg/dev-isms-owner"
review_cycle_months: 24
classification: internal
controls: []
---

# Control of Documented Information

This document is part of the information security management system of dev-test. It is maintained under version control; the signed git history and the release packs are its change record.

## 1. Purpose

This procedure ensures that ISMS documented information is identifiable, approved, available to authorised users, protected from unintended change, and disposed of or retained consistently.

## 2. Scope

It covers policies, procedures, context, registers, the Statement of Applicability, objectives, evidence indexes, manually authored evidence, and controlled templates in the dev-test repository. It also covers external documents needed to operate the ISMS where their owner and current version are known.

## 3. Roles and responsibilities

The ISMS owner maintains the document register, review calendar, and repository structure. A document owner remains accountable for its accuracy, bilingual consistency, and review readiness. Authors propose changes. A member of the required CODEOWNER team independently approves the final pull-request revision; GitHub records the approver. The engineering lead maintains repository protection and automation; the IT lead supports access and backup; the managing director approves governance documents and material changes.

## 4. Requirements

Each controlled document has its identifier, title, language, version, owner, review cycle, classification, and applicable controls in source. The pipeline derives lifecycle status, approver, approval date, and next-review date from GitHub's final review and merge record. Authors submit changes through a reviewed pull request; the owner checks bilingual parity, references, links, and schema; the CODEOWNER approver accepts or rejects the change. Approved versions are released through the existing pipeline. The repository history is the change record and generated release outputs remain pipeline-owned. Superseded content is marked or retained according to legal, contractual, and business retention needs; access is limited to the classification. Inputs are approved source changes, review findings, requirements, and operational lessons. Outputs are the approved document, review record, and derived metadata.

## 5. Exceptions

Urgent corrections may be merged with expedited review when delay creates a security or compliance risk. The author records the reason and compensating review. No one may alter generated build output, collector output, signatures, checksums, or GitHub records as a substitute for changing the source document.

## 6. Monitoring and compliance

The ISMS owner checks monthly for overdue reviews, blank metadata, broken links, duplicate IDs, unresolved placeholders, language drift, and unapproved changes. The validator and pipeline checks are authoritative for structural consistency. Deviations are corrected or recorded as nonconformities, and management review receives the status of document reviews and retention issues. Review occurs on the next-review date or after a material standard, legal, organisational, or scope change.

## 7. References

ISO/IEC 27001:2022 clause 7.5; the repository contribution rules; the information-classification, retention, and change-management policies; `tools/check_isms.py`; and the existing rendering and release pipeline.

## 8. Related Annex A controls

None directly. This document satisfies a requirement from clauses 4 to 10 of the standard.
