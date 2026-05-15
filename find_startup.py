#!/usr/bin/env python3
# Check ext2 for startup scripts and env
import struct

def read_null_terminated_string(data, offset):
    end = data.find(b'\x00', offset)
    return data[offset:end].decode('utf-8', errors='replace')

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Look for init scripts, rc.local, profiles
patterns = [b'env', b'dev_mode', b'DEV_MODE', b'debug', b'/etc/init', b'rc.local']
for pattern in patterns:
    pos = 0
    count = 0
    while count < 5:
        pos = data.find(pattern, pos)
        if pos < 0:
            break
        print(f"Found '{pattern.decode()}' at offset {pos}")
        # Get surrounding context
        start = max(0, pos - 200)
        end = min(len(data), pos + 400)
        context = data[start:end].decode('utf-8', errors='replace')
        print(f"  Context:\n{context}\n")
        pos += 1
        count += 1