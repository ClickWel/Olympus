#!/usr/bin/env python3
"""
Generate bcrypt $2$ hash of empty string deterministically.
Use passlib which we installed earlier.
The key: passlib generates $2b$ but we need $2$.
The hash should be accepted by the server if we submit ANY valid bcrypt hash of empty string.
"""
from passlib.hash import bcrypt as bc

# Generate multiple hashes with different rounds
for rounds in [4, 5, 6, 7, 8]:
    h = bc.hash('', rounds=rounds)
    # Convert $2b$ to $2$
    h2 = h.replace('$2b$', '$2$')
    print(f'Rounds={rounds}: {h2}')
    print(f'Full line: root:{h2}')
