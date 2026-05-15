#!/usr/bin/env python3
import bcrypt

passwords = ['root', 'admin', 'password', '', 'toor', 'openwrt']

for pw in passwords:
    salt = b'$2b$04$01234567890123456789u'
    try:
        hash_b = bcrypt.hashpw(pw.encode() if pw else b'', salt)
        hash_2 = hash_b.decode().replace('$2b$', '$2$')
        label = pw if pw else '(empty)'
        print(f"{label}: root:{hash_2}")
    except Exception as e:
        print(f"{pw}: Error - {e}")