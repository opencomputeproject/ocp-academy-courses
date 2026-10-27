#!/usr/bin/env python3
"""Create a strict SCORM ZIP and separate LMS catalog metadata sidecars.

Usage:
  python zip_for_lms.py <runtime-folder> [-o output.zip] [--course-json source/course.json]

The archive contains only manifest-listed runtime files plus imsmanifest.xml.
The formal LMS title/descriptions are exported beside it as
<zip-stem>.lms-catalog.{json,md,html}; they are not the source README or SCORM
runtime. Source lms-catalog.json and lms-catalog.md are refreshed for Git tracking.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile

from course_delivery_summary import catalog_files, catalog_metadata, write_catalog
import json


def manifest_file_list(manifest_path):
    root = ET.parse(manifest_path).getroot()
    return ['imsmanifest.xml'] + sorted({node.get('href') for node in root.iter()
                                       if node.tag.rsplit('}', 1)[-1] == 'file' and node.get('href') and node.get('href') != 'imsmanifest.xml'})


def find_course_source(folder, explicit=None):
    if explicit is not None:
        source = Path(explicit).resolve()
        if not source.is_file():
            raise ValueError(f'Course source not found: {source}')
        return source
    for root in (folder, folder.parent):
        source = root / 'course.json'
        if source.is_file():
            return source
    raise ValueError('No course.json beside the runtime or in its parent. Pass --course-json to export the formal LMS catalog metadata with the ZIP')


def package(folder, output=None, course_json=None):
    folder = Path(folder).resolve()
    manifest = folder / 'imsmanifest.xml'
    if not manifest.is_file():
        raise ValueError(f'No imsmanifest.xml in {folder}')
    source = find_course_source(folder, course_json)
    course = json.loads(source.read_text(encoding='utf-8'))
    catalog_metadata(course)  # Fail before touching an existing delivery.
    files = manifest_file_list(manifest)
    for rel in files:
        if Path(rel).is_absolute() or '..' in Path(rel).parts or not (folder / rel).is_file():
            raise ValueError(f'Missing or invalid manifest runtime file: {rel}')
        if 'lms-catalog' in Path(rel).name:
            raise ValueError('LMS catalog exports belong beside the ZIP, not in the SCORM manifest')
    output = Path(output).resolve() if output else folder.parent / (folder.name + '.zip')
    if output.suffix.casefold() != '.zip':
        raise ValueError('Output filename must end in .zip')
    sidecars = catalog_files(course, output.stem + '.lms-catalog', include_html=True)
    # Prevent an accidental output/metadata collision with an input runtime file.
    for target in [output, *(output.parent / name for name in sidecars)]:
        if target in {(folder / rel).resolve() for rel in files} or target == source:
            raise ValueError(f'Delivery output would overwrite an input: {target}')
    output.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, prefix=output.name+'.', suffix='.tmp', delete=False) as handle:
            temp_path = Path(handle.name)
        with zipfile.ZipFile(temp_path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for rel in files:
                archive.write(folder / rel, rel)
        # Refresh source-tracked metadata and prepare delivery copy before publishing the ZIP.
        write_catalog(course, source.parent)
        for name, content in sidecars.items():
            (output.parent / name).write_text(content, encoding='utf-8')
        os.replace(temp_path, output)
        temp_path = None
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
    return output, [output.parent / name for name in sidecars], len(files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    parser.add_argument('-o', '--output', type=Path)
    parser.add_argument('--course-json', type=Path, help='Editable source; otherwise find course.json in the runtime or its parent')
    args = parser.parse_args()
    try:
        output, sidecars, count = package(args.folder, args.output, args.course_json)
    except (OSError, ValueError, ET.ParseError) as error:
        parser.exit(1, f'Packaging error: {error}\n')
    print(f'Wrote {output}\n  {count} runtime files, {output.stat().st_size/1024/1024:.1f} MiB')
    print('LMS catalog metadata (separate from README and SCORM runtime):')
    for path in sidecars:
        print(f'  {path}')


if __name__ == '__main__':
    main()
