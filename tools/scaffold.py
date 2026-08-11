#!/usr/bin/env python3
"""Create missing ISMS document skeletons and seed the Statement of Applicability.

Idempotent: existing files are never touched. Run it again after adding an
entry to DOCUMENTS below to create just the new pair of files.

The document set covers the documented information ISO/IEC 27001:2022 requires
(clauses 4 to 10) plus a topic policy set that between them claims every one of
the 93 Annex A controls. `make check` reports any control left unclaimed.
"""

from __future__ import annotations

import os
import sys

from isms import DOCS, LANGS, ROOT, load_controls, load_yaml

# id, folder, title_en, title_de, review_cycle_months, classification, controls
DOCUMENTS = [
    ("ctx-scope", "00-context",
     "ISMS Scope Statement", "Anwendungsbereich des ISMS", 12, "internal",
     ["A.5.1"]),
    ("ctx-organisation", "00-context",
     "Organisational Context and Interested Parties", "Organisationskontext und interessierte Parteien", 12, "internal",
     ["A.5.5", "A.5.6"]),
    ("ctx-roles", "00-context",
     "Information Security Roles and Responsibilities", "Informationssicherheitsrollen und -verantwortlichkeiten", 12, "internal",
     ["A.5.2", "A.5.3", "A.5.4"]),

    ("pol-information-security", "10-policies",
     "Information Security Policy", "Informationssicherheitsrichtlinie", 12, "internal",
     ["A.5.1"]),
    ("pol-acceptable-use", "10-policies",
     "Acceptable Use Policy", "Richtlinie zur zulässigen Nutzung", 12, "internal",
     ["A.5.10", "A.5.11", "A.6.7", "A.7.7", "A.8.1"]),
    ("pol-access-control", "10-policies",
     "Access Control Policy", "Zugangssteuerungsrichtlinie", 12, "internal",
     ["A.5.15", "A.5.16", "A.5.17", "A.5.18", "A.8.2", "A.8.3", "A.8.5", "A.8.18"]),
    ("pol-asset-management", "10-policies",
     "Asset Management and Information Classification Policy", "Richtlinie für Werteverwaltung und Informationsklassifizierung", 12, "internal",
     ["A.5.9", "A.5.12", "A.5.13", "A.7.10", "A.7.14", "A.8.10"]),
    ("pol-cryptography", "10-policies",
     "Cryptography Policy", "Kryptographierichtlinie", 12, "internal",
     ["A.8.24"]),
    ("pol-supplier-security", "10-policies",
     "Supplier and Cloud Security Policy", "Richtlinie für Lieferanten- und Cloud-Sicherheit", 12, "internal",
     ["A.5.19", "A.5.20", "A.5.21", "A.5.22", "A.5.23"]),
    ("pol-secure-development", "10-policies",
     "Secure Development Policy", "Richtlinie für sichere Entwicklung", 12, "internal",
     ["A.8.4", "A.8.25", "A.8.26", "A.8.27", "A.8.28", "A.8.29", "A.8.30", "A.8.31", "A.8.33"]),
    ("pol-operations-security", "10-policies",
     "Operations Security Policy", "Richtlinie für Betriebssicherheit", 12, "internal",
     ["A.5.37", "A.8.6", "A.8.7", "A.8.8", "A.8.9", "A.8.13", "A.8.15", "A.8.16",
      "A.8.17", "A.8.19", "A.8.32", "A.8.34"]),
    ("pol-network-security", "10-policies",
     "Network and Information Transfer Security Policy", "Richtlinie für Netzwerk- und Übertragungssicherheit", 12, "internal",
     ["A.5.14", "A.8.11", "A.8.12", "A.8.20", "A.8.21", "A.8.22", "A.8.23"]),
    ("pol-physical-security", "10-policies",
     "Physical and Environmental Security Policy", "Richtlinie für physische und umgebungsbezogene Sicherheit", 12, "internal",
     ["A.7.1", "A.7.2", "A.7.3", "A.7.4", "A.7.5", "A.7.6", "A.7.8", "A.7.9",
      "A.7.11", "A.7.12", "A.7.13"]),
    ("pol-hr-security", "10-policies",
     "Human Resource Security Policy", "Richtlinie für Personalsicherheit", 12, "internal",
     ["A.6.1", "A.6.2", "A.6.3", "A.6.4", "A.6.5", "A.6.6"]),
    ("pol-incident-management", "10-policies",
     "Information Security Incident Management Policy", "Richtlinie für die Handhabung von Informationssicherheitsvorfällen", 12, "internal",
     ["A.5.24", "A.6.8"]),
    ("pol-business-continuity", "10-policies",
     "Business Continuity and ICT Readiness Policy", "Richtlinie für Business Continuity und IKT-Bereitschaft", 12, "internal",
     ["A.5.29", "A.5.30", "A.8.14"]),
    ("pol-compliance", "10-policies",
     "Legal, Regulatory and Compliance Policy", "Richtlinie für rechtliche und regulatorische Konformität", 12, "internal",
     ["A.5.7", "A.5.8", "A.5.31", "A.5.32", "A.5.33", "A.5.34", "A.5.35", "A.5.36"]),

    ("proc-risk-management", "20-procedures",
     "Risk Management Procedure", "Verfahren für das Risikomanagement", 12, "internal",
     []),
    ("proc-document-control", "20-procedures",
     "Control of Documented Information", "Lenkung dokumentierter Information", 24, "internal",
     []),
    ("proc-change-management", "20-procedures",
     "Change Management Procedure", "Verfahren für die Änderungssteuerung", 24, "internal",
     []),
    ("proc-access-review", "20-procedures",
     "Access Review Procedure", "Verfahren für die Überprüfung von Zugangsrechten", 12, "internal",
     []),
    ("proc-incident-response", "20-procedures",
     "Incident Response Procedure", "Verfahren für die Reaktion auf Vorfälle", 12, "internal",
     ["A.5.25", "A.5.26", "A.5.27", "A.5.28"]),
    ("proc-internal-audit", "20-procedures",
     "Internal Audit Procedure", "Verfahren für interne Audits", 24, "internal",
     []),
    ("proc-management-review", "20-procedures",
     "Management Review Procedure", "Verfahren für die Managementbewertung", 24, "internal",
     []),
    ("proc-nonconformity", "20-procedures",
     "Nonconformity and Corrective Action Procedure", "Verfahren für Nichtkonformität und Korrekturmaßnahmen", 24, "internal",
     []),
]

SECTIONS = {
    "en": ["Purpose", "Scope", "Roles and responsibilities", "Requirements",
           "Exceptions", "Monitoring and compliance", "References"],
    "de": ["Zweck", "Anwendungsbereich", "Rollen und Verantwortlichkeiten", "Anforderungen",
           "Ausnahmen", "Überwachung und Konformität", "Referenzen"],
}

INTRO = {
    "en": ("This document is part of the information security management system of "
           "dev-test. It is maintained under version control; the "
           "signed git history and the release packs are its change record."),
    "de": ("Dieses Dokument ist Teil des Informationssicherheits-Managementsystems von "
           "dev-test. Es wird unter Versionskontrolle gepflegt; die "
           "signierte git-Historie und die Release-Pakete sind sein Änderungsnachweis."),
}

CONTROLS_HEADING = {"en": "Related Annex A controls", "de": "Zugehörige Maßnahmen aus Anhang A"}
NO_CONTROLS = {
    "en": "None directly. This document satisfies a requirement from clauses 4 to 10 of the standard.",
    "de": "Keine unmittelbar. Dieses Dokument erfüllt eine Anforderung aus den Abschnitten 4 bis 10 der Norm.",
}


def render_document(doc, lang, controls) -> str:
    doc_id, _folder, title_en, title_de, cycle, classification, refs = doc
    title = title_en if lang == "en" else title_de

    front = [
        "---",
        f"id: {doc_id}",
        f"title: {title}",
        f"lang: {lang}",
        "version: 0.1.0",
        "status: draft",
        'owner: "@isms-testorg/dev-isms-owner"',
        'approver: "@isms-testorg/dev-managing-director"',
        "approved_on:",
        "next_review:",
        f"review_cycle_months: {cycle}",
        f"classification: {classification}",
    ]
    if refs:
        front.append("controls: [" + ", ".join(refs) + "]")
    else:
        front.append("controls: []")
    front.append("---")

    body = [f"# {title}", "", INTRO[lang], ""]
    for number, heading in enumerate(SECTIONS[lang], start=1):
        body += [f"## {number}. {heading}", "", "TODO", ""]

    body += [f"## {len(SECTIONS[lang]) + 1}. {CONTROLS_HEADING[lang]}", ""]
    if refs:
        for cid in refs:
            title_key = "title_en" if lang == "en" else "title_de"
            body.append(f"- **{cid}** {controls[cid][title_key]}")
    else:
        body.append(NO_CONTROLS[lang])
    body.append("")

    return "\n".join(front) + "\n\n" + "\n".join(body)


def seed_soa(controls, risk_controls: set[str]) -> str:
    """Write a Statement of Applicability skeleton, one entry per control.

    Only controls already used to treat a risk are seeded as applicable: that
    decision is implied by the risk register and the checker enforces it
    anyway. Everything else starts undecided. Applicability is the core
    judgement an auditor probes, so the scaffold must not quietly make it on
    the organisation's behalf just because a draft policy mentions the control.
    """
    out = [
        "# Statement of Applicability (clause 6.1.3 d).",
        "#",
        "# One entry per Annex A control. `applicable: null` means nobody has decided",
        "# yet and the check will keep reminding you.",
        "#",
        "# Excluding a control requires justification_en AND justification_de.",
        "#",
        "# Deliberately NOT stored here, because it is derived and would drift:",
        "#   implementing documents -> the `controls:` frontmatter of each document",
        "#   related risks          -> the `controls:` list in data/risks.yml",
        "#   related evidence       -> the `controls:` list in data/evidence-index.yml",
        "# The rendered Statement of Applicability pulls all three in automatically.",
        "#",
        "# status: not_assessed | planned | partially_implemented | implemented | not_applicable",
        "",
        "controls:",
    ]
    for cid, control in controls.items():
        decided = cid in risk_controls
        out += [
            f"  - id: {cid}",
            f"    # {control['title_en']}",
            f"    applicable: {'true' if decided else 'null'}",
            f"    status: {'planned' if decided else 'not_assessed'}",
            "    implementation_note_en:",
            "    implementation_note_de:",
            "    justification_en:",
            "    justification_de:",
            "",
        ]
    return "\n".join(out)


def main() -> int:
    controls, _themes = load_controls()

    known_ids = {d[0] for d in DOCUMENTS}
    if len(known_ids) != len(DOCUMENTS):
        print("ERROR: duplicate document id in DOCUMENTS", file=sys.stderr)
        return 1

    created = 0
    for doc in DOCUMENTS:
        doc_id, folder = doc[0], doc[1]
        for cid in doc[6]:
            if cid not in controls:
                print(f"ERROR: {doc_id} references unknown control {cid}", file=sys.stderr)
                return 1
        for lang in LANGS:
            path = os.path.join(DOCS, lang, folder, f"{doc_id}.md")
            if os.path.exists(path):
                continue
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(render_document(doc, lang, controls))
            created += 1
            print(f"created {os.path.relpath(path, ROOT)}")

    soa_path = os.path.join(ROOT, "data", "soa.yml")
    if os.path.exists(soa_path):
        print("data/soa.yml exists, left untouched")
    else:
        risks = load_yaml("data/risks.yml").get("risks") or []
        risk_controls = {cid for risk in risks for cid in (risk.get("controls") or [])}
        with open(soa_path, "w", encoding="utf-8") as fh:
            fh.write(seed_soa(controls, risk_controls))
        print(f"created data/soa.yml with {len(controls)} entries")

    unclaimed = sorted(set(controls) - {cid for doc in DOCUMENTS for cid in doc[6]})
    if unclaimed:
        print(f"\nnote: {len(unclaimed)} controls are not claimed by any document: "
              f"{', '.join(unclaimed)}")

    print(f"\n{created} files created")
    return 0


if __name__ == "__main__":
    sys.exit(main())
