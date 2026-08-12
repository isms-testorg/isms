#!/usr/bin/env python3
"""Render the derived ISMS documents from the data layer.

Output goes to build/ and is never committed. Everything here is a pure
function of data/ plus the document frontmatter, so the Statement of
Applicability in a release pack cannot disagree with the risk register that
shipped beside it.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys

from isms import LANGS, ROOT, band_for, evidence_files, load_controls, load_docs, load_yaml

T = {
    "en": {
        "soa_title": "Statement of Applicability",
        "soa_intro": ("Required by ISO/IEC 27001:2022 clause 6.1.3 d). Lists every control in "
                      "Annex A, whether it applies, and why. Generated from the data layer; do "
                      "not edit by hand."),
        "control": "Control", "title": "Title", "applicable": "Applicable", "status": "Status",
        "documents": "Documents", "risks": "Risks", "evidence": "Evidence",
        "yes": "Yes", "no": "No", "undecided": "Not decided",
        "exclusions": "Justification for excluded controls",
        "impl_notes": "Implementation notes",
        "no_exclusions": "No control has been excluded.",
        "no_notes": "No implementation notes recorded yet.",
        "summary": "Summary",
        "risk_title": "Risk Register",
        "risk_intro": ("Clause 6.1.2 risk assessment results and clause 6.1.3 risk treatment "
                       "plan. Scores are likelihood x impact on a 1 to 5 scale."),
        "risk_matrix": "Residual risk distribution",
        "inherent": "Inherent", "residual": "Residual", "band": "Band", "owner": "Owner",
        "due": "Due", "treatment": "Treatment", "assets": "Asset groups",
        "threat": "Threat", "vulnerability": "Weakness", "plan": "Treatment plan",
        "likelihood": "Likelihood", "impact": "Impact",
        "cov_title": "Control Coverage Report",
        "cov_intro": ("Where the management system is thin. Not an audit deliverable in itself, "
                      "but the fastest way to find the gaps before an auditor does."),
        "by_theme": "By theme", "theme": "Theme", "total": "Total",
        "gaps": "Gaps", "no_gaps": "No gaps found.",
        "ev_title": "Evidence Index",
        "ev_intro": "Records held to demonstrate that controls operate, and how current they are.",
        "files": "Files", "newest": "Newest", "valid": "Valid for",
        "months": "months", "collector": "Collector", "manual": "manual",
        "asset_title": "Asset Inventory",
        "asset_intro": "Asset groups per A.5.9, with owner and classification.",
        "name": "Name", "type": "Type", "classification": "Classification", "location": "Location",
        "obj_title": "Information Security Objectives",
        "obj_intro": "Clause 6.2 objectives with their measurement and plan.",
        "target": "Target", "measure": "Measurement", "responsible": "Responsible",
        "ip_title": "Interested Parties and Requirements",
        "ip_intro": "Clause 4.2. Who has a stake in our information security and what they need.",
        "party": "Interested party", "requirements": "Requirements", "monitored": "Monitored via",
        "approval_title": "Document Approval Register",
        "approval_intro": "Pipeline-derived lifecycle metadata. The owner maintains the document; GitHub records the independent approver.",
        "approver": "Approver", "approved": "Approved", "next_review": "Next review",
        "generated": "Generated", "from_commit": "from commit",
        "not_recorded": "not recorded",
    },
    "de": {
        "soa_title": "Erklärung zur Anwendbarkeit",
        "soa_intro": ("Gefordert durch ISO/IEC 27001:2022 Abschnitt 6.1.3 d). Listet jede Maßnahme "
                      "aus Anhang A auf, ob sie anwendbar ist und warum. Aus der Datenschicht "
                      "erzeugt; nicht von Hand bearbeiten."),
        "control": "Maßnahme", "title": "Titel", "applicable": "Anwendbar", "status": "Status",
        "documents": "Dokumente", "risks": "Risiken", "evidence": "Nachweise",
        "yes": "Ja", "no": "Nein", "undecided": "Nicht entschieden",
        "exclusions": "Begründung für ausgeschlossene Maßnahmen",
        "impl_notes": "Umsetzungshinweise",
        "no_exclusions": "Es wurde keine Maßnahme ausgeschlossen.",
        "no_notes": "Noch keine Umsetzungshinweise erfasst.",
        "summary": "Zusammenfassung",
        "risk_title": "Risikoregister",
        "risk_intro": ("Ergebnisse der Risikobeurteilung nach Abschnitt 6.1.2 und Risikobehandlungsplan "
                       "nach Abschnitt 6.1.3. Bewertung ist Eintrittswahrscheinlichkeit x Auswirkung "
                       "auf einer Skala von 1 bis 5."),
        "risk_matrix": "Verteilung der Restrisiken",
        "inherent": "Brutto", "residual": "Netto", "band": "Stufe", "owner": "Verantwortlich",
        "due": "Fällig", "treatment": "Behandlung", "assets": "Wertegruppen",
        "threat": "Bedrohung", "vulnerability": "Schwachstelle", "plan": "Behandlungsplan",
        "likelihood": "Wahrscheinlichkeit", "impact": "Auswirkung",
        "cov_title": "Bericht zur Maßnahmenabdeckung",
        "cov_intro": ("Wo das Managementsystem dünn ist. Selbst kein Auditnachweis, aber der "
                      "schnellste Weg, Lücken vor dem Auditor zu finden."),
        "by_theme": "Nach Themenbereich", "theme": "Themenbereich", "total": "Gesamt",
        "gaps": "Lücken", "no_gaps": "Keine Lücken gefunden.",
        "ev_title": "Nachweisverzeichnis",
        "ev_intro": "Aufzeichnungen, die den Betrieb der Maßnahmen belegen, und ihre Aktualität.",
        "files": "Dateien", "newest": "Neueste", "valid": "Gültig für",
        "months": "Monate", "collector": "Sammler", "manual": "manuell",
        "asset_title": "Werteverzeichnis",
        "asset_intro": "Wertegruppen nach A.5.9, mit Verantwortlichen und Klassifizierung.",
        "name": "Name", "type": "Typ", "classification": "Klassifizierung", "location": "Ort",
        "obj_title": "Informationssicherheitsziele",
        "obj_intro": "Ziele nach Abschnitt 6.2 mit Messung und Planung.",
        "target": "Zielwert", "measure": "Messung", "responsible": "Verantwortlich",
        "ip_title": "Interessierte Parteien und Anforderungen",
        "ip_intro": ("Abschnitt 4.2. Wer ein Interesse an unserer Informationssicherheit hat und "
                     "was er benötigt."),
        "party": "Interessierte Partei", "requirements": "Anforderungen", "monitored": "Überwacht durch",
        "approval_title": "Dokumentenfreigabeverzeichnis",
        "approval_intro": "Vom Pipeline abgeleitete Lebenszyklusmetadaten. Der Owner pflegt das Dokument; GitHub zeichnet die unabhängige Freigabe auf.",
        "approver": "Genehmigt von", "approved": "Genehmigt am", "next_review": "Nächste Überprüfung",
        "generated": "Erzeugt", "from_commit": "aus Commit",
        "not_recorded": "nicht erfasst",
    },
}


def git_commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def esc(value) -> str:
    """Escape a value for a Markdown pipe table cell."""
    if value is None:
        return ""
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def table(headers: list[str], rows: list[list]) -> list[str]:
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        out.append("| " + " | ".join(esc(cell) for cell in row) + " |")
    out.append("")
    return out


def header(t: dict, title: str, intro: str, commit: str) -> list[str]:
    stamp = dt.date.today().isoformat()
    return [f"# {title}", "",
            f"*{t['generated']} {stamp} {t['from_commit']} `{commit}`*", "",
            intro, ""]


class Model:
    """Everything the renderers need, loaded once and cross-linked."""

    def __init__(self, document_state: str | None = None) -> None:
        self.controls, self.themes = load_controls()
        self.docs = load_docs()
        self.soa = {e["id"]: e for e in load_yaml("data/soa.yml").get("controls") or []}
        risks_doc = load_yaml("data/risks.yml")
        self.risks = risks_doc.get("risks") or []
        self.risk_meta = risks_doc.get("meta") or {}
        self.assets = load_yaml("data/assets.yml").get("asset_groups") or []
        self.objectives = load_yaml("data/objectives.yml")
        self.parties = load_yaml("data/interested-parties.yml").get("interested_parties") or []
        self.evidence = load_yaml("data/evidence-index.yml").get("evidence") or []
        self.document_state = {}
        if document_state:
            with open(document_state, encoding="utf-8") as fh:
                self.document_state = (json.load(fh).get("documents") or {})

        # Derived reverse indexes. Built here so nothing has to be stored twice.
        self.docs_for: dict[str, list[str]] = {}
        for doc_id, doc in self.docs["en"].items():
            for cid in (doc["meta"] or {}).get("controls") or []:
                self.docs_for.setdefault(cid, []).append(doc_id)
        self.risks_for: dict[str, list[str]] = {}
        for risk in self.risks:
            for cid in risk.get("controls") or []:
                self.risks_for.setdefault(cid, []).append(risk["id"])
        self.evidence_for: dict[str, list[str]] = {}
        for item in self.evidence:
            for cid in item.get("controls") or []:
                self.evidence_for.setdefault(cid, []).append(item["id"])

    def doc_title(self, doc_id: str, lang: str) -> str:
        doc = self.docs[lang].get(doc_id)
        return (doc["meta"] or {}).get("title", doc_id) if doc else doc_id

    def band(self, score: int) -> str:
        return band_for(score, self.risk_meta.get("bands") or [{"max": 25, "level": "?"}])


def render_soa(m: Model, lang: str, commit: str) -> str:
    t = T[lang]
    out = header(t, t["soa_title"], t["soa_intro"], commit)

    counts = {"applicable": 0, "excluded": 0, "undecided": 0, "implemented": 0}
    rows = []
    for cid, control in m.controls.items():
        entry = m.soa.get(cid, {})
        applicable = entry.get("applicable")
        if applicable is True:
            counts["applicable"] += 1
            label = t["yes"]
        elif applicable is False:
            counts["excluded"] += 1
            label = t["no"]
        else:
            counts["undecided"] += 1
            label = t["undecided"]
        if entry.get("status") == "implemented":
            counts["implemented"] += 1
        rows.append([
            cid,
            control["title_en"] if lang == "en" else control["title_de"],
            label,
            entry.get("status", ""),
            ", ".join(m.docs_for.get(cid, [])),
            ", ".join(m.risks_for.get(cid, [])),
            ", ".join(m.evidence_for.get(cid, [])),
        ])

    out += [f"## {t['summary']}", ""]
    out += table([t["total"], t["applicable"], t["no"], t["undecided"], "implemented"],
                 [[len(m.controls), counts["applicable"], counts["excluded"],
                   counts["undecided"], counts["implemented"]]])

    for theme_id, theme in m.themes.items():
        theme_rows = [r for r in rows if r[0].rsplit(".", 1)[0] == theme_id]
        out += [f"## {theme_id} {theme[lang]}", ""]
        out += table([t["control"], t["title"], t["applicable"], t["status"],
                      t["documents"], t["risks"], t["evidence"]], theme_rows)

    out += [f"## {t['exclusions']}", ""]
    excluded = [(cid, e) for cid, e in m.soa.items() if e.get("applicable") is False]
    if not excluded:
        out += [t["no_exclusions"], ""]
    for cid, entry in excluded:
        title = m.controls[cid]["title_en"] if lang == "en" else m.controls[cid]["title_de"]
        out += [f"**{cid} {title}**", "",
                str(entry.get(f"justification_{lang}") or "").strip(), ""]

    out += [f"## {t['impl_notes']}", ""]
    notes = [(cid, e) for cid, e in m.soa.items()
             if e.get("applicable") is True and str(e.get(f"implementation_note_{lang}") or "").strip()]
    if not notes:
        out += [t["no_notes"], ""]
    for cid, entry in notes:
        title = m.controls[cid]["title_en"] if lang == "en" else m.controls[cid]["title_de"]
        out += [f"**{cid} {title}**", "",
                str(entry[f"implementation_note_{lang}"]).strip(), ""]

    return "\n".join(out)


def render_risks(m: Model, lang: str, commit: str) -> str:
    t = T[lang]
    out = header(t, t["risk_title"], t["risk_intro"], commit)

    rows = []
    for risk in m.risks:
        inherent = risk["likelihood"] * risk["impact"]
        residual = risk["residual_likelihood"] * risk["residual_impact"]
        rows.append([risk["id"], risk[f"title_{lang}"], risk.get("owner"),
                     inherent, residual, m.band(residual), risk.get("treatment"),
                     risk.get("status"), risk.get("due")])
    out += table(["ID", t["title"], t["owner"], t["inherent"], t["residual"], t["band"],
                  t["treatment"], t["status"], t["due"]], rows)

    # 5x5 grid of residual scores. Rows are likelihood 5 down to 1 so that the
    # top right corner is the worst place to be, as in every risk matrix.
    out += [f"## {t['risk_matrix']}", ""]
    grid: dict[tuple[int, int], list[str]] = {}
    for risk in m.risks:
        grid.setdefault((risk["residual_likelihood"], risk["residual_impact"]), []).append(risk["id"])
    matrix_rows = []
    for likelihood in range(5, 0, -1):
        row = [f"**{t['likelihood']} {likelihood}**"]
        for impact in range(1, 6):
            row.append(" ".join(grid.get((likelihood, impact), [])) or "-")
        matrix_rows.append(row)
    out += table([""] + [f"{t['impact']} {i}" for i in range(1, 6)], matrix_rows)

    for risk in m.risks:
        out += [f"## {risk['id']} {risk[f'title_{lang}']}", ""]
        out += table([t["title"], ""], [
            [t["owner"], risk.get("owner")],
            [t["assets"], ", ".join(risk.get("asset_groups") or [])],
            [t["threat"], risk.get(f"threat_{lang}")],
            [t["vulnerability"], risk.get(f"vulnerability_{lang}")],
            [t["inherent"], f"{risk['likelihood']} x {risk['impact']} = "
                            f"{risk['likelihood'] * risk['impact']} "
                            f"({m.band(risk['likelihood'] * risk['impact'])})"],
            [t["treatment"], risk.get("treatment")],
            ["Annex A", ", ".join(risk.get("controls") or [])],
            [t["plan"], risk.get(f"treatment_plan_{lang}")],
            [t["residual"], f"{risk['residual_likelihood']} x {risk['residual_impact']} = "
                            f"{risk['residual_likelihood'] * risk['residual_impact']} "
                            f"({m.band(risk['residual_likelihood'] * risk['residual_impact'])})"],
            [t["status"], risk.get("status")],
            [t["due"], risk.get("due")],
        ])
    return "\n".join(out)


def render_coverage(m: Model, lang: str, commit: str) -> str:
    t = T[lang]
    out = header(t, t["cov_title"], t["cov_intro"], commit)

    out += [f"## {t['by_theme']}", ""]
    rows = []
    for theme_id, theme in m.themes.items():
        ids = [c for c in m.controls if c.rsplit(".", 1)[0] == theme_id]
        rows.append([
            f"{theme_id} {theme[lang]}", len(ids),
            sum(1 for c in ids if m.soa.get(c, {}).get("applicable") is True),
            sum(1 for c in ids if m.soa.get(c, {}).get("status") == "implemented"),
            sum(1 for c in ids if c in m.docs_for),
            sum(1 for c in ids if c in m.evidence_for),
        ])
    out += table([t["theme"], t["total"], t["applicable"], "implemented",
                  t["documents"], t["evidence"]], rows)

    out += [f"## {t['gaps']}", ""]
    gaps = []
    for cid in m.controls:
        entry = m.soa.get(cid, {})
        if entry.get("applicable") is None:
            gaps.append([cid, "applicability not decided"])
        elif entry.get("applicable") is True:
            if cid not in m.docs_for:
                gaps.append([cid, "applicable but no document claims it"])
            elif cid not in m.evidence_for:
                gaps.append([cid, "documented but no evidence indexed"])
    orphans = [d for d in m.docs["en"] if not (m.docs["en"][d]["meta"] or {}).get("controls")
               and not d.startswith(("proc-", "ctx-"))]
    for doc_id in orphans:
        gaps.append([doc_id, "policy claims no control"])
    if gaps:
        out += table([t["control"], t["gaps"]], gaps)
    else:
        out += [t["no_gaps"], ""]
    return "\n".join(out)


def render_evidence(m: Model, lang: str, commit: str) -> str:
    t = T[lang]
    out = header(t, t["ev_title"], t["ev_intro"], commit)
    rows = []
    for item in m.evidence:
        matches = evidence_files(item.get("path", ""))
        newest = max((os.path.basename(os.path.dirname(p)) for p in matches), default="")
        rows.append([item["id"], item.get(f"title_{lang}"), item.get("path"),
                     len(matches), newest or t["not_recorded"],
                     f"{item.get('valid_months', '')} {t['months']}",
                     item.get("collector") or t["manual"],
                     ", ".join(item.get("controls") or [])])
    out += table(["ID", t["title"], "Path", t["files"], t["newest"], t["valid"],
                  t["collector"], t["control"]], rows)
    return "\n".join(out)


def render_assets(m: Model, lang: str, commit: str) -> str:
    t = T[lang]
    out = header(t, t["asset_title"], t["asset_intro"], commit)
    rows = [[a["id"], a.get(f"name_{lang}"), a.get("type"), a.get("owner"),
             a.get("classification"), a.get("location")] for a in m.assets]
    out += table(["ID", t["name"], t["type"], t["owner"], t["classification"], t["location"]], rows)
    return "\n".join(out)


def render_objectives(m: Model, lang: str, commit: str) -> str:
    t = T[lang]
    out = header(t, t["obj_title"], t["obj_intro"], commit)
    for obj in m.objectives.get("objectives") or []:
        out += [f"## {obj['id']} {obj.get(f'title_{lang}')}", ""]
        out += table([t["title"], ""], [
            [t["target"], obj.get("target")],
            [t["measure"], obj.get("measurement")],
            ["Baseline", obj.get("baseline")],
            [t["responsible"], obj.get("responsible")],
            [t["due"], obj.get("due")],
            [t["status"], obj.get("status")],
            [t["risks"], ", ".join(obj.get("risks") or [])],
        ])
    return "\n".join(out)


def render_parties(m: Model, lang: str, commit: str) -> str:
    t = T[lang]
    out = header(t, t["ip_title"], t["ip_intro"], commit)
    for party in m.parties:
        out += [f"## {party['id']} {party.get(f'name_{lang}')}", ""]
        for req in party.get(f"requirements_{lang}") or []:
            out.append(f"- {req}")
        out += ["", f"*{t['monitored']}: {party.get('monitored_via', '')}*", ""]
    return "\n".join(out)


def render_document_approvals(m: Model, lang: str, commit: str) -> str:
    t = T[lang]
    out = header(t, t["approval_title"], t["approval_intro"], commit)
    rows = []
    for doc_id, state in sorted(m.document_state.items()):
        rows.append([doc_id, m.doc_title(doc_id, lang), state.get("owner", ""),
                     state.get("status", ""), state.get("approver", ""),
                     state.get("approved_on", ""), state.get("next_review", "")])
    if rows:
        out += table(["ID", t["title"], t["owner"], t["status"], t["approver"],
                      t["approved"], t["next_review"]], rows)
    else:
        out += [t["not_recorded"], ""]
    return "\n".join(out)


RENDERERS = {
    "90-statement-of-applicability": render_soa,
    "91-risk-register": render_risks,
    "92-asset-inventory": render_assets,
    "93-objectives": render_objectives,
    "94-interested-parties": render_parties,
    "95-evidence-index": render_evidence,
    "96-control-coverage": render_coverage,
    "97-document-approval-register": render_document_approvals,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="build")
    parser.add_argument("--document-state", help="JSON generated by tools/document_state.py")
    args = parser.parse_args()

    model = Model(args.document_state)
    commit = git_commit()
    written = 0
    for lang in LANGS:
        outdir = os.path.join(ROOT, args.out, lang)
        os.makedirs(outdir, exist_ok=True)
        for name, fn in RENDERERS.items():
            path = os.path.join(outdir, f"{name}.md")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(fn(model, lang, commit) + "\n")
            written += 1
    print(f"rendered {written} documents into {args.out}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
