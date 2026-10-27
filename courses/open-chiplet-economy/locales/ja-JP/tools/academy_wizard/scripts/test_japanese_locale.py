"""Japanese words have no whitespace delimiters; looped CC has a speech clock."""
import unittest
from glossary_audit import match_term
from render_module import _figure_caption_tracks
class JapaneseLocale(unittest.TestCase):
 def test_terms_in_unspaced_japanese(self):
  self.assertEqual(match_term({'term':'チップレット'},'チップレットを組み立てる。'),'チップレット')
  self.assertEqual(match_term({'term':'PHY'},'PHYとチャネルの条件。'),'PHY')
  self.assertIsNone(match_term({'term':'PHY'},'PHYSICS'))
 def test_narration_clock_does_not_start_a_native_vtt_load(self):
  track={'path':'captions/test.ja.vtt','language':'ja-JP','label':'日本語','_cues':[{'start':1,'end':3,'text':'ダイ間リンク'}]}
  tags,data=_figure_caption_tracks({'captions':[track],'captions_time_source':'narration'})
  self.assertNotIn(' src=',tags)
  self.assertIn('"time_source": "narration"',data)
  tags,data=_figure_caption_tracks({'captions':[track]})
  self.assertIn('src="captions/test.ja.vtt"',tags)
  self.assertIn('"time_source": "video"',data)
if __name__=='__main__':unittest.main()
