# Goose Ultimate Usage Dashboard

A real-time usage dashboard for [Goose](https://github.com/block/goose) sessions.

## Status

**Working prototype.** Tested on Windows 10 with Goose Desktop v1.43.0.

> This is an early version. Some features (like true 5-second live sync inside the Goose app sandbox) are still being worked out. The dashboard renders correctly with embedded data and will fall back to embedded data if live sync is unavailable.

## What it does

- Reads your Goose SQLite sessions.db
- Displays total/input/output tokens, models used, cache rate, peak context, and more
- Shows Last 5 Hours, Weekly, Monthly, Model breakdown, per-session, input/output, and context growth charts
- Detects anomalies (context bloat, empty sessions, high input ratio, no cache)
- Gives recommendations (split sessions, enable caching, clean empty sessions)
- Visualizes token flow by provider
- Lists all sessions in a sortable table
- **Cost of inference tracking** — calculates estimated inference cost per session and per model
- **Cost breakdown by model** — see which models are driving your spend
- **Cost efficiency** — tokens per dollar metric for each session
- **Cost trend analysis** — track how your inference costs change over time

## Folder Structure

- app/ - Final Goose app and Chart.js bundle
- data/ - Sample data and empty template
- scripts/ - Python extraction script
- src/ - Build helpers
- docs/ - Architecture docs (TBD)
- manifest.json - Project metadata
- README.md - This file

## Quick Start

### 1. Extract your data

Windows:
    python scripts/extract_data.py --db "%APPDATA%\Block\goose\data\sessions\sessions.db" --out data/goose_usage_data.json

macOS:
    python scripts/extract_data.py --db "~/Library/Application Support/Block/goose/data/sessions/sessions.db" --out data/goose_usage_data.json

Linux:
    python scripts/extract_data.py --db "~/.local/share/Block/goose/data/sessions/sessions.db" --out data/goose_usage_data.json

### 2. Install in Goose

Copy app/goose-usage-dashboard.html and app/chart.js to your Goose apps directory:

- Windows: %APPDATA%\Block\goose\data\apps\
- macOS: ~/Library/Application Support/Block/goose/data/apps/
- Linux: ~/.local/share/Block/goose/data/apps/

Then open Goose -> Apps -> "Goose Usage Dashboard".

## Known Issues

- Live 5s sync via data.json does not work inside the Goose app sandbox. The dashboard uses embedded data as fallback and renders immediately.
- macOS / Linux / Safari are not tested.
- No license has been applied yet.

## License

No license has been applied. Open an issue if you want to use it.
