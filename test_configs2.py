#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Check current state
print("=== Service status ===")
r = requests.get(f"{URL}/", auth=AUTH, timeout=5)
print(f"GET /: {r.status_code}")

r = requests.get(f"{URL}/admin", auth=AUTH, timeout=5)
print(f"GET /admin: {r.status_code}")

# Check if maybe dev mode is tied to a specific config being used
print("\n=== Try using 'dev' config ===")
r = requests.get(f"{URL}/configs/use/dev", auth=AUTH, timeout=5)
print(f"GET /configs/use/dev: {r.status_code} - {r.text[:100]}")

# Try 'debug' config
print("\n=== Try using 'debug' config ===")
r = requests.get(f"{URL}/configs/use/debug", auth=AUTH, timeout=5)
print(f"GET /configs/use/debug: {r.status_code} - {r.text[:100]}")

# Create a config named 'dev' and try to use it
print("\n=== Try saving 'dev' config ===")
r = requests.post(f"{URL}/configs/save", auth=AUTH, data={"name": "dev"}, timeout=5)
print(f"POST /configs/save: {r.status_code} - {r.text[:100]}")

if r.status_code == 302 or "Redirect" in r.text:
    # Follow redirect
    loc = r.headers.get('Location', '')
    print(f"Redirect to: {loc}")