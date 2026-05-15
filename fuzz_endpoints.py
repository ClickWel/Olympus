#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Try some fuzzing for potential hidden endpoints
endpoints = [
    "/admin/",
    "/admin/setup",
    "/admin/enable",
    "/admin/init",
    "/enable-dev",
    "/dev/enable",
    "/debug/enable",
    "/api/admin",
    "/api/dev",
    "/api/enable",
    "/v1/admin",
    "/internal/enable",
    "/_dev",
    "/.dev",
]

print("=== Testing hidden endpoints ===")
for path in endpoints:
    try:
        r = requests.get(f"{URL}{path}", auth=AUTH, timeout=3)
        if r.status_code != 404:
            print(f"{path}: {r.status_code}")
            if "Not Found" not in r.text:
                print(r.text[:150])
    except:
        pass

# Try POST with various methods
print("\n=== Try POST to various endpoints ===")
for path in ["/admin", "/admin/", "/enable", "/_dev", "/internal"]:
    try:
        r = requests.post(f"{URL}{path}", auth=AUTH, data={"enable": "true"}, timeout=3)
        if r.status_code != 404:
            print(f"POST {path}: {r.status_code}")
    except:
        pass

# Try with different content types
print("\n=== Try JSON to /admin ===")
r = requests.post(f"{URL}/admin", auth=AUTH, json={"devMode": True}, timeout=3)
print(f"POST /admin JSON: {r.status_code} - {r.text[:100]}")

# Try PUT
print("\n=== Try PUT to /admin ===")
r = requests.put(f"{URL}/admin", auth=AUTH, data={"devMode": "true"}, timeout=3)
print(f"PUT /admin: {r.status_code} - {r.text[:100]}")