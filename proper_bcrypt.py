#!/usr/bin/env python3
"""
The $2$ bcrypt format is the ORIGINAL buggy bcrypt implementation.
It differs from $2a$ in how it handles non-ASCII characters.
For ASCII-only passwords (including empty string), $2$ and $2a$ should produce
the same hash, but the prefix is different.

Since OpenWrt might use a specific implementation, let me try:
1. Using the exact format expected
2. The password might be something specific to generate the example hash
"""
import hashlib
import base64
import struct

def bcrypt_hash(password, salt, prefix='$2b$'):
    """
    Manual bcrypt for reference - too complex to implement fully.
    Use the bcrypt library and convert.
    """
    import bcrypt
    # Generate with the library
    hash_result = bcrypt.hashpw(password.encode(), salt.encode() if isinstance(salt, str) else salt)

    # Convert prefix
    if isinstance(hash_result, bytes):
        hash_result = hash_result.decode()

    # Convert $2b$ to $2$
    hash_2 = hash_result.replace('$2b$', '$2$').replace('$2a$', '$2$')
    return hash_2

# Try with empty password and various salts
import bcrypt

# Generate hash with fixed salt to see if we can match the example
# Example from prompt: root:$2$JgiaOAai....
# Let's try different rounds

for rounds in [4, 5, 6, 7, 8]:
    # Try to get exact format
    salt = bcrypt.gensalt(rounds=rounds)
    hash_result = bcrypt.hashpw(b'', salt)
    hash_2 = hash_result.decode().replace('$2b$', '$2$')
    print(f"Rounds {rounds}: {hash_2}")

print("\nNow trying with specific bcrypt parameters to match format...")

# The example hash has specific length - bcrypt hashes are always 60 chars
# $2$ + 22 char salt + $ + 31 char hash
# root:$2$JgiaOAai.... would be: $2$ + 22 chars + $ + 31 chars = 55 chars total
# Actually let me count: $2$ + 22 + $ + 31 = 56 chars after root:
# Format: root:$2$salt$hash

print("\nGenerating with controlled salt:")
# Try with known salt
test_salt = '$2b$05$X5X.5L6W2TyQfbIVJrK6.'  # Fixed salt from earlier
hash_result = bcrypt.hashpw(b'', test_salt.encode())
print(f"With test salt: {hash_result.decode()}")
hash_2 = hash_result.decode().replace('$2b$', '$2$')
print(f"As $2$: {hash_2}")