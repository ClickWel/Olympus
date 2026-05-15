#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Try a direct approach - maybe dev mode is enabled via a cookie or header
# Check response headers and try various auth combinations

print("=== Testing headers and cookies ===")

# Try with cookie
cookies = {"devMode": "true", "debug": "true"}
r = requests.get(f"{URL}/admin/ping", auth=AUTH, cookies=cookies, timeout=5)
print(f"With devMode cookie: {r.status_code} - {r.text[:200]}")

# Try with header
headers = {"X-Dev-Mode": "true", "X-Debug": "true"}
r = requests.get(f"{URL}/admin/ping", auth=AUTH, headers=headers, timeout=5)
print(f"With X-Dev-Mode header: {r.status_code} - {r.text[:200]}")

# Check what endpoints exist
print("\n=== Trying common web app endpoints ===")
paths = ["/", "/home", "/index", "/api", "/api/enable", "/api/dev", "/router", "/web"]
for path in paths:
    r = requests.get(f"{URL}{path}", auth=AUTH, timeout=5)
    print(f"{path}: {r.status_code}")

# Check if maybe we need to POST to /admin with devMode form data
print("\n=== Trying POST with devMode to /admin ===")
r = requests.post(f"{URL}/admin", auth=AUTH, data={"devMode": "true"}, timeout=5)
print(f"POST /admin with devMode: {r.status_code} - {r.text[:200]}")