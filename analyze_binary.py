#!/usr/bin/env python3
# Check if there's a route that enables dev mode by examining the binary more carefully

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Find "Enabling; Previous Dev Mode:" - this must be triggered by something
# The string is at offset 6007092
# Let's search for what function contains this

# Look for function names around this area
print("=== Looking for function references ===")
# In the C++ binary, look for _Z prefixes (mangled names)
import re
# Find all mangled names near the enabling string
start = 6005000
end = 6010000
section = data[start:end]

# Find patterns like _Z*enable or _Z*dev
matches = re.findall(rb'_Z[a-zA-Z0-9_]*(enable|dev|mode)[a-zA-Z0-9_]*', section)
for m in sorted(set(matches)):
    print(f"Found: {m.decode()}")

# Also look for the route strings more carefully
print("\n=== Route strings ===")
# The routes are around 6019884
route_section = data[6019850:6020200]
strings = []
i = 0
while i < len(route_section):
    if route_section[i] >= 32 and route_section[i] < 127:
        j = i
        while j < len(route_section) and route_section[j] >= 32 and route_section[j] < 127 and route_section[j] != 0:
            j += 1
        if j - i >= 2:
            strings.append(route_section[i:j].decode('utf-8', errors='replace'))
        i = j + 1
    else:
        i += 1

for s in strings:
    if s.startswith('/') or 'enable' in s.lower() or 'dev' in s.lower():
        print(f"  {s}")