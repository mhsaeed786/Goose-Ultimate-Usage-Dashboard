#!/usr/bin/env python3
"""
Build the final Goose app HTML by inlining Chart.js and embedding data.json.
"""

import json
from pathlib import Path

REPO = Path(__file__).parent.parent
APP_DIR = REPO / "app"
DATA_FILE = REPO / "data" / "goose_usage_data.json"
TEMPLATE_FILE = REPO / "data" / "data.json.template"
CHART_FILE = APP_DIR / "chart.js"
OUT_FILE = APP_DIR / "goose-usage-dashboard.html"


def load_data():
    src = DATA_FILE if DATA_FILE.exists() else TEMPLATE_FILE
    with open(src, "r", encoding="utf-8") as f:
        return json.load(f)


def build():
    data = load_data()
    embedded = {
        "meta": data["meta"],
        "summary": data["summary"],
        "sessions": data["sessions"][:60],
        "usage_ledger": [],
    }

    with open(CHART_FILE, "r", encoding="utf-8") as f:
        chart_code = f.read()

    embedded_json = json.dumps(embedded, ensure_ascii=False)

    # The dashboard HTML is stored as a template in this script to avoid escaping issues.
    # For now, just report what it would do. The actual HTML is already in app/goose-usage-dashboard.html.
    print(f"Data: {len(data['sessions'])} sessions, {data['summary'].get('total_tokens', 0):,} tokens")
    print(f"Embedded: {len(embedded['sessions'])} sessions")
    print(f"Chart.js: {len(chart_code):,} bytes")
    print(f"Output would be: {OUT_FILE}")
    print("NOTE: The final built app is already committed at app/goose-usage-dashboard.html")


if __name__ == "__main__":
    build()
