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

TODO

## 2. Scope

TODO

## 3. Roles and responsibilities

The document owner maintains accuracy, bilingual consistency, and review readiness. Authors propose changes. The required CODEOWNER reviewer independently approves the final pull-request revision. GitHub records the review and merge; the pipeline derives lifecycle status, approver, approval date, and next-review date.

## 4. Requirements

Source frontmatter contains only stable metadata: identifier, title, language, version, owner, review cycle, classification, and applicable controls. Changed documents appear as `in_review` in pull-request previews. After independent approval and merge, release and review workflows derive `approved` metadata from GitHub without modifying the reviewed source revision.

## 5. Exceptions

TODO

## 6. Monitoring and compliance

TODO

## 7. References

TODO

## 8. Related Annex A controls

None directly. This document satisfies a requirement from clauses 4 to 10 of the standard.
