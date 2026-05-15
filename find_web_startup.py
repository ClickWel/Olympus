#!/usr/bin/env python3
# Look for web server startup

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Search for web server or router web related strings
patterns = [b'web-panel', b'router', b'web', b'http', b'server', b'crow', b'python', b'node']
for pat in patterns:
    pos = data.find(pat, 6000000)  # In the binary area
    if pos >= 0:
        context = data[max(0,pos-100):pos+200].decode('utf-8', errors='replace')
        print(f"'{pat.decode()}' at {pos}: {context[:200]}")

# Also search for process startup patterns
print("\n=== Process startup patterns ===")
for pat in [b'::respawn:', b'::sysinit:', b'-daemon']:
    pos = 0
    count = 0
    while count < 3 and pos >= 0:
        pos = data.find(pat, pos)
        if pos < 0:
            break
        context = data[max(0,pos-50):pos+150].decode('utf-8', errors='replace')
        print(f"'{pat.decode()}' at {pos}: {context}")
        pos += 1
        count += 1