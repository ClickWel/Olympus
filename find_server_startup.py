#!/usr/bin/env python3
# Look for server startup in init scripts

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Find SXX scripts (startup scripts run by rcS)
print("=== Looking for startup scripts (S99, S50, etc) ===")
# Search for S99 or similar patterns
patterns = [b'S99', b'S50', b'S40', b'S01']
for pat in patterns:
    pos = data.find(pat)
    while pos >= 0 and pos < 2000000:
        context = data[max(0,pos-100):pos+200].decode('utf-8', errors='replace')
        if '/server' in context or 'web' in context or 'crow' in context:
            print(f"Found '{pat.decode()}' at {pos}:")
            print(context)
        pos = data.find(pat, pos+1)

# Also look for what starts the web server
print("\n=== Looking for web server start ===")
# Search for common web server process names
for pat in [b'router_web', b'router-web', b'crow', b'main', b'./']:
    pos = 0
    count = 0
    while count < 3:
        pos = data.find(pat, pos)
        if pos < 0 or pos > 6000000:
            break
        context = data[max(0,pos-100):pos+150].decode('utf-8', errors='replace')
        if any(kw in context for kw in [b'server', b'web', b'S', b'::respawn']):
            print(f"'{pat.decode()}' at {pos}: {context[:200]}")
        pos += 1
        count += 1