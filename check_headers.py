#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Check what headers the server returns
r = requests.get(f"{URL}/", auth=AUTH, timeout=5)
print("=== Response headers ===")
for k, v in r.headers.items():
    print(f"{k}: {v}")

# Check the /configs/current page for the form
print("\n=== GET /configs/current ===")
r = requests.get(f"{URL}/configs/current", auth=AUTH, timeout=5)
print(r.text[:1000])