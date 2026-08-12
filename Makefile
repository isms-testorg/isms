.PHONY: help check test render pdf docx pack verify clean scaffold

BUILD := build
LANGS := en de

help:
	@echo "check    validate all ISMS data and document frontmatter"
	@echo "test     self-test the helpers and fault-inject the validator"
	@echo "render   generate SoA, risk register, coverage report into $(BUILD)/"
	@echo "pdf      render + build PDFs (needs pandoc + xelatex)"
	@echo "docx     render + build DOCX (needs pandoc)"
	@echo "pack     pdf + docx + SHA256SUMS, one zip per language"
	@echo "verify   verify signature chain from previous tag to HEAD"
	@echo "scaffold create missing document skeletons from tools/scaffold.py"

check:
	python3 tools/check_isms.py

test:
	python3 tools/isms.py
	python3 tools/test_check_isms.py
	python3 tools/test_finalize_approval.py

render: check
	python3 tools/render.py --out $(BUILD)

pdf: render
	python3 tools/build_docs.py --out $(BUILD) --format pdf

docx: render
	python3 tools/build_docs.py --out $(BUILD) --format docx

pack: pdf docx
	python3 tools/build_docs.py --out $(BUILD) --pack

verify:
	tools/verify_chain.sh

scaffold:
	python3 tools/scaffold.py

clean:
	rm -rf $(BUILD)
