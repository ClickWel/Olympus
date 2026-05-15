#!/usr/bin/env python3
"""
Generate bcrypt $2$ format hash for empty password.
The $2$ prefix is the original buggy bcrypt format.
"""

# Since standard bcrypt doesn't support $2$ prefix directly,
# we need to find another approach.

# Approach 1: Check if there's a known test vector for $2$
# The hash $2$JgiaOAai.... in the example might be specific

# Approach 2: Try online or Linux tools
# Approach 3: The password might be something else entirely

# Let me try to construct manually based on bcrypt algorithm
# Or check if there's a specific way the challenge expects

import subprocess
import os

# Try using htpasswd if available
try:
    result = subprocess.run(['htpasswd', '-nbm', 'test', ''], capture_output=True, text=True)
    print(f"htpasswd result: {result.stdout} {result.stderr}")
except FileNotFoundError:
    print("htpasswd not available")

# Alternative: The empty hash in shadow might mean we need to provide
# the format as-is: root:::0:99999:7:::
# Let's try variations

test_answers = [
    "root:::0:99999:7:::",  # exact from shadow
    "root:::",               # minimal
    "root::0:99999:7:::",    # with day 0
    "root:x:0:0:root:/root:/bin/ash",  # passwd line
]

print("\nPossible answers to try:")
for ans in test_answers:
    print(f"  {ans}")

# The $p$ in rpcd might be a hint - let's investigate
# $p$root could mean "password is 'root' stored as plaintext"
# Or it could be a special format

# Let me check if $p$root is the actual answer format
print("\n$p$root from rpcd config:")
print("The rpcd config has option password '$p$root'")
print("This might be the expected format!")