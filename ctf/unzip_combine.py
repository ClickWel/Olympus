import zipfile, os, re

parts_dir = 'D:/Olympus/ctf/parts'
output_dir = 'D:/Olympus/ctf/output'
os.makedirs(output_dir, exist_ok=True)

# Read passwords
passwords = {}
with open(os.path.join(parts_dir, 'passwords.txt')) as f:
    for line in f:
        if ':' in line:
            fname, pw = line.strip().split(': ')
            passwords[fname] = pw

# Unzip all parts
pdf_parts = {}
for fname, pw in passwords.items():
    zip_path = os.path.join(parts_dir, fname)
    try:
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(output_dir, pwd=pw.encode())
            for f in z.namelist():
                match = re.search(r'part(\d+)', f)
                if match:
                    part_num = int(match.group(1))
                    src = os.path.join(output_dir, f)
                    pdf_parts[part_num] = src
                    print(f"Extracted {f} -> part {part_num}")
    except Exception as e:
        print(f"Failed to extract {fname}: {e}")

# Sort parts by number and combine
print(f"\nFound {len(pdf_parts)} PDF parts")
if pdf_parts:
    sorted_parts = sorted(pdf_parts.items())
    combined_path = os.path.join(output_dir, 'phreaks_plan.pdf')
    with open(combined_path, 'wb') as outf:
        for part_num, part_path in sorted_parts:
            with open(part_path, 'rb') as inf:
                outf.write(inf.read())
            print(f"Added part {part_num}")
    print(f"\nCombined PDF saved to {combined_path}")
    print(f"Total size: {os.path.getsize(combined_path)} bytes")
else:
    print("No PDF parts found")
