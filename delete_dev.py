#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# The HTML has /use/test but routes say /configs/use/<string>
# Maybe the server doesn't have the route working correctly?

# Let me check if maybe I need to DELETE the dev config to enable dev mode
# Or create a special config

# First let me check if dev mode is tied to something specific
# Delete the dev config
print("=== DELETE /configs/delete/dev ===")
r = requests.get(f"{URL}/configs/delete/dev", auth=AUTH, timeout=5)
print(f"Status: {r.status_code}")

# Check admin again
print("\n=== GET /admin ===")
r = requests.get(f"{URL}/admin", auth=AUTH, timeout=5)
print(f"Status: {r.status_code}")

# Check configs
print("\n=== GET /configs ===")
r = requests.get(f"{URL}/configs", auth=AUTH, timeout=5)
# Count configs
import re
configs = re.findall(r'Config <code>([^<]+)</code>', r.text)
print(f"Configs: {configs}")