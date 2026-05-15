#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Try /use/test
print("=== GET /use/test ===")
r = requests.get(f"{URL}/use/test", auth=AUTH, timeout=5)
print(f"Status: {r.status_code}")
print(r.text[:200] if r.status_code != 404 else "Not found")

# Try /use/dev
print("\n=== GET /use/dev ===")
r = requests.get(f"{URL}/use/dev", auth=AUTH, timeout=5)
print(f"Status: {r.status_code}")

# Check if dev is already in use and /admin works
print("\n=== GET /admin (dev is in use) ===")
r = requests.get(f"{URL}/admin", auth=AUTH, timeout=5)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    print("SUCCESS! Dev mode is enabled!")
    print(r.text[:500])