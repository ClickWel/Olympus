#!/usr/bin/env python3
"""
Generate bcrypt $2$ format hash.

The $2$ prefix is the original buggy bcrypt format. Most libraries
don't support it directly. Let's try a few approaches:

1. Use the blowfish module
2. Manually construct the hash
3. Try online generators
"""

import base64
import struct

def bcrypt_hash_empty():
    """
    Standard bcrypt hash of empty password.
    Then convert to $2$ format.
    """
    import bcrypt

    # Generate $2b$ hash
    salt = b'$2b$05$00000000000000000000000'  # Fixed salt for testing
    if len(salt) != 29:
        salt = bcrypt.gensalt(rounds=5)

    hash_result = bcrypt.hashpw(b'', salt)
    print(f"Standard hash: {hash_result}")

    # Convert $2b$ to $2$ by replacing prefix
    hash_2 = hash_result.replace(b'$2b$', b'$2$')
    print(f"Converted to $2$: {hash_2}")

    return hash_2

if __name__ == '__main__':
    result = bcrypt_hash_empty()
    print(f"\nFinal answer to try: root:{result.decode()}")