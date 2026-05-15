#!/usr/bin/env python3
# Search for any hidden or special routes

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# The "Enabling; Previous Dev Mode:" string is at 6007092
# Let's look at what code path leads to this

enabling_pos = 6007092

# Look for patterns that might indicate a route handler
# Check if there's anything like "enable" or "toggle" near the binary routes section
print("=== Search for enable/toggle patterns near routes ===")
for pattern in [b'enable', b'disable', b'toggle', b'switch', b'flip']:
    pos = data.find(pattern, 6019000)  # Near the routes
    while pos >= 6019000 and pos < 6030000:
        context = data[max(0,pos-100):pos+150].decode('utf-8', errors='replace')
        print(f"'{pattern.decode()}' at {pos}: {context[:200]}")
        pos = data.find(pattern, pos+1)

# Check if dev mode could be tied to the rweb user
print("\n=== Check for user-related dev mode logic ===")
pos = data.find(b'dev_mode_enabled', 10642380)
if pos >= 0:
    context = data[pos-500:pos+500].decode('utf-8', errors='replace')
    print(f"Context around dev_mode_enabled: {context[:500]}")