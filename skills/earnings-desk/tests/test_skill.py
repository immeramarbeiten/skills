"""Local sanity checks. Run: python -m unittest discover -s tests -v"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_report import check
from render_infographic import render


class TestEarningsSkill(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "assets/example-report.json").read_text())

    def test_valid_example(self):
        self.assertEqual(check(self.data), [])

    def test_svg_is_real_vector_and_contains_demo_flag(self):
        svg = render(self.data)
        self.assertIn("<svg", svg)
        self.assertIn("FICTIONAL DEMO", svg)
        self.assertIn("Quarterly revenue", svg)
        self.assertIn("Northstar Cloud", svg)

    def test_invalid_grade_fails(self):
        self.data["grades"][0]["stars"] = 5.3
        self.assertTrue(any("stars" in s for s in check(self.data)))

    def test_linked_revenue_yoy_mismatch_fails(self):
        self.data["kpis"][0]["yoy_pct"] = 40.0
        self.assertTrue(any("YoY" in s for s in check(self.data)))

    def test_no_fake_market_move_without_timestamp(self):
        self.data["market"].pop("as_of")
        self.assertTrue(any("market.as_of" in s for s in check(self.data)))

    def test_xss_input_escaped(self):
        self.data["company"] = "North & <script>alert(1)</script>"
        svg = render(self.data)
        self.assertNotIn("<script>", svg)
        self.assertIn("&lt;script&gt;", svg)


if __name__ == "__main__":
    unittest.main()
