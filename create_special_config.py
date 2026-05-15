#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Create configs with GET /configs/save
# From HTML: <form action="/save" method="POST">
# But OPTIONS shows GET for /configs/save

# Try GET with params
for name in ["dev", "Dev", "DEBUG", "debug", "enable"]:
    r = requests.get(f"{URL}/configs/save", auth=AUTH, params={"name": name}, timeout=5)
    print(f"GET /configs/save?name={name}: {r.status_code}")

# Try POST  
print("\n=== POST attempts ===")
for name in ["dev", "debug", "enable"]:
    r = requests.post(f"{URL}/configs/save", auth=AUTH, data={"name": name}, timeout=5)
    print(f"POST /configs/save name={name}: {r.status_code}")

# Check current configs
print("\n=== GET /configs ===")
r = requests.get(f"{URL}/configs", auth=AUTH, timeout=5)
print(r.text[:500])