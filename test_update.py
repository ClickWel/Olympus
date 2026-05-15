#!/usr/bin/env python3
import requests
import json

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Try proper JSON format for /configs/update
print("=== POST to /configs/update ===")
data = {
    "dns1": "8.8.8.8",
    "dns2": "8.8.4.4",
    "firewall": "Low",
    "port_forwards": []
}
r = requests.post(f"{URL}/configs/update", auth=AUTH, json=data, timeout=5)
print(f"POST /configs/update JSON: {r.status_code}")
print(r.text[:300] if r.status_code != 200 else "Success")

# Check /admin again
print("\n=== Check /admin ===")
r = requests.get(f"{URL}/admin", auth=AUTH, timeout=3)
print(f"GET /admin: {r.status_code}")

# Try with form data
print("\n=== POST /configs/update with form ===")
r = requests.post(f"{URL}/configs/update", auth=AUTH, data={
    "dns1": "8.8.8.8",
    "dns2": "8.8.4.4", 
    "firewall": "Low",
    "portForwarding": ""
}, timeout=5)
print(f"POST /configs/update form: {r.status_code}")