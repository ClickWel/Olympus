#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Try various ways to enable dev mode
endpoints = [
    ("/enable", "POST"),
    ("/enable-dev", "POST"),
    ("/dev", "POST"),
    ("/config/dev", "POST"),
    ("/api/dev", "POST"),
    ("/admin/enable", "POST"),
]

for ep, method in endpoints:
    print(f"\n--- {method} {ep} ---")
    try:
        if method == "POST":
            r = requests.post(f"{URL}{ep}", auth=AUTH, data={"devMode": "true"}, timeout=10)
        else:
            r = requests.get(f"{URL}{ep}", auth=AUTH, timeout=10)
        print(f"Status: {r.status_code}")
        print(r.text[:200] if len(r.text) > 200 else r.text)
    except Exception as e:
        print(f"Error: {e}")

# Try GET with devMode param
print("\n--- GET /admin?devMode=true ---")
r = requests.get(f"{URL}/admin?devMode=true", auth=AUTH, timeout=10)
print(f"Status: {r.status_code}")
print(r.text[:200])

# Try with X- headers
for header, val in [("X-Dev-Mode", "true"), ("X-Debug", "1")]:
    print(f"\n--- GET /admin with {header}: {val} ---")
    r = requests.get(f"{URL}/admin", auth=AUTH, headers={header: val}, timeout=10)
    print(f"Status: {r.status_code}")
    print(r.text[:200])