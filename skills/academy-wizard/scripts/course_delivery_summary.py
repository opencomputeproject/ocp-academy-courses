#!/usr/bin/env python3
"""Validate and export formal LMS catalog metadata without changing learner time.

Usage:
  python course_delivery_summary.py course.json
  python course_delivery_summary.py course.json --write
  python course_delivery_summary.py course.json --check
  python course_delivery_summary.py course.json --output-dir delivery --basename course.catalog --html

course.json.lms_catalog is editable source. Exports are deterministic and contain
no narration credentials, machine paths, timestamps, or synthesized estimates.
"""
from __future__ import annotations

import argparse
import html
import json
import math
from pathlib import Path

SHORT_MAX = 130
MARKDOWN_BREAK = '\\' + '\n'  # CommonMark hard break without trailing spaces.


def _text(value, location):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{location} must be non-empty text")
    return value.strip()


def _minutes(value, location):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ValueError(f"{location} must be a positive finite number of minutes")
    return value


def _number(value):
    return f"{value:g}"


def catalog_labels(source, language, unit_label):
    defaults = {'title': 'Title', 'short_description': 'Short Description',
                'long_description': 'Long Description',
                'overall_duration': 'Overall duration: {duration} minutes',
                'unit_heading': unit_label + ' {number}: {title} — {duration} minutes.'}
    supplied = source.get('labels')
    if str(language).split('-')[0].casefold() != 'en' and not isinstance(supplied, dict):
        raise ValueError('Non-English LMS metadata needs translated lms_catalog.labels as well as translated descriptions')
    if supplied is not None:
        if not isinstance(supplied, dict) or set(supplied) != set(defaults):
            raise ValueError('lms_catalog.labels must contain title, short_description, long_description, overall_duration, and unit_heading')
        defaults = {key: _text(value, f'lms_catalog.labels.{key}') for key, value in supplied.items()}
    import string
    for key, required in [('overall_duration', {'duration'}), ('unit_heading', {'number', 'title', 'duration'})]:
        try:
            fields = {field for _, field, _, _ in string.Formatter().parse(defaults[key]) if field is not None}
            if fields != required:
                raise ValueError(f'lms_catalog.labels.{key} must use exactly these placeholders: {sorted(required)}')
            defaults[key].format(number=1, title='Example', duration='10')
        except (KeyError, IndexError, ValueError) as error:
            raise ValueError(f'Invalid LMS label template {key}: {error}') from error
    return defaults


def catalog_metadata(course):
    """Use approved editorial metadata, never a subtitle or WAV-only fallback."""
    source = course.get('lms_catalog')
    if not isinstance(source, dict):
        raise ValueError('Missing course.json.lms_catalog; author the formal short description, overview, learner duration, and unit summaries before delivery')
    title = _text(source.get('title'), 'lms_catalog.title')
    short = _text(source.get('short_description'), 'lms_catalog.short_description')
    if '\n' in short or '\r' in short or len(short) > SHORT_MAX:
        raise ValueError(f'lms_catalog.short_description must be one line of at most {SHORT_MAX} characters (got {len(short)}); edit it rather than truncating approved wording')
    overview = _text(source.get('overview'), 'lms_catalog.overview')
    if '\n\n' in overview.replace('\r\n', '\n'):
        raise ValueError('lms_catalog.overview must be one overview paragraph')
    duration = _minutes(source.get('duration_minutes'), 'lms_catalog.duration_minutes')
    if source.get('duration_basis') != 'estimated_learner_time':
        raise ValueError('lms_catalog.duration_basis must be estimated_learner_time; narration runtime alone is not the course duration')
    target = course.get('target_duration_minutes')
    if target is not None and abs(_minutes(target, 'target_duration_minutes') - duration) > .01:
        raise ValueError('lms_catalog.duration_minutes must match the approved target_duration_minutes; resolve editorial differences before exporting')
    scrolling = str(course.get('style') or 'Slides').casefold() == 'scrolling'
    key, label = ('lessons', 'Lesson') if scrolling else ('modules', 'Module')
    units, rows = course.get(key), source.get(key)
    if not isinstance(units, list) or not units:
        raise ValueError(f'course.{key} must contain the authored units')
    if not isinstance(rows, list):
        raise ValueError(f'lms_catalog.{key} must contain a duration and summary for every authored unit')
    by_id = {}
    for row in rows:
        if not isinstance(row, dict) or row.get('id') is None:
            raise ValueError(f'Every lms_catalog.{key} row needs its authored id')
        ident = str(row['id'])
        if ident in by_id:
            raise ValueError(f'Duplicate lms_catalog.{key} id: {ident}')
        by_id[ident] = row
    expected = [str(unit.get('id')) for unit in units]
    if any(unit.get('id') is None for unit in units) or len(set(expected)) != len(expected):
        raise ValueError(f'Authored {key} must have unique non-null ids')
    if set(expected) != set(by_id):
        raise ValueError(f'lms_catalog.{key} ids must match the authored units exactly (missing {sorted(set(expected)-set(by_id))}; unexpected {sorted(set(by_id)-set(expected))})')
    exported = []
    for unit in units:
        row = by_id[str(unit['id'])]
        exported.append({'id': unit['id'], 'title': _text(unit.get('title'), f'{key} title'),
                         'duration_minutes': _minutes(row.get('duration_minutes'), f'{key} {unit["id"]} duration'),
                         'summary': _text(row.get('summary'), f'{key} {unit["id"]} summary')})
    total = sum(row['duration_minutes'] for row in exported)
    if abs(total - duration) > .01:
        raise ValueError(f'Unit durations total {_number(total)} minutes, but overall duration is {_number(duration)}; reconcile the approved estimates')
    note = source.get('duration_note')
    if note is not None:
        note = _text(note, 'lms_catalog.duration_note')
    overview = ' '.join(overview.split())
    labels = catalog_labels(source, course.get('language') or 'en-US', label)
    overall = labels['overall_duration'].format(duration=_number(duration))
    long_md = [overview, f'**{overall}**']
    long_html = [f'<p>{html.escape(overview)}</p>', f'<p><strong>{html.escape(overall)}</strong></p>']
    for index, row in enumerate(exported, 1):
        heading = labels['unit_heading'].format(number=index, title=row['title'], duration=_number(row['duration_minutes']))
        summary = ' '.join(row['summary'].split())
        row['summary'] = summary
        long_md.append(f'**{heading}**{MARKDOWN_BREAK}{summary}')
        long_html.append(f'<p><strong>{html.escape(heading)}</strong><br>\n{html.escape(summary)}</p>')
    result = {'schema_version': 1, 'metadata_purpose': 'LMS catalog fields; separate from the course README', 'labels': labels, 'course_slug': course.get('course_slug'),
              'language': course.get('language') or 'en-US', 'title': title,
              'short_description': short, 'short_description_characters': len(short),
              'overview': overview, 'duration_minutes': duration,
              'duration_basis': 'estimated_learner_time', key: exported,
              'long_description': '\n\n'.join(long_md),
              'long_description_html': '\n'.join(long_html)}
    if note:
        result['duration_note'] = note
    return result


def catalog_files(course, basename='lms-catalog', include_html=False):
    if not basename or Path(basename).name != basename or basename in {'.', '..'}:
        raise ValueError('Catalog basename must be a filename stem without a directory')
    metadata = catalog_metadata(course)
    labels = metadata['labels']
    md = (f'**{labels["title"]}**{MARKDOWN_BREAK}{metadata["title"]}\n\n**{labels["short_description"]}**  \n'
          f'{metadata["short_description"]}\n\n**{labels["long_description"]}**\n\n'
          f'{metadata["long_description"]}\n')
    files = {basename + '.json': json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', basename + '.md': md}
    if include_html:
        files[basename + '.html'] = ('<!doctype html>\n<html lang="' + html.escape(metadata['language'], quote=True) + '">\n'
            '<meta charset="utf-8">\n<title>' + html.escape(metadata['title']) + '</title>\n'
            '<h1>' + html.escape(metadata['title']) + '</h1>\n'
            '<h2>' + html.escape(labels['short_description']) + '</h2>\n<p>' + html.escape(metadata['short_description']) + '</p>\n'
            '<h2>' + html.escape(labels['long_description']) + '</h2>\n' + metadata['long_description_html'] + '\n</html>\n')
    return files


def write_catalog(course, output_dir, basename='lms-catalog', include_html=False, check=False):
    files = catalog_files(course, basename, include_html)
    output_dir = Path(output_dir)
    if check:
        stale = [name for name, value in files.items() if not (output_dir / name).is_file() or (output_dir / name).read_text(encoding='utf-8') != value]
        if stale:
            raise ValueError('Missing or stale catalog exports: ' + ', '.join(stale) + '; regenerate from course.json')
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
        for name, value in files.items():
            (output_dir / name).write_text(value, encoding='utf-8')
    return [output_dir / name for name in files]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('course_json', type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true', help='Write source lms-catalog.json and lms-catalog.md')
    mode.add_argument('--check', action='store_true', help='Check committed metadata exports without changing them')
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--basename', default='lms-catalog')
    parser.add_argument('--html', action='store_true', help='Also export an HTML copy for LMS rich-text fields')
    parser.add_argument('--short-max', type=int, choices=range(1,131), default=130, metavar='1..130', help='Optional stricter short-description check; never truncates wording')
    args = parser.parse_args()
    try:
        source = args.course_json.resolve()
        course = json.loads(source.read_text(encoding='utf-8'))
        metadata = catalog_metadata(course)
        if len(metadata['short_description']) > args.short_max:
            raise ValueError(f'Short description exceeds requested {args.short_max}-character limit')
        if args.write or args.check or args.output_dir is not None or args.html:
            paths = write_catalog(course, args.output_dir or source.parent, args.basename, args.html, args.check)
            print(('Checked: ' if args.check else 'Wrote: ') + ', '.join(str(path) for path in paths))
        else:
            print(catalog_files(course,args.basename)[args.basename+'.md'],end='')
    except (OSError, ValueError) as error:
        parser.exit(1, f'Catalog metadata error: {error}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
