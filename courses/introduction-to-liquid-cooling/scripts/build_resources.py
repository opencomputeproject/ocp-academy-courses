"""Stage offline resources and render contributor credits from editable data."""
from pathlib import Path
from html import escape
import json
import shutil
import sys

source = Path(__file__).resolve().parents[1]
output = Path(sys.argv[1]).resolve().parent
course = json.loads((source / 'course.json').read_text())
assert course['scorm']['include_home_sco'] is True
assert [module['id'] for module in course['modules']] == [1, 2, 3, 4]
shutil.copytree(source / 'assets', output / 'assets', dirs_exist_ok=True)
shutil.copy2(source / 'thumbnail.png', output / 'thumbnail.png')
credits = json.loads((source / 'authoring/credits.json').read_text())
title = escape(credits['title'])
paragraphs = ''.join('<p>' + escape(text) + '</p>' for text in credits['paragraphs'])
links = ' · '.join('<a href="' + escape(link['url'], quote=True) + '" target="_blank" rel="noopener">' + escape(link['label']) + '</a>' for link in credits['links'])
html = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + title + '</title><style>body{font:18px/1.6 Arial,sans-serif;max-width:820px;margin:4rem auto;padding:0 24px;color:#252a28}a{color:#315580}</style><h1>' + title + '</h1>' + paragraphs + '<p>' + links + '</p></html>'
(output / 'credits.html').write_text(html)
