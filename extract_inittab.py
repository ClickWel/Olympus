#!/usr/bin/env python3
# Extract full inittab content

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Find inittab content
init_pos = data.find(b'::sysinit:/bin/mount')
if init_pos >= 0:
    print(f"=== inittab content starting at {init_pos} ===")
    # Extract a large section
    end = data.find(b'/etc/services', init_pos)
    if end < 0:
        end = init_pos + 3000
    section = data[init_pos-500:end].decode('utf-8', errors='replace')
    print(section)