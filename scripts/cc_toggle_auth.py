"""
cc_toggle_auth.py - Toggle Claude Code between API key and subscription auth.

Usage:
    python cc_toggle_auth.py api          - Switch to API key mode
    python cc_toggle_auth.py subscription - Switch to subscription (OAuth) mode
    python cc_toggle_auth.py status       - Show current mode

The API key is saved to cc_api_key.txt on first removal so it can be restored.
.claude.json is the shared Claude Code config for all terminals.
"""

import sys
import json
import os

CLAUDE_JSON = os.path.join(os.path.expanduser("~"), ".claude.json")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_BACKUP = os.path.join(SCRIPT_DIR, "cc_api_key.txt")


def load_config():
    with open(CLAUDE_JSON, encoding="utf-8") as f:
        return json.load(f)


def save_config(data):
    with open(CLAUDE_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def current_mode(data):
    if data.get("primaryApiKey"):
        return "api"
    return "subscription"


def cmd_status(data):
    mode = current_mode(data)
    if mode == "api":
        key = data["primaryApiKey"]
        print(f"Mode: API key ({key[:20]}...)")
    else:
        acct = data.get("oauthAccount", {})
        email = acct.get("emailAddress", "unknown") if isinstance(acct, dict) else "cached"
        print(f"Mode: Subscription / OAuth ({email})")


def cmd_subscription(data):
    if not data.get("primaryApiKey"):
        print("Already in subscription mode. Nothing changed.")
        return

    key = data["primaryApiKey"]

    # Save key to backup file so we can restore it later
    with open(KEY_BACKUP, "w", encoding="utf-8") as f:
        f.write(key)
    print(f"API key saved to: {KEY_BACKUP}")

    del data["primaryApiKey"]
    save_config(data)
    print("Switched to subscription (OAuth) mode.")
    print("Restart your Claude Code terminals to apply.")


def cmd_api(data):
    if data.get("primaryApiKey"):
        print("Already in API key mode. Nothing changed.")
        return

    if not os.path.exists(KEY_BACKUP):
        print(f"ERROR: No saved API key found at {KEY_BACKUP}")
        print("Cannot restore - key was never backed up by this script.")
        print("Set it manually: add your key to cc_api_key.txt in this folder.")
        sys.exit(1)

    with open(KEY_BACKUP, encoding="utf-8") as f:
        key = f.read().strip()

    if not key:
        print("ERROR: cc_api_key.txt is empty.")
        sys.exit(1)

    data["primaryApiKey"] = key
    save_config(data)
    print("Switched to API key mode.")
    print("Restart your Claude Code terminals to apply.")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("api", "subscription", "status"):
        print("Usage: python cc_toggle_auth.py [api|subscription|status]")
        sys.exit(1)

    cmd = sys.argv[1]
    data = load_config()

    if cmd == "status":
        cmd_status(data)
    elif cmd == "subscription":
        cmd_subscription(data)
    elif cmd == "api":
        cmd_api(data)


if __name__ == "__main__":
    main()
