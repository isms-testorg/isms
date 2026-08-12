#!/usr/bin/env python3
"""Small lifecycle regression check; no GitHub access required."""

from __future__ import annotations

import datetime as dt

from document_state import approval_state, review_state
from review_due import due_documents


DOC = {"meta": {"owner": "@owner", "review_cycle_months": 12}}
PR = {
    "number": 5,
    "merged_at": "2026-08-12T10:00:00Z",
    "head": {"sha": "final"},
    "user": {"login": "author"},
}


def review(login: str, commit: str = "final", state: str = "APPROVED",
           submitted: str = "2026-08-12T09:00:00Z") -> dict:
    return {"state": state, "commit_id": commit, "submitted_at": submitted,
            "user": {"login": login}}


def rejected(reviews: list[dict]) -> None:
    try:
        approval_state(DOC, PR, reviews)
    except ValueError:
        return
    raise AssertionError("invalid approval was accepted")


def main() -> None:
    assert review_state(DOC) == {
        "status": "in_review", "owner": "@owner", "review_cycle_months": 12,
    }
    state = approval_state(DOC, PR, [review("reviewer")])
    assert state["status"] == "approved"
    assert state["approver"] == "@reviewer"
    assert state["approved_on"] == "2026-08-12"
    assert state["next_review"] == "2027-08-12"
    assert state["pull_request"] == 5
    assert state["approved_revision"] == "final"

    rejected([review("author")])
    rejected([review("owner")])
    rejected([review("reviewer", commit="stale")])
    rejected([review("reviewer"),
              review("reviewer", state="CHANGES_REQUESTED",
                     submitted="2026-08-12T09:30:00Z")])

    docs = {"en": {"x": {"meta": {"title": "X", "version": "1.0.0"}}},
            "de": {"x": {"relpath": "docs/de/x.md"}}}
    docs["en"]["x"]["relpath"] = "docs/en/x.md"
    states = {"x": {**state, "next_review": "2026-08-20"}}
    due = due_documents(docs, states, dt.date(2026, 8, 10), 30)
    assert due["x"]["days"] == 10
    assert due["x"]["owner"] == "owner"
    print("document lifecycle tests passed")


if __name__ == "__main__":
    main()
