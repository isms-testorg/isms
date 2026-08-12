#!/usr/bin/env python3
"""Regression checks for the PDF-specific Pandoc command."""

from __future__ import annotations

from pathlib import Path

from build_docs import LANDSCAPE_TABLES, PDF_THEME, pandoc_command


def main() -> None:
    assert Path(PDF_THEME).is_file()
    assert Path(LANDSCAPE_TABLES).is_file()
    assert Path("assets/company-logo.png").is_file()
    _out, pdf = pandoc_command("build/en/isms-pack.md", "pdf")
    assert "--pdf-engine" in pdf and "xelatex" in pdf
    assert PDF_THEME in pdf
    assert LANDSCAPE_TABLES in pdf
    assert "mainfont=TeX Gyre Pagella" in pdf
    assert "linkcolor=BrandBlue" in pdf

    _out, docx = pandoc_command("build/en/isms-pack.md", "docx")
    assert PDF_THEME not in docx and LANDSCAPE_TABLES not in docx
    print("PDF build tests passed")


if __name__ == "__main__":
    main()
