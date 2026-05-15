#!/usr/bin/env python3
# Try to find the correct way to interact with configs

import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# First, use the form on /configs/current to save a config
# The form posts to "" (same URL) with the config data
print("=== POST to /configs/current ===")
r = requests.post(f"{URL}/configs/current", auth=AUTH, data={
    "dns1": "8.8.8.8",
    "dns2": "8.8.4.4",
    "firewall": "Low",
    "portForwarding": ""
}, timeout=5)
print(f"POST /configs/current: {r.status_code}")
print(r.text[:300] if r.status_code != 200 else "Success")

# Check /configs/save with GET (options showed GET allowed)
print("\n=== GET /configs/save with params ===")
r = requests.get(f"{URL}/configs/save", auth=AUTH, params={"name": "test"}, timeout=5)
print(f"GET /configs/save?name=test: {r.status_code}")
print(r.text[:200])

# Try the /save endpoint (from HTML form action)
print("\n=== POST /save ===")
r = requests.post(f"{URL}/save", auth=AUTH, data={"name": "dev"}, timeout=5)
print(f"POST /save: {r.status_code}")
print(r.text[:200])