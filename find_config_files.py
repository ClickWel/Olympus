#!/usr/bin/env python3
# Check for any config files or environment that might enable dev mode

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Look for any JSON or config files
print("=== Looking for config files ===")
for pattern in [b'.json', b'.conf', b'.cfg', b'config']:
    pos = 0
    count = 0
    while count < 5 and pos >= 0:
        pos = data.find(pattern, pos)
        if pos < 0 or pos > 1200000:
            break
        context = data[max(0,pos-50):min(len(data), pos+100)].decode('utf-8', errors='replace')
        print(f"'{pattern.decode()}' at {pos}: {context}")
        pos += 1
        count += 1

# Look for the -s flag or debug flag usage (from run.sh --debug option)
print("\n=== Debug/startup flags ===")
for pattern in [b'--debug', b'-s ', b'EXTRA_ARGS']:
    pos = data.find(pattern)
    if pos >= 0 and pos < 1200000:
        context = data[max(0,pos-50):pos+150].decode('utf-8', errors='replace')
        print(f"'{pattern.decode()}' at {pos}: {context[:200]}")