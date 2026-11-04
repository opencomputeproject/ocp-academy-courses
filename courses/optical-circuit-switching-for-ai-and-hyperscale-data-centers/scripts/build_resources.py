#!/usr/bin/env python3
"""Stage course-owned offline assets into the repository build folder."""
import json
from pathlib import Path
import shutil
import sys


def main():
    course_file = Path(sys.argv[1]).resolve()
    source = Path(__file__).resolve().parents[1]
    destination = course_file.parent
    course = json.loads(course_file.read_text())
    copied = 0
    for value in course.get("resource_assets", []):
        relative = Path(value)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Resource path must be course relative: {value}")
        original = source / relative
        target = destination / relative
        if not original.is_file():
            raise FileNotFoundError(original)
        if original.resolve() != target.resolve():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original, target)
            copied += 1
    print(f"Staged {copied} declared offline resources.")


if __name__ == "__main__":
    main()
