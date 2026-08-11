#!/usr/bin/env python3
"""Fault injection tests for the validator.

A checker that never fires is worse than no checker: it produces a green tick
that nobody questions. Each test here feeds in data with one specific defect
and asserts that the matching rule catches it, plus a clean case that must
produce no errors at all.

Synthetic dicts, no filesystem, no framework. Run with `make test`.
"""

from __future__ import annotations

import datetime as dt
import sys

from check_isms import (
    Report,
    check_documents,
    check_evidence,
    check_objectives,
    check_risks,
    check_soa,
    check_translation_parity,
)

TODAY = dt.date(2026, 8, 10)
CONTROLS = {
    "A.5.15": {"id": "A.5.15", "theme": "A.5", "title_en": "Access control", "title_de": "Zugangssteuerung"},
    "A.8.2": {"id": "A.8.2", "theme": "A.8", "title_en": "Privileged access rights", "title_de": "Privilegierte Zugangsrechte"},
    "A.7.4": {"id": "A.7.4", "theme": "A.7", "title_en": "Physical security monitoring", "title_de": "Überwachung der physischen Sicherheit"},
}


def doc(**overrides):
    meta = {
        "id": "pol-access-control", "title": "Access Control Policy", "lang": "en",
        "version": "1.0.0", "status": "approved", "owner": "@alice", "approver": "@bob",
        "approved_on": dt.date(2026, 1, 15), "next_review": dt.date(2027, 1, 15),
        "review_cycle_months": 12, "classification": "internal", "controls": ["A.5.15"],
    }
    meta.update(overrides)
    return {"path": "/x", "relpath": f"docs/{meta['lang']}/pol-access-control.md",
            "meta": meta, "body": "", "filename_id": meta["id"]}


def docs_pair(en_overrides=None, de_overrides=None):
    en = doc(**(en_overrides or {}))
    de = doc(lang="de", **(de_overrides or {}))
    return {"en": {en["meta"]["id"]: en}, "de": {de["meta"]["id"]: de}}


def risk(**overrides):
    base = {
        "id": "R-001", "title_en": "t", "title_de": "t", "owner": "@alice",
        "asset_groups": ["AG-SRC"], "likelihood": 4, "impact": 4,
        "residual_likelihood": 2, "residual_impact": 2,
        "treatment": "modify", "controls": ["A.5.15"], "status": "in_treatment",
        "due": dt.date(2027, 1, 1),
    }
    base.update(overrides)
    return base


RISK_META = {"meta": {"acceptance": [{"max_residual": 6, "approval": "none"},
                                     {"max_residual": 25, "approval": "top management"}]}}


def soa_entry(cid, **overrides):
    base = {"id": cid, "applicable": True, "status": "planned"}
    base.update(overrides)
    return base


def errors_from(fn, *args) -> list[str]:
    rep = Report()
    fn(rep, *args)
    rep.flush_bulk()
    return rep.errors


def expect_error(name: str, errors: list[str], fragment: str) -> None:
    assert any(fragment in e for e in errors), \
        f"{name}: expected an error containing {fragment!r}, got {errors or '[none]'}"
    print(f"  caught  {name}")


def expect_clean(name: str, errors: list[str]) -> None:
    assert not errors, f"{name}: expected no errors, got {errors}"
    print(f"  clean   {name}")


def test_documents() -> None:
    print("documents")
    expect_clean("valid document", errors_from(check_documents, docs_pair(), CONTROLS, TODAY))

    expect_error("unknown control reference",
                 errors_from(check_documents, docs_pair({"controls": ["A.9.99"]},
                                                        {"controls": ["A.9.99"]}), CONTROLS, TODAY),
                 "unknown control 'A.9.99'")

    expect_error("next_review does not match the cycle",
                 errors_from(check_documents, docs_pair({"next_review": dt.date(2026, 6, 1)}),
                             CONTROLS, TODAY),
                 "does not equal approved_on")

    expect_error("review overdue",
                 errors_from(check_documents,
                             docs_pair({"approved_on": dt.date(2024, 1, 15),
                                        "next_review": dt.date(2025, 1, 15)}),
                             CONTROLS, TODAY),
                 "review overdue")

    expect_error("approved without an approver",
                 errors_from(check_documents, docs_pair({"approver": None}), CONTROLS, TODAY),
                 "no approver is named")

    expect_error("bad version format",
                 errors_from(check_documents, docs_pair({"version": "1.0"}), CONTROLS, TODAY),
                 "is not MAJOR.MINOR.PATCH")

    expect_error("lang does not match the directory",
                 errors_from(check_documents, docs_pair({"lang": "fr"}), CONTROLS, TODAY),
                 "but file is under docs/en/")

    expect_error("unknown classification",
                 errors_from(check_documents, docs_pair({"classification": "secret"}),
                             CONTROLS, TODAY),
                 "is not one of")


def test_parity() -> None:
    print("translation parity")
    expect_clean("languages in sync", errors_from(check_translation_parity, docs_pair()))

    expect_error("version drift between languages",
                 errors_from(check_translation_parity, docs_pair({}, {"version": "1.1.0"})),
                 "translations are out of sync")

    expect_error("controls drift between languages",
                 errors_from(check_translation_parity, docs_pair({}, {"controls": ["A.8.2"]})),
                 "controls list differs")

    missing_de = docs_pair()
    missing_de["de"] = {}
    expect_error("no German counterpart",
                 errors_from(check_translation_parity, missing_de),
                 "no German counterpart")


def test_soa() -> None:
    print("statement of applicability")
    full = {"controls": [soa_entry(c) for c in CONTROLS]}
    docs = docs_pair()

    expect_error("control missing from the SoA",
                 errors_from(check_soa, {"controls": [soa_entry("A.5.15")]}, CONTROLS, docs),
                 "has no Statement of Applicability entry")

    expect_error("excluded without a justification",
                 errors_from(check_soa,
                             {"controls": [soa_entry("A.5.15", applicable=False,
                                                     status="not_applicable"),
                                           soa_entry("A.8.2"), soa_entry("A.7.4")]},
                             CONTROLS, docs),
                 "excluded without a justification_en")

    expect_error("excluded but a document still claims it",
                 errors_from(check_soa,
                             {"controls": [soa_entry("A.5.15", applicable=False,
                                                     status="not_applicable",
                                                     justification_en="x", justification_de="x"),
                                           soa_entry("A.8.2"), soa_entry("A.7.4")]},
                             CONTROLS, docs),
                 "still claims it in the frontmatter")

    expect_error("applicable but flagged not_applicable",
                 errors_from(check_soa,
                             {"controls": [soa_entry("A.5.15", status="not_applicable"),
                                           soa_entry("A.8.2"), soa_entry("A.7.4")]},
                             CONTROLS, docs),
                 "applicable is true but status is 'not_applicable'")

    expect_error("implemented with no document behind it",
                 errors_from(check_soa,
                             {"controls": [soa_entry("A.5.15"),
                                           soa_entry("A.8.2", status="implemented"),
                                           soa_entry("A.7.4")]},
                             CONTROLS, docs),
                 "no document lists it in its frontmatter")

    expect_error("derived key stored in the SoA",
                 errors_from(check_soa,
                             {"controls": [soa_entry("A.5.15", implemented_by=["pol-access-control"]),
                                           soa_entry("A.8.2"), soa_entry("A.7.4")]},
                             CONTROLS, docs),
                 "unexpected key 'implemented_by'")

    expect_error("duplicate SoA entry",
                 errors_from(check_soa,
                             {"controls": [soa_entry("A.5.15"), soa_entry("A.5.15"),
                                           soa_entry("A.8.2"), soa_entry("A.7.4")]},
                             CONTROLS, docs),
                 "duplicate entry")

    expect_clean("complete SoA", errors_from(check_soa, full, CONTROLS, docs))


def test_risks() -> None:
    print("risks")
    soa = {c: soa_entry(c) for c in CONTROLS}
    assets = {"AG-SRC"}

    expect_clean("valid risk",
                 errors_from(check_risks, {**RISK_META, "risks": [risk()]},
                             CONTROLS, soa, assets, TODAY))

    excluded = dict(soa, **{"A.5.15": soa_entry("A.5.15", applicable=False,
                                                status="not_applicable")})
    expect_error("treated with an excluded control",
                 errors_from(check_risks, {**RISK_META, "risks": [risk()]},
                             CONTROLS, excluded, assets, TODAY),
                 "declares not applicable")

    expect_error("modify with no control",
                 errors_from(check_risks, {**RISK_META, "risks": [risk(controls=[])]},
                             CONTROLS, soa, assets, TODAY),
                 "no control is referenced")

    expect_error("unknown asset group",
                 errors_from(check_risks, {**RISK_META, "risks": [risk(asset_groups=["AG-NOPE"])]},
                             CONTROLS, soa, assets, TODAY),
                 "unknown asset group")

    expect_error("likelihood out of range",
                 errors_from(check_risks, {**RISK_META, "risks": [risk(likelihood=9)]},
                             CONTROLS, soa, assets, TODAY),
                 "must be an integer 1..5")

    expect_error("treatment overdue",
                 errors_from(check_risks, {**RISK_META, "risks": [risk(due=dt.date(2026, 1, 1))]},
                             CONTROLS, soa, assets, TODAY),
                 "treatment overdue")

    expect_error("high residual accepted without approval",
                 errors_from(check_risks,
                             {**RISK_META, "risks": [risk(status="accepted",
                                                          residual_likelihood=4,
                                                          residual_impact=4)]},
                             CONTROLS, soa, assets, TODAY),
                 "requires approval by top management")

    expect_clean("high residual accepted with approval",
                 errors_from(check_risks,
                             {**RISK_META, "risks": [risk(status="accepted",
                                                          residual_likelihood=4,
                                                          residual_impact=4,
                                                          accepted_by="@managing-director")]},
                             CONTROLS, soa, assets, TODAY))

    expect_error("duplicate risk id",
                 errors_from(check_risks, {**RISK_META, "risks": [risk(), risk()]},
                             CONTROLS, soa, assets, TODAY),
                 "duplicate risk id")


def test_objectives_and_evidence() -> None:
    print("objectives and evidence")
    good = {"objectives": [{"id": "OBJ-01", "target": "100%", "measurement": "monthly",
                            "responsible": "@alice", "due": dt.date(2026, 12, 31),
                            "risks": ["R-001"]}]}
    expect_clean("valid objective", errors_from(check_objectives, good, {"R-001"}))

    expect_error("objective missing a clause 6.2 field",
                 errors_from(check_objectives,
                             {"objectives": [dict(good["objectives"][0], measurement=None)]},
                             {"R-001"}),
                 "clause 6.2 requires 'measurement'")

    expect_error("objective points at an unknown risk",
                 errors_from(check_objectives, good, set()),
                 "unknown risk id")

    expect_error("manual evidence file missing",
                 errors_from(check_evidence,
                             {"evidence": [{"id": "EV-X", "path": "evidence/manual/nope.md",
                                            "controls": ["A.5.15"]}]},
                             CONTROLS, set(), TODAY),
                 "no file matches")

    expect_error("evidence points at an unknown control",
                 errors_from(check_evidence,
                             {"evidence": [{"id": "EV-X", "path": "evidence/manual/nope.md",
                                            "controls": ["A.9.99"]}]},
                             CONTROLS, set(), TODAY),
                 "unknown control 'A.9.99'")


def main() -> int:
    for test in (test_documents, test_parity, test_soa, test_risks,
                 test_objectives_and_evidence):
        test()
    print("\nall fault injection tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
