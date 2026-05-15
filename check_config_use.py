#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Check responses
for cfg in ["debug", "test", "default", "production"]:
    r = requests.get(f"{URL}/configs/use/{cfg}", auth=AUTH, timeout=3)
    print(f"=== /configs/use/{cfg} ===")
    print(f"Status: {r.status_code}")
    if "Config does not exist" in r.text:
        print("Config does not exist")
    else:
        print(r.text[:200])
    print()

# Check /admin after using each
print("=== Check /admin ===")
for cfg in ["debug", "test"]:
    r = requests.get(f"{URL}/configs/use/{cfg}", auth=AUTH, timeout=3)
    r2 = requests.get(f"{URL}/admin", auth=AUTH, timeout=3)
    print(f"After /configs/use/{cfg}: /admin = {r2.status_code}")