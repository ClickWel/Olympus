#!/usr/bin/env python3
"""
Try various passwords with bcrypt $2$ format.
"""
import bcrypt

passwords = [
    '',           # empty
    'root',       # root
    'admin',      # admin
    'password',   # password
    'openwrt',    # openwrt
    '123456',     # common
    'toor',       # toor
]

print("Testing various passwords with bcrypt $2$ format:")
for pw in passwords:
    salt = bcrypt.gensalt(rounds=5)
    hash_result = bcrypt.hashpw(pw.encode(), salt)
    hash_2 = hash_result.decode().replace('$2b$', '$2$')
    print(f"{pw or '(empty)'}: {hash_2}")