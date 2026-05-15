# Try XOR decoding on the suspicious strings from library.so
data = open(r'C:\Users\click\Desktop\rev_satellitehijack\library.so', 'rb').read()

# The suspicious strings we found
strings_to_decode = ['FOWJSPOH', 'QSPEH', 'SPONFOU', 'VfRb', 'b~hQ_', 'qwkvkwkt', 'qwkvkwktku', 'qwkvkwktkut']

def xor_decode(s, key):
    result = ''
    for i, c in enumerate(s):
        result += chr(ord(c) ^ key[i % len(key)])
    return result

# Try common XOR keys
keys = [b'satellite', b'SATELLITE', b'control', b'CONTROL', b'HTB{', b'flag', b'pass', b'key', b'backdoor', b'hack']

for s in strings_to_decode:
    print(f"\n{s}:")
    # Try single byte XOR
    for key in range(256):
        decoded = xor_decode(s, bytes([key] * len(s)))
        if all(32 <= ord(c) < 127 for c in decoded):
            if 'HTB' in decoded or 'flag' in decoded.lower() or 'control' in decoded.lower() or 'sat' in decoded.lower():
                print(f'  XOR {key}: {decoded}')
    # Try word keys
    for key in keys:
        decoded = xor_decode(s, key)
        if all(32 <= ord(c) < 127 for c in decoded):
            if 'HTB' in decoded or 'flag' in decoded.lower():
                print(f'  XOR {key.decode()}: {decoded}')