#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Try enabling dev mode via cookie/headers
endpoints = [
    ("/admin", {}),
    ("/admin?devMode=true", {}),
    ("/admin", {"Cookie": "devMode=true"}),
    ("/admin", {"Cookie": "dev_mode=1"}),
    ("/admin", {"X-Dev-Mode": "true"}),
    ("/enable", {}),
    ("/settings", {}),
    ("/debug", {}),
]

for ep, extra in endpoints:
    print(f"\n--- GET {ep} ---")
    try:
        r = requests.get(f"{URL}{ep}", auth=AUTH, headers=extra, timeout=10)
        print(f"Status: {r.status_code}")
        print(r.text[:300])
    except Exception as e:
        print(f"Error: {e}")