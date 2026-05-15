import re

firmware_path = r"C:\Users\click\Desktop\forensics_silicon_data_sleuthing (1)\chal_router_dump.bin"
output_squashfs = r"D:\Olympus\squashfs.img"

with open(firmware_path, "rb") as f:
    data = f.read()

# Find SquashFS magic: 'hsqs' (0x68 0x73 0x71 0x73)
magic = b'hsqs'
offset = data.find(magic)
if offset == -1:
    # Try big endian
    magic = b'sqsh'
    offset = data.find(magic)
if offset == -1:
    print("SquashFS magic not found!")
    exit(1)

print(f"SquashFS found at offset 0x{offset:x} ({offset})")

# Extract from this offset to end (or known size)
# SquashFS size: let's take up to next partition or end of firmware
# Firmware is 16MB, so max size is 16MB - offset
squashfs_data = data[offset:]
print(f"Extracted SquashFS size: {len(squashfs_data)} bytes")

with open(output_squashfs, "wb") as f:
    f.write(squashfs_data)

print(f"SquashFS saved to {output_squashfs}")