# Goose Ultimate Usage Dashboard

A standalone HTML dashboard for visualizing Goose AI assistant token usage from the SQLite session database. Every KPI, chart, and panel is computed live from your own data — there are no hardcoded placeholder numbers.

## Pipeline: extract → save data.json → open dashboard

```
┌──────────────────────────┐   ┌─────────────┐   ┌──────────────────┐
│ 1. Extract from SQLite   │ → │ 2. data.json│ → │ 3. Open dashboard │
│ scripts/extract_data.py  │   │ (repo root) │   │ index.html        │
└──────────────────────────┘   └─────────────┘   └──────────────────┘
```

### Step 1 — Extract

```bash
# Auto-detects the Goose database (Windows / macOS / Linux paths below)
python scripts/extract_data.py --output data.json

# Or pass the DB path explicitly
python scripts/extract_data.py "%APPDATA%\Block\goose\data\sessions\sessions.db" -o data.json

# Optional: only include rows created on or after a date
python scripts/extract_data.py --output data.json --since 2026-08-01
```

The script opens the database **read-only** and writes `data.json` next to `index.html`.

### Step 2 — Serve or open

The dashboard fetches `data.json` on load, so it needs to be served over HTTP (a plain double-click of `index.html` works in some browsers, but Chrome/Edge block `file://` fetches):

```bash
python -m http.server 8000
# then open http://localhost:8000
```

Alternatively, paste the extractor's JSON output directly into the `SESSIONS` / `LEDGER` handling by saving it as `data.json` — that is the only data file the page reads.

### Step 3 — Read the dashboard

- **Top row**: exactly 3 KPI cards (Sessions, Total Tokens, Avg Tokens/Session), each showing metric → trend delta vs the previous equal-length period → supporting detail.
- **Charts**: daily (14d), weekly, monthly tokens; tokens by model; top sessions; input vs output; session size over time.
- **Anomaly Detection & Recommendations** panels appear only when computed from real data:
  - zero-token sessions flagged,
  - sessions >50K tokens flagged with compaction advice,
  - high input/output ratio flagged.
- If `data.json` is missing or unreadable, an explicit empty state tells you to run `scripts/extract_data.py`.

## Expected JSON schema (`data.json`)

```jsonc
{
  "sessions": [                       // required (one of sessions/usage_ledger must be non-empty)
    {
      "session_id": "abc123",         // string — unique session id (falls back to "id")
      "name": "Refactor auth module", // optional display name (falls back to "title")
      "model": "claude-sonnet-4",     // optional model identifier
      "provider": "anthropic",        // optional provider name
      "created_at": "2026-08-20T14:32:00", // ISO timestamp (or created_timestamp/timestamp/created)
      "total_tokens": 12345,          // number — token totals per session;
      "input_tokens": 11000,          //   if absent/zero they are rolled up
      "output_tokens": 1345           //   from usage_ledger by session_id
    }
  ],
  "usage_ledger": [                   // optional per-turn rows
    {
      "session_id": "abc123",
      "created_timestamp": "2026-08-20T14:35:00",
      "total_tokens": 500,
      "input_tokens": 450,
      "output_tokens": 50
    }
  ]
}
```

All numeric fields are optional-safe (missing → 0); timestamps are parsed with `new Date()`.

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
- `messages` — individual messages (not used by the dashboard)

## Accessibility & UX notes

- Dark-mode text colors meet WCAG AA contrast (≥4.5:1).
- Trend deltas pair color with ▲/▼/→ icons and signed percentage labels.
- Every chart canvas carries a descriptive `aria-label`; loading shows a skeleton state.
- Untrusted strings (session names, model ids) are HTML-escaped before rendering.

## Status

Prototype — tested on Windows 10/11 + Edge/Chrome. Chart.js is loaded from CDN.

## Contributing

Pull requests welcome. The dashboard is a single HTML file — edit and test in-browser.

## License

No license has been applied yet. If you want to use this code, open an issue and ask.
