"""
kimaki_setup_agents.py
One-time setup for Atlas, Argus, and Talos Kimaki instances.
Run AFTER each agent's Kimaki has been launched at least once (so the DB exists).
"""

import sqlite3
import json
import os
import sys

TOKEN_FILE = r"D:\Shared\discord_bot_tokens.json"

with open(TOKEN_FILE, encoding="utf-8") as f:
    tokens = json.load(f)

AGENTS = {
    "atlas": {
        "data_dir": os.path.expanduser(r"~/.kimaki-atlas"),
        "app_id":   "1500640402976407662",
        "token":    tokens["atlas"],
        "channel":  ("1500652417643970791", r"D:\Atlas", "text"),
    },
    "argus": {
        "data_dir": os.path.expanduser(r"~/.kimaki-argus"),
        "app_id":   "1500641382849712190",
        "token":    tokens["argus"],
        "channel":  ("1500652453278777424", r"D:\Argus", "text"),
    },
    "talos": {
        "data_dir": os.path.expanduser(r"~/.kimaki-talos"),
        "app_id":   "1500642350228312064",
        "token":    tokens["talos"],
        "channel":  ("1500652476649705664", r"D:\Talos", "text"),
    },
}

errors = 0
for name, cfg in AGENTS.items():
    db_path = os.path.join(cfg["data_dir"], "discord-sessions.db")
    if not os.path.exists(db_path):
        print(f"[{name}] SKIP - DB not found at {db_path}")
        print(f"         Launch Kimaki for {name} first, then re-run this script.")
        errors += 1
        continue

    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            "INSERT OR REPLACE INTO bot_tokens (app_id, token, bot_mode) VALUES (?, ?, ?)",
            (cfg["app_id"], cfg["token"], "self_hosted"),
        )
        ch_id, directory, ch_type = cfg["channel"]
        conn.execute(
            "INSERT OR REPLACE INTO channel_directories (channel_id, directory, channel_type) VALUES (?, ?, ?)",
            (ch_id, directory, ch_type),
        )
        conn.commit()
        print(f"[{name}] OK - token + channel mapping seeded")
    except Exception as e:
        print(f"[{name}] ERROR - {e}")
        errors += 1
    finally:
        conn.close()

if errors:
    print(f"\n{errors} agent(s) skipped or failed. Launch their Kimaki instances first, then re-run.")
    sys.exit(1)
else:
    print("\nAll agents set up. You're good to launch.")
