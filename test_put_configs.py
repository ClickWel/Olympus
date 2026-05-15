#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Check what methods each route allows
routes = ["/configs", "/configs/save", "/configs/current", "/admin", "/admin/ping"]

for route in routes:
    # Try PUT
    r = requests.put(f"{URL}{route}", auth=AUTH, data={"name": "test"}, timeout=3)
    print(f"PUT {route}: {r.status_code}")

# Try to understand the config flow from the UI
print("\n=== Full /configs response ===")
r = requests.get(f"{URL}/configs", auth=AUTH, timeout=5)
print(r.text[:500])