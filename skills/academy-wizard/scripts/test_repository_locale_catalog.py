"""A locale belongs in the translation matrix, under its English catalog course."""
import json
import struct
import tempfile
import unittest
from pathlib import Path

from slides_course_qa import check_course


class RepositoryLocaleCatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.root = self.repo / 'courses/example/locales/ja-JP'
        self.root.mkdir(parents=True)
        self.course = {'style': 'Slides', 'language': 'ja-JP', 'course_title': '例',
                       'localization': {'source_course': '../../course.json'},
                       'modules': [{'id': 1, 'slides': [{'id': 1, 'type': 'title'},
                           {'id': 2, 'type': 'content_diagram', 'figure': {
                               'path': 'teaching.mp4', 'poster': 'poster.png',
                               'media_type': 'video', 'autoplay': True, 'loop': True,
                               'muted': True, 'alt': 'Diagram', 'caption': 'Teaching'}},
                           {'id': 3, 'type': 'course_complete'}]}]}
        (self.root / 'teaching.mp4').write_bytes(b'reviewed-video-placeholder')
        (self.root / 'poster.png').write_bytes(b'poster-placeholder')
        (self.root.parent.parent / 'thumbnail.png').write_bytes(
            b'\x89PNG\r\n\x1a\n' + struct.pack('>I', 13) + b'IHDR' + struct.pack('>II', 800, 400))
        (self.root / 'README.md').write_text('# 例\n')

    def audit(self, translated=True):
        (self.root / 'course.json').write_text(json.dumps(self.course))
        (self.repo / 'README.md').write_text(
            '## Available Courses\n[Example](courses/example/README.md)\n'
            '## Repository layout\ncourses/example/\n'
            '## Translations\n' + ('[ja-JP](courses/example/locales/ja-JP/)\n' if translated else ''))
        return check_course(self.root / 'course.json', self.repo, set())[0]

    def test_locale_uses_canonical_course_catalog_entry(self):
        self.assertEqual(self.audit(), [])

    def test_missing_translation_matrix_entry_is_rejected(self):
        self.assertTrue(any('Translations table is missing' in e for e in self.audit(False)))

    def test_locale_and_declared_language_must_match(self):
        self.course['language'] = 'ko-KR'
        self.assertTrue(any('locale folder does not match' in e for e in self.audit()))

    def test_prepared_locale_poster_requires_explicit_retention(self):
        poster = self.root / 'thumbnail.png'
        poster.write_bytes((self.root.parent.parent / 'thumbnail.png').read_bytes())
        self.assertTrue(any('without a local duplicate' in e for e in self.audit()))
        self.assertEqual(check_course(self.root / 'course.json', self.repo, set(),
                                     allow_localized_poster=True)[0], [])


if __name__ == '__main__':
    unittest.main()
