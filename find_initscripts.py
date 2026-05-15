#!/usr/bin/env python3
# Extract strings around known file paths to understand the filesystem structure
import struct

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Look for /etc/init.d/ content
print("=== /etc/init.d scripts ===")
init_d_pos = data.find(b'/etc/init.d')
if init_d_pos >= 0:
    end = min(len(data), init_d_pos + 5000)
    segment = data[init_d_pos:end].decode('utf-8', errors='replace')
    print(segment[:2000])