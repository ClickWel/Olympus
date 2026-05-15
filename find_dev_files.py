#!/usr/bin/env python3

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Look for any files that might be checked for dev mode
# Like /tmp/dev_mode, /var/dev, etc.

print("=== Looking for dev mode files ===")
patterns = [b'/tmp/', b'/var/', b'/dev/', b'dev_mode', b'debug', b'.env']
for pat in patterns:
    pos = 0
    count = 0
    while count < 5:
        pos = data.find(pat, pos)
        if pos < 0 or pos > 6000000:
            break
        context = data[max(0,pos-50):pos+100].decode('utf-8', errors='replace')
        if 'dev' in context.lower() or 'mode' in context.lower():
            print(f"Pattern '{pat.decode()}' at {pos}: {context[:100]}")
        pos += 1
        count += 1

# Look for the actual router-web-panel binary path
print("\n=== Router web panel binary path ===")
pos = data.find(b'/usr/bin/router-web-panel')
if pos >= 0:
    context = data[max(0,pos-100):pos+200].decode('utf-8', errors='replace')
    print(context)