import re

firmware_path = r"C:\Users\click\Desktop\forensics_silicon_data_sleuthing (1)\chal_router_dump.bin"

with open(firmware_path, "rb") as f:
    data = f.read()

print(f"Firmware size: {len(data)} bytes")

# Search for $2$ bcrypt hashes
bcrypt_pattern = rb'\$2\$[\.\/A-Za-z0-9]+\$[\.\/A-Za-z0-9]+'
matches = re.findall(bcrypt_pattern, data)
print(f"\nFound {len(matches)} bcrypt ($2$) hashes:")
for m in matches[:10]:
    print(m.decode('utf-8', errors='replace'))

# Search for $1$ (MD5), $5$ (SHA256), $6$ (SHA512) hashes
for algo, name in [(rb'\$1\$', 'MD5'), (rb'\$5\$', 'SHA256'), (rb'\$6\$', 'SHA512'), (rb'\$2a\$', 'bcrypt-a'), (rb'\$2y\$', 'bcrypt-y')]:
    matches = re.findall(algo + rb'[\.\/A-Za-z0-9]+\$[\.\/A-Za-z0-9]+', data)
    if matches:
        print(f"\nFound {len(matches)} {name} hashes:")
        for m in matches[:5]:
            print(m.decode('utf-8', errors='replace'))

# Search for "root:" context (password hashes in passwd/shadow)
root_matches = [(m.start(), data[m.start():m.start()+200]) for m in re.finditer(rb'root:', data)]
print(f"\nFound {len(root_matches)} 'root:' occurrences:")
for pos, context in root_matches[:10]:
    print(f"\nOffset 0x{pos:x} ({pos}):")
    print(context.decode('utf-8', errors='replace').strip())

# Search for shadow line pattern (root:*:*...)
shadow_pattern = rb'root:([^:\n]+):[^:\n]+:[^:\n]+:[^:\n]+:[^:\n]+:[^:\n]*:[^:\n]*:[^:\n]*'
matches = re.findall(shadow_pattern, data)
print(f"\nFound {len(matches)} shadow-like root entries:")
for m in matches[:10]:
    print(f"Password field: {m.decode('utf-8', errors='replace')}")

# Search for $p$root or other $p$ hashes
p_hashes = re.findall(rb'\$p\$[\.\/A-Za-z0-9]+', data)
print(f"\nFound {len(p_hashes)} '$p$' hashes:")
for m in p_hashes[:10]:
    print(m.decode('utf-8', errors='replace'))