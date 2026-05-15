#!/usr/bin/env python3
"""
The $2$ prefix is the ORIGINAL buggy bcrypt format from OpenBSD.
For ASCII passwords like empty string, $2$ and $2a$ produce identical hashes.

The difference is in how non-ASCII characters are handled:
- $2$ (original): buggy handling of non-ASCII
- $2a$: fixed handling

For empty password, we can use $2a$ and just change the prefix.

Let me also check if there's any way to get the exact bcrypt hash that the challenge expects.
Maybe the answer relies on a specific salt being used.
"""
import bcrypt

# Empty password - the shadow file shows root::: which means empty password field
# In OpenWrt, this means the account has NO password set (passwordless login)
# But the challenge asks for a hash - so maybe they want the bcrypt hash of empty string

password = b''

# Try with different rounds
for rounds in [4, 5, 6, 7, 8, 9, 10]:
    salt = bcrypt.gensalt(rounds=rounds)
    hash_result = bcrypt.hashpw(password, salt)
    # Convert to $2$ prefix
    hash_2 = hash_result.decode().replace('$2b$', '$2$')
    print(f"root:{hash_2}")