# Earnings Desk — reusable ChatGPT / Codex agent skill

Earnings research, subjective-but-accountable financial grades, call Q&A, contemporary investor reaction, concise highlights, and chart-led editorial visuals.

**The folder `earnings-desk/` is the installable skill.** It follows the Agent Skills `SKILL.md` convention. No accounts, API keys, paid data providers or libraries are bundled. The skill uses whichever external research/market tools your agent has; its local renderer takes **already-verified data** and does not fetch finance data. The demo is a fictional company with deliberately synthetic data.

## Use in Codex

Copy the entire `earnings-desk/` folder to either your global `~/.agents/skills/earnings-desk/` directory or your repository's `.agents/skills/earnings-desk/`. Then call `$earnings-desk` (or select it via `/skills`). Codex can discover it implicitly. Restart/reload Codex if the newly installed skill does not appear.

## Use in ChatGPT

Where **Skills** uploading is available, open **Plugins → Skills → Create → Upload from your computer** and upload the ZIP containing the one top-level `earnings-desk` folder. Availability differs by ChatGPT plan and workspace and is not guaranteed for every account. In supported ChatGPT desktop environments, standalone skills can also be discovered. For wider distribution, package the skill in a plugin; distribution is distinct from writing the skill.

## Prompts

- `$earnings-desk Analyze $NOW Q3 FY2026. Full report with Q&A and the market's reaction. Confirm the release first.`
- `$earnings-desk Flash recap of $GOOGL's latest earnings; only sourced consensus comparisons.`
- `$earnings-desk Compare $NOW and its closest public software peers on operating leverage. Show grades and caveats.`
- `$earnings-desk Full earnings report on $MSFT, including a sourced chart story and a Google Drive report.`

## Render a sample chart story

```sh
python scripts/render_story_chart.py assets/example-story.json --svg example.svg
python -m unittest discover -s tests -v
```

SVG rendering uses only the standard library. A PNG requires a separately available SVG converter. The sample chart uses fictional data. The previous card renderer remains available as `scripts/render_infographic.py` with `assets/example-report.json`; it is not the default visual.

## Production workflow

1. Identify the correct fiscal period and release date.
2. Download primary earnings PDFs / filings and transcript/replay; use licensed consensus and price data when available.
3. Write a claim-level evidence ledger including units and as-of date; use the report sections in `references/report-format.md`.
4. Judge sector/stage-adjusted results and compute the two star grades; do not equate consensus beats with business excellence.
5. Choose chart forms that explain the quarter and render a chart story from verified inputs; inspect it at a usable size.
6. Save the complete sourced report to the user's configured Google Drive or verified private Git repository, or provide a local fallback. Link the saved report and chart, and explain unverifiable parts rather than guessing.

## Known limitations

A skill is a repeatable procedure, **not** a live financial data service. Chart scripts check input structure and formatting, not data provenance, share prices, consensus licensing, arithmetic across filings, or the final visual layout. Complete market reports require current access to IR filings, transcripts, price data, estimate vendors and contemporary reaction. Drive and Git saving depend on the user's connected tools and permissions. The chart helper supports up to two panels and three plot forms; use other plotting tools for more complex stories.
