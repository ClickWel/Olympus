#!/usr/bin/env python3
"""Generate bcrypt $2$ hash using WSL Python's bcrypt library."""
import bcrypt
import sys

BCRYPT_B64 = b'./ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

def to_b64(data):
    """Encode bytes to bcrypt base64."""
    result = []
    for i in range(0, len(data), 3):
        b1 = data[i]
        b2 = data[i+1] if i+1 < len(data) else 0
        b3 = data[i+2] if i+2 < len(data) else 0
        result.append(chr(BCRYPT_B64[b1 >> 2]))
        result.append(chr(BCRYPT_B64[((b1 & 0x03) << 4) | (b2 >> 4)]))
        if i+1 < len(data):
            result.append(chr(BCRYPT_B64[((b2 & 0x0F) << 2) | (b3 >> 6)]))
        if i+2 < len(data):
            result.append(chr(BCRYPT_B64[b3 & 0x3F]))
    return ''.join(result)

def from_b64(s):
    """Decode bcrypt base64 to bytes."""
    rev = {}
    for i, c in enumerate(BCRYPT_B64):
        rev[chr(c)] = i

    result = bytearray()
    for i in range(0, len(s), 4):
        c1 = rev[s[i]]
        c2 = rev[s[i+1]]
        c3 = rev[s[i+2]] if i+2 < len(s) else 0
        c4 = rev[s[i+3]] if i+3 < len(s) else 0

        result.append((c1 << 2) | (c2 >> 4))
        if i+2 < len(s):
            result.append(((c2 & 0x0F) << 4) | (c3 >> 2))
        if i+3 < len(s):
            result.append(((c3 & 0x03) << 6) | c4)
    return bytes(result)

# Test: generate hash with specific salt bytes
print("Generating bcrypt hashes of empty string...")
print()

# Try with different salt values
salt_tests = [
    ('zero_16', b'\x00' * 16),
    ('JgiaOAai_then_zero', from_b64('JgiaOAai') + b'\x00' * 10),
    ('all_0x42', b'\x42' * 16),  # All 'B' in ASCII
]

for name, salt_bytes in salt_tests:
    salt_b64 = to_b64(salt_bytes)
    print(f'Salt ({name}): {salt_b64} (len={len(salt_b64)})')

    for cost in [4, 5, 6, 8]:
        # Construct salt param for bcrypt.hashpw
        salt_param = f'$2a${cost:02d}${salt_b64}'.encode()

        try:
            # Hash empty string (null-terminated for bcrypt)
            h = bcrypt.hashpw(b'\x00', salt_param)
            h_str = h.decode().replace('$2a$', '$2$', 1)
            print(f'  Cost={cost}: root:{h_str}')
        except Exception as e:
            print(f'  Cost={cost}: Error - {e}')

    print()
