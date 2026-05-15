#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# The form posts to /save (not /configs/save)
print("=== POST /save ===")
r = requests.post(f"{URL}/save", auth=AUTH, data={"name": "dev"}, timeout=5)
print(f"POST /save: {r.status_code}")
print(r.text[:300] if r.status_code != 405 else "Method not allowed")

r = requests.get(f"{URL}/save", auth=AUTH, timeout=5)
print(f"GET /save: {r.status_code}")

# Also check /configs with POST 
print("\n=== POST /configs ===")
r = requests.post(f"{URL}/configs", auth=AUTH, data={"name": "dev"}, timeout=5)
print(f"POST /configs: {r.status_code}")

# Maybe the enable is through /devices somehow?
print("\n=== Check devices update ===")
r = requests.post(f"{URL}/devices/update", auth=AUTH, data={"id": "0", "name": "test"}, timeout=5)
print(f"POST /devices/update: {r.status_code}")