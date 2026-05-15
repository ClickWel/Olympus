#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# The run.sh has --debug option that adds -s to QEMU
# This might enable GDB stub but could also affect the target

# Let me also check if maybe the dev mode is tied to the "rweb" user
# or if there's a way to escalate

print("=== Testing if dev mode is always disabled ===")
# Try all paths with dev in name
for path in ["/dev", "/dev/", "/debug", "/_dev", "/__dev", "/_debug", "/enable", "/init"]:
    r = requests.get(f"{URL}{path}", auth=AUTH, timeout=3)
    if r.status_code != 404:
        print(f"{path}: {r.status_code}")

# Check if there's anything in the response that indicates next steps
print("\n=== Check home page ===")
r = requests.get(f"{URL}/", auth=AUTH, timeout=5)
print(r.text)

# Check devices page for clues
print("\n=== Check devices ===")
r = requests.get(f"{URL}/devices", auth=AUTH, timeout=5)
print(r.text[:500])