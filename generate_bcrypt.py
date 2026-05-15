import bcrypt
import hashlib

# Try generating $2$ hashes
# Note: bcrypt typically uses $2a$, $2b$, but we need $2$ (original format)

# First, let's see what we get with standard bcrypt of empty password
empty_pw = b""
salt = bcrypt.gensalt(rounds=5)  # Lower rounds for match
print(f"Standard salt: {salt}")

# Try to force $2$ prefix
# In bcrypt, $2$ is the original format but rarely used
# Let's manually construct or find a method

# bcrypt.hashpw with prefix
try:
    # Standard approach - this will give us $2b$
    hash_result = bcrypt.hashpw(empty_pw, bcrypt.gensalt())
    print(f"Standard output: {hash_result}")
except Exception as e:
    print(f"Error: {e}")

# Try using passlib which might support $2$
try:
    from passlib.hash import bcrypt as passlib_bcrypt
    result = passlib_bcrypt.using(rounds=5).hash("")
    print(f"Passlib result: {result}")
except ImportError:
    print("passlib not available")
except Exception as e:
    print(f"Passlib error: {e}")

# Manual construction attempt
# $2$ format: 22-char salt, 31-char hash
# Let's try to find if there's a specific method

print("\nTrying different approaches...")

# Try with openssl or other crypto
import base64
import struct

# bcrypt uses a specific format based on Blowfish
# The $2$ prefix is very rare - it had a bug that was fixed in $2a$