#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Try to use the dev config
print("=== Using dev config ===")
r = requests.get(f"{URL}/configs/use/dev", auth=AUTH, timeout=5)
print(f"GET /configs/use/dev: {r.status_code}")
print(r.text[:200] if "success" in r.text.lower() else r.text[:100])

# Check /admin after
print("\n=== GET /admin after using dev ===")
r = requests.get(f"{URL}/admin", auth=AUTH, timeout=5)
print(f"Status: {r.status_code}")

# Try the ping endpoint
print("\n=== POST /admin/ping ===")
r = requests.post(f"{URL}/admin/ping", auth=AUTH, data={"ip": "127.0.0.1"}, timeout=5)
print(f"Status: {r.status_code}")
print(r.text[:500] if r.status_code != 401 else "Still 401")