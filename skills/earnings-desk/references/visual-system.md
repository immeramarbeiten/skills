# Earnings Desk visual language

## Editorial principle

The chart carries an argument. Identify the quarter's most consequential, verifiable tension and express it in an informative headline. Choose one to three plots that explain it; the user's references illustrate clear hierarchy, direct series labels, disciplined use of color, compact annotations and source notes. They are inspiration for these principles, not templates or a license to reproduce a publisher's distinctive trade dress, logo, masthead, or exact layout.

Examples of questions: Is growth accelerating while cash conversion weakens? Which segments explain the change? Has guidance shifted? Is demand growing faster than capacity? Use the actual quarter's facts, sector and available comparisons; never invent a time series to fit a template. Grades, consensus, quotes and share-price moves belong in the figure only if they advance its argument and are verified.

## House style

- Use a consistent, original Earnings Desk identity: warm off-white `#F8F7F2`, deep ink `#182630`, dark teal `#146C71`, muted vermilion `#BF573F`, and secondary slate `#758590`. Use at most two prominent data colors per panel; avoid company-brand theming by default.
- Use a strong sentence-style headline, a brief explanatory deck, chart titles that say what changed, and a smaller unit/period subtitle. System sans-serif fonts and generous whitespace keep the visual accessible across platforms. No publisher masthead or fake company logo.
- Direct-label series and end values when possible; use unobtrusive gridlines and sparse ticks. Distinguish series with labels or shapes as well as color. Use annotations only to explain a real inflection, benchmark, or event.
- Bars start at zero, except an explicitly and prominently disclosed justified break. Line axes may start elsewhere when it improves legibility, with visible ticks and no misleading break. Label all units, currency, periods, accounting basis, transformations, and any rebasing. Never imply causality from a coincident event.
- Show actual, forecast, and guidance as distinct series; clearly label any estimate and date. Use source names and URLs in a readable footer or adjacent caption and specify the market observation time when showing a price. Separate data and subjective grades.

## Composition and use of space

- Size a plot for the information it contains. A two-period comparison usually needs only a compact slope or paired-bar plot; do not stretch it across the canvas just to fill the width or imply a long time series.
- On a wide canvas, consider a two-column editorial composition: a compact plot on the left and a purposeful, aligned context column on the right. That column can hold a short interpretation, 1–3 relevant metrics, a verified attributed quote, or a caveat. Choose what advances the chart’s argument and cite the claims. Do not invent filler; intentional whitespace is better than irrelevant content.
- Let the data determine proportions and chart type. Use sufficient width for readable labels and honest scales; a complex time series may deserve the full width. On narrow screens stack the plot and context in reading order, or make a dedicated portrait version. Avoid tiny text or shrinking an entire wide page to phone width.
- Treat chart, explanatory text and source notes as one composition, with clear hierarchy, aligned edges, restrained rules and sufficient margins. Keep the narrative visually distinct from reported values and quotes, and make source references readable at delivery size.

## Choose the chart for the question

| Question | Useful form |
|---|---|
| Trajectory, acceleration, or divergence | Line chart with direct labels; only use equal spacing for equally spaced periods. |
| Relative segment contribution or ranking | Sorted horizontal bars; meaningful zero baseline. |
| Before/after change across categories | Paired bars or slope chart; label both periods and endpoints. |
| Drivers that reconcile a total | Waterfall or bridge with a checked arithmetic reconciliation. |
| Composition and change over time | Stacked bars or small multiples where part-to-whole comparison is meaningful. |
| Price reaction versus a peer/index | Indexed lines or paired changes with aligned windows, currency, and timestamps. |

`scripts/render_story_chart.py` supports a focused subset: one or two vertically arranged line, slope, and horizontal bar panels. Its fixed, full-width layout does not support a right-hand editorial column. When a compact plot with adjacent context better fits the story, use another deterministic plotting or layout tool to build the composition; use the renderer only when its layout fits. Use another deterministic plotting tool for waterfalls, indexed price charts, or other forms. Do not force available data into an unsuitable template. The older card renderer remains available for explicit card requests.

## Output and QA

Produce editable SVG and, when conversion support exists, a PNG suitable for a phone or a saved Google Doc. Landscape 1600×1000 is a useful starting point, not a compulsory layout; use a portrait layout or multiple figures when that makes the story clearer. Source each panel, show the as-of date, and supply descriptive alt text. Keep source notes and labels legible when resized; prefer fewer panels over tiny type. Check arithmetic, axis ranges, labels, clipping, contrast, and source/caption agreement. Inspect a rendered image if a supported preview is available, and state when visual inspection or PNG conversion could not be completed.
