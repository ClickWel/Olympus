#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Test /static route
print("=== Testing /static ===")
r = requests.get(f"{URL}/static", auth=AUTH, timeout=5)
print(f"GET /static: {r.status_code}")

r = requests.get(f"{URL}/static/", auth=AUTH, timeout=5)
print(f"GET /static/: {r.status_code}")

# Check if there's /internal or /debug
print("\n=== Testing internal/debug ===")
for path in ["/internal", "/debug", "/debug/enable", "/dev-enable", "/setup-dev", "/init-dev"]:
    r = requests.get(f"{URL}{path}", auth=AUTH, timeout=3)
    print(f"GET {path}: {r.status_code}")

# Try DELETE on admin (some frameworks use DELETE for enable/disable)
print("\n=== Trying DELETE ===")
r = requests.delete(f"{URL}/admin", auth=AUTH, timeout=3)
print(f"DELETE /admin: {r.status_code} - {r.text[:100]}")