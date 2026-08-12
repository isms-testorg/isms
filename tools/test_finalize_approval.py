import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path

from finalize_approval import approved_approver, finalize_documents, flatten_pages


class FinalizeApprovalTests(unittest.TestCase):
    def test_latest_eligible_approval(self):
        reviews = [{"user": {"login": "director"}, "state": "COMMENTED"},
                   {"user": {"login": "director"}, "state": "APPROVED"}]
        self.assertEqual(approved_approver(reviews, [{"login": "director"}], "author"), "director")
        self.assertIsNone(approved_approver(reviews, [{"login": "owner"}], "author"))

    def test_finalize_preserves_bilingual_metadata_and_clamps_date(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for lang in ("en", "de"):
                path = root / "docs" / lang / "demo.md"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("---\nid: demo\nstatus: in_review\nreview_cycle_months: 1\napproved_on:\nnext_review:\n---\n", encoding="utf-8")
            changed = finalize_documents(root, dt.date(2026, 1, 31))
            self.assertEqual(len(changed), 2)
            self.assertTrue(all("status: approved" in p.read_text() for p in changed))
            self.assertTrue(all("next_review: 2026-02-28" in p.read_text() for p in changed))

    def test_flatten_pages(self):
        self.assertEqual(flatten_pages([[{"login": "a"}], [{"login": "b"}]]), [{"login": "a"}, {"login": "b"}])


if __name__ == "__main__":
    unittest.main()
