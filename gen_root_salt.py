#!/usr/bin/env python3
import bcrypt

B64 = './ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

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

# Salt: 'root' (4 bytes) + 12 zero bytes = 16 bytes
salt_bytes = b'root' + b'\x00' * 12
print(f'Salt bytes (hex): {salt_bytes.hex()}')
salt_b64 = bcrypt_b64_encode(salt_bytes)
print(f'Salt b64: {salt_b64} (len: {len(salt_b64)})')

for cost in [4,5,6,8,10,12]:
    salt_param = f'$2a${cost:02d}${salt_b64}'.encode()
    print(f'\nCost {cost}:')
    try:
        hash_res = bcrypt.hashpw(b'\x00', salt_param)
        hash_str = hash_res.decode()
        hash_2 = hash_str.replace('$2a$', '$2$', 1)
        print(f'  $2$: {hash_2}')
        print(f'  Full line: root:{hash_2}')
    except Exception as e:
        print(f'  Error: {e}')
