#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Try to find if there's a /enable or similar route I missed
# Let me list all routes again from the binary

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Find all routes in the binary (around 6019884-6021000)
routes_zone = data[6019800:6021000]

# Extract all strings that look like routes
print("=== All route strings in binary ===")
i = 0
routes = []
while i < len(routes_zone):
    if routes_zone[i] >= 32 and routes_zone[i] < 127:
        j = i
        while j < len(routes_zone) and routes_zone[j] >= 32 and routes_zone[j] < 127 and routes_zone[j] != 0:
            j += 1
        if j - i >= 2:
            s = routes_zone[i:j].decode('utf-8', errors='replace')
            if s.startswith('/') and len(s) < 60:
                routes.append(s)
        i = j + 1
    else:
        i += 1

for r in sorted(set(routes)):
    print(f"  {r}")