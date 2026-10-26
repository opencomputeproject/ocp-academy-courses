import json,tempfile,unittest
from pathlib import Path
from validate_package import _narration_caption_fallback_count as count,_validate_source_caption_files as validate
class NarrationCaptionValidation(unittest.TestCase):
 def payload(self,cues,clock='narration'):
  return '<script type="application/json" data-figure-caption-tracks>'+json.dumps([{'time_source':clock,'cues':cues}])+'</script>'
 def test_valid_narration_clock_is_accepted(self):
  self.assertEqual(count(self.payload([{'start':0,'end':2,'text':'ダイ間リンク'}])),1)
 def test_missing_or_video_clock_payload_is_not_an_exception(self):
  self.assertEqual(count(''),0)
  self.assertEqual(count(self.payload([{'start':0,'end':2,'text':'ダイ間リンク'}],'video')),0)
 def test_bad_payloads_never_hide_a_missing_caption_file(self):
  for cues in [[],[{'start':2,'end':1,'text':'text'}],[{'start':0,'end':1,'text':''}],[{'start':0,'end':2,'text':'A'},{'start':1,'end':3,'text':'B'}],[{'start':True,'end':2,'text':'A'}]]:
   self.assertEqual(count(self.payload(cues)),0)
  self.assertEqual(count('<script data-figure-caption-tracks>{bad}</script>'),0)
 def test_vtt_resources_are_still_required(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);course={'modules':[{'slides':[{'figure':{'captions_time_source':'narration','captions':[{'path':'ja.vtt'}]}}]}]}
   self.assertEqual(len(validate(course,root)),1)
   (root/'ja.vtt').write_text('WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nダイ間リンク\n')
   self.assertEqual(validate(course,root),[])
   (root/'ja.vtt').write_text('WEBVTT\n')
   self.assertEqual(len(validate(course,root)),1)
if __name__=='__main__':unittest.main()
