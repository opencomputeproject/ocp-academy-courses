#!/usr/bin/env python3
"""
new_course.py — scaffold a new SCORM package folder.

Usage:
    python new_course.py <output_dir> <course.json>

Creates the folder layout the renderers expect, copies scorm_api.js into place,
copies any provided brand logos that exist next to course.json, and pre-creates
empty audio/moduleN/ subdirectories plus a figures/ directory.
"""

from __future__ import annotations
import argparse
import json
import shutil
import sys
from pathlib import Path
from motion_intro import motion_intro_logo

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSETS_DIR = SKILL_DIR / "assets"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("output_dir", type=Path)
    p.add_argument("course_json", type=Path)
    args = p.parse_args()

    course = json.loads(args.course_json.read_text())
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    # scorm_api.js — guard against re-running scaffold over an existing
    # output dir, where shutil.copy would raise SameFileError or hit a
    # read-only target.
    api_dst = out / "scorm_api.js"
    api_src = ASSETS_DIR / "scorm_api.js"
    if api_dst.exists() and api_src.resolve() == api_dst.resolve():
        print(f"skip: scorm_api.js already in place")
    elif api_dst.exists():
        try:
            shutil.copy(api_src, api_dst)
            print(f"refreshed scorm_api.js -> {out}")
        except (PermissionError, shutil.SameFileError) as e:
            print(f"skip: could not refresh scorm_api.js ({e})")
    else:
        shutil.copy(api_src, api_dst)
        print(f"copied scorm_api.js -> {out}")

    # brand logos: look for them next to course.json. Skip if source and
    # destination resolve to the same file (common when course.json and
    # the logo live in the output folder).
    brand = course.get("brand", {})
    src_dir = args.course_json.resolve().parent
    copied_logo_dests: set[Path] = set()

    def copy_logo_candidate(logo: str, key: str):
        if not logo:
            return
        rel = Path(logo)
        dst = out / (rel.name if rel.is_absolute() else rel)
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst in copied_logo_dests:
            print(f"skip: {logo} already copied")
            return
        candidates = [rel if rel.is_absolute() else src_dir / rel, ASSETS_DIR / rel.name]
        src = next((c for c in candidates if c.exists()), None)
        if src is None:
            print(f"NOTE: {key} = {logo!r} but file not found next to course.json "
                  f"or in skill assets; ensure it lands in the output folder before render.")
            return
        if dst.exists() and src.resolve() == dst.resolve():
            print(f"skip: {logo} already in place")
            return
        shutil.copy(src, dst)
        copied_logo_dests.add(dst)
        print(f"copied logo {logo} -> {dst.relative_to(out)}")

    for key in ("course_logo", "academy_logo"):
        logo = brand.get(key)
        copy_logo_candidate(logo, f"brand.{key}")

    # Motion intro logo: the skill ships a default white OCP Academy SVG so
    # every generated package can play the intro without requiring the user
    # to provide a logo file alongside course.json.
    copy_logo_candidate(motion_intro_logo(course), "motion_intro.logo")

    # audio + figures dirs
    figures = out / "figures"
    figures.mkdir(exist_ok=True)
    for mod in course["modules"]:
        d = out / "audio" / f"module{mod['id']}"
        d.mkdir(parents=True, exist_ok=True)
    print("created audio/moduleN/ subdirs and figures/")

    # If course.json itself is not yet in out_dir, copy it so renderers can find it.
    target_json = out / args.course_json.name
    if not target_json.exists() or target_json.resolve() != args.course_json.resolve():
        shutil.copy(args.course_json, target_json)
        print(f"copied {args.course_json.name} -> {target_json}")

    print("\nScaffold complete. Next steps:")
    print(f"  1. Write narration scripts under {out}/audio/moduleN/slide_*.txt")
    print(f"  2. Drop or generate figures under {out}/figures/")
    print(f"  3. Run gen_audio.py, then render_module.py --all, then render_index.py")


if __name__ == "__main__":
    main()
