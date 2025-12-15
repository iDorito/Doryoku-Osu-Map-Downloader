#!/usr/bin/env python # 
"""\
Helper module to find osu beatmapset ids inside folders for lazer.

By: Ricardo Faria
Osu User: Doryoku

Usage: run the script in cmd/terminal: python get_existing_ids_lazer.py
"""
import os
import json
import config
import sys

# --- FILES PATHS---
if sys.platform.startswith("win"):
    LASER_FILES_PATH = os.path.join(os.environ.get("APPDATA", ""), "osu", "files")
elif sys.platform.startswith("darwin"):
    LASER_FILES_PATH = os.path.expanduser("~/Library/Application Support/osu/files")
elif sys.platform.startswith("linux"):
    LASER_FILES_PATH = os.path.expanduser("~/.local/share/osu/files")
elif sys.platform.startswith("android"):
    LASER_FILES_PATH = "/storage/emulated/0/Android/data/sh.ppy.osulazer/files"
else:
    LASER_FILES_PATH = ""

# JSON FILE
JSON_FILE = open(config.DB_JSON_PATH)

if not os.path.exists(config.DB_JSON_PATH):
    with open(config.DB_JSON_PATH, "w") as f:
        json.dump({}, f)


def is_osu_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            first_line = f.readline()
            return first_line.startswith('osu file format')
    except Exception:
        return False

def extract_beatmapset_id(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            f.readline()  # Skip the first line, already checked
            for line in f:
                if line.startswith('BeatmapSetID:'):
                    parts = line.split(':')
                    if len(parts) > 1:
                        try:
                            return int(parts[1].strip())
                        except ValueError:
                            return None
                    break
                if line.startswith('[HitObjects]'):
                    break
    except Exception:
        return None
    return None

def lazer_beatmapsets_ids_scan():
    print(f"Scanning path: {LASER_FILES_PATH}")
    print("This can take a while depending on how many maps you have...")

    found_id_sets = set()
    revised_files = 0
    maps_found = 0

    for root, dirs, files in os.walk(LASER_FILES_PATH):
        for filename in files:
            full_path = os.path.join(root, filename)
            revised_files += 1

            if not is_osu_file(full_path):
                continue

            maps_found += 1
            beatmapset_id = extract_beatmapset_id(full_path)
            if beatmapset_id is not None:
                found_id_sets.add(beatmapset_id)

    print("\n--- RESUME ---")
    print(f"Scanned files: {revised_files}")
    print(f"Files detected of .osu extension: {maps_found}")
    print(f"Unique sets found: {len(found_id_sets)}")

    return list(found_id_sets)

# --- USO ---
if __name__ == "__main__":
    if os.path.exists(LASER_FILES_PATH):
        mis_ids = lazer_beatmapsets_ids_scan()
        print(f"IDs: {mis_ids[:20]} ... (y mas)")
        
        # Opcional: Guardarlos en un txt para no escanear siempre
        with open("db.json", "w") as f:
            json.dump({"downloaded_maps": mis_ids}, f, indent=4)
    else:
        print("Error: Osu!Lazer files folder wasn't found")