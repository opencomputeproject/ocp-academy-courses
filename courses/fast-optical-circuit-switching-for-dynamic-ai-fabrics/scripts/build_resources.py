"""Stage the verified published paper into a built course; keep PDFs out of Git."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import sys
import urllib.request


def main() -> None:
    course_path = Path(sys.argv[1]).resolve()
    course = json.loads(course_path.read_text(encoding='utf-8'))
    source_root = Path(__file__).resolve().parent.parent
    for asset in course.get('resource_assets', []):
        if asset.startswith('assets/'):
            source, destination = source_root / asset, course_path.parent / asset
            if source.resolve() != destination.resolve():
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
    paper = next(source for source in course['sources'] if source.get('kind') == 'pdf')
    target = course_path.parent / paper['path']
    expected = paper['sha256']
    if target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() == expected:
        print('Published OCP paper already staged and verified.')
        return
    request = urllib.request.Request(paper['publication_url'], headers={'User-Agent': 'OCP-Academy-course-build'})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
    if not data.startswith(b'%PDF-') or hashlib.sha256(data).hexdigest() != expected:
        raise SystemExit('Published paper differs from the reviewed PDF. Verify the new edition and its page references before updating the recorded SHA-256.')
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix('.pdf.tmp')
    temporary.write_bytes(data)
    temporary.replace(target)
    print('Published October 19, 2026 OCP paper downloaded and SHA-256 verified.')


if __name__ == '__main__':
    main()
