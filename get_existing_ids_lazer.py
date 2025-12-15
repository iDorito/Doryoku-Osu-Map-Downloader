#!/usr/bin/env python
"""\
Helper module to find osu beatmapset ids inside folders for lazer.
"""

import os
import json
import config
from pathlib import Path

# MAIN PATHS - directamente desde config (ya son Path objects)
LASER_FILES_PATH = config.LASER_FILES_PATH
DOWNLOAD_PATH = config.DOWNLOAD_PATH
DB_JSON_DIR = config.DB_JSON          # Esto es la carpeta: .../domd/
JSON_FILE_PATH = DB_JSON_DIR / "db.json"   # Ruta completa al archivo

# === CREAR CARPETAS SI NO EXISTEN ===
# Usamos los métodos de pathlib directamente (más seguro y claro)

DOWNLOAD_PATH.mkdir(parents=True, exist_ok=True)
LASER_FILES_PATH.mkdir(parents=True, exist_ok=True)
DB_JSON_DIR.mkdir(parents=True, exist_ok=True)   # Crea la carpeta domd

print(f"Carpeta downloads: {DOWNLOAD_PATH}")
print(f"Carpeta lazer files: {LASER_FILES_PATH}")
print(f"Carpeta DB: {DB_JSON_DIR}")
print(f"Archivo JSON será: {JSON_FILE_PATH}")

# === CREAR ARCHIVO JSON SI NO EXISTE ===
if not JSON_FILE_PATH.exists():
    print("Creando nuevo db.json vacío...")
    JSON_FILE_PATH.write_text(json.dumps({"downloaded_maps": []}, indent=4), encoding='utf-8')
else:
    print("db.json ya existe.")

# === TUS FUNCIONES (sin cambios) ===
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
            f.readline()  # Skip first line
            for line in f:
                if line.startswith('BeatmapSetID:'):
                    try:
                        return int(line.split(':', 1)[1].strip())
                    except ValueError:
                        return None
                if line.startswith('[HitObjects]'):
                    break
    except Exception:
        return None
    return None

def lazer_beatmapsets_ids_scan():
    print(f"Escaneando: {LASER_FILES_PATH}")
    print("Esto puede tardar dependiendo de cuántos mapas tengas...")

    found_id_sets = set()
    revised_files = 0
    maps_found = 0

    if not LASER_FILES_PATH.exists():
        print("Error: La carpeta de osu!lazer no existe. ¿Tienes osu!lazer instalado?")
        return []

    for root, dirs, files in os.walk(LASER_FILES_PATH):
        for filename in files:
            full_path = Path(root) / filename
            revised_files += 1

            if not is_osu_file(full_path):
                continue

            maps_found += 1
            beatmapset_id = extract_beatmapset_id(full_path)
            if beatmapset_id is not None and beatmapset_id != -1:  # -1 es común en mapas locales
                found_id_sets.add(beatmapset_id)

    print("\n--- RESUMEN ---")
    print(f"Archivos escaneados: {revised_files}")
    print(f"Archivos .osu detectados: {maps_found}")
    print(f"Sets únicos encontrados: {len(found_id_sets)}")

    return sorted(found_id_sets)

# === EJECUCIÓN PRINCIPAL ===
if __name__ == "__main__":
    ids_encontrados = lazer_beatmapsets_ids_scan()

    resultado = {"downloaded_maps": ids_encontrados}

    # Guardar en el JSON
    with open(JSON_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4)

    print(f"\n¡Listo! IDs guardados en:")
    print(f"   {JSON_FILE_PATH}")
    print(f"   Total de sets únicos: {len(ids_encontrados)}")
    if ids_encontrados:
        print(f"   Primeros 20: {ids_encontrados[:20]}")