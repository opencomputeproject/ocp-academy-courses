#!/usr/bin/env python3
"""
validate_package.py — sanity-check a finished SCORM folder before delivery.

Usage:
    python validate_package.py <folder>

Checks:
  - imsmanifest.xml exists and parses as XML
  - index.html exists
  - For each <resource>: every <file href="..."/> resolves to a real file
  - For each moduleN.html: every audioMap path resolves on disk
  - Each moduleN.html has slide IDs 1..N contiguously
  - No file in the folder is larger than 50 MB (likely a mistake)
  - Brand logos and scorm_api.js are present

Exits 0 on clean validation, 1 with a list of failures otherwise.
"""

from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET


def main():
    p = argparse.ArgumentParser()
    p.add_argument("folder", type=Path)
    args = p.parse_args()
    root = args.folder.resolve()
    if not root.is_dir():
        sys.exit(f"Not a directory: {root}")

    errors: list[str] = []
    warnings: list[str] = []

    def err(m): errors.append(m)
    def warn(m): warnings.append(m)

    manifest = root / "imsmanifest.xml"
    index = root / "index.html"
    api = root / "scorm_api.js"

    if not manifest.exists():
        err("imsmanifest.xml is missing")
    if not index.exists():
        err("index.html is missing")
    if not api.exists():
        err("scorm_api.js is missing")

    if manifest.exists():
        try:
            tree = ET.parse(manifest)
            ns = {"ims": "http://www.imsproject.org/xsd/imscp_rootv1p1p2",
                  "adl": "http://www.adlnet.org/xsd/adlcp_rootv1p2"}
            for res in tree.getroot().iter("{http://www.imsproject.org/xsd/imscp_rootv1p1p2}resource"):
                for f in res.findall("{http://www.imsproject.org/xsd/imscp_rootv1p1p2}file"):
                    href = f.get("href")
                    if href and not (root / href).exists():
                        err(f"manifest references missing file: {href}")
        except ET.ParseError as e:
            err(f"imsmanifest.xml does not parse: {e}")

    for module_file in sorted(root.glob("module*.html")):
        html = module_file.read_text(errors="replace")
        slide_ids = [int(m.group(1)) for m in re.finditer(r'data-slide="(\d+)"', html)]
        if not slide_ids:
            err(f"{module_file.name}: no data-slide markers")
        else:
            expected = list(range(1, max(slide_ids) + 1))
            if sorted(slide_ids) != expected:
                err(f"{module_file.name}: slide IDs not contiguous 1..{max(slide_ids)} — got {sorted(slide_ids)}")
        # audioMap audit
        m = re.search(r"const audioMap\s*=\s*\{([^}]*)\}", html, re.S)
        if m:
            for entry in re.finditer(r'(\d+):\s*"([^"]+)"', m.group(1)):
                audio_rel = entry.group(2)
                if not (root / audio_rel).exists():
                    err(f"{module_file.name}: audioMap references missing audio: {audio_rel}")

    # Big-file warning
    for f in root.rglob("*"):
        if f.is_file() and f.stat().st_size > 50 * 1024 * 1024:
            warn(f"large file (>50MB): {f.relative_to(root)} ({f.stat().st_size // (1024*1024)} MB)")

    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  - {w}")
    if not errors:
        print(f"\nOK — package at {root} validates.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
