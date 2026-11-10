"""Protect the distinct teaching-animation and imported-recording players."""
import unittest
from render_module import _figure_html
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
if __name__=='__main__':unittest.main()
