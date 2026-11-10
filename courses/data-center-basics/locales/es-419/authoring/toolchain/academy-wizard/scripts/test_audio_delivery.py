"""Regression: compressed delivery never replaces authoring WAV metadata."""
import copy
import re
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
from render_module import render_module
from render_index import render_manifest


class AudioDeliveryTests(unittest.TestCase):
    def course(self):
        return {
            'style': 'Slides', 'course_slug': 'audio_delivery_test',
            'course_title': 'Audio delivery test',
            'scorm': {'version': '1.2', 'organization': 'multi-sco',
                      'include_home_sco': True, 'expected_sco_count': 2},
            'modules': [{'id': 1, 'title': 'Module one', 'slides': [{
                'id': 1, 'type': 'title', 'title': 'One',
                'audio': {'script_file': 'audio/one.txt', 'wav_file': 'audio/one.wav'},
            }]}],
        }

    def runtime_paths(self, course):
        html = render_module(course, 0)
        audio_map = re.search(r'const audioMap\s*=\s*\{([^}]*)\}', html, re.S).group(1)
        with tempfile.TemporaryDirectory() as folder:
            manifest = ET.fromstring(render_manifest(course, Path(folder)))
        files = {node.get('href') for node in manifest.iter() if node.tag.rsplit('}', 1)[-1] == 'file'}
        return audio_map, files

    def test_wav_default_is_unchanged(self):
        audio_map, files = self.runtime_paths(self.course())
        self.assertIn('audio/one.wav', audio_map)
        self.assertIn('audio/one.wav', files)

    def test_mp3_delivery_excludes_master_without_mutating_source(self):
        course = self.course()
        course['modules'][0]['slides'][0]['audio']['delivery_file'] = 'audio/one.mp3'
        before = copy.deepcopy(course)
        audio_map, files = self.runtime_paths(course)
        self.assertIn('audio/one.mp3', audio_map)
        self.assertNotIn('audio/one.wav', audio_map)
        self.assertIn('audio/one.mp3', files)
        self.assertNotIn('audio/one.wav', files)
        self.assertEqual(course, before)

    def test_empty_delivery_falls_back(self):
        course = self.course()
        course['modules'][0]['slides'][0]['audio']['delivery_file'] = ''
        audio_map, files = self.runtime_paths(course)
        self.assertIn('audio/one.wav', audio_map)
        self.assertIn('audio/one.wav', files)

    def test_disabled_slide_narration_is_not_delivered(self):
        course = self.course()
        course['modules'][0]['slides'][0]['narration_enabled'] = False
        audio_map, files = self.runtime_paths(course)
        self.assertNotIn('audio/one.wav', audio_map)
        self.assertNotIn('audio/one.wav', files)

    def test_original_recording_does_not_gain_slide_audio(self):
        course = self.course()
        course['modules'][0]['slides'][0]['figure'] = {
            'path': 'video.mp4', 'role': 'original_video', 'media_type': 'video',
        }
        audio_map, files = self.runtime_paths(course)
        self.assertNotIn('audio/one.wav', audio_map)
        self.assertNotIn('audio/one.wav', files)


if __name__ == '__main__':
    unittest.main()

