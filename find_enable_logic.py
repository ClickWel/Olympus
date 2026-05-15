#!/usr/bin/env python3

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Found at 6007092 and 6007124
enabling_pos = 6007092
disabling_pos = 6007124

print("=== Around Enabling string ===")
context = data[enabling_pos-500:enabling_pos+500].decode('utf-8', errors='replace')
print(context)

print("\n=== Around Disabling string ===")
context = data[disabling_pos-500:disabling_pos+500].decode('utf-8', errors='replace')
print(context)

# Find any route patterns near these
print("\n=== Looking for routes near these strings ===")
routes = []
for pat in [b'/enable', b'/disable', b'/dev', b'/debug', b'/setup']:
    pos = data.find(pat, enabling_pos-1000)
    while pos >= enabling_pos-1000 and pos < disabling_pos+1000:
        routes.append((pos, pat))
        pos = data.find(pat, pos+1)

for pos, pat in sorted(routes):
    context = data[max(0,pos-20):pos+30].decode('utf-8', errors='replace')
    print(f"Found '{pat.decode()}' at {pos}: ...{context}...")