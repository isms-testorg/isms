#!/usr/bin/env python3
"""Regression checks for the PDF-specific Pandoc command."""

from __future__ import annotations

from pathlib import Path

from build_docs import (LANDSCAPE_TABLES, PDF_THEME, annotate_references, pandoc_command,
                        pdf_header, reference_target)


def main() -> None:
    theme = Path(PDF_THEME).read_text(encoding="utf-8")
    assert "\\usepackage{graphicx}" in theme
    assert "SourceSans3-Regular" in theme
    assert "\\fancyhead[L]{\\includegraphics[height=10mm]" in theme
    assert "Created \\pdfpackdate" in theme
    assert "Version \\pdfpackversion" in theme
    assert "g_pdfpack_landscape_header_coffin" in theme
    assert "g_pdfpack_landscape_footer_coffin" in theme
    assert "shipout/foreground" in theme
    assert "\\addtolength{\\textheight}{-24mm}" in theme
    landscape = Path(LANDSCAPE_TABLES).read_text(encoding="utf-8")
    assert "function Pandoc(doc)" in landscape
    assert "rows >= 6" in landscape
    assert "rows >= 10" in landscape
    assert "(#table.colspecs >= 3 and rows >= LARGE_TABLE_ROWS)" in landscape
    assert "table.colspecs[column][2] = 1 / columns" in landscape
    assert "pdfpackcompacttabletrue" in landscape
    assert r"\\Needspace{16\\baselineskip}" in landscape
    assert 'heading.t == "Header"' in landscape
    assert "pdfpacklandscapefalse" in landscape
    assert "\\ifpdfpackcompacttable" in theme
    assert Path("assets/company-logo.png").is_file()
    for face in ("Regular", "Semibold", "It", "SemiboldIt"):
        assert Path(f"assets/fonts/SourceSans3-{face}.otf").is_file()
    header = pdf_header("/tmp/isms-pack.md", "2026-08-12", "v1_2&3")
    header_text = Path(header).read_text(encoding="utf-8")
    assert r"\renewcommand{\pdfpackdate}{2026-08-12}" in header_text
    assert r"\renewcommand{\pdfpackversion}{v1\_2\&3}" in header_text
    references = {}
    annotated = annotate_references(
        "See `tools/check_isms.py`, evidence/manual/example.md, and [site](https://example.test).",
        references, "https://github.com/example/repo", "deadbeef")
    assert "[REF-001]" in annotated and "[REF-002]" in annotated and "[REF-003]" in annotated
    assert references == {"https://example.test": "REF-001", "tools/check_isms.py": "REF-002",
                          "evidence/manual/example.md": "REF-003"}
    evidence_references = {}
    annotated = annotate_references("github/*/members.json", evidence_references,
                                   "https://github.com/example/repo", "deadbeef")
    assert annotated == "github/*/members.json [REF-001]"
    assert evidence_references == {"evidence/github/*/members.json": "REF-001"}
    assert reference_target("tools/check_isms.py", "https://github.com/example/repo", "deadbeef") == \
        "https://github.com/example/repo/blob/deadbeef/tools/check_isms.py"
    assert reference_target("evidence/github/*/members.json", "https://github.com/example/repo", "deadbeef") == \
        "https://github.com/example/repo/tree/deadbeef/evidence/github"
    assert reference_target("evidence/", "https://github.com/example/repo", "deadbeef") == \
        "https://github.com/example/repo/tree/deadbeef/evidence"
    _out, pdf = pandoc_command("build/en/isms-pack.md", "pdf")
    assert "--pdf-engine" in pdf and "xelatex" in pdf
    assert PDF_THEME in pdf
    assert LANDSCAPE_TABLES in pdf
    assert not any("mainfont=" in arg or "sansfont=" in arg for arg in pdf)
    assert "linkcolor=BrandBlue" in pdf

    _out, docx = pandoc_command("build/en/isms-pack.md", "docx")
    assert PDF_THEME not in docx and LANDSCAPE_TABLES not in docx
    print("PDF build tests passed")


if __name__ == "__main__":
    main()
