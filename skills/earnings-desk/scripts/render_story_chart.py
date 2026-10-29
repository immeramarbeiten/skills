#!/usr/bin/env python3
"""Render an evidence-led earnings chart story as editable SVG.

Input is a manually researched JSON document; this script cannot verify sources.
See references/story-chart-schema.md for the schema and chart limitations.
"""
import argparse
import json
import math
import textwrap
from decimal import Decimal, ROUND_HALF_UP
from html import escape
from pathlib import Path
from urllib.parse import urlparse

W, H = 1600, 1000
PAPER, INK, MUTED = "#F8F7F2", "#182630", "#596970"
GRID, TEAL, RED, SLATE = "#D9DFDA", "#146C71", "#BF573F", "#758590"
COLORS = (TEAL, RED, SLATE, "#8C7132")


def esc(value):
    return escape(str(value), quote=True)


def text(x, y, value, size=20, color=INK, weight=400, anchor="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, Helvetica, sans-serif" '
            f'font-size="{size}" font-weight="{weight}" fill="{esc(color)}" '
            f'text-anchor="{anchor}">{esc(value)}</text>')


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and abs(value) < 1e15


def display(value):
    if value == 0:
        return "0"
    if abs(value) < .1:
        return f"{value:.4g}"
    rounded = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{rounded:,.2f}".rstrip("0").rstrip(".")


def validate(doc):
    errors = []
    if not isinstance(doc, dict):
        return ["Input must be an object"]
    for key, maximum in (("headline", 90), ("deck", 150), ("as_of", 70), ("alt_text", 300)):
        value = doc.get(key)
        if not isinstance(value, str) or not value.strip() or len(value) > maximum:
            errors.append(f"{key} must be a nonempty string of at most {maximum} characters")
    sources = doc.get("sources")
    if not isinstance(sources, list) or not 1 <= len(sources) <= 4:
        errors.append("sources must contain 1–4 sources")
        sources = []
    for source in sources:
        if not isinstance(source, dict) or not isinstance(source.get("name"), str) or not 1 <= len(source["name"]) <= 32:
            errors.append("each source needs a short name")
            continue
        url = source.get("url", "")
        if not isinstance(url, str) or urlparse(url).scheme != "https" or not urlparse(url).hostname:
            errors.append("each source needs an https URL")
    panels = doc.get("panels")
    if not isinstance(panels, list) or not 1 <= len(panels) <= 2:
        return errors + ["panels must contain 1–2 panels"]
    for i, p in enumerate(panels):
        if not isinstance(p, dict):
            errors.append(f"panel {i+1} must be an object")
            continue
        for key, maxlen in (("title", 75), ("unit", 50)):
            if not isinstance(p.get(key), str) or not 1 <= len(p[key]) <= maxlen:
                errors.append(f"panel {i+1} {key} must be 1–{maxlen} characters")
        refs = p.get("sources")
        if not isinstance(refs, list) or not refs or any(type(n) is not int or n < 1 or n > len(sources) for n in refs):
            errors.append(f"panel {i+1} must reference valid 1-based source numbers")
        kind = p.get("type")
        if kind in ("line", "slope"):
            periods, series = p.get("periods"), p.get("series")
            if not isinstance(periods, list) or not 2 <= len(periods) <= 8 or any(not isinstance(q, str) or not 1 <= len(q) <= 18 for q in periods):
                errors.append(f"panel {i+1} needs 2–8 short periods")
                continue
            if kind == "slope" and len(periods) != 2:
                errors.append(f"panel {i+1} slope requires exactly two periods")
            if not isinstance(series, list) or not 1 <= len(series) <= 4:
                errors.append(f"panel {i+1} needs 1–4 series")
                continue
            for s in series:
                if (not isinstance(s, dict) or not isinstance(s.get("name"), str) or not 1 <= len(s["name"]) <= 32
                        or not isinstance(s.get("values"), list) or len(s["values"]) != len(periods)
                        or not all(number(v) for v in s["values"]) or s.get("kind", "actual") not in ("actual", "forecast", "guidance")):
                    errors.append(f"panel {i+1} has an invalid series; values must match periods")
        elif kind == "bar":
            bars = p.get("bars")
            if not isinstance(bars, list) or not 1 <= len(bars) <= 7:
                errors.append(f"panel {i+1} needs 1–7 bars")
                continue
            if len(panels) == 2 and len(bars) > 5:
                errors.append(f"panel {i+1}: use at most 5 bars in a two-panel figure")
            for b in bars:
                if not isinstance(b, dict) or not isinstance(b.get("label"), str) or not 1 <= len(b["label"]) <= 28 or not number(b.get("value")):
                    errors.append(f"panel {i+1} contains an invalid bar")
        else:
            errors.append(f"panel {i+1} type must be line, slope or bar")
    return errors


def limits(values, include_zero=False):
    lo, hi = min(values), max(values)
    if include_zero:
        lo, hi = min(lo, 0), max(hi, 0)
    span = hi - lo
    if span == 0 and include_zero and hi == 0:
        return 0, 1
    if span == 0:
        pad = max(abs(hi) * .2, 1)
    else:
        pad = span * .13
    return ((lo if include_zero and lo == 0 else lo - pad),
            (hi if include_zero and hi == 0 else hi + pad))


def nice_scale(lo, hi):
    """Round bounds and ticks to readable values without excluding observations."""
    raw = (hi-lo) / 4
    magnitude = 10 ** math.floor(math.log10(raw))
    step = min((magnitude*x for x in (1, 2, 2.5, 5, 10)), key=lambda x: abs(x-raw))
    lower, upper = math.floor(lo/step)*step, math.ceil(hi/step)*step
    count = round((upper-lower)/step)
    return lower, upper, [lower + i*step for i in range(count+1)]


def line_panel(p, top, height):
    out = []
    x0, x1 = 150, 1120
    y0, y1 = top + 100, top + height - 55
    values = [v for s in p["series"] for v in s["values"]]
    lo, hi, ticks = nice_scale(*limits(values))
    for val in ticks:
        y = y1 - (val-lo)/(hi-lo)*(y1-y0)
        out.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{GRID}"/>')
        out.append(text(x0 - 20, y + 7, display(val), 18, MUTED, anchor="end"))
    periods = p["periods"]
    xs = [x0 + i * (x1-x0)/(len(periods)-1) for i in range(len(periods))]
    for x, label in zip(xs, periods):
        out.append(text(x, y1 + 34, label, 18, MUTED, anchor="middle"))
    endpoints = []
    for i, s in enumerate(p["series"]):
        ys = [y1 - (v-lo)/(hi-lo)*(y1-y0) for v in s["values"]]
        color = COLORS[i]
        coords = " ".join(f"{x:.1f},{y:.1f}" for x,y in zip(xs,ys))
        dash = ' stroke-dasharray="9 6"' if s.get("kind", "actual") != "actual" else ""
        out.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="4"{dash}/>')
        for x, y in zip(xs, ys):
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{PAPER}" stroke="{color}" stroke-width="3"/>')
        if p["type"] == "slope":
            out.append(text(xs[0] + 10, ys[0] - 12, display(s["values"][0]), 17, color, 700))
        label = f'{s["name"]} {display(s["values"][-1])}'
        if s.get("kind", "actual") != "actual":
            label += f' ({s["kind"]})'
        endpoints.append([ys[-1], label, color])
    # Separate labels vertically without changing the plotted positions.
    endpoints.sort(key=lambda e: e[0])
    for j in range(1, len(endpoints)):
        endpoints[j][0] = max(endpoints[j][0], endpoints[j-1][0] + 26)
    if endpoints and endpoints[-1][0] > y1 + 5:
        shift = endpoints[-1][0] - (y1 + 5)
        for e in endpoints:
            e[0] -= shift
    for y, label, color in endpoints:
        out.append(text(x1 + 25, y + 6, label, 19, color, 700))
    return "".join(out)


def bar_panel(p, top, height):
    out = []
    x0, x1 = 380, 1280
    y0, y1 = top + 100, top + height - 35
    bars = p["bars"]
    lo, hi, ticks = nice_scale(*limits([b["value"] for b in bars], include_zero=True))
    zero = x0 + (0-lo)/(hi-lo)*(x1-x0)
    for val in ticks:
        x = x0 + (val-lo)/(hi-lo)*(x1-x0)
        out.append(f'<line x1="{x:.1f}" y1="{y0-12:.1f}" x2="{x:.1f}" y2="{y1:.1f}" stroke="{GRID}"/>')
        out.append(text(x, y0-20, display(val), 17, MUTED, anchor="middle"))
    row = (y1-y0) / len(bars)
    for i, bar in enumerate(bars):
        y = y0 + i*row + row*.18
        end = x0 + (bar["value"]-lo)/(hi-lo)*(x1-x0)
        h = min(row*.60, 34)
        color = TEAL if bar["value"] >= 0 else RED
        out.append(text(x0-20, y+h*.75, bar["label"], 20, INK, anchor="end"))
        out.append(f'<rect x="{min(zero,end):.1f}" y="{y:.1f}" width="{abs(end-zero):.1f}" height="{h:.1f}" fill="{color}"/>')
        label_x = end+10 if bar["value"] >= 0 else end-10
        out.append(text(label_x, y+h*.75, display(bar["value"]), 19, color, 700, "start" if bar["value"] >= 0 else "end"))
    out.append(f'<line x1="{zero:.1f}" y1="{y0-12:.1f}" x2="{zero:.1f}" y2="{y1:.1f}" stroke="{INK}" stroke-width="1.5"/>')
    return "".join(out)


def render(doc):
    errors = validate(doc)
    if errors:
        raise ValueError("; ".join(errors))
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(doc["alt_text"])}">',
           f'<title>{esc(doc["headline"])}</title><desc>{esc(doc["alt_text"])}</desc>',
           f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
           f'<rect x="70" y="40" width="62" height="7" fill="{TEAL}"/>',
           text(147, 48, "EARNINGS DESK  /  CHARTS", 16, MUTED, 700)]
    for i, line in enumerate(textwrap.wrap(doc["headline"], width=57)):
        out.append(text(70, 102 + i*45, line, 43, INK, 700))
    for i, line in enumerate(textwrap.wrap(doc["deck"], width=120)):
        out.append(text(70, 182 + i*24, line, 20, MUTED))
    panels = doc["panels"]
    tops = [245] if len(panels) == 1 else [245, 560]
    height = 610 if len(panels) == 1 else 295
    for p, top in zip(panels, tops):
        out.append(f'<line x1="70" y1="{top}" x2="1530" y2="{top}" stroke="{INK}" stroke-width="1.5"/>')
        out.append(text(70, top + 35, p["title"], 26, INK, 700))
        refs = ", ".join(f"[{n}]" for n in p["sources"])
        out.append(text(70, top + 65, p["unit"] + "  ·  Source " + refs, 17, MUTED))
        out.append(bar_panel(p, top, height) if p["type"] == "bar" else line_panel(p, top, height))
    out.append(f'<line x1="70" y1="880" x2="1530" y2="880" stroke="{INK}" stroke-width="1"/>')
    out.append(text(70, 911, "SOURCES", 15, MUTED, 700))
    for i, source in enumerate(doc["sources"]):
        label = f'[{i+1}] {source["name"]}'
        x = 185 + i*325
        out.append(f'<a xlink:href="{esc(source["url"])}"><title>{esc(source["url"])}</title>{text(x, 911, label, 16, INK)}</a>')
    out.append(text(70, 950, "Snapshot: " + doc["as_of"], 16, MUTED))
    if doc.get("demo"):
        out.append(text(1530, 950, "FICTIONAL DATA", 16, RED, 700, "end"))
    out.append("</svg>")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--svg", required=True, type=Path)
    args = parser.parse_args()
    try:
        doc = json.loads(args.input.read_text(encoding="utf-8"))
        result = render(doc)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    args.svg.parent.mkdir(parents=True, exist_ok=True)
    args.svg.write_text(result, encoding="utf-8")
    print(f"SVG: {args.svg} (facts and visual layout require independent review)")


if __name__ == "__main__":
    main()
