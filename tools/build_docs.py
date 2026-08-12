#!/usr/bin/env python3
"""Assemble the ISMS into one document per language and convert it with Pandoc.

The authored Markdown and the rendered data documents are concatenated into
build/<lang>/isms-pack.md first, with frontmatter turned into a visible header
table. Concatenating ourselves rather than handing Pandoc a list of files is
deliberate: Pandoc merges the YAML metadata block of every input file, so the
title of the pack would silently become the title of whichever policy sorted
last.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile

from isms import DOCS, LANGS, ROOT, split_frontmatter

ORG = "dev-test"
PDF_THEME = os.path.join(ROOT, "tools", "pdf-theme.tex")
LANDSCAPE_TABLES = os.path.join(ROOT, "tools", "landscape-tables.lua")

PACK_TITLE = {
    "en": "Information Security Management System",
    "de": "Informationssicherheits-Managementsystem",
}
PACK_SUBTITLE = {
    "en": "ISO/IEC 27001:2022 documentation pack",
    "de": "Dokumentationspaket nach ISO/IEC 27001:2022",
}
FIELD_LABELS = {
    "en": {"id": "ID", "version": "Version", "owner": "Owner",
           "classification": "Classification", "controls": "Annex A controls"},
    "de": {"id": "ID", "version": "Version", "owner": "Verantwortlich",
           "classification": "Klassifizierung", "controls": "Maßnahmen aus Anhang A"},
}
STATE_LABELS = {
    "en": {"status": "Lifecycle", "approver": "Approved by", "approved_on": "Approved", "next_review": "Next review"},
    "de": {"status": "Lebenszyklus", "approver": "Genehmigt von", "approved_on": "Genehmigt am", "next_review": "Nächste Überprüfung"},
}
SECTION_TITLES = {
    "00-context": {"en": "Context and Scope", "de": "Kontext und Anwendungsbereich"},
    "10-policies": {"en": "Policies", "de": "Richtlinien"},
    "20-procedures": {"en": "Procedures", "de": "Verfahren"},
    "generated": {"en": "Generated Records", "de": "Erzeugte Aufzeichnungen"},
}
LEADING_H1 = re.compile(r"\A\s*#\s+.*?\n")
ATX_HEADING = re.compile(r"^(#{1,5})(\s+\S)")
FENCE = re.compile(r"^\s*(```|~~~)")


def demote_headings(body: str) -> str:
    """Push every heading down one level so it nests under the document title.

    Section is h1, document title is h2, so a policy's own "## Purpose" has to
    become h3 or the table of contents comes out flat. Fenced blocks are
    skipped: a shell comment is not a heading.
    """
    out, in_fence = [], False
    for line in body.split("\n"):
        if FENCE.match(line):
            in_fence = not in_fence
        elif not in_fence:
            line = ATX_HEADING.sub(r"#\1\2", line)
        out.append(line)
    return "\n".join(out)


def doc_header_table(meta: dict, lang: str, state: dict | None) -> list[str]:
    labels = FIELD_LABELS[lang]
    cells = []
    for key, label in labels.items():
        value = meta.get(key)
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        cells.append(f"**{label}:** {value if value not in (None, '', []) else '-'}")
    if state:
        for key, label in STATE_LABELS[lang].items():
            value = state.get(key)
            if value:
                cells.append(f"**{label}:** {value}")
    return ["> " + "  \n> ".join(cells), ""]


def collect_sources(lang: str, build: str) -> list[tuple[str, str]]:
    """(section_key, path) in the order they appear in the pack."""
    out = []
    for section in ("00-context", "10-policies", "20-procedures"):
        directory = os.path.join(DOCS, lang, section)
        if not os.path.isdir(directory):
            continue
        for name in sorted(os.listdir(directory)):
            if name.endswith(".md") and name.upper() != "README.MD":
                out.append((section, os.path.join(directory, name)))
    generated = os.path.join(build, lang)
    if os.path.isdir(generated):
        for name in sorted(os.listdir(generated)):
            if name.endswith(".md") and name != "isms-pack.md":
                out.append(("generated", os.path.join(generated, name)))
    return out


def build_pack(lang: str, build: str, version: str, states: dict) -> str:
    sources = collect_sources(lang, build)
    stamp = dt.date.today().isoformat()

    lines = [
        "---",
        f'title: "{PACK_TITLE[lang]}"',
        f'subtitle: "{PACK_SUBTITLE[lang]} - {version}"',
        f'author: "{ORG}"',
        f'date: "{stamp}"',
        f"lang: {lang}",
        "toc: true",
        "toc-depth: 2",
        "numbersections: true",
        "geometry: margin=2.5cm",
        "papersize: a4",
        "---",
        "",
    ]

    current_section = None
    for section, path in sources:
        if section != current_section:
            lines += ["", f"# {SECTION_TITLES[section][lang]}", ""]
            current_section = section
        with open(path, encoding="utf-8") as fh:
            meta, body = split_frontmatter(fh.read())
        title = (meta or {}).get("title")
        body = demote_headings(LEADING_H1.sub("", body, count=1))
        if not title:
            # Generated documents carry no frontmatter; their own H1 is the title.
            with open(path, encoding="utf-8") as fh:
                first = fh.readline().strip()
            title = first.lstrip("# ").strip() or os.path.basename(path)
        lines += ["", f"## {title}", ""]
        if meta:
            lines += doc_header_table(meta, lang, states.get(meta.get("id")))
        lines += [body.strip(), ""]

    outdir = os.path.join(build, lang)
    os.makedirs(outdir, exist_ok=True)
    pack = os.path.join(outdir, "isms-pack.md")
    with open(pack, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"assembled {os.path.relpath(pack, ROOT)} from {len(sources)} documents")
    return pack


def pandoc_command(pack: str, fmt: str) -> tuple[str, list[str]]:
    out = os.path.splitext(pack)[0] + ("." + fmt)
    cmd = ["pandoc", pack, "-o", out, "--from", "markdown", "--standalone"]
    if fmt == "pdf":
        cmd += [
            "--pdf-engine", "xelatex",
            "--include-in-header", PDF_THEME,
            "--lua-filter", LANDSCAPE_TABLES,
            "--variable", "mainfont=TeX Gyre Pagella",
            "--variable", "sansfont=TeX Gyre Heros",
            "--variable", "monofont=Latin Modern Mono",
            "--variable", "fontsize=10.5pt",
            "--variable", "linestretch=1.12",
            "--variable", "colorlinks=true",
            "--variable", "linkcolor=BrandBlue",
            "--variable", "urlcolor=BrandBlue",
        ]
    return out, cmd


def pandoc(pack: str, fmt: str) -> str:
    out, cmd = pandoc_command(pack, fmt)
    subprocess.run(cmd, check=True, cwd=ROOT)
    print(f"wrote {os.path.relpath(out, ROOT)}")
    return out


def sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def make_pack_zip(build: str, version: str) -> str:
    """One zip with both languages, the source data, and a checksum manifest."""
    stage = os.path.join(build, "pack")
    shutil.rmtree(stage, ignore_errors=True)
    os.makedirs(stage)

    included = []
    for lang in LANGS:
        for ext in ("pdf", "docx", "md"):
            src = os.path.join(build, lang, f"isms-pack.{ext}")
            if os.path.exists(src):
                dst = os.path.join(stage, f"isms-{lang}-{version}.{ext}")
                shutil.copy2(src, dst)
                included.append(dst)

    # The YAML the pack was generated from travels with it, so an auditor can
    # re-run the checks against the exact inputs.
    data_dst = os.path.join(stage, "data")
    shutil.copytree(os.path.join(ROOT, "data"), data_dst)
    for dirpath, _dirnames, filenames in os.walk(data_dst):
        included += [os.path.join(dirpath, n) for n in sorted(filenames)]

    chain = os.path.join(ROOT, build, "signature-chain.txt")
    if os.path.exists(chain):
        dst = os.path.join(stage, "signature-chain.txt")
        shutil.copy2(chain, dst)
        included.append(dst)

    state = os.path.join(ROOT, build, "document-state.json")
    if os.path.exists(state):
        dst = os.path.join(stage, "document-state.json")
        shutil.copy2(state, dst)
        included.append(dst)

    manifest = os.path.join(stage, "SHA256SUMS")
    with open(manifest, "w", encoding="utf-8") as fh:
        for path in sorted(included):
            fh.write(f"{sha256(path)}  {os.path.relpath(path, stage)}\n")

    archive = os.path.join(build, f"isms-{version}.zip")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for dirpath, _dirnames, filenames in os.walk(stage):
            for name in sorted(filenames):
                full = os.path.join(dirpath, name)
                zf.write(full, os.path.relpath(full, stage))
    print(f"wrote {os.path.relpath(archive, ROOT)} ({len(included) + 1} entries)")
    return archive


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="build")
    parser.add_argument("--format", choices=["pdf", "docx", "md"], action="append",
                        help="repeatable; default is md only")
    parser.add_argument("--pack", action="store_true", help="also build the release zip")
    parser.add_argument("--version", default=os.environ.get("ISMS_VERSION", "dev"))
    parser.add_argument("--document-state", help="JSON generated by tools/document_state.py")
    args = parser.parse_args()

    build = os.path.join(ROOT, args.out)
    formats = args.format or ["md"]
    states = {}
    if args.document_state:
        with open(args.document_state, encoding="utf-8") as fh:
            states = (json.load(fh).get("documents") or {})
    if any(f in ("pdf", "docx") for f in formats) and not shutil.which("pandoc"):
        print("ERROR: pandoc is not installed; 'make check' and 'make render' still work",
              file=sys.stderr)
        return 1

    for lang in LANGS:
        pack = build_pack(lang, build, args.version, states)
        for fmt in formats:
            if fmt != "md":
                pandoc(pack, fmt)

    if args.pack:
        make_pack_zip(args.out, args.version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
