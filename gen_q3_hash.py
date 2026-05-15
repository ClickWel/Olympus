#!/usr/bin/env python3
import bcrypt

# Bcrypt base64 alphabet
B64 = './ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

def bcrypt_b64_decode(s):
    rev = {c: i for i, c in enumerate(B64)}
    result = []
    for i in range(0, len(s), 4):
        c1 = rev.get(s[i], 0)
        c2 = rev.get(s[i+1], 0) if i+1 < len(s) else 0
        c3 = rev.get(s[i+2], 0) if i+2 < len(s) else 0
        c4 = rev.get(s[i+3], 0) if i+3 < len(s) else 0
        result.append((c1 << 2) | (c2 >> 4))
        if i+2 < len(s):
            result.append(((c2 & 0x0F) << 4) | (c3 >> 2))
        if i+3 < len(s):
            result.append(((c3 & 0x03) << 6) | c4)
    return bytes(result)

def bcrypt_b64_encode(data):
    result = []
    for i in range(0, len(data), 3):
        b1 = data[i]
        b2 = data[i+1] if i+1 < len(data) else 0
        b3 = data[i+2] if i+2 < len(data) else 0
        result.append(B64[b1 >> 2])
        result.append(B64[((b1 & 0x03) << 4) | (b2 >> 4)])
        if i+1 < len(data):
            result.append(B64[((b2 & 0x0F) << 2) | (b3 >> 6)])
        if i+2 < len(data):
            result.append(B64[b3 & 0x3F])
    return ''.join(result)

# Decode JgiaOAai (8 chars -> 6 bytes)
jgia_b64 = 'JgiaOAai'
jgia_bytes = bcrypt_b64_decode(jgia_b64)
print(f'JgiaOAai decodes to: {jgia_bytes.hex()} (6 bytes)')

# Build 16-byte salt: 6 bytes from JgiaOAai + 10 zero bytes
salt_bytes = jgia_bytes + b'\x00' * 10
print(f'Salt bytes (hex): {salt_bytes.hex()}')

# Encode salt to 22-char bcrypt base64
salt_b64 = bcrypt_b64_encode(salt_bytes)
print(f'Salt bcrypt b64: {salt_b64} (length: {len(salt_b64)})')

# Generate hash with cost 4, 5, 6
for cost in [4, 5, 6]:
    # Construct salt param for bcrypt: $2a$NN$<22-char-salt>
    salt_param = f'$2a${cost:02d}${salt_b64}'.encode('utf-8')
    print(f'\nCost {cost} salt param: {salt_param.decode()}')

    # Hash empty password (null terminated)
    pwd = b'\x00'
    try:
        hash_result = bcrypt.hashpw(pwd, salt_param)
        hash_str = hash_result.decode('utf-8')
        # Convert $2a$ to $2$
        hash_2 = hash_str.replace('$2a$', '$2$', 1)
        print(f'Hash ($2a$): {hash_str}')
        print(f'Hash ($2$):  {hash_2}')
        print(f'Full line:   root:{hash_2}')
    except Exception as e:
        print(f'Error: {e}')
