#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Try to set a cookie that might enable dev mode
print("--- Testing with devMode cookie ---")
r = requests.get(f"{URL}/configs", auth=AUTH, cookies={"devMode": "true"}, timeout=10)
print(f"Status: {r.status_code}")

# Try posting to various endpoints with devMode
for endpoint in ["/configs", "/devices", "/save"]:
    print(f"\n--- POST {endpoint} with devMode ---")
    r = requests.post(f"{URL}{endpoint}", auth=AUTH, data={"devMode": "true", "name": "test"}, timeout=10)
    print(f"Status: {r.status_code}")
    print(r.text[:200] if len(r.text) > 200 else r.text)

# Check if there's an environment file or config we need to set
print("\n--- GET /.env, /.config, /settings ---")
for path in ["/.env", "/.config", "/settings.json", "/config.json", "/app/config"]:
    r = requests.get(f"{URL}{path}", auth=AUTH, timeout=10)
    if r.status_code != 404:
        print(f"{path}: {r.status_code} - {r.text[:100]}")