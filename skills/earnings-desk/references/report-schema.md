# Infographic input schema — `report.json`

The input is a **manually researched and validated evidence summary**, not an automatic financial data feed. Validate before rendering.

```json
{
  "company": "Fictional Corporation",
  "ticker": "FICT",
  "quarter": "Q3 FY2026",
  "release_date": "2026-10-29",
  "as_of": "2026-10-29 19:00 ET",
  "thesis": "A short, evidence-backed earnings takeaway.",
  "branding": {"primary": "#15243B", "accent": "#386FC1"},
  "demo": true,
  "kpis": [
    {"label": "Revenue", "actual": 9.7, "estimate": 9.4, "unit": "B", "prefix": "$", "yoy_pct": 18.1},
    {"label": "Adjusted EPS", "actual": 1.2, "estimate": 1.16, "unit": "", "prefix": "$"},
    {"label": "Free cash flow", "actual": 1.5, "estimate": null, "unit": "B", "prefix": "$"}
  ],
  "trend": {"title": "Revenue trend", "unit": "$B", "linked_kpi_label": "Revenue", "points": [{"period": "Q3'25", "value": 7.1}, {"period": "Q4'25", "value": 8.0}]},
  "grades": [
    {"label": "Income statement", "stars": 4.0, "verdict": "Growth with improving operating leverage"},
    {"label": "Balance sheet", "stars": 3.5, "verdict": "Ample liquidity; capex demands monitoring"}
  ],
  "call_takeaways": ["One short confirmed call theme", "One short confirmed call theme"],
  "market": {"session": "After-hours", "change_pct": 2.4, "benchmark_pct": 0.1, "as_of": "2026-10-29 18:00 ET", "note": "Move vs prior regular-session close"},
  "sources": [{"name": "Company IR", "url": "https://example.com/ir"}],
  "disclaimer": "Illustrative, entirely fictional data"
}
```

All numeric values are ordinary JSON numbers, not formatted strings. When financial evidence is missing, `grades[].stars` can be `null` (displaying N/R); never use a fabricated default grade. The renderer computes concise display strings and estimate differences. The sign of the estimate difference describes *above/below*, not inherently good/bad. Accept `null` when estimates, market move or benchmark are unavailable; show missingness. No fixed hardcoded logo. All source names and labels are included as vector text.

Run:

```sh
python scripts/validate_report.py assets/example-report.json
python scripts/render_infographic.py assets/example-report.json --svg /tmp/earnings.svg --png /tmp/earnings.png
```

Optional PNG requires `cairosvg`; SVG uses the Python standard library. This also checks that a trend explicitly linked to a KPI agrees with its last actual and first-to-last YoY growth. Other historical-series logic must be checked against filings. This validates structural and numerical plausibility only: it **cannot establish that sources or reported figures are true**.
