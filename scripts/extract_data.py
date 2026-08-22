# -*- coding: utf-8 -*-
"""Extract Goose session data from SQLite for the dashboard."""
import sqlite3
import json
import sys
import os
import argparse

def find_db():
    """Auto-detect Goose database path."""
    candidates = [
        os.path.expandvars(r"%APPDATA%\Block\goose\data\sessions\sessions.db"),
        os.path.expanduser("~/.local/share/goose/sessions.db"),
        os.path.expanduser("~/.config/goose/sessions.db"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def extract(db_path):
    """Extract sessions and usage ledger as JSON."""
    # Open read-only so extraction can never mutate the source database
    uri = "file:" + db_path.replace("\\", "/") + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM sessions ORDER BY created_at")
    sessions = [dict(r) for r in cur.fetchall()]
    ledger = []
    try:
        cur.execute("SELECT * FROM usage_ledger ORDER BY created_timestamp")
        ledger = [dict(r) for r in cur.fetchall()]
    except sqlite3.OperationalError as e:
        print(f"Warning: usage_ledger query failed (table missing?): {e}", file=sys.stderr)
    conn.close()
    return {"sessions": sessions, "usage_ledger": ledger}

def main():
    parser = argparse.ArgumentParser(description="Extract Goose usage data to JSON.")
    parser.add_argument("db", nargs="?", default=None, help="Path to the Goose SQLite DB")
    parser.add_argument("--output", "-o", default=None, help="Write JSON to this file instead of stdout")
    args = parser.parse_args()

    db = args.db or find_db()
    if not db:
        print("Error: Could not find Goose database. Pass path as argument.")
        sys.exit(1)
    print(f"Extracting from: {db}")
    data = extract(db)
    payload = json.dumps(data, indent=2, default=str)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(payload)
        print(f"Wrote {args.output}")
    else:
        print(payload)

if __name__ == "__main__":
    main()
