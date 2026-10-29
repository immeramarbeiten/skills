# Chart-story input

`scripts/render_story_chart.py` creates an editable 1600×1000 SVG from researched data using only the Python standard library. It is a rendering helper, not a financial feed: the analyst must check the figures, accounting definitions, sourcing, time spacing, and visual output. When a different plot is better, use another deterministic plotting tool.

```sh
python scripts/render_story_chart.py assets/example-story.json --svg /tmp/story.svg
```

## Fields

- `headline`, `deck`, `as_of`, `alt_text`: sourced argument, explanatory sentence, snapshot time with timezone, and a text description that includes the essential data and comparison.
- `sources`: 1–4 `{ "name": "short label", "url": "https://..." }` entries; source labels are clickable in the SVG. Never use example URLs for real data.
- `panels`: 1–2 panel objects. Each has `type`, `title`, `unit` (include currency, percentage, accounting basis and period when relevant), and `sources`, a list of 1-based source indices.
- A `line` or `slope` panel has `periods` and `series`: `[{"name":"...", "values":[...], "kind":"actual"}]`. Values align one-for-one with periods; 1–4 series and 2–8 periods. `slope` requires exactly two periods. `kind` may also be `forecast` or `guidance`, which renders as dashed and is labeled accordingly. Only use equally spaced periods; this helper does not implement continuous time or missing data. Do not use it when precise temporal spacing is important.
- A `bar` panel has `bars`: `[{"label":"...", "value":42.1}]`; 1–7 rows for a single panel, or 1–5 with two panels. The scale always includes zero, including for negative values. Sort before passing data when rank is the story.
- `demo: true` marks the visual as fictional. Production reports must use sourced inputs and should set `demo: false`.

All values must be finite JSON numbers. Axis limits are calculated from the data; line axes may be truncated and therefore have visible ticks. For quarterly or yearly categories, do not skip periods while retaining equal spacing. Direct labels reduce legend hunting; visually inspect for overlaps and clipping and use fewer series if necessary. The renderer checks basic structure, source URLs and values; it cannot establish truth, timing, consensus comparability, causal claims or layout quality.

SVG is the canonical output. For a PNG, use an available local SVG conversion library or tool; lack of PNG support does not make an SVG a PNG. Check the resulting image at a phone-readable size. The old `report-schema.md` and `render_infographic.py` describe an optional legacy card template.
