# Earnings Desk output contract

Lead with useful findings rather than methodology. The opening wire is a scannable financial brief; reserve analysis, grading rationale and call interpretation for their dedicated sections. Cite facts in short linked group source lines rather than crowding every metric with a long citation.

## Header
`COMPANY $TICKER | Q# FY20## | Released YYYY-MM-DD | Snapshot YYYY-MM-DD HH:MM TZ`
`Status: company release [confirmed/not yet]; call [reviewed/unavailable]; after-hours [confirmed/unavailable]`
`Fast read: [one sentence on the quarter's main tension]`

## 1 — The wire
Put 4–6 short headline lines first, each with one metric and its actual, comparable estimate where verified, accounting basis, and YoY change. Follow with only the short groups that matter for this company: segments, guidance, sector KPIs, capital return, and material one-offs. Use 1–4 short lines per group; omit empty groups. Aim for a quick phone scan, not a transcript of the income statement. One brief attributed quote is optional. Add a compact group source line and a short estimate-basis caveat when needed.

Example format (illustrative layout only; not real company data):

```text
COMPANY $TICKER Q# FY## EARNINGS HIGHLIGHTS | release date
Fast read: [one evidence-backed sentence].

🔹 Revenue: $X (Est. $Y) 🟢; +Z% YoY
🔹 GAAP EPS: $X; Est.: unavailable; +Z% YoY
🔹 Operating margin: X%; +Y percentage points YoY
Sources: [release] · [dated estimate source]

Segments
🔹 Segment A: $X; +Y% YoY

Guidance
🔹 FY revenue: $X–$Y; prior guide $A–$B
```

Only apply 🟢/🔴 to an independently sourced, accounting-comparable estimate with a credible pre-release cutoff. If the basis or cutoff cannot be verified, say `Est.: unavailable` and do not make a beat/miss judgment. Label guidance as management outlook, never as actuals. Use figures from the current company, not the illustrative layout.

## 2 — Professor's report card
`Income statement ★... n/5 — [one sentence]`
`Balance sheet ★... n/5 — [one sentence]`
Then a short table with `Why | What loses points | Stage/peer context | To gain a star` for each. Separate `Earnings quality / cash conversion:` diagnostic. 1–2 paragraph verdict; no mechanical grade for unverified finances.

## 3 — Inside the call
Three management themes; the 2–3 toughest analyst questions; 1 unexpected disclosure or unresolved tension; up to 3 very short quotations with speaker attribution; `Rewind [mm:ss]` only when verified and linkable; next call's decisive question. Distinguish prepared remarks vs Q&A.

## 4 — The market's verdict
`Tape: [price and percentage] ([market session], [timestamp/timezone], vs [baseline]).` `Comparator: ...`. Two-sided perspectives `Bull case`, `Bear case`; at least one sourced journalist view if published; 2–3 sourced retail arguments if available, tagged non-representative; `My take:` one sharp paragraph. If prices unavailable, omit numbers and label unverified. No fake consensus or market narrative.

## 5 — Editorial chart story
One standalone, chart-led figure, or a small coherent set if the story requires it. Lead with a specific evidence-backed takeaway, show one to three charts chosen for the question, and include units, source/date notes and concise alt text. Direct-label comparisons where practical. Source SVG and a phone-friendly PNG are useful when available. Do not force grades, market reaction or fixed KPI tiles into a chart. Use white space rather than invented entries.

## Saved report
Return a working link to the native Google Doc or requested private Git report, plus a link to its chart when saved separately. Follow `saving-reports.md`; distinguish a chat-only answer or local file from a verified remote save. Include the source and observation dates inside the saved report so it remains useful independently of the conversation.

## Reliability note
`Primary documents: ... | Consensus: [vendor, as of] | Pricing: [vendor, timestamp] | Limitations: ...`

## Possible follow-up questions
Only as relevant: `What is priced in?`, `Compare this quarter with [peer]`, `Show guidance revision history`, `Break down AI monetization`, `Create a 5-quarter earnings grade timeline`. Avoid forcing user to specify a stock if they already gave one.
