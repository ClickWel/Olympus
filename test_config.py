#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Try to use a config - maybe dev mode is enabled by using a specific config
print("=== GET /configs ===")
r = requests.get(f"{URL}/configs", auth=AUTH, timeout=5)
print(f"Status: {r.status_code}")
print(r.text[:800])

# Try to use the config
print("\n=== GET /configs/current ===")
r = requests.get(f"{URL}/configs/current", auth=AUTH, timeout=5)
print(f"Status: {r.status_code}")
print(r.text[:500])

# Try to save a config - maybe the "dev" config name?
print("\n=== POST /configs/save with dev config ===")
r = requests.post(f"{URL}/configs/save", auth=AUTH, data={"name": "dev"}, timeout=5)
print(f"Status: {r.status_code}")
print(r.text[:300])

# Try using dev config
print("\n=== GET /configs/use/dev ===")
r = requests.get(f"{URL}/configs/use/dev", auth=AUTH, timeout=5)
print(f"Status: {r.status_code}")
print(r.text[:300])

# Check /admin again
print("\n=== GET /admin after config ===")
r = requests.get(f"{URL}/admin", auth=AUTH, timeout=5)
print(f"Status: {r.status_code}")