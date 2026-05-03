"""
clean_downloads.py
Moves keepers out of Downloads to proper homes, then wipes what's left.
Run once. Review the log before confirming the wipe.
"""

import shutil
import os
from pathlib import Path

DOWNLOADS = Path(r"C:\Users\click\Downloads")
DOCS      = Path(r"C:\Users\click\Documents")
STREAM    = Path(r"D:\StreamContentPipeline")
VTUBER    = Path(r"D:\VTuber")

# Where keepers go
PDF_DEST    = DOCS / "PDFs"
STREAM_DEST = STREAM / "Assets"
VTUBER_DEST = VTUBER / "Source_PSDs"

moved = []
deleted = []
errors = []

def move(src, dest_dir):
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    if dest.exists():
        dest = dest_dir / ("_dup_" + src.name)
    try:
        shutil.move(str(src), str(dest))
        moved.append(f"MOVED: {src.name} -> {dest_dir}")
    except Exception as e:
        errors.append(f"ERROR moving {src.name}: {e}")

def delete(src):
    try:
        if src.is_dir():
            shutil.rmtree(src)
        else:
            src.unlink()
        deleted.append(f"DELETED: {src.name}")
    except Exception as e:
        errors.append(f"ERROR deleting {src.name}: {e}")

# --- PDFs -> Documents/PDFs ---
pdfs = [
    "Fusion9_Tool_Reference.pdf",
    "ENGLISH_START_AFILIADOS_2025.pdf",
    "ll-rulebook.pdf",
]

# --- Streaming assets -> D:\StreamContentPipeline\Assets ---
stream_assets = [
    "BorderBuddies_7of9_assets.zip",
    "border_buddies_frames_all.zip",
    "BB_clean_frames_selected.zip",
    "emotespics-20260224T152000Z-1-001.zip",
    "up_in_lights.rmskin",
    "Clickwell_pfp_animated-min.png",
    "vTuber Kit - Eye Outline spyxfamily.png",
    "vTuber Kit - Eye Outline spyxfamily(1).png",
]

# Well-Coin gifs
stream_assets += [f.name for f in DOWNLOADS.iterdir()
                  if not f.is_dir() and "Well-Coin" in f.name]

# --- PSD files -> D:\VTuber\Source_PSDs ---
psds = [f.name for f in DOWNLOADS.iterdir()
        if not f.is_dir() and f.suffix.lower() == ".psd"]

# --- Move keepers ---
for name in pdfs:
    f = DOWNLOADS / name
    if f.exists():
        move(f, PDF_DEST)

for name in stream_assets:
    f = DOWNLOADS / name
    if f.exists():
        move(f, STREAM_DEST)

for name in psds:
    f = DOWNLOADS / name
    if f.exists():
        move(f, VTUBER_DEST)

# --- Wipe everything remaining ---
for item in DOWNLOADS.iterdir():
    delete(item)

# --- Report ---
print("\n=== MOVES ===")
for line in moved:
    print(line)

print("\n=== DELETED ===")
for line in deleted:
    print(line)

if errors:
    print("\n=== ERRORS ===")
    for line in errors:
        print(line)

print(f"\nDone. {len(moved)} moved, {len(deleted)} deleted, {len(errors)} errors.")
