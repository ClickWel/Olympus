#!/usr/bin/env python3
import bcrypt

passwords = ['root', 'admin', 'password', '', 'toor', 'openwrt']

for pw in passwords:
    salt = bcrypt.gensalt(rounds=4)
    hash_b = bcrypt.hashpw(pw.encode() if pw else b'', salt)
    hash_2 = hash_b.decode().replace('$2b$', '$2$')
    print(f"root:{hash_2}")