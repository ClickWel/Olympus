#!/usr/bin/env python3
"""
Try password as 'root' (from rpcd config where it says $p$root)
"""
import bcrypt

password = b'root'
salt = bcrypt.gensalt(rounds=4)
hash_b = bcrypt.hashpw(password, salt)
hash_2 = hash_b.decode().replace('$2b$', '$2$')

print(f'Password: root')
print(f'Hash: {hash_2}')
print(f'Full answer: root:{hash_2}')