"""Locale source QA uses the one canonical English catalog poster and listing."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from slides_course_qa import check_course


class SharedCatalogPosterTests(unittest.TestCase):
    def test_locale_reuses_canonical_poster_and_rejects_duplicate(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            canonical = repo / 'courses/example'
            locale = canonical / 'locales/ko-KR'
            locale.mkdir(parents=True)
            course = {'course_title': 'Localized course', 'style': 'Slides',
                      'modules': [{'id': 1, 'slides': [{'id': 1, 'type': 'title'}]}]}
            source = locale / 'course.json'
            source.write_text(json.dumps(course))
            (locale / 'README.md').write_text('Localized course')
            (repo / 'README.md').write_text(
                '## Repository layout\nexample\n\n## Available Courses\n'
                '[Example](courses/example/README.md)\n')
            reference = Path(__file__).resolve().parents[1] / 'references/posters/sst.png'
            shutil.copy2(reference, canonical / 'thumbnail.png')
            errors, notes = check_course(source, repo, {1})
            self.assertEqual(errors, [])
            self.assertTrue(any('shared English catalog poster' in note for note in notes))
            shutil.copy2(reference, locale / 'thumbnail.png')
            errors, _ = check_course(source, repo, {1})
            self.assertTrue(any('without a local duplicate' in error for error in errors))
            (locale / 'thumbnail.png').unlink()
            (canonical / 'thumbnail.png').unlink()
            errors, _ = check_course(source, repo, {1})
            self.assertIn('thumbnail.png is missing', errors)


if __name__ == '__main__':
    unittest.main()
