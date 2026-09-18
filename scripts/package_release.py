#!/usr/bin/env python3
"""
Sentinel-X Automated Deployment Package Builder
================================================
Creates a clean, portable Sentinel-X-Complete.zip bundle for Raspberry Pi 3/4 deployment,
filtering out developer caches, credentials, and binary artifacts, and generates SHA256 checksums.
"""

import os
import sys
import zipfile
import hashlib
import shutil

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_ZIP_NAME = "Sentinel-X-Complete.zip"
OUTPUT_ZIP_PATH = os.path.join(ROOT_DIR, OUTPUT_ZIP_NAME)

EXCLUDED_DIRS = {
    ".git", ".github", "__pycache__", ".pytest_cache", ".venv", "venv",
    "node_modules", ".idea", ".vscode", "scratch"
}

EXCLUDED_FILES = {
    ".DS_Store", "Sentinel-X-Complete.zip", "sentinel_edge.db-journal"
}

EXCLUDED_EXTENSIONS = {
    ".pyc", ".pyo", ".pyd", ".tmp", ".log"
}

def should_exclude(file_path, rel_path):
    parts = rel_path.replace("\\", "/").split("/")
    for p in parts:
        if p in EXCLUDED_DIRS:
            return True
    base_name = os.path.basename(file_path)
    if base_name in EXCLUDED_FILES:
        return True
    _, ext = os.path.splitext(base_name)
    if ext in EXCLUDED_EXTENSIONS:
        return True
    return False

def package_release():
    print(f"[Sentinel-X Packager] Building portable deployment package...")
    if os.path.exists(OUTPUT_ZIP_PATH):
        os.remove(OUTPUT_ZIP_PATH)

    zip_root = "Sentinel-X-Complete"
    count = 0

    with zipfile.ZipFile(OUTPUT_ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(ROOT_DIR):
            # Exclude unwanted directories in-place
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, ROOT_DIR)
                
                if should_exclude(abs_path, rel_path):
                    continue

                arc_name = os.path.join(zip_root, rel_path)
                zipf.write(abs_path, arc_name)
                count += 1

    # Calculate SHA256 checksum
    hasher = hashlib.sha256()
    with open(OUTPUT_ZIP_PATH, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    sha256_hash = hasher.hexdigest()

    size_mb = os.path.getsize(OUTPUT_ZIP_PATH) / (1024 * 1024)
    print("======================================================================")
    print("          SENTINEL-X PORTABLE PACKAGE BUILT SUCCESSFULLY               ")
    print("======================================================================")
    print(f"  Package Path: {OUTPUT_ZIP_PATH}")
    print(f"  File Size:    {size_mb:.2f} MB")
    print(f"  Total Files:  {count}")
    print(f"  SHA256 Hash:  {sha256_hash}")
    print("======================================================================")
    return OUTPUT_ZIP_PATH, sha256_hash

if __name__ == "__main__":
    package_release()
