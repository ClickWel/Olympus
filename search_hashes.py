import re

with open(r'C:\Users\click\Desktop\forensics_silicon_data_sleuthing (1)\chal_router_dump.bin', 'rb') as f:
    data = f.read()

# Old $2$ bcrypt format (not $2a$ or $2b$)
# Format: $2$ + 22 char salt + $ + 31 char hash
pattern = rb'\$2\$[a-zA-Z0-9./]{22}\$[a-zA-Z0-9./]{31}'
matches = re.findall(pattern, data)
print(f'$2$ (old bcrypt) format: {len(matches)} matches')
for m in matches[:20]:
    print(m.decode())

# Also check $2a$ and $2b$
pattern_2a = rb'\$2a\$[a-zA-Z0-9./]{22}\$[a-zA-Z0-9./]{31}'
pattern_2b = rb'\$2b\$[a-zA-Z0-9./]{22}\$[a-zA-Z0-9./]{31}'
matches_2a = re.findall(pattern_2a, data)
matches_2b = re.findall(pattern_2b, data)
print(f'\n$2a$ format: {len(matches_2a)} matches')
print(f'$2b$ format: {len(matches_2b)} matches')

# Also check for $p$ pattern
pattern_p = rb'\$p\$[a-zA-Z0-9./]+'
matches_p = re.findall(pattern_p, data)
print(f'\n$p$ format: {len(matches_p)} matches')
for m in matches_p[:20]:
    print(m.decode())