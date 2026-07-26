# -*- coding: utf-8 -*-
"""Extract Goose session data from SQLite for the dashboard."""
import sqlite3
import json
import sys
import os

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
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM sessions ORDER BY created_at")
    sessions = [dict(r) for r in cur.fetchall()]
    cur.execute("SELECT * FROM usage_ledger ORDER BY created_timestamp")
    ledger = [dict(r) for r in cur.fetchall()]
    conn.close()
    return {"sessions": sessions, "usage_ledger": ledger}

if __name__ == "__main__":
    db = sys.argv[1] if len(sys.argv) > 1 else find_db()
    if not db:
        print("Error: Could not find Goose database. Pass path as argument.")
        sys.exit(1)
    print(f"Extracting from: {db}")
    data = extract(db)
    print(json.dumps(data, indent=2, default=str))
