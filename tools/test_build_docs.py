#!/usr/bin/env python3
"""Regression checks for the PDF-specific Pandoc command."""

from __future__ import annotations

from pathlib import Path

from build_docs import LANDSCAPE_TABLES, PDF_THEME, pandoc_command, pdf_header


def main() -> None:
    theme = Path(PDF_THEME).read_text(encoding="utf-8")
    assert "\\usepackage{graphicx}" in theme
    assert "SourceSans3-Regular" in theme
    assert "\\fancyhead[L]{\\includegraphics[height=10mm]" in theme
    assert "Created \\pdfpackdate" in theme
    assert "Version \\pdfpackversion" in theme
    landscape = Path(LANDSCAPE_TABLES).read_text(encoding="utf-8")
    assert "function Pandoc(doc)" in landscape
    assert 'heading.t == "Header"' in landscape
    assert Path("assets/company-logo.png").is_file()
    for face in ("Regular", "Semibold", "It", "SemiboldIt"):
        assert Path(f"assets/fonts/SourceSans3-{face}.otf").is_file()
    header = pdf_header("/tmp/isms-pack.md", "2026-08-12", "v1_2&3")
    header_text = Path(header).read_text(encoding="utf-8")
    assert r"\renewcommand{\pdfpackdate}{2026-08-12}" in header_text
    assert r"\renewcommand{\pdfpackversion}{v1\_2\&3}" in header_text
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
