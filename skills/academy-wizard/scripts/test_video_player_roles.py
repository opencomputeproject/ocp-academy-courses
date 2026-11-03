"""Protect the distinct teaching-animation and imported-recording players."""
import unittest
from render_module import _figure_html, render_content_diagram
class PlayerRoles(unittest.TestCase):
    def test_generated_modes_keep_standard_figure_controls(self):
        for synced in (False, True):
            with self.subTest(synced=synced):
                rendered=_figure_html({'path':'figures/example.mp4','media_type':'video','sync_to_narration':synced,'muted':True,'loop':not synced,'autoplay':not synced})
                self.assertIn('class="figure-video"',rendered)
                self.assertIn('class="figure-video-controls"',rendered)
                self.assertIn('data-video-toggle',rendered)
                self.assertIn('data-video-zoom',rendered)
                self.assertNotIn('data-video-player',rendered)
                self.assertNotIn('academy-video__controls',rendered)
                self.assertEqual('data-narration-sync="true"' in rendered,synced)
    def test_imported_recording_keeps_exposed_black_player(self):
        rendered=_figure_html({'path':'resources/original.mp4','media_type':'video','role':'original_video'})
        self.assertIn('data-video-player',rendered)
        self.assertIn('academy-video__controls',rendered)
        self.assertIn('class="original-video"',rendered)
        self.assertNotIn('class="figure-video-controls"',rendered)
    def test_media_only_keeps_recording_player_without_slide_copy(self):
        slide={'id':4,'title':'Original recording','media_only':True,
               'section_label':'Watch','caption':'Teaching copy',
               'figure':{'path':'resources/original.mp4','role':'original_video',
                         'media_type':'video','caption':'Metadata caption'}}
        rendered=render_content_diagram(slide,{}, {})
        self.assertIn('data-video-player',rendered)
        self.assertNotIn('<h2',rendered)
        self.assertNotIn('section-label',rendered)
        self.assertNotIn('Metadata caption',rendered)
        self.assertNotIn('Teaching copy',rendered)
        self.assertEqual(slide['figure']['caption'],'Metadata caption')
    def test_media_only_rejects_a_generated_teaching_animation(self):
        with self.assertRaisesRegex(ValueError,'original_video'):
            render_content_diagram({'id':1,'media_only':True,'figure':{'role':'teaching_video'}},{},{})
if __name__=='__main__':unittest.main()
