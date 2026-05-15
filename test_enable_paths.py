#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Try paths that might enable dev mode
paths = [
    "/enable",
    "/enabled",
    "/disabled",
    "/toggle",
    "/switch",
    "/on",
    "/off",
    "/start",
    "/begin",
    "/init-dev",
    "/dev/enable",
    "/dev/enabled",
    "/debug/enable",
    "/admin/enable",
    "/admin/start",
    "/__dev",
    "/__enable",
]

print("=== Testing potential enable paths ===")
for path in paths:
    r = requests.get(f"{URL}{path}", auth=AUTH, timeout=3)
    if r.status_code != 404:
        print(f"{path}: {r.status_code} - {r.text[:100]}")

# Try POST to some paths
print("\n=== Testing POST to paths ===")
for path in ["/enable", "/toggle", "/admin", "/configs/use/dev"]:
    r = requests.post(f"{URL}{path}", auth=AUTH, data={"enable": "true"}, timeout=3)
    if r.status_code != 404:
        print(f"POST {path}: {r.status_code} - {r.text[:100]}")