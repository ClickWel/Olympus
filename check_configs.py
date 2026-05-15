#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Get full configs page
r = requests.get(f"{URL}/configs", auth=AUTH, timeout=5)
print(r.text)

# Try all listed configs
for cfg in ["test", "dev", "Default"]:
    r = requests.get(f"{URL}/configs/use/{cfg}", auth=AUTH, timeout=3)
    print(f"\n=== /configs/use/{cfg} ===")
    print(f"Status: {r.status_code}")
    if "In Use" in r.text or "success" in r.text.lower():
        print("Config set successfully!")
        r2 = requests.get(f"{URL}/admin", auth=AUTH, timeout=3)
        print(f"/admin status: {r2.status_code}")