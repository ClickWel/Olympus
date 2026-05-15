#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# POST to /configs/current (form action is "")
print("=== POST /configs/current ===")
r = requests.post(f"{URL}/configs/current", auth=AUTH, data={
    "dns1": "8.8.8.8",
    "dns2": "8.8.4.4",
    "firewall": "Low",
    "portForwarding": ""
}, timeout=5)
print(f"Status: {r.status_code}")
print(r.text[:300] if r.status_code != 200 else "Success")

# Check if config was created
print("\n=== GET /configs ===")
r = requests.get(f"{URL}/configs", auth=AUTH, timeout=5)
print(r.text[:800])