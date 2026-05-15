# Analyze the satellite hijack challenge
import re

data = open(r'C:\Users\click\Desktop\rev_satellitehijack\satellite', 'rb').read()

# Find the main function and input handling
# Look for format strings and input prompts

strings = re.findall(rb'[A-Za-z0-9_{}][A-Za-z0-9_{}!@#$%\*\(\)\[\]:;,.\/<>?|~` ]{3,}', data)
print("Strings related to input/output:")
for s in sorted(set(strings)):
    decoded = s.decode('utf-8', errors='replace')
    if any(x in decoded.lower() for x in ['ready', 'start', 'send', 'transmit', 'enter', 'input']):
        print(f'  {decoded}')

# Look for the check values - find hardcoded comparisons
print("\nLooking for 4-byte patterns that could be check values...")
# Check for array of 4-byte compares (like cmp eax, [addr])
for i in range(len(data) - 4):
    val = int.from_bytes(data[i:i+4], 'little')
    if 0x4854427b <= val <= 0x7d20736e:  # HTB{ to } sn
        print(f"  Potential flag byte at {i}: {data[i:i+4].hex()} -> {data[i:i+4]}")