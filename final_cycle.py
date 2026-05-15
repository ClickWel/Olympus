#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Check if we missed anything - try the router-web startup script's logic
# The script shows: setsid /opt/router-web-panel/run.sh
# This suggests the server might read from /opt/router-web-panel/

# Let me also try if there's a POST that creates a config with special properties
# Try to create Default config and see if that affects dev mode

print("=== Full cycle test ===")
# First, check current state
r = requests.get(f"{URL}/configs", auth=AUTH, timeout=5)
print("Current page:")
print(r.text[:500])

# Try POST to /use/Default (based on HTML link)
print("\n=== GET /use/Default ===")
r = requests.get(f"{URL}/use/Default", auth=AUTH, timeout=5)
print(f"Status: {r.status_code}")

# Check admin
print("\n=== GET /admin ===")
r = requests.get(f"{URL}/admin", auth=AUTH, timeout=5)
print(f"Status: {r.status_code}")