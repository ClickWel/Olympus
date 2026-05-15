#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Try admin endpoints that might toggle dev mode
endpoints = [
    "/admin/enable",
    "/admin/setup", 
    "/admin/init",
    "/admin/start",
    "/admin/debug",
    "/admin/config",
    "/setup",
    "/init",
    "/start",
    "/debug",
    # POST variations
    "/admin/dev",
    "/admin/mode",
    "/toggle",
    "/enable",
]

for path in endpoints:
    print(f"\n--- GET {path} ---")
    try:
        r = requests.get(f"{URL}{path}", auth=AUTH, timeout=5)
        print(f"Status: {r.status_code}")
        if "Not Found" not in r.text and len(r.text) < 500:
            print(r.text[:300])
    except Exception as e:
        print(f"Error: {e}")