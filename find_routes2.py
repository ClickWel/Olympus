#!/usr/bin/env python3
import re

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Find all route-like patterns with the format: /something
# Focus on the binary region (around 6000000-6200000)
routes_zone = data[6000000:6200000]

# Look for patterns like /word/word or /word
# The routes we know: /configs, /configs/save, /configs/update, /devices, etc.

# Extract strings and look for routes
print("=== Looking for route patterns in binary ===")
i = 0
while i < len(routes_zone) - 10:
    # Find null-terminated strings
    if routes_zone[i] >= 32 and routes_zone[i] < 127:
        j = i
        while j < len(routes_zone) and routes_zone[j] >= 32 and routes_zone[j] < 127 and routes_zone[j] != 0:
            j += 1
        if j - i >= 3:
            s = routes_zone[i:j].decode('utf-8', errors='replace')
            # Check if it looks like a route
            if s.startswith('/') and len(s) < 50 and any(c in s for c in ['/', '<']):
                # Skip time zone entries
                if s not in ['/America/', '/Europe/', '/Asia/', '/Pacific/']:
                    print(f"  {s}")
        i = j + 1
    else:
        i += 1