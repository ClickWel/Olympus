#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Check OPTIONS for each endpoint
endpoints = ["/admin", "/admin/ping", "/configs", "/configs/save", "/configs/current", "/devices"]

print("=== OPTIONS for endpoints ===")
for ep in endpoints:
    r = requests.options(f"{URL}{ep}", auth=AUTH, timeout=3)
    allow = r.headers.get('Allow', 'N/A')
    print(f"{ep}: {allow}")

# Try PUT for save
print("\n=== Try PUT to save config ===")
r = requests.put(f"{URL}/configs/save", auth=AUTH, data={"name": "dev"}, timeout=3)
print(f"PUT /configs/save: {r.status_code}")