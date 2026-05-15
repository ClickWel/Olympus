#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# /configs/save shows GET allowed - try GET
print("=== GET /configs/save ===")
r = requests.get(f"{URL}/configs/save", auth=AUTH, params={"name": "dev"}, timeout=5)
print(f"Status: {r.status_code}")
print(r.text[:500])

# Try with the name in the URL
print("\n=== GET /configs/save/dev ===")
r = requests.get(f"{URL}/configs/save/dev", auth=AUTH, timeout=5)
print(f"Status: {r.status_code}")
print(r.text[:300])

r = requests.get(f"{URL}/configs/save?name=dev", auth=AUTH, timeout=5)
print(f"GET /configs/save?name=dev: {r.status_code}")