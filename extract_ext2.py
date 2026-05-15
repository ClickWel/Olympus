#!/usr/bin/env python3
# Extract ext2 filesystem files by parsing raw filesystem
import struct
import os
import re

def parse_ext2_superblock(data):
    # EXT2 superblock is at offset 1024
    sb_offset = 1024
    # s_inodes_count (0), s_blocks_count (4), s_r_blocks_count (8), s_free_blocks_count (12)
    # s_free_inodes_count (16), s_first_data_block (20), s_log_block_size (24)
    # s_log_frag_size (28), s_blocks_per_group (32), s_frags_per_group (34), s_inodes_per_group (36)
    # s_mtime (40), s_wtime (44), s_mnt_count (46), s_max_mnt_count (48), s_magic (50)
    
    # Read magic at offset 1024 + 56 (s_magic) for ext2 rev 1.0
    magic_offset = 1024 + 56
    magic = struct.unpack('<H', data[magic_offset:magic_offset + 2])[0]
    print(f"Magic bytes at offset {magic_offset}: {hex(data[magic_offset])} {hex(data[magic_offset+1])}")
    if magic != 0xEF53:
        # Try alternate offset
        magic = struct.unpack('<H', data[1024 + 50:1024 + 52])[0]
        print(f"Trying alternate magic at offset {1024 + 50}: {hex(magic)}")
        if magic != 0xEF53:
            raise ValueError(f"Not an ext2 filesystem, magic: {hex(magic)}")
    
    blocks_count = struct.unpack('<I', data[sb_offset + 4:sb_offset + 8])[0]
    log_block_size = struct.unpack('<I', data[sb_offset + 24:sb_offset + 28])[0]
    block_size = 1024 << log_block_size
    blocks_per_group = struct.unpack('<H', data[sb_offset + 32:sb_offset + 34])[0]
    inodes_per_group = struct.unpack('<I', data[sb_offset + 36:sb_offset + 40])[0]
    first_data_block = struct.unpack('<I', data[sb_offset + 20:sb_offset + 24])[0]
    
    print(f"Magic: {hex(magic)}, Block size: {block_size}, Blocks: {blocks_count}")
    print(f"Blocks per group: {blocks_per_group}, Inodes per group: {inodes_per_group}")
    
    return block_size, blocks_count, blocks_per_group, inodes_per_group

def extract_files_from_ext2(img_path, output_dir):
    with open(img_path, 'rb') as f:
        data = f.read()
    
    block_size, blocks_count, blocks_per_group, inodes_per_group = parse_ext2_superblock(data)
    
    # Group descriptor follows superblock
    # Each group descriptor is 32 bytes
    # gd_bg_block_bitmap (0), gd_bg_inode_bitmap (4), gd_bg_inode_table (8)
    # gd_bg_free_blocks_count (12), gd_bg_free_inodes_count (14), gd_bg_used_dirs_count (16)
    
    # Try reading some known paths
    # Let's look for common web app directories
    print("Searching for files...")
    
    # For now, let's just dump raw blocks that look like text
    os.makedirs(output_dir, exist_ok=True)
    
    # Dump the filesystem content around known text blocks
    print("\n--- Extracting key files ---")
    
    # Get content around /var/www
    www_offset = data.find(b'/var/www')
    if www_offset >= 0:
        context_start = max(0, www_offset - 200)
        context_end = min(len(data), www_offset + 500)
        print(f"\nContext around /var/www:")
        print(data[context_start:context_end].decode('utf-8', errors='replace'))
    
    # Get content around HTML
    html_offset = data.find(b'<!DOCTYPE html')
    if html_offset >= 0:
        print(f"\n--- HTML Content (block 4899) ---")
        # Find the extent boundaries
        block_num = html_offset // block_size
        block_start = block_num * block_size
        block_end = min(len(data), (block_num + 20) * block_size)
        content = data[block_start:block_end]
        print(content.decode('utf-8', errors='replace'))
    
    # Try to find typical web paths
    search_patterns = [b'<!DOCTYPE html', b'<html', b'<?xml', b'HTB{', b'flag', b'/var/www', b'cgi-bin']
    for pattern in search_patterns:
        pos = data.find(pattern)
        if pos >= 0:
            print(f"Found '{pattern.decode()}' at offset {pos} (block {pos // block_size})")
    
    # Extract flag if found
    flag_start = data.find(b'HTB{')
    if flag_start >= 0:
        # Find the end of the flag
        flag_end = data.find(b'}', flag_start) + 1
        flag = data[flag_start:flag_end].decode()
        print(f"POTENTIAL FLAG: {flag}")
    
    # Found the real flags (64 char hex after HTB{)
    flags = re.findall(rb'HTB\{[a-f0-9]{64}\}', data)
    for f in flags:
        print(f"REAL FLAG CANDIDATE: {f.decode()}")
    
    # Dump XML config (block 5401)
    print("\n--- XML Config (block 5401) ---")
    xml_offset = data.find(b'<?xml')
    if xml_offset >= 0:
        print(data[xml_offset:xml_offset+2000].decode('utf-8', errors='replace'))
    
    # Look for server binary or CGI scripts
    print("\n--- Searching for server binaries ---")
    elf_magic = b'\x7fELF'
    elf_offsets = []
    pos = 0
    while True:
        pos = data.find(elf_magic, pos)
        if pos < 0:
            break
        elf_offsets.append(pos)
        pos += 1
    print(f"Found {len(elf_offsets)} ELF binaries")
    for eo in elf_offsets[:5]:
        print(f"  ELF at offset {eo} (block {eo // block_size})")
    
    # Look for dev_mode, debug config
    print("\n--- Searching for dev_mode, debug config ---")
    search_patterns = [b'devMode', b'dev_mode', b'debug', b'DEBUG', b'enable',\
                       b'devmode', b'devModeEnabled', b'IsDevMode']
    for pattern in search_patterns:
        pos = 0
        count = 0
        while count < 3:
            pos = data.find(pattern, pos)
            if pos < 0:
                break
            context = data[max(0,pos-50):pos+100].decode('utf-8', errors='replace')
            if context.strip():
                print(f"Found '{pattern.decode()}' at offset {pos}:")
                print(f"  Context: {context[:120]}")
            pos += 1
            count += 1
    
    # Look for config files
    print("\n--- Looking for config files ---")
    config_patterns = [b'app.config', b'server.config', b'web.config', b'settings.json', b'.env']
    for pattern in config_patterns:
        pos = data.find(pattern)
        if pos >= 0:
            print(f"Found '{pattern.decode()}' at offset {pos}")

if __name__ == '__main__':
    extract_files_from_ext2('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'D:/CTF/challenges/router-web/extracted')