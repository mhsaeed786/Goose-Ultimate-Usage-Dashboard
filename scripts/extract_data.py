#!/usr/bin/env python3
"""
Extract Goose session data from SQLite into data.json.
Usage:
    python extract_data.py --db "~/Library/Application Support/Block/goose/data/sessions/sessions.db" --out data.json
    python extract_data.py --db "%APPDATA%\Block\goose\data\sessions\sessions.db" --out data.json
"""

import argparse
import json
import sqlite3
from datetime import datetime
from pathlib import Path


def parse_time_ms(v):
    if not v:
        return 0
    try:
        t = datetime.fromisoformat(str(v).replace("Z", "+00:00")).timestamp()
        return int(t * 1000)
    except Exception:
        try:
            return int(v)
        except Exception:
            return 0


def extract(db_path, out_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sessions = []
    c.execute("""
        SELECT id, name, created_at, provider_name,
               total_tokens, input_tokens, output_tokens,
               accumulated_total_tokens, accumulated_input_tokens, accumulated_output_tokens,
               accumulated_cache_read_tokens, accumulated_cache_write_tokens,
               model_config_json
        FROM sessions
        ORDER BY created_at
    """)
    for row in c.fetchall():
        model = "unknown"
        try:
            cfg = json.loads(row[12] or "{}")
            model = cfg.get("model_name") or cfg.get("model") or "unknown"
        except Exception:
            pass

        sessions.append({
            "id": row[0],
            "name": row[1] or row[0],
            "created_at": row[2],
            "provider_name": row[3] or "unknown",
            "total_tokens": int(row[7] or row[4] or 0),
            "input_tokens": int(row[8] or row[5] or 0),
            "output_tokens": int(row[9] or row[6] or 0),
            "cache_read_tokens": int(row[10] or 0),
            "cache_write_tokens": int(row[11] or 0),
            "duration_ms": 0,
            "model": model,
        })

    ledger = []
    try:
        c.execute("""
            SELECT id, session_id, created_timestamp, model,
                   input_tokens, output_tokens, total_tokens,
                   cache_read_tokens, cache_write_tokens
            FROM usage_ledger
            ORDER BY created_timestamp
        """)
        for row in c.fetchall():
            ts = row[2]
            dt = datetime.fromtimestamp(ts / 1000).isoformat() if ts else None
            ledger.append({
                "id": row[0],
                "session_id": row[1],
                "created_at": dt,
                "created_timestamp": dt,
                "model": row[3] or "unknown",
                "input_tokens": int(row[4] or 0),
                "output_tokens": int(row[5] or 0),
                "total_tokens": int(row[6] or 0),
                "cache_read_tokens": int(row[7] or 0),
                "cache_write_tokens": int(row[8] or 0),
            })
    except Exception as e:
        print(f"Warning: could not read usage_ledger: {e}")

    total = sum(s["total_tokens"] for s in sessions)
    input_t = sum(s["input_tokens"] for s in sessions)
    output_t = sum(s["output_tokens"] for s in sessions)
    cache_r = sum(s["cache_read_tokens"] for s in sessions)
    cache_w = sum(s["cache_write_tokens"] for s in sessions)
    models = sorted({s["model"] for s in sessions if s["model"] != "unknown"})

    model_totals = {}
    for s in sessions:
        model_totals[s["model"]] = model_totals.get(s["model"], 0) + s["total_tokens"]
    model_breakdown = sorted(
        [{"model": m, "tokens": t, "percent": round(t / total * 100, 1) if total else 0}
         for m, t in model_totals.items()],
        key=lambda x: -x["tokens"],
    )

    active = [s for s in sessions if s["total_tokens"]]

    data = {
        "meta": {
            "source": str(db_path),
            "extracted_at": datetime.now().isoformat(),
            "goose_version": "1.43.0",
        },
        "summary": {
            "total_sessions": len(sessions),
            "active_sessions": len(active),
            "total_tokens": total,
            "total_input_tokens": input_t,
            "total_output_tokens": output_t,
            "total_cache_read_tokens": cache_r,
            "total_cache_write_tokens": cache_w,
            "models_used": len(models),
            "models": models,
            "model_breakdown": model_breakdown,
            "input_output_ratio": round(input_t / output_t, 1) if output_t else 0,
            "avg_per_session": round(total / len(active)) if active else 0,
        },
        "sessions": sessions,
        "usage_ledger": ledger,
    }

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Extracted {len(sessions)} sessions, {len(ledger)} ledger entries, {total:,} total tokens")
    print(f"Wrote {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Extract Goose usage data to JSON")
    parser.add_argument("--db", required=True, help="Path to Goose sessions.db")
    parser.add_argument("--out", default="data.json", help="Output JSON path")
    args = parser.parse_args()
    extract(args.db, args.out)


if __name__ == "__main__":
    main()
