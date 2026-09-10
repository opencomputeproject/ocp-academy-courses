"""Evidence-based glossary placement checks. No media playback or OCR claims.

Uses the maintained renderer, spoken script bodies and human-reviewed, hash-bound
media text inventories. Glossary metadata cannot count as its own evidence.
"""
from __future__ import annotations

import copy
import hashlib
import re
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

NON_TEACHING = {'title', 'course_overview', 'objectives', 'knowledge_check', 'up_next', 'course_complete'}
VIDEO_EXTENSIONS = {'.mp4', '.webm', '.mov', '.m4v'}


def glossary_exclusion_reason(slide, index, count):
    """Shared audit/render gate; boundaries use array position, never slide IDs."""
    if slide.get('type') in NON_TEACHING:
        return slide['type']
    if index == 0:
        return 'the first slide of a module (regardless of type)'
    if index == count - 1:
        return 'the last slide of a module (regardless of type)'
    return None


class ReadingText(HTMLParser):
    """Read rendered text, not attributes, script data, tooltips or hidden text."""
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = set(attrs.get('class', '').split())
        hidden = (any(blocked for _, blocked in self.stack)
                  or tag in {'script', 'style', 'head', 'title', 'desc', 'defs', 'metadata'}
                  or 'hidden' in attrs or attrs.get('aria-hidden') == 'true'
                  or bool(classes & {'glossary-strip', 'glossary-chip', 'reference-strip', 'reference-pill'})
                  or bool(re.search(r'(?:display\s*:\s*none|visibility\s*:\s*hidden)', attrs.get('style', ''))))
        if tag in {'br', 'p', 'div', 'li', 'td', 'th', 'h1', 'h2', 'h3'}:
            self.parts.append('\n')
        if tag not in self.VOID:
            self.stack.append((tag, hidden))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break
        if tag in {'p', 'div', 'li', 'td', 'th', 'h1', 'h2', 'h3'}:
            self.parts.append('\n')

    def handle_data(self, data):
        if not any(blocked for _, blocked in self.stack):
            self.parts.append(data)


def normalize(value):
    value = unicodedata.normalize('NFKC', str(value)).casefold()
    value = re.sub(r'https?://\S+', '', value)
    value = re.sub(r'[-‐‑‒–—]', ' ', value)
    value = re.sub(r'\s*/\s*', '/', value)
    return re.sub(r'\s+', ' ', value).strip()


def match_term(term, text):
    text = normalize(text)
    for alias in [term.get('term', ''), *(term.get('aliases') or [])]:
        needle = normalize(alias)
        if needle and re.search(r'(?<!\w)' + re.escape(needle) + r'(?!\w)', text):
            return str(alias)
        # Pronunciation spelling of an actual acronym, e.g. S L A, not synonyms.
        if re.fullmatch(r'[A-Z]{2,8}', str(alias)):
            letters = r'[\s.]+'.join(re.escape(c.casefold()) for c in alias)
            if re.search(r'(?<!\w)' + letters + r'(?!\w)', text):
                return str(alias)
    return None


def slide_sources(slide, course, module, root):
    from render_module import RENDERERS
    errors, sources = [], []
    sid = f'M{module.get("id")}S{slide.get("id")}'
    clean = copy.deepcopy(slide)
    clean['term_refs'] = []
    clean['reference_links'] = []
    renderer = RENDERERS.get(clean.get('type'))
    if renderer:
        parser = ReadingText()
        parser.feed(renderer(clean, course, module))
        sources.append({'kind': 'slide', 'text': ''.join(parser.parts)})
    else:
        errors.append(f'{sid}: cannot audit unknown slide type {clean.get("type")!r}')
    script = (slide.get('audio') or {}).get('script_file')
    if script:
        file = root / script
        if not file.is_file():
            errors.append(f'{sid}: missing narration script {script}')
        else:
            body = '\n'.join(line for line in file.read_text(encoding='utf-8').splitlines()
                             if not line.lstrip().startswith('#'))
            sources.append({'kind': 'script', 'path': script, 'text': body})
    elif slide.get('transcript'):
        sources.append({'kind': 'transcript', 'text': slide['transcript']})
    figure = slide.get('figure') or {}
    if figure:
        file = root / str(figure.get('path') or '')
        inventory = figure.get('text_inventory')
        if not isinstance(inventory, dict) or not isinstance(inventory.get('entries'), list):
            errors.append(f'{sid}: missing reviewed figure.text_inventory; inspect visible media text (including video states)')
        elif not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest() != inventory.get('sha256'):
            errors.append(f'{sid}: stale or missing media for text_inventory; review the current asset again')
        else:
            video = figure.get('media_type') == 'video' or file.suffix.lower() in VIDEO_EXTENSIONS
            for entry in inventory['entries']:
                if not isinstance(entry, dict) or not isinstance(entry.get('text'), str) or not entry['text'].strip():
                    errors.append(f'{sid}: invalid media text inventory entry')
                    continue
                when = entry.get('at_seconds')
                if video and (isinstance(when, bool) or not isinstance(when, (int, float)) or not 0 <= when < float('inf')):
                    errors.append(f'{sid}: video text evidence needs a finite nonnegative at_seconds locator')
                    continue
                sources.append({'kind': 'video' if video else 'figure', 'path': figure['path'], **entry})
    return sources, errors


def audit_glossary(course, root):
    """Return errors and traceable evidence for every attached glossary pill.

    Text inventories are needed for every figure in a module with glossary pills,
    so an earlier media-only occurrence cannot be silently ignored. Inventory
    text must be visually reviewed; a file hash proves freshness, not correctness.
    """
    errors, evidence = [], []
    glossary = {t['id']: t for t in course.get('term_glossary', []) if isinstance(t, dict) and t.get('id')}
    for tid, term in glossary.items():
        if normalize(tid) in {'ocp', 'ai', 'ml', 'ai/ml'} or normalize(term.get('term')) in {'ocp', 'ai', 'ml', 'ai/ml'}:
            errors.append(f'Excluded baseline vocabulary in glossary: {tid}')
        if not str(term.get('term', '')).strip():
            errors.append(f'Glossary {tid}: missing learner-facing term')
        if not isinstance(term.get('aliases', []), list) or any(not isinstance(a, str) or not a.strip() for a in term.get('aliases', [])):
            errors.append(f'Glossary {tid}: aliases must be a list of nonempty same-term variants')
            term = dict(term, aliases=[])
            glossary[tid] = term
    for module in course.get('modules', []):
        slides = module.get('slides', [])
        if not any(s.get('term_refs') for s in slides):
            continue
        texts = {}
        for index, slide in enumerate(slides):
            excluded = glossary_exclusion_reason(slide, index, len(slides))
            if excluded:
                if slide.get('term_refs'):
                    errors.append(f'M{module["id"]}S{slide["id"]}: glossary belongs on a substantive teaching slide, not {excluded}')
                continue
            sources, flags = slide_sources(slide, course, module, root)
            texts[slide['id']] = sources
            errors.extend(flags)
        for index, slide in enumerate(slides):
            if glossary_exclusion_reason(slide, index, len(slides)):
                continue
            for tid in slide.get('term_refs', []):
                if tid not in glossary:
                    continue  # Existing structural QA reports undefined IDs.
                term = glossary[tid]
                hits = [(source, match_term(term, source['text'])) for source in texts.get(slide['id'], [])]
                hits = [(source, alias) for source, alias in hits if alias]
                first = next((s['id'] for s in slides if any(match_term(term, t['text']) for t in texts.get(s['id'], []))), None)
                sid = f'M{module["id"]}S{slide["id"]}'
                if not hits:
                    errors.append(f'{sid}: glossary {tid!r} is absent from rendered teaching text, script and verified media text')
                if first is not None and first != slide['id']:
                    errors.append(f'{sid}: glossary {tid!r} first appears on M{module["id"]}S{first}; move its pill there')
                if slide.get('type') == 'full_slide_image':
                    errors.append(f'{sid}: full_slide_image does not render glossary pills; retain image-only layout or obtain approval for a different layout')
                evidence.append({'slide': sid, 'term_id': tid, 'term': term.get('term'),
                                 'first_slide': first, 'matches': [dict(source, matched_as=alias) for source, alias in hits]})
    return errors, evidence
