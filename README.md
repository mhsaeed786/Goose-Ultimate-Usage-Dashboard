# Goose Ultimate Usage Dashboard

A standalone HTML dashboard for visualizing Goose AI assistant token usage from the SQLite session database.

## ⚠️ Status

This is a **prototype**. It has been tested on:
- ✅ Windows 10 + Edge (primary dev environment)
- ❓ macOS — not yet tested
- ❓ Linux — not yet tested
- ❓ Safari — not yet tested

Chart.js is loaded from CDN, so it *should* work cross-platform, but this is not verified.

## Features

- **Live KPI Strip**: Sessions, total tokens, input/output breakdown, models used, date range
- **Time-Window Charts**: Last 5 Hours, Weekly, Monthly usage
- **Model Breakdown**: Token distribution (doughnut) + per-session horizontal bars
- **Token Flow**: Provider to Model to Total visual flow
- **Agent-Aware Analytics**: Context window evolution, input vs output ratio
- **Anomaly Detection**: Context bloat, empty sessions, cache utilization flags
- **Cost Optimization**: Actionable recommendations based on usage patterns
- **Session Table**: Full details with color-coded model badges

## Quick Start

1. Open `index.html` in a modern Chromium-based browser (Edge, Chrome, Brave)
2. The file contains **demo placeholder data** — replace it with your own extracted data
3. To use your own data, run the extraction script and paste the JSON into the `SESSIONS` and `LEDGER` arrays

## Data Source

Goose stores session data in a SQLite database:

| Platform | Path |
|----------|------|
| Windows  | `%APPDATA%\Block\goose\data\sessions\sessions.db` |
| macOS    | `~/.local/share/goose/sessions.db` (unverified) |
| Linux    | `~/.local/share/goose/sessions.db` (unverified) |

Tables:
- `sessions` — per-session token totals, provider, model
- `usage_ledger` — per-turn token counts with timestamps
- `messages` — individual messages

## Extract Your Own Data

```bash
python scripts/extract_data.py
```

Or manually with sqlite3:

```bash
sqlite3 "$APPDATA/Block/goose/data/sessions/sessions.db" "SELECT * FROM sessions;"
```

Paste the JSON output into the `SESSIONS` and `LEDGER` arrays in `index.html`.

## Contributing

Pull requests welcome. The dashboard is a single HTML file — edit and test in-browser.

## License

No license has been applied yet. If you want to use this code, open an issue and ask.
