#!/usr/bin/env python3
"""
Sentinel-X Automated Cross-Platform Release Packager
===================================================
Creates a clean, portable Sentinel-X-Complete.zip bundle specifically configured
for Raspberry Pi OS (Debian/Linux ARM64/ARM32):
  1. Uses standard Unix forward slashes (/) for all directory paths inside the archive
  2. Converts all scripts and text configuration files to Linux LF line endings
  3. Applies executable POSIX file permissions (0o755) to all shell scripts
  4. Excludes unnecessary ZIP files, development caches, and virtual environments
"""

import os
import sys
import zipfile
import hashlib
import time

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_ZIP_NAME = "Sentinel-X-Complete.zip"
OUTPUT_ZIP_PATH = os.path.join(ROOT_DIR, OUTPUT_ZIP_NAME)

EXCLUDED_DIRS = {
    ".git", ".github", "__pycache__", ".pytest_cache", ".venv", "venv",
    "node_modules", ".idea", ".vscode", "scratch", ".agents", "college id"
}

EXCLUDED_FILES = {
    ".DS_Store", "Sentinel-X-Complete.zip", "sentinel_edge.db-journal",
    "Zipped PDF Files.zip", "sentinel-x-frontend.zip"
}

EXCLUDED_EXTENSIONS = {
    ".pyc", ".pyo", ".pyd", ".tmp", ".log", ".zip"
}

TEXT_EXTENSIONS = {
    ".sh", ".py", ".json", ".yaml", ".yml", ".txt", ".md", ".html",
    ".js", ".css", ".conf", ".service", ".env", ".example", ".sql",
    ".ini", ".desktop"
}

def is_text_file(filename):
    _, ext = os.path.splitext(filename)
    if ext.lower() in TEXT_EXTENSIONS:
        return True
    if filename in {"VERSION", "LICENSE", "CODEOWNERS", ".gitignore", ".env.example"}:
        return True
    return False

def should_exclude(file_path, rel_path):
    parts = rel_path.replace("\\", "/").split("/")
    for p in parts:
        if p in EXCLUDED_DIRS:
            return True
    base_name = os.path.basename(file_path)
    if base_name in EXCLUDED_FILES:
        return True
    _, ext = os.path.splitext(base_name)
    if ext.lower() in EXCLUDED_EXTENSIONS:
        return True
    return False

def package_release():
    print(f"[Sentinel-X Packager] Building portable deployment package for Raspberry Pi...")
    if os.path.exists(OUTPUT_ZIP_PATH):
        try:
            os.remove(OUTPUT_ZIP_PATH)
        except Exception:
            pass

    zip_root = "Sentinel-X-Complete"
    count = 0

    with zipfile.ZipFile(OUTPUT_ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(ROOT_DIR):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, ROOT_DIR)
                
                if should_exclude(abs_path, rel_path):
                    continue

                # Force standard Unix forward slash separators
                arc_name = f"{zip_root}/{rel_path.replace(os.sep, '/')}"
                is_exec = file.endswith(".sh") or file == "install"
                
                # Check if text file to normalize CRLF -> LF
                if is_text_file(file):
                    try:
                        with open(abs_path, 'rb') as f:
                            content = f.read()
                        # Convert Windows CRLF to Unix LF
                        content = content.replace(b'\r\n', b'\n')
                        
                        zinfo = zipfile.ZipInfo(arc_name, time.localtime(os.path.getmtime(abs_path))[:6])
                        # Set Unix file permissions (0o755 for executable scripts, 0o644 for regular files)
                        zinfo.external_attr = (0o755 if is_exec else 0o644) << 16
                        zipf.writestr(zinfo, content, compress_type=zipfile.ZIP_DEFLATED)
                        count += 1
                        continue
                    except Exception as e:
                        print(f"  [!] Fallback writing {rel_path}: {e}")

                # Binary file write
                zinfo = zipfile.ZipInfo.from_file(abs_path, arcname=arc_name)
                zinfo.external_attr = (0o755 if is_exec else 0o644) << 16
                with open(abs_path, 'rb') as f:
                    zipf.writestr(zinfo, f.read(), compress_type=zipfile.ZIP_DEFLATED)
                count += 1

    # Calculate SHA256 checksum
    hasher = hashlib.sha256()
    with open(OUTPUT_ZIP_PATH, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    sha256_hash = hasher.hexdigest()

    size_mb = os.path.getsize(OUTPUT_ZIP_PATH) / (1024 * 1024)
    print("======================================================================")
    print("      SENTINEL-X PORTABLE PACKAGE (PI OPTIMIZED) BUILT SUCCESSFULLY   ")
    print("======================================================================")
    print(f"  Package Path: {OUTPUT_ZIP_PATH}")
    print(f"  File Size:    {size_mb:.2f} MB")
    print(f"  Total Files:  {count}")
    print(f"  SHA256 Hash:  {sha256_hash}")
    print("======================================================================")
    return OUTPUT_ZIP_PATH, sha256_hash

if __name__ == "__main__":
    package_release()
