#!/usr/bin/env python3
import struct

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Find strings that look like config paths or shell commands
patterns = [
    b'/etc/', b'/home/', b'/root/', b'/var/', b'/tmp/',
    b'enable', b'start', b'init', b'mode', b'dev'
]

# Also look for environment variable patterns
print("=== Looking for .profile, .bashrc, environment ===")
for pattern in [b'.profile', b'.bashrc', b'.env', b'export ', b'ENV']:
    pos = 0
    while True:
        pos = data.find(pattern, pos)
        if pos < 0 or pos > 1200000:
            break
        context = data[max(0,pos-100):pos+150].decode('utf-8', errors='replace')
        if 'binary' not in context.lower() and len(context.strip()) > 10:
            print(f"Found at {pos}: {context[:150]}")
        pos += 1

# Check for startup scripts
print("\n=== Looking for rc scripts and startup ===")
for pattern in [b'rcS', b'rc.local', b'SXX', b'S99']:
    pos = 0
    while True:
        pos = data.find(pattern, pos)
        if pos < 0:
            break
        context = data[max(0,pos-50):pos+100].decode('utf-8', errors='replace')
        print(f"Found '{pattern.decode()}' at {pos}: {context}")
        pos += 1