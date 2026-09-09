"""Source-only regression checks; no TTS requests or audio playback."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from gen_audio import iter_module_slides, pick_elevenlabs_speed
from render_module import fill_missing_transcripts, render_content_diagram, render_module
from render_scrolling import render_scrolling_course


class SlidesPortabilityTests(unittest.TestCase):
    def test_default_and_recorded_speed_precedence(self):
        with patch.dict('os.environ', {}, clear=True):
            self.assertEqual((1.18, 'maintained default'), pick_elevenlabs_speed({}))
        with patch.dict('os.environ', {'ELEVENLABS_SPEED':'1.05'}, clear=True):
            self.assertEqual(1.05, pick_elevenlabs_speed({})[0])
            self.assertEqual(1.18, pick_elevenlabs_speed({'narration':{'speed':1.18}})[0])

    def test_invalid_speed_is_blocked(self):
        for speed in ['slow', 0.69, 1.21, float('nan')]:
            with self.subTest(speed=speed), self.assertRaises(ValueError):
                pick_elevenlabs_speed({'narration':{'speed':speed}})

    def test_targeted_audio_selects_one_slide(self):
        course={'modules':[{'id':m,'slides':[{'id':s} for s in [1,2,3]]} for m in [1,2]]}
        self.assertEqual([(2,3)], [(m['id'],s['id']) for m,s in iter_module_slides(course,2,3)])

    def test_legacy_transcript_fallback_preserves_authored_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'script.txt').write_text('# pronunciation comment\n\nA real teaching sentence.\n')
            slides=[{'audio':{'script_file':'script.txt'}},
                    {'audio':{'script_file':'script.txt'},'transcript':'Authored display text.'},
                    {'audio':{'script_file':'missing.txt'}}]
            course={'modules':[{'slides':slides}]}
            fill_missing_transcripts(course,root)
            self.assertEqual('A real teaching sentence.',slides[0]['transcript'])
            self.assertEqual('Authored display text.',slides[1]['transcript'])
            self.assertNotIn('transcript',slides[2])

    def test_media_focus_is_explicit(self):
        slide={'id':2,'type':'content_diagram','title':'Diagram','figure':{'path':'figure.svg'}}
        self.assertNotIn('slide--media-focus',render_content_diagram(slide,{},{}))
        slide['media_focus']=True
        self.assertIn('slide--media-focus',render_content_diagram(slide,{},{}))

    def test_localized_navigation_hints_are_retained(self):
        course={'course_title':'Test','language':'ja-JP','ui_labels':{'previous_slide_hint':'前のスライド','next_slide_hint':'次のスライド','slide_counter_hint':'矢印キーで移動'},
                'modules':[{'id':1,'title':'Test','slides':[{'id':1,'type':'title','title':'Test'},{'id':2,'type':'course_complete'}]}]}
        result=render_module(course,0)
        for text in course['ui_labels'].values():self.assertIn(text,result)

    def test_scrolling_still_renders_without_slides_glossary_gate(self):
        course={'style':'Scrolling','course_title':'Reading course','course_slug':'reading',
                'lessons':[{'id':1,'title':'Introduction','slug':'intro','blocks':[{'type':'text','body_html':'<p>Read this lesson.</p>'}]}]}
        result=render_scrolling_course(course)
        self.assertIn('Read this lesson.',result)
        self.assertNotIn('id="transcriptBtn"',result)


if __name__=='__main__':
    unittest.main()
