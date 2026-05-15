#!/usr/bin/env python3
"""
Pure Python implementation of original bcrypt $2$ format.
Based on OpenBSD bcrypt specification.
"""
import struct

# Blowfish S-boxes (standard initial values)
S_ORIG = [
    0xd1310ba6, 0x98dfb5ac, 0x2ffd72db, 0xd01adfb7, 0xb8e1afed, 0x6a267e96,
    0xba7c9045, 0xf12c7f99, 0x24a19947, 0xb3916cf7, 0x0801f2e2, 0x858efc16,
    0x636920d8, 0x71574e69, 0xa458fea3, 0xf4933d7e, 0x0d95748f, 0x728eb658,
    0x718bcd58, 0x82154aee, 0x7b54a41d, 0xc25a59b5, 0x9c30d539, 0x2af26013,
    0xc5d1b023, 0x286085f0, 0xca417918, 0xb8db38ef, 0x8e79dcb0, 0x603a180e,
    0x6c9e0e8b, 0xb01e8a3e, 0xd71577c1, 0xbd314b27, 0x78af2fda, 0x55605c60,
    0xe65525f3, 0xaa55ab94, 0x57489862, 0x63e81440, 0x55ca396a, 0x2aab10b6,
    0xb4cc5c34, 0x1141e8ce, 0xa15486af, 0x7c72e993, 0xb3ee1411, 0x636fbc2a,
    0x2ba9c55d, 0x741831f6, 0xce5c3e16, 0x9b87931e, 0xafd6ba33, 0x6c24cf5c,
    0x7a325381, 0x28958677, 0x3b8f4898, 0x6b4bb9af, 0xc4bfe81b, 0x66282193,
    0x61d809cc, 0xfb21a991, 0x487cac60, 0x5dec8032, 0xef845d5d, 0xe98575b1,
    0xdc262302, 0xeb651b88, 0x23893e81, 0xd396acc5, 0x0f6d6ff3, 0x83f44239,
    0x2e0b4482, 0xa4842004, 0x69c8f04a, 0x9e1f9b5e, 0x21c66842, 0xf6e96c9a,
    0x670c9c61, 0xabd388f0, 0x6a51a0d2, 0xd8542f68, 0x960fa728, 0xab5133a3,
    0x6eef0b6c, 0x137a3be4, 0xba3bf050, 0x7efb2a98, 0xa1f1651d, 0x39af0176,
    0x66ca593e, 0x82430e88, 0x8cee8619, 0x456f9fb4, 0x7d84a5c3, 0x3b8b5ebe,
    0xe06f75d8, 0x85c12073, 0x401a449f, 0x56c16aa6, 0x4ed3aa62, 0x363f7706,
    0x1bfedf72, 0x429b023d, 0x37d0d724, 0xd00a1248, 0xdb0fead3, 0x49f1c09b,
    0x075372c9, 0x80991b7b, 0x25d479d8, 0xf6e8def7, 0xe3fe501a, 0xb6794c3b,
    0x976ce0bd, 0x04c006ba, 0xc1a94fb6, 0x409f60c4, 0x5e5c9ec2, 0x196a2463,
    0x68fb6faf, 0x3e6c53b5, 0x1339b2eb, 0x3b52ec6f, 0x6dfc511f, 0x9b30952c,
    0xcc814544, 0xaf5ebd09, 0xbee3d004, 0xde334afd, 0x660f2807, 0x192e4bb3,
    0xc0cba857, 0x45c8740f, 0xd20b5f39, 0xb9d3fbdb, 0x5579c0bd, 0x1a60320a,
    0xd6a100c6, 0x402c7279, 0x679f25fe, 0xfb1fa3cc, 0x8ea5e9f8, 0xdb3222f8,
    0x3c7516df, 0xfd616b15, 0x2f501ec8, 0xad0552ab, 0x323db5fa, 0xfd238760,
    0x53317b48, 0x3e00df82, 0x9e5c57bb, 0x6f2fec10, 0x6e72162f, 0x0a18f08a,
    0xe2eb78e1, 0xdc4970fa, 0x3b05d3c2, 0x806c27c6, 0xf147ba1d, 0x2c93546c,
    0x65e01cc2, 0x3de97b2a, 0x69c95d35, 0x462e41bf, 0x19f69f26, 0xae888ec2,
    0x8a9c0bef, 0xba225e8a, 0x4e24b03a, 0x0ba7e4dd, 0xc1b1a6e4, 0x3b09abce,
    0xf796cec0, 0x4de0b68e, 0x52f17e38, 0x49eac5fc, 0xbbceeeee, 0x3fdc7e9b,
    0x5c451e20, 0xc35b48b5, 0x4d8c8c27, 0x47a0c842, 0x68c124b7, 0x1e15e9c2,
    0x42c7c4e4, 0xcc5e48f6, 0x659d60dc, 0xb67298fd, 0x6c782c41, 0x7b3fab45,
]

# P-array (initial)
P_ORIG = [
    0x243f6a88, 0x85a308d3, 0x13198a2e, 0x03707344, 0xa4093822, 0x299f31d0,
    0x082efa98, 0xec4e6c89, 0x452821e6, 0x38d01377, 0xbe5466cf, 0x34e90c6c,
    0xc0ac29b7, 0xc97c50dd, 0x3f84d5b5, 0xb5470917, 0x9216d5d9, 0x8979fb1b,
]

BCRYPT_CTEXT = b'OrpheanBeholderScryDoubt'

BCRYPT_BASE64 = "./ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

def bcrypt_base64_encode(data):
    result = []
    for i in range(0, len(data), 3):
        if i + 2 < len(data):
            b1, b2, b3 = data[i], data[i+1], data[i+2]
            result.append(BCRYPT_BASE64[b1 >> 2])
            result.append(BCRYPT_BASE64[((b1 & 0x03) << 4) | (b2 >> 4)])
            result.append(BCRYPT_BASE64[((b2 & 0x0F) << 2) | (b3 >> 6)])
            result.append(BCRYPT_BASE64[b3 & 0x3F])
        elif i + 1 < len(data):
            b1, b2 = data[i], data[i+1]
            result.append(BCRYPT_BASE64[b1 >> 2])
            result.append(BCRYPT_BASE64[((b1 & 0x03) << 4) | (b2 >> 4)])
            result.append(BCRYPT_BASE64[(b2 & 0x0F) << 2])
        else:
            b1 = data[i]
            result.append(BCRYPT_BASE64[b1 >> 2])
            result.append(BCRYPT_BASE64[(b1 & 0x03) << 4])
    return ''.join(result)

def blowfish_f(P, S, x):
    return ((S[0][x >> 24] + S[1][(x >> 16) & 0xFF]) & 0xFFFFFFFF) ^ S[2][(x >> 8) & 0xFF] + S[3][x & 0xFF]

def blowfish_encipher(P, S, xl, xr):
    for i in range(0, 16, 2):
        xl ^= P[i]
        xr ^= blowfish_f(P, S, xl)
        xr ^= P[i+1]
        xl ^= blowfish_f(P, S, xr)
    return xr ^ P[17], xl ^ P[16]

def bcrypt_hash(password, salt, cost):
    P = list(P_ORIG)
    S = [list(S_ORIG[i*64:(i+1)*64]) for i in range(4)]

    key_len = len(password)
    for i in range(18):
        data = 0
        for j in range(4):
            data = (data << 8) | password[i * 4 + j % key_len]
        P[i] ^= data

    salt_len = len(salt)

    def get_block(p, idx):
        idx = idx % salt_len
        return salt[idx]

    xl, xr = 0, 0
    for i in range(0, 18, 2):
        xl = 0
        for j in range(4):
            xl = (xl << 8) | get_block(salt, i * 4 + j)
        xr = 0
        for j in range(4):
            xr = (xr << 8) | get_block(salt, i * 4 + j + 4)
        xl ^= xl
        xr ^= xr
        xl, xr = blowfish_encipher(P, S, xl, xr)
        P[i] = xl
        P[i+1] = xr

    for i in range(4):
        for j in range(0, 256, 2):
            xl = 0
            for k in range(4):
                xl = (xl << 8) | get_block(salt, (i * 256 + j) * 4 + k)
            xr = 0
            for k in range(4):
                xr = (xr << 8) | get_block(salt, (i * 256 + j + 1) * 4 + k)
            xl, xr = blowfish_encipher(P, S, xl, xr)
            S[i][j] = xl
            S[i][j+1] = xr

    # Re-key with salt first, then password
    # Standard bcrypt: expand key with (key, salt), then expand key with (salt, key)

    # Now hash the ctext
    ctext = BCRYPT_CTEXT
    blocks = []
    for i in range(0, len(ctext), 8):
        xl = int.from_bytes(ctext[i:i+4], 'big')
        xr = int.from_bytes(ctext[i+4:i+8], 'big')
        blocks.append([xl, xr])

    for _ in range(1 << cost):
        for j in range(len(blocks)):
            blocks[j][0], blocks[j][1] = blowfish_encipher(P, S, blocks[j][0], blocks[j][1])

    result = b''
    for xl, xr in blocks:
        result += xl.to_bytes(4, 'big') + xr.to_bytes(4, 'big')
    return result

def bcrypt(password, cost, salt):
    if isinstance(password, str):
        password = password.encode('utf-8')
    password = password + b'\x00'

    raw_hash = bcrypt_hash(password, salt, cost)
    salt_b64 = bcrypt_base64_encode(salt)
    hash_b64 = bcrypt_base64_encode(raw_hash)
    return f'$2{chr(36)}{cost:02d}${salt_b64}{hash_b64[:31]}'

if __name__ == '__main__':
    password = b''
    cost = 4
    salt = b'\x00' * 16
    result = bcrypt(password, cost, salt)
    print(f'Result: {result}')
