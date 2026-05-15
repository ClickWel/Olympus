#!/usr/bin/env python3
from passlib.hash import bcrypt

# Check what variants are supported
print("Bcrypt variants:", bcrypt.variants if hasattr(bcrypt, 'variants') else "unknown")

# Try different approaches
try:
    # Standard
    result = bcrypt.using(rounds=5).hash("")
    print(f"Standard: {result}")
except Exception as e:
    print(f"Error: {e}")

# Check the salt format
salt = bcrypt.gen_salt(rounds=5)
print(f"Generated salt: {salt}")

# Manual construction for $2$ prefix
# The $2$ variant uses the same algorithm as $2a$ for ASCII passwords
# So converting $2a$ to $2$ should work for the hash verification

# Try with empty password
import bcrypt as py_bcrypt
hash_result = py_bcrypt.hashpw(b'', py_bcrypt.gensalt(rounds=5))
print(f"Py bcrypt hash: {hash_result}")
print(f"As $2$: {hash_result.decode().replace('$2b$', '$2$')}")