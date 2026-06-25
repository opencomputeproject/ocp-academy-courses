#!/usr/bin/env python3
"""
zip_for_lms.py — build a strict SCORM zip containing ONLY files listed in
imsmanifest.xml (plus the manifest itself). Working files like course.json,
.txt narration scripts, _outline.md, gen_audio_standalone.py, .DS_Store, etc.
are excluded.

Why this exists: some LMSes reject SCORM uploads that contain files not
declared in the manifest's resource blocks. A "right-click → Compress" zip
of the package folder picks up every working file alongside the runtime
assets, and gets rejected.

Usage:
    python zip_for_lms.py <package-folder> [-o <output.zip>]

Default output: <parent>/<package-folder-name>.zip
"""

from __future__ import annotations
import argparse
import re
import sys
import zipfile
from pathlib import Path


def manifest_file_list(manifest_path: Path) -> list[str]:
    """Return every `href` referenced by <file> entries in the manifest,
    plus imsmanifest.xml itself."""
    text = manifest_path.read_text(encoding="utf-8")
    hrefs = sorted(set(re.findall(r'<file\s+href="([^"]+)"', text)))
    return ["imsmanifest.xml"] + hrefs


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("folder", type=Path, help="SCORM package folder containing imsmanifest.xml")
    p.add_argument("-o", "--output", type=Path,
                   help="Output .zip path (default: <parent>/<folder-name>.zip)")
    args = p.parse_args()

    folder = args.folder.resolve()
    if not folder.is_dir():
        sys.exit(f"ERROR: {folder} is not a directory")
    manifest = folder / "imsmanifest.xml"
    if not manifest.exists():
        sys.exit(f"ERROR: no imsmanifest.xml in {folder}")

    files = manifest_file_list(manifest)
    # Verify every referenced file exists on disk
    missing = [f for f in files if not (folder / f).exists()]
    if missing:
        sys.stderr.write(f"ERROR: {len(missing)} files referenced by manifest are missing on disk:\n")
        for m in missing[:20]:
            sys.stderr.write(f"  {m}\n")
        if len(missing) > 20:
            sys.stderr.write(f"  ... and {len(missing)-20} more\n")
        sys.exit(1)

    out_path = args.output or folder.parent / f"{folder.name}.zip"
    out_path = Path(out_path).resolve()
    if out_path.exists():
        out_path.unlink()

    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for rel in files:
            src = folder / rel
            # Store files at the root of the zip — imsmanifest.xml must be at
            # the archive root for strict LMSes (SCORM Cloud, many corporate
            # LMSes). Some LMSes reject zips with a folder wrapper.
            z.write(src, rel)

    total_bytes = out_path.stat().st_size
    print(f"wrote {out_path}")
    print(f"  {len(files)} files, {total_bytes/1024/1024:.1f} MiB")


if __name__ == "__main__":
    main()
