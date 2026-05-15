#!/usr/bin/env python3
import struct

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Find the main server binary - look for HTTP-related strings near ELF headers
# We know there are ELF binaries at offsets: 756736, 1721344, 1744632, etc.

# Look for HTTP server indicators
patterns = [
    b'router', b'Server:', b'Content-Type', b'HTTP/1.',
    b'Crow', b'crow::', b'mustache', b'mustache::'
]

for pattern in patterns:
    pos = 0
    count = 0
    while count < 3:
        pos = data.find(pattern, pos)
        if pos < 0:
            break
        # Check if this looks like a string in the binary (not filesystem data)
        if pos > 700000 and pos < 1100000:  # Around the main binary
            context = data[max(0,pos-100):pos+150].decode('utf-8', errors='replace')
            print(f"Found '{pattern.decode()}' at offset {pos}:")
            print(f"  {context[:200]}")
            print()
        pos += 1
        count += 1

# Also try to find main function or startup logic
print("\n--- Looking for startup logic ---")
# Check what's around the main ELF
elf_start = 756736
print(f"Data around first ELF ({elf_start}):")
print(data[elf_start:elf_start+200].decode('utf-8', errors='replace'))