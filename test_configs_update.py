#!/usr/bin/env python3
import requests
import json

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Try to update config via POST JSON (the HTML shows it uses fetch with JSON)
print("=== POST /configs/update JSON ===")
data = {
    "dns1": "1.1.1.1",
    "dns2": "1.0.0.1",
    "firewall": "High",
    "port_forwards": [[80, 8080], [443, 8443]],
    "timestamp": 1234567890
}
r = requests.post(f"{URL}/configs/update", auth=AUTH, json=data, timeout=5)
print(f"Status: {r.status_code}")
print(r.text[:500])

# Try with form data
print("\n=== POST /configs/update form ===")
r = requests.post(f"{URL}/configs/update", auth=AUTH, data={
    "dns1": "1.1.1.1",
    "dns2": "1.0.0.1",
    "firewall": "High",
    "portForwarding": "80,8080,443,8443"
}, timeout=5)
print(f"Status: {r.status_code}")
print(r.text[:300])