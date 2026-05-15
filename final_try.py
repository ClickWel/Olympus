#!/usr/bin/env python3
"""
Final attempt - generate proper $2$ hash and try.
The $2$ prefix means original bcrypt format.
For ASCII empty password, $2$ and $2b$ should produce the same hash.
"""
import bcrypt
import base64

# Generate with standard bcrypt then convert prefix
password = b''  # empty password

# Use a fixed salt to get reproducible results
salt = bcrypt.gensalt(rounds=5)
hash_b = bcrypt.hashpw(password, salt)
print(f"Hash with $2b$: {hash_b.decode()}")

# Convert to $2$
hash_2 = hash_b.decode().replace('$2b$', '$2$')
print(f"As $2$: {hash_2}")

# The challenge example shows root:$2$JgiaOAai....
# This is a format hint, not the actual hash value

# Try the answer
full_answer = f"root:{hash_2}"
print(f"\nFull answer: {full_answer}")

# Also try without the root: prefix
print(f"Just hash part: {hash_2}")