import re

def extract_strings(filepath, min_len=4):
    with open(filepath, 'rb') as f:
        data = f.read()
    # Extract ASCII strings
    strings = re.findall(rb'[a-zA-Z0-9./$@_-]{' + str(min_len).encode() + rb',}', data)
    return [s.decode('utf-8', errors='replace') for s in strings]

# Check rpcd binary
strings = extract_strings(r'D:\Olympus\SquashFS_root\sbin\rpcd', min_len=10)
crypto_strings = [s for s in strings if any(c in s for c in ['$', 'hash', 'pass', 'crypt', '2a', '2b', '2b'])]
print('Crypto-related strings in rpcd:')
for s in crypto_strings[:50]:
    print(f'  {s}')

# Check uhttpd
strings = extract_strings(r'D:\Olympus\SquashFS_root\usr\sbin\uhttpd', min_len=10)
crypto_strings = [s for s in strings if '$' in s or 'hash' in s.lower() or 'pass' in s.lower()]
print('\nCrypto-related strings in uhttpd:')
for s in crypto_strings[:50]:
    print(f'  {s}')