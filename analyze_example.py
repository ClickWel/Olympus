#!/usr/bin/env python3
"""
Analyze the example from the challenge: root:$2$JgiaOAai....

The salt in bcrypt is 22 characters. JgiaOAai is only 8 characters of salt.
This means the example is truncated - JgiaOAai1234567890ab would be a full salt.

Let me try to find if there's a pattern or if I need to use a specific salt.
"""
import bcrypt

# The JgiaOAai part could match a specific salt pattern
# Let me try to construct a URL-safe base64 salt that starts with JgiaOAai

# URL-safe base64 uses: A-Za-z0-9 (no +/ or =)
# JgiaOAai -> need 14 more chars

possible_salts = [
    'JgiaOAai1234567890ab',  # Extend with numbers and lowercase
    'JgiaOAaiABCDEFGHIJKLb',  # Extend with uppercase
    'JgiaOAai0123456789ab',   # Mix
]

for salt_base in possible_salts:
    # Try to use this as salt
    try:
        # Build proper 29-char salt string
        full_salt = f'$2b$05${salt_base}'
        # Check if it's valid base64
        import base64
        decoded = base64.urlsafe_b64decode(salt_base + '==')  # Pad
        print(f'Salt {salt_base} decodes to {len(decoded)} bytes')
    except Exception as e:
        print(f'Error with {salt_base}: {e}')

# Also try the password 'root' with various formats
passwords = ['root', '', 'admin', 'password']
for pw in passwords:
    for rounds in [5, 10, 12]:
        salt = bcrypt.gensalt(rounds=rounds)
        h = bcrypt.hashpw(pw.encode() if pw else b'', salt)
        h2 = h.decode().replace('$2b$', '$2$')
        # Print only if it starts with JgiaOAai-like pattern
        if h2.startswith('$2$05$Jgia') or h2.startswith('$2$12$Jgia'):
            print(f'Close match: {h2}')