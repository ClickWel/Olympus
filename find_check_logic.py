#!/usr/bin/env python3
# Find all references to dev mode check

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# The dev_mode_enabled variable is around 10642383
# Let's look for patterns that might indicate how it's checked

# Look for "dev_mode" in the error context (around 6019884)
dev_error_zone = data[6000000:6100000]
print("=== Strings near Dev Mode error ===")
strings = []
i = 0
while i < len(dev_error_zone) - 10:
    if dev_error_zone[i:i+10].isascii() and dev_error_zone[i:i+10].isprintable():
        for j in range(i+10, min(i+100, len(dev_error_zone))):
            if dev_error_zone[j:j+1] == b'\x00' or not dev_error_zone[j:j+1].isascii() or not dev_error_zone[j:j+1].isprintable():
                if j - i > 5:
                    strings.append((i+6000000, dev_error_zone[i:j].decode('utf-8', errors='replace')))
                break
        i = j
    else:
        i += 1

for offset, s in strings:
    if 'admin' in s.lower() or 'dev' in s.lower() or 'ping' in s.lower() or 'mode' in s.lower():
        print(f"  {offset}: {s}")

# Look for function that checks dev mode
print("\n=== Looking for dev mode check logic ===")
# Search for patterns that could be the check
check_patterns = [b'dev_mode_enabled', b'DevMode', b'devMode', b'isDevMode', b'IsDev']
for pat in check_patterns:
    pos = 6000000
    while True:
        pos = data.find(pat, pos)
        if pos < 6000000 or pos > 6100000 or pos < 0:
            break
        context = data[max(6000000,pos-100):min(6100000,pos+100)].decode('utf-8', errors='replace')
        print(f"Found '{pat.decode()}' at {pos}: {context}")
        pos += 1