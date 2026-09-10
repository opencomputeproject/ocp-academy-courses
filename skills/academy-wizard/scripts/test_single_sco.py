"""The opt-in mode changes packaging, not other courses' defaults or media."""
import copy
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

import render_index
import single_sco


class SingleSCOTests(unittest.TestCase):
    def setUp(self):
        self.course = {"style": "Slides", "course_slug": "test", "course_title": "Course & Test",
                       "motion_intro": {"enabled": False}, "modules": [
                           {"id": i, "title": f"Module {i}", "slides": [
                               {"id": 1, "type": "content_diagram", "figure": {"path": f"figures/m{i}.svg"}},
                               {"id": 2, "type": "knowledge_check", "questions": [{"id": f"m{i}_q1"}, {"id": f"m{i}_q2"}]}]}
                           for i in (1, 2)]}

    def single(self):
        course = copy.deepcopy(self.course)
        course["scorm"] = {"version": "1.2", "organization": "single-sco"}
        return course

    def test_legacy_default_remains_multi_sco(self):
        self.assertFalse(single_sco.enabled(self.course))
        root = ET.fromstring(render_index.render_manifest(self.course, Path('.')))
        self.assertEqual(len(list(root.iter(f'{{{single_sco.IMS}}}item'))), 3)
        self.assertEqual(root.findtext(f'{{{single_sco.IMS}}}metadata/{{{single_sco.IMS}}}schemaversion'), '1.2')

    def test_single_has_one_launch_and_all_legacy_assets(self):
        multi = ET.fromstring(render_index.render_manifest(self.course, Path('.')))
        root = ET.fromstring(render_index.render_manifest(self.single(), Path('.')))
        files = lambda tree: {n.get('href') for n in tree.iter(f'{{{single_sco.IMS}}}file')}
        self.assertEqual(files(root), files(multi) | {'launch.html', 'single_sco_runtime.js'})
        resources = list(root.iter(f'{{{single_sco.IMS}}}resource'))
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0].get('href'), 'launch.html')
        self.assertEqual(len(list(root.iter(f'{{{single_sco.IMS}}}item'))), 1)

    def test_course_data_is_not_mutated(self):
        course = self.single()
        before = copy.deepcopy(course)
        render_index.render_manifest(course, Path('.'))
        self.assertEqual(course, before)

    def test_unimplemented_version_is_rejected(self):
        course = self.single()
        course['scorm']['version'] = '2004'
        with self.assertRaisesRegex(ValueError, 'Only SCORM 1.2'):
            render_index.render_manifest(course, Path('.'))

    def test_quiz_requirements_are_preserved(self):
        self.assertEqual(single_sco.configuration(self.single())['modules'][1]['quizzes'], ['m2_q1', 'm2_q2'])

    def test_storage_overflow_is_rejected_before_build(self):
        course = self.single()
        course['modules'][0]['slides'][1]['questions'][0]['id'] = 'q' * 4096
        with self.assertRaisesRegex(ValueError, '4096-character'):
            single_sco.configuration(course)

    def test_question_ids_cannot_collide_between_modules(self):
        course = self.single()
        course['modules'][1]['slides'][1]['questions'][0]['id'] = 'm1_q1'
        with self.assertRaisesRegex(ValueError, 'unique across all modules'):
            single_sco.configuration(course)

    def test_validator_rejects_multi_sco_and_missing_shell(self):
        with tempfile.TemporaryDirectory() as folder:
            tree = ET.ElementTree(ET.fromstring(render_index.render_manifest(self.course, Path(folder))))
            issues = single_sco.validate(self.single(), tree, Path(folder))
            self.assertTrue(any('exactly one' in issue for issue in issues))
            self.assertTrue(any('launch.html' in issue for issue in issues))


if __name__ == '__main__':
    unittest.main()
