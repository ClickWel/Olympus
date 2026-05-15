#!/usr/bin/env python3
"""Generate bcrypt $2$ hash of empty string with deterministic salt."""
import bcrypt

BCRYPT_B64 = b'./ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

def bytes_to_bcrypt_b64(data):
    """Encode bytes to bcrypt base64 (no padding)."""
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

def gen_hash(cost, salt_bytes):
    """Generate bcrypt hash with specific salt bytes and cost."""
    # Encode salt to 22-char bcrypt base64
    salt_b64 = bytes_to_bcrypt_b64(salt_bytes)
    # Construct salt param for bcrypt.hashpw: $2a$NN$<22-chars>
    salt_param = f'$2a${cost:02d}${salt_b64}'.encode('utf-8')

    # Hash empty password (null-terminated)
    pwd = b'\x00'

    result = bcrypt.hashpw(pwd, salt_param)
    # Convert $2a$ to $2$
    result_str = result.decode('utf-8').replace('$2a$', '$2$', 1)
    return result_str

# Generate with different salts and costs
print("Bcrypt $2$ hashes of empty string:")
print()

# Salt: all zeros
salt_zero = b'\x00' * 16
for cost in [4, 5, 6]:
    h = gen_hash(cost, salt_zero)
    print(f'Cost={cost}, zero salt: {h}')
    print(f'  root:{h}')
print()

# Salt: "JgiaOAai" as first 8 chars of salt + zeros
# "JgiaOAai" in bcrypt b64 decodes to 6 bytes
# Let's just use "JgiaOAai" + zeros for remaining 14 chars of the 22-char b64
# That means: decode "JgiaOAai" + "AA" = 8 chars = 6 bytes, then 10 more bytes of zeros
# Actually, let's just try: salt bytes = first 6 bytes from "JgiaOAai" + 10 zero bytes
rev = {}
for i, c in enumerate(BCRYPT_B64):
    rev[chr(c)] = i

jgia_bytes = bytes([
    (rev['J'] << 2) | (rev['g'] >> 4),
    ((rev['g'] & 0x0F) << 4) | (rev['i'] >> 2),
    ((rev['i'] & 0x03) << 6) | rev['a'],
    (rev['O'] << 2) | (rev['A'] >> 4),
    ((rev['A'] & 0x0F) << 4) | (rev['i'] >> 2),
    ((rev['i'] & 0x03) << 6) | rev['a'],
])
print(f'JgiaOAai decodes to {len(jgia_bytes)} bytes: {jgia_bytes.hex()}')

salt_jgia = jgia_bytes + b'\x00' * 10
for cost in [4, 5, 6]:
    h = gen_hash(cost, salt_jgia)
    print(f'Cost={cost}, JgiaOAai salt: {h}')
    print(f'  root:{h}')
