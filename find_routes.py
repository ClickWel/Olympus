#!/usr/bin/env python3
# Extract all routes from the binary

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# From earlier: routes found near error message at 6019884
# /configs, /configs/save, /configs/update, /configs/delete/<string>, /configs/use/<string>
# /configs/current, /devices, /devices/add, /devices/update, /admin, /admin/ping

# Look for more routes
print("=== All route patterns ===")
import re

# Find URL-like patterns
routes = re.findall(rb'/[\w/]+(?:</\w+>|\s|\x00)', data)
seen = set()
for r in routes:
    r_str = r.decode('utf-8', errors='replace').rstrip('\x00')
    if r_str not in seen and len(r_str) > 2:
        seen.add(r_str)

for r in sorted(seen):
    print(r)