"""Shared loading helpers for the ISMS tooling.

Kept deliberately small: one place that knows where files live and how a
document's frontmatter is parsed, so check_isms.py, render.py and scaffold.py
cannot drift apart on those two questions.
"""

from __future__ import annotations

import calendar
import datetime as dt
import glob
import os
import re

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DOCS = os.path.join(ROOT, "docs")
EVIDENCE = os.path.join(ROOT, "evidence")

LANGS = ("en", "de")

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.DOTALL)


def load_yaml(relpath: str) -> dict:
    with open(os.path.join(ROOT, relpath), encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def load_controls() -> tuple[dict, dict]:
    """Return (controls_by_id, themes). Order of the catalogue is preserved."""
    raw = load_yaml("data/controls/annex-a-2022.yml")
    return {c["id"]: c for c in raw["controls"]}, raw.get("themes", {})


def split_frontmatter(text: str) -> tuple[dict | None, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, text
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def load_docs() -> dict:
    """Return {lang: {doc_id: {"path", "relpath", "meta", "body"}}}."""
    out: dict[str, dict] = {lang: {} for lang in LANGS}
    for lang in LANGS:
        pattern = os.path.join(DOCS, lang, "**", "*.md")
        for path in sorted(glob.glob(pattern, recursive=True)):
            if os.path.basename(path).upper() == "README.MD":
                continue
            with open(path, encoding="utf-8") as fh:
                meta, body = split_frontmatter(fh.read())
            relpath = os.path.relpath(path, ROOT)
            doc_id = (meta or {}).get("id") or os.path.splitext(os.path.basename(path))[0]
            out[lang][doc_id] = {
                "path": path,
                "relpath": relpath,
                "meta": meta,
                "body": body,
                "filename_id": os.path.splitext(os.path.basename(path))[0],
            }
    return out


def add_months(start: dt.date, months: int) -> dt.date:
    """Date `months` later, clamped to the last valid day of the target month."""
    total = start.month - 1 + months
    year = start.year + total // 12
    month = total % 12 + 1
    day = min(start.day, calendar.monthrange(year, month)[1])
    return dt.date(year, month, day)


def as_date(value) -> dt.date | None:
    """Coerce a YAML scalar to a date, or None if it is not one."""
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        try:
            return dt.date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


def band_for(score: int, bands: list[dict]) -> str:
    for band in sorted(bands, key=lambda b: b["max"]):
        if score <= band["max"]:
            return band["level"]
    return bands[-1]["level"]


def evidence_files(pattern: str) -> list[str]:
    return sorted(glob.glob(os.path.join(ROOT, pattern)))


def _selftest() -> None:
    assert add_months(dt.date(2026, 1, 31), 1) == dt.date(2026, 2, 28), "clamp short month"
    assert add_months(dt.date(2024, 1, 31), 1) == dt.date(2024, 2, 29), "clamp leap year"
    assert add_months(dt.date(2026, 8, 10), 12) == dt.date(2027, 8, 10), "plain year"
    assert add_months(dt.date(2026, 12, 1), 1) == dt.date(2027, 1, 1), "year rollover"
    assert add_months(dt.date(2026, 8, 10), 0) == dt.date(2026, 8, 10), "zero months"

    bands = [{"max": 4, "level": "low"}, {"max": 9, "level": "medium"},
             {"max": 14, "level": "high"}, {"max": 25, "level": "critical"}]
    assert band_for(1, bands) == "low"
    assert band_for(4, bands) == "low", "boundary is inclusive"
    assert band_for(5, bands) == "medium"
    assert band_for(25, bands) == "critical"

    assert as_date("2026-08-10") == dt.date(2026, 8, 10)
    assert as_date("TODO: later") is None
    assert as_date(None) is None

    meta, body = split_frontmatter("---\nid: x\n---\nhello\n")
    assert meta == {"id": "x"} and body == "hello\n"
    assert split_frontmatter("no frontmatter")[0] is None

    print("isms.py self-test OK")


if __name__ == "__main__":
    _selftest()
