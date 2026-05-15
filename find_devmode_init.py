#!/usr/bin/env python3
# Search more broadly for dev mode enable mechanism

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Look for startup-related strings around the main binary
print("=== Looking for main function and init logic ===")
# Search for "main" string and related function calls in the binary region (around 700KB-1100KB)

# Also check if dev mode is set via environment at startup
print("=== Environment variables and startup ===")
for pattern in [b'DEV_MODE', b'dev_mode', b'start_up', b'startup', b'initial', b'INIT']:
    pos = 0
    count = 0
    while count < 3 and pos >= 0:
        pos = data.find(pattern, pos)
        if pos < 0 or pos > 1200000:
            break
        context = data[max(0,pos-100):pos+150].decode('utf-8', errors='replace')
        print(f"'{pattern.decode()}' at {pos}: {context[:150]}")
        pos += 1
        count += 1

# Look for where dev_mode_enabled variable might be set
print("\n=== Looking for variable assignments ===")
for pattern in [b'dev_mode_enabled', b'IsDevMode', b'DevMode']:
    pos = 0
    count = 0
    while count < 5 and pos >= 0:
        pos = data.find(pattern, pos)
        if pos < 0:
            break
        context = data[max(0,pos-100):pos+200].decode('utf-8', errors='replace')
        print(f"'{pattern.decode()}' at {pos}:")
        print(f"  {context}")
        print()
        pos += 1
        count += 1