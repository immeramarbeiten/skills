#!/usr/bin/env python3
"""Validate structured infographic input. Checks form and math bounds, not source truth."""
import argparse
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def check(obj):
    errors = []

    def err(msg):
        errors.append(msg)

    def string(obj_, key, maxlen=240, required=True):
        value = obj_.get(key)
        if (required and not isinstance(value, str)) or (isinstance(value, str) and (not value.strip() or len(value) > maxlen)):
            err(f"{key}: must be nonempty string up to {maxlen} chars")
        return value

    def number(value):
        return type(value) in (float, int) and abs(value) < 1e16

    if not isinstance(obj, dict):
        return ["Root must be JSON object"]
    for key, size in [("company", 65), ("ticker", 15), ("quarter", 28), ("release_date", 30), ("as_of", 60), ("thesis", 160)]:
        string(obj, key, size)
    try:
        date.fromisoformat(obj.get("release_date", ""))
    except (ValueError, TypeError):
        err("release_date: must be ISO YYYY-MM-DD")
    branding = obj.get("branding", {})
    if not isinstance(branding, dict):
        err("branding: must be object")
        branding = {}
    for k in ("primary", "accent"):
        if k in branding and not (isinstance(branding[k], str) and HEX.fullmatch(branding[k])):
            err(f"branding.{k}: use #RRGGBB")

    kpis = obj.get("kpis")
    if not isinstance(kpis, list) or not 1 <= len(kpis) <= 3:
        err("kpis: supply 1–3 metric objects")
        kpis = []
    for i, metric in enumerate(kpis):
        if not isinstance(metric, dict):
            err(f"kpis[{i}]: expected object")
            continue
        if not isinstance(metric.get("label"), str) or not 1 <= len(metric["label"]) <= 32:
            err(f"kpis[{i}].label: must be 1–32 chars")
        if not number(metric.get("actual")):
            err(f"kpis[{i}].actual: must be numeric")
        if metric.get("estimate") is not None and not number(metric.get("estimate")):
            err(f"kpis[{i}].estimate: must be numeric or null")
        if metric.get("yoy_pct") is not None and not number(metric.get("yoy_pct")):
            err(f"kpis[{i}].yoy_pct: must be numeric or null")
        if not isinstance(metric.get("unit", ""), str) or len(metric.get("unit", "")) > 5:
            err(f"kpis[{i}].unit: must be short string")
        if not isinstance(metric.get("prefix", ""), str) or len(metric.get("prefix", "")) > 3:
            err(f"kpis[{i}].prefix: must be short string")

    trend = obj.get("trend")
    if not isinstance(trend, dict):
        err("trend: must be object")
        trend = {}
    points = trend.get("points")
    if not isinstance(points, list) or not 2 <= len(points) <= 8:
        err("trend.points: 2–8 points required")
        points = []
    string(trend, "title", 50)
    string(trend, "unit", 15)
    for i, pt in enumerate(points):
        if not isinstance(pt, dict) or not isinstance(pt.get("period"), str) or not number(pt.get("value")):
            err(f"trend.points[{i}]: needs period string and numeric value")
        elif len(pt["period"]) > 12:
            err(f"trend.points[{i}].period: max 12 chars")

    # If an explicitly linked quarterly series covers the YoY pair, reconcile it.
    linked = trend.get("linked_kpi_label")
    if linked is not None:
        if not isinstance(linked, str):
            err("trend.linked_kpi_label: must be a KPI label")
        else:
            matched = next((k for k in kpis if isinstance(k, dict) and k.get("label") == linked), None)
            if matched is None:
                err("trend.linked_kpi_label: KPI not found")
            elif len(points) >= 2 and all(isinstance(p, dict) and number(p.get("value")) for p in [points[0], points[-1]]):
                last, first = points[-1]["value"], points[0]["value"]
                if number(matched.get("actual")) and abs(last - matched["actual"]) > max(.001, abs(last)*0.001):
                    err("trend last value disagrees with linked KPI actual")
                if number(matched.get("yoy_pct")) and first != 0:
                    implied = (last / first - 1) * 100
                    if abs(implied - matched["yoy_pct"]) > 0.2:
                        err(f"trend YoY {implied:.1f}% disagrees with linked KPI yoy_pct {matched['yoy_pct']}%")

    grades = obj.get("grades")
    if not isinstance(grades, list) or len(grades) != 2:
        err("grades: exactly two grade objects (income statement, balance sheet)")
        grades = []
    for i, g in enumerate(grades):
        if not isinstance(g, dict):
            err(f"grades[{i}]: must be object")
            continue
        for field, maxlen in [("label", 40), ("verdict", 100)]:
            string(g, field, maxlen)
        v = g.get("stars")
        if v is not None and (not number(v) or not (0 <= v <= 5) or v * 2 != round(v * 2)):
            err(f"grades[{i}].stars: use 0–5 in 0.5 increments, or null for N/R")
    calls = obj.get("call_takeaways", [])
    if not isinstance(calls, list) or len(calls) > 2 or any(not isinstance(c, str) or not (1 <= len(c) <= 150) for c in calls):
        err("call_takeaways: list of 0–2 strings, max 150 chars each")

    market = obj.get("market")
    if market is not None:
        if not isinstance(market, dict):
            err("market: object or null")
        else:
            for k in ("change_pct", "benchmark_pct"):
                if market.get(k) is not None and not number(market.get(k)):
                    err(f"market.{k}: number or null")
            for k, maxlen in [("session", 25), ("as_of", 50), ("note", 100)]:
                if market.get(k) is not None:
                    string(market, k, maxlen)
            if market.get("change_pct") is not None and not market.get("as_of"):
                err("market.as_of required for any quoted price move")

    sources = obj.get("sources")
    if not isinstance(sources, list) or not 1 <= len(sources) <= 5:
        err("sources: 1–5 cited links required")
    else:
        for i, s in enumerate(sources):
            if not isinstance(s, dict):
                err(f"sources[{i}]: must be object")
                continue
            name = s.get("name")
            uri = s.get("url")
            if not isinstance(name, str) or not 1 <= len(name) <= 40:
                err(f"sources[{i}].name: 1–40 chars")
            if not isinstance(uri, str) or urlparse(uri).scheme != "https" or not urlparse(uri).hostname:
                err(f"sources[{i}].url: valid https URL required")
    if obj.get("demo") is True and not obj.get("disclaimer"):
        err("demo examples require a disclaimer")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    report = json.loads(args.input.read_text(encoding="utf-8"))
    errors = check(report)
    if errors:
        for issue in errors:
            print(f"ERROR: {issue}")
        raise SystemExit(1)
    print(f"Valid infographic input for {report['ticker']} ({report['quarter']}). External facts not checked.")


if __name__ == "__main__":
    main()
