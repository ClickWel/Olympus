#!/usr/bin/env python3
"""
Bcrypt requires specific base64 alphabet: ./A-Za-z0-9
"""
import bcrypt
import string

# Valid bcrypt characters
valid_chars = './' + string.ascii_letters + string.digits

# Try generating with a valid salt format
salt = 'JgiaOAai1234567890ab'  # This should be 22 chars using valid chars only
# The issue is bcrypt expects the salt to be base64 encoded properly

# Let's just use a gensalt and see what format it produces
salt = bcrypt.gensalt(rounds=5)
print(f"Generated salt: {salt}")

# Now let's verify the hash of empty string
hash_result = bcrypt.hashpw(b'', salt)
print(f"Hash: {hash_result}")

# The $2$ prefix - let me check if there's a library that supports it
# Python bcrypt doesn't support $2$ directly

# Let me try using passlib with the $2$ prefix
try:
    from passlib.hash import bcrypt
    # Check if passlib supports $2$
    result = bcrypt.using(rounds=5, variant='original').hash('')
    print(f"Passlib $2$ hash: {result}")
except ImportError:
    print("passlib not installed")
except Exception as e:
    print(f"Passlib error: {e}")