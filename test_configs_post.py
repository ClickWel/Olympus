#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Try posting to /configs with dev flag
print("=== POST to /configs with various data ===")
for data in [
    {"devMode": "true"},
    {"enableDev": "true"},
    {"dev": "true"},
    {"mode": "dev"},
    {"name": "dev", "devMode": "true"},
]:
    r = requests.post(f"{URL}/configs", auth=AUTH, data=data, timeout=3)
    print(f"POST /configs with {list(data.keys())}: {r.status_code}")

# Try /configs/update
print("\n=== POST to /configs/update ===")
r = requests.post(f"{URL}/configs/update", auth=AUTH, json={"devMode": True}, timeout=3)
print(f"POST /configs/update JSON: {r.status_code}")

# Check /devices/update
print("\n=== Try /devices endpoints ===")
r = requests.get(f"{URL}/devices", auth=AUTH, timeout=3)
print(f"GET /devices: {r.status_code}")

# Maybe there's a way via devices?
r = requests.post(f"{URL}/devices/add", auth=AUTH, data={
    "name": "test",
    "mac": "aa:bb:cc:dd:ee:ff",
    "type": "Desktop"
}, timeout=3)
print(f"POST /devices/add: {r.status_code}")