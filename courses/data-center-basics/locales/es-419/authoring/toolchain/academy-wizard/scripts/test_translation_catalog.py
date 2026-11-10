"""A concise README layout must not change translation-series naming."""
import json
from pathlib import Path
import tempfile
import unittest

from update_translation_catalog import collect_translations, repository_layout_series_folders


class TranslationLayoutTests(unittest.TestCase):
    def test_flat_and_detailed_layouts_preserve_series_and_standalone_titles(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for folder, title, translated in [
                ('optics/first', 'First course', True),
                ('optics/second', 'Second course', False),
                ('standalone', 'Standalone course', True),
            ]:
                source = root / 'courses' / folder
                source.mkdir(parents=True)
                (source / 'course.json').write_text(json.dumps({'course_title': title}))
                if translated:
                    locale = source / 'locales' / 'zh-CN'
                    locale.mkdir(parents=True)
                    (locale / 'course.json').write_text('{"language":"zh-CN"}')
            for layout in [
                'courses/\n  optics/\n  standalone/',
                'courses/\n  optics/\n    first/\n    second/\n  standalone/\n    figures/\n    audio/',
            ]:
                readme = '## Repository layout\n\n```text\n'+layout+'\n```\n'
                (root / 'README.md').write_text(readme)
                self.assertEqual(repository_layout_series_folders(readme, root), {'optics'})
                self.assertEqual(sorted(t.course_title for t in collect_translations(root)),
                                 ['Optics: First course', 'Standalone course'])

    def test_one_child_is_not_a_multicourse_series(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'courses' / 'group' / 'only'
            source.mkdir(parents=True)
            (source / 'course.json').write_text('{}')
            self.assertEqual(repository_layout_series_folders(
                '## Repository layout\n\n```text\ncourses/\n  group/\n```\n', root), set())


if __name__ == '__main__':
    unittest.main()
