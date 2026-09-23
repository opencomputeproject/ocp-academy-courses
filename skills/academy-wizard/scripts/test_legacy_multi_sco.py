"""Preservation checks for the approved, opt-in module-only deployment."""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest

import legacy_multi_sco
from render_module import render_module

SKILL = Path(__file__).resolve().parent.parent


class LegacyMultiSCOTests(unittest.TestCase):
    def setUp(self):
        self.course = {
            'style': 'Slides', 'course_slug': 'legacy-test', 'course_title': 'Test',
            'motion_intro': {'enabled': False},
            'scorm': {'version': '1.2', 'organization': 'multi-sco',
                      'navigation': 'direct', 'compatibility_profile': 'hbf-module-only'},
            'modules': [{'id': 1, 'title': 'One', 'slides': [
                {'id': 1, 'type': 'title', 'title': 'One'},
                {'id': 2, 'type': 'course_complete'}]}]}

    def test_absent_profile_preserves_default(self):
        self.assertFalse(legacy_multi_sco.enabled({}))
        del self.course['scorm']['compatibility_profile']
        result = render_module(self.course, 0)
        self.assertIn('const BOOKMARK_KEY', result)
        self.assertIn('SCORM.getLocation()', result)
        self.assertIn('lms-navigation-note', result)

    def test_profile_requires_approved_combination(self):
        self.assertTrue(legacy_multi_sco.enabled(self.course))
        for key, value in [('version', '2004'), ('organization', 'single-sco'),
                           ('navigation', None), ('compatibility_profile', 'unknown')]:
            course = deepcopy(self.course)
            course['scorm'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                legacy_multi_sco.enabled(course)
        self.course['style'] = 'Scrolling'
        with self.assertRaises(ValueError):
            legacy_multi_sco.enabled(self.course)

    def test_rejects_deployment_maps_and_diagnostics(self):
        for key in ('docebo_navigation', 'diagnostic_navigation'):
            course = deepcopy(self.course)
            course['scorm'][key] = {'enabled': True}
            with self.subTest(key=key), self.assertRaises(ValueError):
                legacy_multi_sco.enabled(course)

    def test_module_only_runtime_and_review_preserved(self):
        result = render_module(self.course, 0)
        self.assertIn('href="index.html" aria-label="Course home"', result)
        self.assertIn("if (inLMS) SCORM.setLocation('module'", result)
        self.assertIn("window.addEventListener('academy:slide', updateTranscript)", result)
        self.assertIn("url.searchParams.set('review', '1')", result)
        for text in ('BOOKMARK_KEY', 'SCORM.getLocation()', 'storeBookmark',
                     'Use the LMS course navigation', 'TEST ONLY', '/learn/courses/'):
            self.assertNotIn(text, result)

    def test_original_wrapper_is_preserved(self):
        self.assertEqual(hashlib.sha256((SKILL / 'assets/scorm_api_hbf.js').read_bytes()).hexdigest(),
                         '47280be7e47182ca2a2283c479180fe8b9b5a60da866a99dcca01baaf3cf2ffb')

    def test_scaffold_selects_wrapper_only_for_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'course.json'
            for profile in (True, False):
                course = deepcopy(self.course)
                if not profile:
                    del course['scorm']['compatibility_profile']
                source.write_text(json.dumps(course))
                out = root / ('legacy' if profile else 'default')
                subprocess.run([sys.executable, str(SKILL / 'scripts/new_course.py'),
                                str(out), str(source)], check=True, capture_output=True)
                expected = SKILL / 'assets' / ('scorm_api_hbf.js' if profile else 'scorm_api.js')
                self.assertEqual((out / 'scorm_api.js').read_bytes(), expected.read_bytes())


if __name__ == '__main__':
    unittest.main()
