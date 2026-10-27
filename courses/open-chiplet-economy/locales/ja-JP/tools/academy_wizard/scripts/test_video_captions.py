"""Caption resources, default language, safe cue embedding, and SCO ownership."""
import json
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from render_index import render_manifest
from render_module import _figure_html, _figure_caption_control
from render_scrolling import scrolling_video_icon
from render_scrolling import hydrate_caption_cues


class VideoCaptions(unittest.TestCase):
    def test_recording_has_direct_cc_in_bottom_toolbar_and_no_top_controls(self):
        figure = {'path': 'v.mp4', 'playback_mode': 'recorded', 'controls': True,
                  'autoplay': False, 'muted': False, 'loop': False,
                  'captions': [{'path': 'en.vtt', 'label': 'English', 'language': 'en',
                   'default': False, '_cues': [{'start': 1, 'end': 2, 'text': 'A chiplet.'}]}]}
        markup = _figure_html(figure)
        controls = markup.split('<div class="academy-video__controls">', 1)[1]
        self.assertIn('data-video-menu-button="captions"', controls)
        self.assertIn(scrolling_video_icon('captions'), controls)
        self.assertLess(controls.index('data-video-menu-button="captions"'), controls.index('data-video-action="fullscreen"'))
        self.assertNotIn('figure-video-controls', markup)
        self.assertNotIn('data-video-zoom', markup)
        self.assertEqual(markup.count('data-video-action="toggle"'), 1)
        self.assertNotIn('academy-video__big-play', markup)

    def test_optional_cc_control_uses_scrolling_glyph_and_starts_off(self):
        figure = {'path': 'v.mp4', 'captions': [{'path': 'en.vtt', 'label': 'English', 'language': 'en',
                   'default': False, '_cues': [{'start': 1, 'end': 2, 'text': 'A chiplet.'}]}]}
        markup = _figure_html(figure)
        control = _figure_caption_control(figure, {})
        self.assertIn(scrolling_video_icon('captions'), control)
        self.assertIn('data-caption-index="-1" aria-checked="true"', control)
        self.assertIn('data-caption-index="0" aria-checked="false"', control)
        self.assertNotIn('label="English" default', markup)

    def test_native_tracks_and_fallback_come_from_editable_vtt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'english.vtt').write_text('WEBVTT\n\n00:00:01.000 --> 00:00:03.000\nChiplets & packages.\n')
            (root / 'french.vtt').write_text('WEBVTT\n\n00:00:01.000 --> 00:00:03.000\nPuce et boîtier.\n')
            figure = {'path': 'v.mp4', 'captions': [
                {'path': 'english.vtt', 'label': 'English', 'language': 'en', 'default': True},
                {'path': 'french.vtt', 'label': 'Français', 'language': 'fr'}]}
            course = {'modules': [{'id': 1, 'slides': [{'figure': figure}]}]}
            hydrated = hydrate_caption_cues(course, root)
            markup = _figure_html(hydrated['modules'][0]['slides'][0]['figure'])
            self.assertIn('src="english.vtt" srclang="en" label="English" default', markup)
            self.assertIn('src="french.vtt" srclang="fr" label="Français">', markup)
            self.assertEqual(markup.count('kind="captions"'), 2)
            self.assertIn('Chiplets & packages.', markup)
            self.assertNotIn('_cues', json.dumps(course))

    def test_missing_and_invalid_vtt_stop_rendering(self):
        for cues in (None, []):
            track = {'path': 'missing.vtt', 'label': 'English', 'language': 'en', '_cues': cues}
            with self.assertRaisesRegex(ValueError, 'no readable WebVTT cues'):
                _figure_html({'path': 'v.mp4', 'captions': [track]})

    def test_fallback_cannot_close_script_element(self):
        track = {'path': 'a.vtt', 'label': 'English', 'language': 'en',
                 '_cues': [{'start': 0, 'end': 1, 'text': '</script><b>test</b>'}]}
        markup = _figure_html({'path': 'v.mp4', 'captions': [track]})
        self.assertIn('\\u003c/script>', markup)
        self.assertNotIn('</script><b>', markup)

    def test_caption_belongs_to_its_module_resource_only(self):
        course = {'course_title': 'Test', 'scorm': {'include_home_sco': False},
                  'modules': [{'id': 1, 'title': 'One', 'slides': [{'figure': {
                      'path': 'v.mp4', 'captions': [{'path': 'a.vtt'}]}}]},
                              {'id': 2, 'title': 'Two', 'slides': []}]}
        with tempfile.TemporaryDirectory() as tmp:
            xml = ET.fromstring(render_manifest(course, Path(tmp)))
        ns = {'i': 'http://www.imsproject.org/xsd/imscp_rootv1p1p2'}
        owners = [res.get('href') for res in xml.findall('.//i:resource', ns)
                  if res.find('i:file[@href="a.vtt"]', ns) is not None]
        self.assertEqual(owners, ['module1.html'])


if __name__ == '__main__':
    unittest.main()
