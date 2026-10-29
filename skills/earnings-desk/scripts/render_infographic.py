#!/usr/bin/env python3
"""Render 1600x1000 editorial earnings infographic to SVG and optionally PNG.

All input facts must be pre-verified; no network calls or data scraping happen here.
Usage: python scripts/render_infographic.py report.json --svg chart.svg --png chart.png
"""
import argparse
import json
import math
import re
from html import escape
from pathlib import Path
from urllib.parse import urlparse
from validate_report import check

W, H = 1600, 1000
BG = "#F7F8FA"
TEXT = "#172238"
SUB = "#566174"
BORDER = "#DDE3EB"
WHITE = "#FFFFFF"


def E(value):
    return escape(str(value), quote=True)


def box(x, y, w, h, fill=WHITE, r=12, stroke=None, sw=1):
    attrs = f' stroke="{E(stroke)}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{E(fill)}"{attrs}/>'


def txt(x, y, value, size=20, fill=TEXT, weight=400, anchor=None, letter=None):
    extra = f' text-anchor="{anchor}"' if anchor else ""
    extra += f' letter-spacing="{letter}"' if letter else ""
    return (f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" '
            f'font-size="{size}" font-weight="{weight}" fill="{E(fill)}"{extra}>{E(value)}</text>')


def wrap(value, max_chars, lines=2):
    words = str(value).split()
    result = []
    cur = ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if len(trial) <= max_chars or not cur:
            cur = trial
        else:
            result.append(cur)
            cur = word
    if cur:
        result.append(cur)
    if len(result) > lines:
        result = result[:lines]
        result[-1] = result[-1].rstrip(" .") + "…"
    return result


def wrapped_text(x, y, value, maxchars, n=2, size=18, lineheight=25, fill=SUB, weight=400):
    return "".join(txt(x, y + i * lineheight, text, size, fill, weight) for i, text in enumerate(wrap(value, maxchars, n)))


def fmt_number(v, prefix="", unit=""):
    abs_v = abs(v)
    if abs_v >= 100 or (abs_v >= 10 and v == int(v)):
        body = f"{v:,.0f}"
    elif abs_v >= 10:
        body = f"{v:,.1f}"
    else:
        body = f"{v:,.2f}".rstrip("0").rstrip(".")
    return prefix + body + unit


def grade_stars(x, y, score, accent, key):
    """Draw true vector star shapes, avoiding font-glyph portability issues."""
    out = []
    for i in range(5):
        cx = x + 14 + i * 28
        cy = y
        pts = []
        for j in range(10):
            ang = -math.pi/2 + j * math.pi/5
            rad = 12 if j % 2 == 0 else 5
            pts.append(f"{cx + math.cos(ang)*rad:.2f},{cy + math.sin(ang)*rad:.2f}")
        shape = " ".join(pts)
        out.append(f'<polygon points="{shape}" fill="#D5DDE6"/>')
        ratio = max(0, min(1, score - i))
        if ratio >= 1:
            out.append(f'<polygon points="{shape}" fill="{E(accent)}"/>')
        elif ratio > 0:
            cid = f"star-{key}-{i}"
            out.append(f'<clipPath id="{cid}"><rect x="{cx-12}" y="{cy-12}" width="{24*ratio:.1f}" height="24"/></clipPath>')
            out.append(f'<polygon points="{shape}" fill="{E(accent)}" clip-path="url(#{cid})"/>')
    return "".join(out)


def trend_panel(trend, accent):
    out = [box(66, 424, 881, 448, WHITE, 14, BORDER)]
    out.append(txt(100, 478, trend["title"], 28, TEXT, 700))
    out.append(txt(908, 477, trend.get("unit", ""), 17, SUB, 400, anchor="end"))
    points = trend["points"]
    values = [p["value"] for p in points]
    lo, hi = min(values), max(values)
    pad = max((hi-lo) * 0.25, abs(hi) * 0.1, 0.5)
    low, high = max(0, lo-pad) if lo >= 0 else lo-pad, hi+pad
    if high == low:
        high += 1
    x0, x1 = 125, 880
    y0, y1 = 785, 534
    for i in range(4):
        yy = y0 - i * (y0-y1)/3
        val = low + i*(high-low)/3
        out.append(f'<line x1="{x0}" y1="{yy:.1f}" x2="{x1}" y2="{yy:.1f}" stroke="#E8EDF2" stroke-width="1"/>')
        out.append(txt(106, yy+6, fmt_number(val), 15, SUB, anchor="end"))
    coords = []
    for i, p in enumerate(points):
        xx = x0 + i*(x1-x0)/(len(points)-1)
        yy = y0 - (p["value"] - low)/(high-low)*(y0-y1)
        coords.append((xx, yy))
    for (ax,ay), (bx,by) in zip(coords, coords[1:]):
        out.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{E(accent)}" stroke-width="5" stroke-linecap="round"/>')
    for (xx,yy),p in zip(coords, points):
        out.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="8" fill="{E(accent)}" stroke="white" stroke-width="3"/>')
        out.append(txt(xx, yy-19, fmt_number(p["value"]), 16, TEXT, 700, anchor="middle"))
        out.append(txt(xx, 825, p["period"], 16, SUB, anchor="middle"))
    return "".join(out)


def render(report):
    primary = report.get("branding", {}).get("primary", "#192742")
    accent = report.get("branding", {}).get("accent", "#4877DA")
    pieces = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Earnings infographic for {E(report["company"])}">']
    pieces.append(box(0, 0, W, H, BG, 0))
    pieces.append(box(0, 0, W, 179, primary, 0))
    pieces.append(box(0, 173, W, 6, accent, 0))
    pieces.append(txt(68, 59, "EARNINGS / DESK", 17, "#DBE4F1", 700, letter="3"))
    pieces.append(txt(68, 117, report["company"], 55, WHITE, 700))
    pieces.append(txt(68, 155, report["thesis"][:105], 17, "#D3E0ED", 400))
    pieces.append(txt(1498, 73, report["ticker"].upper(), 28, WHITE, 700, anchor="end"))
    pieces.append(txt(1498, 109, report["quarter"], 20, "#E3EAF3", 500, anchor="end"))
    pieces.append(txt(1498, 142, "Released " + report["release_date"], 16, "#C9D4E4", anchor="end"))

    labels = report["kpis"]
    tile_width = 279
    for i, k in enumerate(labels):
        x = 66 + i * 300
        pieces.append(box(x, 201, tile_width, 194, WHITE, 13, BORDER))
        pieces.append(box(x+19, 223, 6, 26, accent, 2))
        pieces.append(txt(x+36, 243, k["label"], 21, SUB, 700))
        pieces.append(txt(x+21, 310, fmt_number(k["actual"], k.get("prefix", ""), k.get("unit", "")), 45, TEXT, 700))
        if k.get("estimate") is not None:
            diff = k["actual"]-k["estimate"]
            direction = "above" if diff > 0 else "below" if diff < 0 else "in line with"
            comparison = f'{direction} est. {fmt_number(k["estimate"], k.get("prefix", ""), k.get("unit", ""))}'
        else:
            comparison = "Consensus estimate unavailable"
        pieces.append(txt(x+21, 348, comparison, 17, SUB))
        if k.get("yoy_pct") is not None:
            pieces.append(txt(x+21, 376, f'{k["yoy_pct"]:+.1f}% YoY', 15, accent, 700))

    pieces.append(trend_panel(report["trend"], accent))
    pieces.append(box(975, 201, 559, 240, WHITE, 14, BORDER))
    pieces.append(txt(1008, 245, "PROFESSOR'S REPORT CARD", 20, SUB, 700, letter="1"))
    for i, g in enumerate(report["grades"]):
        yy = 287 + i*89
        pieces.append(txt(1008, yy, g["label"].upper(), 17, TEXT, 700))
        score = g["stars"]
        pieces.append(txt(1497, yy, f"{score:.1f}/5" if score is not None else "N/R", 18, accent, 700, anchor="end"))
        pieces.append(grade_stars(1006, yy+26, score if score is not None else 0, accent, i))
        pieces.append(wrapped_text(1158, yy+28, g["verdict"], 35, 2, 15, 18, SUB))

    pieces.append(box(975, 461, 559, 233, WHITE, 14, BORDER))
    pieces.append(txt(1008, 507, "INSIDE THE CALL", 20, SUB, 700, letter="1"))
    if report.get("call_takeaways"):
        for i, item in enumerate(report["call_takeaways"]):
            yy = 552 + i*74
            pieces.append(box(1008, yy-17, 8, 8, accent, 4))
            pieces.append(wrapped_text(1030, yy, item, 53, 2, 18, 25, TEXT))
    else:
        pieces.append(wrapped_text(1008, 567, "Call evidence has not been verified. No Q&A claims shown.", 53, 2, 18, 25, SUB))

    pieces.append(box(975, 715, 559, 157, WHITE, 14, BORDER))
    pieces.append(txt(1008, 759, "THE MARKET'S VERDICT", 20, SUB, 700, letter="1"))
    market = report.get("market")
    if market and market.get("change_pct") is not None:
        change = market["change_pct"]
        pieces.append(txt(1008, 818, f'{change:+.1f}%', 43, TEXT, 700))
        pieces.append(txt(1188, 800, market.get("session", "Price response"), 18, TEXT, 700))
        pieces.append(txt(1188, 823, market.get("as_of", ""), 16, SUB))
        comparison = market.get("note", "")
        if market.get("benchmark_pct") is not None:
            comparison += f' · Bench {market["benchmark_pct"]:+.1f}%'
        pieces.append(txt(1008, 854, comparison[:63], 14, SUB))
    else:
        pieces.append(txt(1008, 817, "Verified reaction not yet available", 23, SUB, 500))

    pieces.append(box(0, 898, 1600, 102, "#E9EDF3", 0))
    pieces.append(txt(68, 931, "SOURCES", 14, SUB, 700, letter="2"))
    src_text = "   ·   ".join(s["name"] for s in report["sources"])
    pieces.append(txt(168, 931, src_text[:145], 16, TEXT, 600))
    for i, s in enumerate(report["sources"]):
        url = s["url"]
        # Machine-readable, actionable source links in SVG; names displayed in footer.
        pieces.append(f'<a xlink:href="{E(url)}"><title>{E(s["name"])}: {E(url)}</title><rect x="{166+i*215}" y="914" width="200" height="30" fill="transparent"/></a>')
    pieces.append(txt(68, 967, 'Snapshot: ' + report["as_of"], 16, SUB))
    if report.get("demo"):
        pieces.append(txt(1520, 968, "FICTIONAL DEMO · NOT REAL DATA", 17, "#963F43", 700, anchor="end"))
    elif report.get("disclaimer"):
        pieces.append(txt(1520, 968, report["disclaimer"][:85], 14, SUB, 600, anchor="end"))
    pieces.append("</svg>")
    return "\n".join(pieces)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path)
    p.add_argument("--svg", type=Path, required=True)
    p.add_argument("--png", type=Path)
    args = p.parse_args()
    report = json.loads(args.input.read_text(encoding="utf-8"))
    errors = check(report)
    if errors:
        p.error("Invalid input:\n" + "\n".join(errors))
    args.svg.parent.mkdir(parents=True, exist_ok=True)
    svg = render(report)
    args.svg.write_text(svg, encoding="utf-8")
    print(f"SVG: {args.svg}")
    if args.png:
        try:
            import cairosvg
        except ImportError:
            p.error("PNG needs cairosvg (pip install cairosvg); SVG already saved")
        args.png.parent.mkdir(parents=True, exist_ok=True)
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(args.png), output_width=W, output_height=H)
        print(f"PNG: {args.png}")


if __name__ == "__main__":
    main()
