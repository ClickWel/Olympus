#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Check current config state
print("=== GET /configs ===")
r = requests.get(f"{URL}/configs", auth=AUTH, timeout=5)
print(r.text[:800])

# Try using the "test" config
print("\n=== GET /configs/use/test ===")
r = requests.get(f"{URL}/configs/use/test", auth=AUTH, timeout=5)
print(f"Status: {r.status_code}")

# Check /admin after
print("\n=== GET /admin after using test ===")
r = requests.get(f"{URL}/admin", auth=AUTH, timeout=5)
print(f"Status: {r.status_code}")