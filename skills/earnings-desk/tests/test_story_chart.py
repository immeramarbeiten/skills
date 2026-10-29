"""Behavioral checks for chart input, scales, labeling, and safe SVG output."""
import copy
import json
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from render_story_chart import display, limits, nice_scale, render, validate


class StoryChartTests(unittest.TestCase):
    def setUp(self):
        self.doc = json.loads((ROOT / "assets/example-story.json").read_text())

    def test_example_is_parseable_svg_with_source_links_and_demo_warning(self):
        self.assertEqual(validate(self.doc), [])
        svg = render(self.doc)
        root = ET.fromstring(svg)
        self.assertEqual(root.attrib["viewBox"], "0 0 1600 1000")
        self.assertIn("FICTIONAL DATA", svg)
        self.assertIn('xlink:href="https://example.com/"', svg)
        self.assertIn("Cloud 60", svg)

    def test_rejects_mismatched_series_and_missing_source(self):
        self.doc["panels"][0]["series"][0]["values"] = [40]
        self.doc["panels"][1]["sources"] = [2]
        failures = " ".join(validate(self.doc))
        self.assertIn("values must match periods", failures)
        self.assertIn("valid 1-based source", failures)

    def test_bar_range_always_includes_zero(self):
        self.assertLessEqual(limits([4, 20], include_zero=True)[0], 0)
        self.assertGreaterEqual(limits([-20, -4], include_zero=True)[1], 0)
        self.assertLess(limits([-5, 8], include_zero=True)[0], 0)
        self.assertEqual(limits([0, 0], include_zero=True), (0, 1))

    def test_scales_use_readable_ticks_and_values_round_consistently(self):
        low, high, ticks = nice_scale(.17, 114.83)
        self.assertEqual((low, high), (0, 125))
        self.assertEqual(ticks, [0, 25, 50, 75, 100, 125])
        self.assertEqual(display(51.355), "51.36")
        self.assertNotEqual(display(.001), "0")

    def test_negative_bars_are_rendered_and_estimates_dashed(self):
        p = self.doc["panels"][0]
        p.update({"type": "bar", "bars": [{"label": "Loss", "value": -5}, {"label": "Gain", "value": 8}]})
        self.doc["panels"][1]["series"][0]["kind"] = "guidance"
        svg = render(self.doc)
        self.assertIn("Loss", svg)
        self.assertIn("-5", svg)
        self.assertIn('stroke-dasharray="9 6"', svg)
        self.assertIn("(guidance)", svg)

    def test_rejects_nonfinite_values_and_unsafe_urls(self):
        self.doc["panels"][0]["series"][0]["values"][0] = float("nan")
        self.doc["sources"][0]["url"] = "javascript:alert(1)"
        self.assertGreaterEqual(len(validate(self.doc)), 2)

    def test_markup_is_escaped(self):
        self.doc["headline"] = "Example <script>alert(1)</script>"
        svg = render(self.doc)
        self.assertNotIn("<script>", svg)
        self.assertIn("&lt;script&gt;", svg)


if __name__ == "__main__":
    unittest.main()
