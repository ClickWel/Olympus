#!/usr/bin/env python3
# Look for init scripts and startup

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Find /etc/init.d content
rcS_pos = data.find(b'/etc/init.d/rcS')
if rcS_pos >= 0:
    print(f"=== /etc/init.d/rcS reference at {rcS_pos} ===")
    # Look backward for the actual script content
    context = data[rcS_pos-100:rcS_pos+500].decode('utf-8', errors='replace')
    print(context)

# Look for any startup script content
print("\n=== Looking for startup script content ===")
# Search for common startup patterns
patterns = [b'/etc/init.d/S', b'SXX', b'start-stop-daemon', b'exec ']
for pat in patterns:
    pos = 0
    count = 0
    while count < 5:
        pos = data.find(pat, pos)
        if pos < 0:
            break
        if pos > 1000000 and pos < 6000000:  # In the script/filesystem area
            context = data[max(0,pos-50):pos+100].decode('utf-8', errors='replace')
            print(f"'{pat.decode()}' at {pos}: {context}")
        pos += 1
        count += 1