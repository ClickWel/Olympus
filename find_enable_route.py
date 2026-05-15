#!/usr/bin/env python3
# Look for the enable route in the binary

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# The routes are registered in the binary. Let's find patterns like "/enable" 
# combined with "dev" or similar

# Search in the route section (around 6019884 where routes are defined)
routes_section = data[6019800:6021000]

print("=== Looking for enable-related routes ===")
# Find strings that might be routes
i = 0
while i < len(routes_section):
    if routes_section[i] >= 32 and routes_section[i] < 127:
        j = i
        while j < len(routes_section) and routes_section[j] >= 32 and routes_section[j] < 127 and routes_section[j] != 0:
            j += 1
        if j - i >= 3:
            s = routes_section[i:j].decode('utf-8', errors='replace')
            if 'enable' in s.lower() or 'dev' in s.lower():
                print(f"  {s}")
        i = j + 1
    else:
        i += 1

# Also look for what comes before/after the known routes
print("\n=== Full route strings in binary ===")
# Find /admin, /ping patterns
for marker in [b'/admin', b'/ping', b'/enable', b'/disabled']:
    pos = data.find(marker, 6000000)
    while pos >= 6000000 and pos < 6030000:
        context = data[max(0,pos-50):min(len(data), pos+100)].decode('utf-8', errors='replace')
        print(f"'{marker.decode()}' at {pos}: ...{context}...")
        pos = data.find(marker, pos+1)