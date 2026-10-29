# Earnings Desk — reusable ChatGPT / Codex agent skill

Earnings research, subjective-but-accountable financial grades, call Q&A, contemporary investor reaction, and a crisp vector infographic.

**The folder `earnings-desk/` is the installable skill.** It follows the Agent Skills `SKILL.md` convention. No accounts, API keys, paid data providers or libraries are bundled. The skill uses whichever external research/market tools your agent has; its local renderer takes **already-verified data** and does not fetch finance data. The demo is a fictional company with deliberately synthetic data.

## Use in Codex

Copy the entire `earnings-desk/` folder to either your global `~/.agents/skills/earnings-desk/` directory or your repository's `.agents/skills/earnings-desk/`. Then call `$earnings-desk` (or select it via `/skills`). Codex can discover it implicitly. Restart/reload Codex if the newly installed skill does not appear.

## Use in ChatGPT

Where **Skills** uploading is available, open **Plugins → Skills → Create → Upload from your computer** and upload the ZIP containing the one top-level `earnings-desk` folder. Availability differs by ChatGPT plan and workspace and is not guaranteed for every account. In supported ChatGPT desktop environments, standalone skills can also be discovered. For wider distribution, package the skill in a plugin; distribution is distinct from writing the skill.

## Prompts

- `$earnings-desk Analyze $NOW Q3 FY2026. Full report with Q&A and the market's reaction. Confirm the release first.`
- `$earnings-desk Flash recap of $GOOGL's latest earnings; only sourced consensus comparisons.`
- `$earnings-desk Compare $NOW and its closest public software peers on operating leverage. Show grades and caveats.`
- `$earnings-desk Full earnings report on $MSFT, including a sourced corporate-theme infographic.`

## Render a sample vector infographic

```sh
python scripts/validate_report.py assets/example-report.json
python scripts/render_infographic.py assets/example-report.json --svg example.svg --png example.png
python -m unittest discover -s tests -v
```

SVG is standard-library only; PNG uses optional `cairosvg` (install with `python -m pip install cairosvg`). The sample image is **not** an actual earnings report and is explicitly labeled as fiction.

## Production workflow

1. Identify the correct fiscal period and release date.
2. Download primary earnings PDFs / filings and transcript/replay; use licensed consensus and price data when available.
3. Write a claim-level evidence ledger including units and as-of date; use the report sections in `references/report-format.md`.
4. Judge sector/stage-adjusted results and compute the two star grades; do not equate consensus beats with business excellence.
5. Prepare a report JSON from validated evidence; run the validator; render and visually inspect SVG/PNG.
6. Write final report with citations and explain unverifiable parts rather than guessing.

## Known limitations

A skill is a repeatable procedure, **not** a live financial data service. The sample script checks schema and formatting, not data provenance, share prices, consensus licensing or arithmetic across filings. Complete market reports require current access to IR filings, transcripts, price data, estimate vendors and contemporary reaction. The graphic's compact layout is suited to 3 KPIs and one trend chart; richer company breakdowns should remain in the main report.
