# Source policy and evidence ledger

## Retrieval hierarchy

1. **Company/filing source** — IR earnings release, quarterly shareholder letter, audited/unaudited financials, regulatory filing, financial tables, official presentation, exchange announcement.
2. **Call primary source** — company-hosted webcast/replay and transcript. A third-party transcript must be attributed; note any automated transcript caveats.
3. **Independent market and expectations source** — exchange-grade/historical quote provider for after-hours/premarket data, licensed consensus consensus provider (identify vendor and freeze cutoff), trusted news reporting and published analyst commentary. Re-check definitions and timestamps.
4. **Community sentiment source** — dated original Reddit/X/Stocktwits posts or polls, properly contextualized as non-representative examples. Never reword a fabricated quote as authentic.

## Evidence ledger columns

`claim_id | metric | source URL | issuer/provider | primary/secondary | fiscal period | publish datetime + timezone | as-of datetime + timezone | accounting basis | currency | unit | actual | consensus | consensus as-of + source | confidence | notes`

For year-over-year comparisons, ensure same reporting period and restatement basis. For segment mix, don't sum overlapping segment labels. For free cash flow, check company definition: often OCF - capex, but may exclude or add other items.

## Sources required by section

- Earnings wire: company release + filing, and estimate source for every comparison.
- Grades: primary financial statements, multiple historical periods, peer comparators; absence lowers confidence, not automatically the grade.
- Call: transcript or replay with speaker and Q&A location. `No replay timestamp verified` rather than inventing one.
- Market: timestamped extended-hours or regular-session data, disclosed exchange/session basis. Sell-side changes and retail posts explicitly sourced.
- Infographic: source caption showing date, reporting unit, named sources, and disclosure of calculated values; hyperlinks in the companion report.

## Important edge cases

- Consensus estimates for *reported* EPS and *adjusted* EPS frequently differ.
- A positive or negative adjusted EPS surprise is not a comprehensive quality signal if one-time gain, stock compensation or tax drove it.
- Management's estimated next-quarter outlook is not an actual result; label guidance period and whether it was raised, reaffirmed or lowered against the previous guide.
- Negative free cash flow may be a planned buildout. Report capital intensity, cash balance, trajectory and financing needs, not a simplistic good/bad badge.
- After-hours percent change can be from prior regular-session close vs a late extended-hours print; show the chosen calculation and time.
- Market may respond to pre-existing rumors and macro/sector moves; never assert causality merely from simultaneity.
- If investment gains/losses drive EPS materially, split operating performance vs non-operating impact and reconcile the reported headline when possible.
- Use newly published, dated news and post-release posts for reaction; a prior-day thread is not post-earnings commentary.
