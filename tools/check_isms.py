#!/usr/bin/env python3
"""Validate the ISMS data layer and document frontmatter.

Run by CI on every pull request. Exit code 1 means the merge would leave the
management system internally inconsistent.

Errors are things that are provably wrong: a reference to a control that does
not exist, a risk treated with a control declared not applicable, an
overdue review. Warnings are things that are incomplete but legitimately so
while the ISMS is being built. `--strict` promotes every warning to an error
and is what the release workflow uses, so a tagged release pack is always
complete.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys

from isms import (
    DOCS,
    EVIDENCE,
    LANGS,
    ROOT,
    add_months,
    as_date,
    evidence_files,
    load_controls,
    load_docs,
    load_yaml,
)

SOA_STATUS = {"not_assessed", "planned", "partially_implemented", "implemented", "not_applicable"}
SOA_KEYS = {"id", "applicable", "status", "implementation_note_en", "implementation_note_de",
            "justification_en", "justification_de"}
RISK_STATUS = {"open", "in_treatment", "treated", "accepted", "closed"}
TREATMENTS = {"modify", "retain", "avoid", "share"}
CLASSIFICATIONS = {"public", "internal", "confidential", "restricted"}
REQUIRED_DOC_FIELDS = ("id", "title", "lang", "version", "owner",
                       "review_cycle_months", "classification")
DERIVED_DOC_FIELDS = {"status", "approver", "approved_on", "next_review"}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self._bulk: dict[tuple[str, str], list[str]] = {}

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")

    def bulk(self, where: str, category: str, item: str) -> None:
        """Collect a warning that will legitimately fire dozens of times.

        93 separate 'applicability not decided' lines drown the two real
        findings next to them, so these collapse into one line at the end.
        """
        self._bulk.setdefault((where, category), []).append(item)

    def flush_bulk(self) -> None:
        for (where, category), items in self._bulk.items():
            shown = ", ".join(items[:12])
            more = f" (+{len(items) - 12} more)" if len(items) > 12 else ""
            self.warn(where, f"{category} [{len(items)}]: {shown}{more}")
        self._bulk.clear()


def check_documents(rep: Report, docs: dict, controls: dict, today: dt.date) -> None:
    for lang in LANGS:
        for doc_id, doc in docs[lang].items():
            where = doc["relpath"]
            meta = doc["meta"]
            if meta is None:
                rep.error(where, "no YAML frontmatter block")
                continue

            for field in REQUIRED_DOC_FIELDS:
                if meta.get(field) in (None, ""):
                    rep.error(where, f"frontmatter is missing required field '{field}'")
            for field in sorted(DERIVED_DOC_FIELDS.intersection(meta)):
                rep.error(where, f"'{field}' is pipeline-derived and must not be stored in frontmatter")

            if doc_id != doc["filename_id"]:
                rep.error(where, f"frontmatter id '{doc_id}' does not match the filename")
            if meta.get("lang") != lang:
                rep.error(where, f"frontmatter lang '{meta.get('lang')}' but file is under docs/{lang}/")
            if meta.get("classification") not in CLASSIFICATIONS:
                rep.error(where, f"classification '{meta.get('classification')}' is not one of {sorted(CLASSIFICATIONS)}")
            version = str(meta.get("version", ""))
            if not SEMVER_RE.match(version):
                rep.error(where, f"version '{version}' is not MAJOR.MINOR.PATCH")
            cycle = meta.get("review_cycle_months")
            if not isinstance(cycle, int) or isinstance(cycle, bool) or cycle <= 0:
                rep.error(where, "review_cycle_months must be a positive integer")

            for ctrl in meta.get("controls") or []:
                if ctrl not in controls:
                    rep.error(where, f"references unknown control '{ctrl}'")



def check_translation_parity(rep: Report, docs: dict) -> None:
    en_ids, de_ids = set(docs["en"]), set(docs["de"])
    for missing in sorted(en_ids - de_ids):
        rep.error("docs/de", f"no German counterpart for '{missing}'")
    for missing in sorted(de_ids - en_ids):
        rep.error("docs/en", f"no English counterpart for '{missing}'")

    for doc_id in sorted(en_ids & de_ids):
        en, de = docs["en"][doc_id], docs["de"][doc_id]
        if not (en["meta"] and de["meta"]):
            continue
        if str(en["meta"].get("version")) != str(de["meta"].get("version")):
            rep.error(de["relpath"], f"version {de['meta'].get('version')} differs from the English "
                                     f"{en['meta'].get('version')}; translations are out of sync")
        if set(en["meta"].get("controls") or []) != set(de["meta"].get("controls") or []):
            rep.error(de["relpath"], "controls list differs from the English version")


def documents_by_control(docs: dict) -> dict[str, list[str]]:
    """Which documents claim which control, taken from frontmatter.

    This mapping is derived, never stored. Storing it in soa.yml as well would
    mean two places to update and a guaranteed drift the day someone forgets.
    """
    out: dict[str, list[str]] = {}
    for doc_id, doc in docs["en"].items():
        for cid in (doc["meta"] or {}).get("controls") or []:
            out.setdefault(cid, []).append(doc_id)
    return {cid: sorted(ids) for cid, ids in out.items()}


def check_soa(rep: Report, soa: dict, controls: dict, docs: dict) -> dict:
    where = "data/soa.yml"
    coverage = documents_by_control(docs)
    seen: dict[str, dict] = {}

    for entry in soa.get("controls") or []:
        cid = entry.get("id")
        if cid not in controls:
            rep.error(where, f"unknown control '{cid}'")
            continue
        if cid in seen:
            rep.error(where, f"duplicate entry for '{cid}'")
            continue
        seen[cid] = entry

        # Anything else is either a typo or an attempt to store something that
        # is derived elsewhere, which is how the two copies start to disagree.
        for key in set(entry) - SOA_KEYS:
            rep.error(where, f"{cid}: unexpected key '{key}'. Documents, risks and evidence "
                             f"link themselves to controls from their own files")

        applicable = entry.get("applicable")
        status = entry.get("status")
        if status not in SOA_STATUS:
            rep.error(where, f"{cid}: status '{status}' is not one of {sorted(SOA_STATUS)}")

        if applicable is None or status == "not_assessed":
            rep.bulk(where, "applicability not decided", cid)
            continue

        if applicable is False:
            if status != "not_applicable":
                rep.error(where, f"{cid}: applicable is false but status is '{status}'")
            for lang in LANGS:
                if not str(entry.get(f"justification_{lang}") or "").strip():
                    rep.error(where, f"{cid}: excluded without a justification_{lang}; "
                                     f"clause 6.1.3 d) requires one")
            if cid in coverage:
                rep.error(where, f"{cid}: excluded, but {', '.join(coverage[cid])} still claims it "
                                 f"in the frontmatter")
            continue

        # applicable is True from here on
        if status == "not_applicable":
            rep.error(where, f"{cid}: applicable is true but status is 'not_applicable'")
        if cid not in coverage:
            if status in ("implemented", "partially_implemented"):
                rep.error(where, f"{cid}: status is '{status}' but no document lists it in "
                                 f"its frontmatter")
            else:
                rep.bulk(where, "applicable, no implementing document yet", cid)

        if not any(str(entry.get(f"implementation_note_{lang}") or "").strip() for lang in LANGS):
            rep.bulk(where, "applicable, no implementation note written", cid)

    for cid in controls:
        if cid not in seen:
            rep.error(where, f"control '{cid}' has no Statement of Applicability entry")

    for cid in sorted(coverage):
        if cid in seen and seen[cid].get("applicable") is None:
            rep.bulk(where, "documented but applicability still undecided", cid)

    return seen


def check_risks(rep: Report, risks_doc: dict, controls: dict, soa: dict,
                asset_ids: set, today: dt.date) -> set:
    where = "data/risks.yml"
    meta = risks_doc.get("meta") or {}
    acceptance = sorted(meta.get("acceptance") or [], key=lambda a: a["max_residual"])
    seen: set[str] = set()

    for risk in risks_doc.get("risks") or []:
        rid = risk.get("id", "<no id>")
        if rid in seen:
            rep.error(where, f"duplicate risk id '{rid}'")
        seen.add(rid)

        if not risk.get("owner"):
            rep.error(where, f"{rid}: no owner")
        for group in risk.get("asset_groups") or []:
            if group not in asset_ids:
                rep.error(where, f"{rid}: references unknown asset group '{group}'")
        if not risk.get("asset_groups"):
            rep.error(where, f"{rid}: not linked to any asset group")

        scores = {}
        for field in ("likelihood", "impact", "residual_likelihood", "residual_impact"):
            value = risk.get(field)
            if not isinstance(value, int) or not 1 <= value <= 5:
                rep.error(where, f"{rid}: {field} must be an integer 1..5, got {value!r}")
            else:
                scores[field] = value

        treatment = risk.get("treatment")
        if treatment not in TREATMENTS:
            rep.error(where, f"{rid}: treatment '{treatment}' is not one of {sorted(TREATMENTS)}")
        status = risk.get("status")
        if status not in RISK_STATUS:
            rep.error(where, f"{rid}: status '{status}' is not one of {sorted(RISK_STATUS)}")

        refs = risk.get("controls") or []
        if treatment == "modify" and not refs:
            rep.error(where, f"{rid}: treatment is 'modify' but no control is referenced")
        for cid in refs:
            if cid not in controls:
                rep.error(where, f"{rid}: references unknown control '{cid}'")
            elif soa.get(cid, {}).get("applicable") is False:
                rep.error(where, f"{rid}: treated with '{cid}', which the Statement of "
                                 f"Applicability declares not applicable")

        if len(scores) == 4:
            inherent = scores["likelihood"] * scores["impact"]
            residual = scores["residual_likelihood"] * scores["residual_impact"]
            if residual > inherent:
                rep.warn(where, f"{rid}: residual score {residual} is higher than the inherent "
                                f"score {inherent}; treatment made it worse")
            needed = next((a["approval"] for a in acceptance if residual <= a["max_residual"]), "top management")
            if status == "accepted" and needed != "none" and not risk.get("accepted_by"):
                rep.error(where, f"{rid}: accepted with residual score {residual}, which requires "
                                 f"approval by {needed}; record it in 'accepted_by'")

        due = as_date(risk.get("due"))
        if status in ("open", "in_treatment"):
            if due is None:
                rep.error(where, f"{rid}: still {status} but no due date")
            elif due < today:
                rep.error(where, f"{rid}: treatment overdue since {due.isoformat()}")

    return seen


def check_assets(rep: Report, assets_doc: dict) -> set:
    where = "data/assets.yml"
    ids: set[str] = set()
    for group in assets_doc.get("asset_groups") or []:
        gid = group.get("id", "<no id>")
        if gid in ids:
            rep.error(where, f"duplicate asset group id '{gid}'")
        ids.add(gid)
        if group.get("classification") not in CLASSIFICATIONS:
            rep.error(where, f"{gid}: classification '{group.get('classification')}' is not one "
                             f"of {sorted(CLASSIFICATIONS)}")
        if not group.get("owner"):
            rep.error(where, f"{gid}: no owner")
    return ids


def check_objectives(rep: Report, objectives_doc: dict, risk_ids: set) -> None:
    where = "data/objectives.yml"
    seen: set[str] = set()
    for obj in objectives_doc.get("objectives") or []:
        oid = obj.get("id", "<no id>")
        if oid in seen:
            rep.error(where, f"duplicate objective id '{oid}'")
        seen.add(oid)
        # Clause 6.2 requires each of these; a blank one is a finding.
        for field in ("target", "measurement", "responsible", "due"):
            if not obj.get(field):
                rep.error(where, f"{oid}: clause 6.2 requires '{field}'")
        if as_date(obj.get("due")) is None:
            rep.error(where, f"{oid}: due '{obj.get('due')}' is not a date")
        for rid in obj.get("risks") or []:
            if rid not in risk_ids:
                rep.error(where, f"{oid}: references unknown risk id '{rid}'")


def check_evidence(rep: Report, evidence_doc: dict, controls: dict,
                   objective_ids: set, today: dt.date) -> set:
    where = "data/evidence-index.yml"
    ids: set[str] = set()
    indexed_files: set[str] = set()

    for item in evidence_doc.get("evidence") or []:
        eid = item.get("id", "<no id>")
        if eid in ids:
            rep.error(where, f"duplicate evidence id '{eid}'")
        ids.add(eid)

        for cid in item.get("controls") or []:
            if cid not in controls:
                rep.error(where, f"{eid}: references unknown control '{cid}'")
        for oid in item.get("objectives") or []:
            if oid not in objective_ids:
                rep.error(where, f"{eid}: references unknown objective '{oid}'")

        pattern = item.get("path")
        if not pattern:
            rep.error(where, f"{eid}: no path")
            continue
        matches = evidence_files(pattern)
        indexed_files.update(matches)

        if not matches:
            # A collector-backed entry is legitimately empty until the workflow
            # has run for the first time; a manual one is simply missing.
            if item.get("collector"):
                rep.warn(where, f"{eid}: no file matches '{pattern}' yet "
                                f"(collector '{item['collector']}' has not run)")
            else:
                rep.error(where, f"{eid}: no file matches '{pattern}'")
            continue

        valid_months = item.get("valid_months")
        newest = newest_collection_date(matches)
        if isinstance(valid_months, int) and newest:
            expires = add_months(newest, valid_months)
            if expires < today:
                rep.error(where, f"{eid}: newest evidence is from {newest.isoformat()} and expired "
                                 f"on {expires.isoformat()}")

    for path in all_evidence_files():
        if path not in indexed_files:
            rep.warn("evidence/", f"{os.path.relpath(path, ROOT)} is not listed in the evidence index")

    return ids


def newest_collection_date(paths: list[str]) -> dt.date | None:
    """Collection date taken from a YYYY-MM directory in the path.

    File mtime is useless here: a fresh git clone sets it to checkout time, so
    every piece of evidence would look brand new to CI.
    """
    dates = []
    for path in paths:
        for part in path.split(os.sep):
            match = re.search(r"(?<!\d)(\d{4})-(\d{2})(?!\d)", part)
            if match:
                try:
                    dates.append(dt.date(int(match[1]), int(match[2]), 1))
                except ValueError:
                    pass
    return max(dates) if dates else None


def all_evidence_files() -> list[str]:
    out = []
    for dirpath, _dirnames, filenames in os.walk(EVIDENCE):
        for name in filenames:
            if name.startswith(".") or name.upper() == "README.MD":
                continue
            out.append(os.path.join(dirpath, name))
    return sorted(out)


def check_todos(rep: Report) -> None:
    """TODO markers are fine while building, never in a released pack."""
    for base in ("data", "docs"):
        for dirpath, _dirnames, filenames in os.walk(os.path.join(ROOT, base)):
            for name in sorted(filenames):
                if not name.endswith((".yml", ".yaml", ".md")):
                    continue
                path = os.path.join(dirpath, name)
                with open(path, encoding="utf-8") as fh:
                    hits = sum(1 for line in fh if "TODO" in line)
                if hits:
                    rep.bulk("TODO", "unresolved placeholders",
                             f"{os.path.relpath(path, ROOT)}({hits})")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true",
                        help="treat warnings as errors (used for release packs)")
    parser.add_argument("--today", help="override today's date, for testing (YYYY-MM-DD)")
    args = parser.parse_args()

    today = as_date(args.today) or dt.date.today()
    rep = Report()

    controls, _themes = load_controls()
    docs = load_docs()
    soa_doc = load_yaml("data/soa.yml")
    risks_doc = load_yaml("data/risks.yml")
    assets_doc = load_yaml("data/assets.yml")
    objectives_doc = load_yaml("data/objectives.yml")
    evidence_doc = load_yaml("data/evidence-index.yml")

    objective_ids = {o.get("id") for o in objectives_doc.get("objectives") or []}
    risk_ids = {r.get("id") for r in risks_doc.get("risks") or []}

    check_documents(rep, docs, controls, today)
    check_translation_parity(rep, docs)
    asset_ids = check_assets(rep, assets_doc)
    check_evidence(rep, evidence_doc, controls, objective_ids, today)
    soa = check_soa(rep, soa_doc, controls, docs)
    check_risks(rep, risks_doc, controls, soa, asset_ids, today)
    check_objectives(rep, objectives_doc, risk_ids)
    check_todos(rep)
    rep.flush_bulk()

    for msg in rep.warnings:
        print(f"WARNING  {msg}")
    for msg in rep.errors:
        print(f"ERROR    {msg}")

    failed = len(rep.errors) + (len(rep.warnings) if args.strict else 0)
    print(f"\n{len(controls)} controls, {len(docs['en'])} documents per language, "
          f"{len(risk_ids)} risks, {len(rep.errors)} errors, {len(rep.warnings)} warnings"
          f"{' (strict: warnings fail)' if args.strict else ''}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
