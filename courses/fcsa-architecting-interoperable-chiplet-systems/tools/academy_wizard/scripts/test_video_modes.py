"""Explicit opt-in and paired-narration validation; no media generation."""
import json,tempfile,unittest
from pathlib import Path
from html.parser import HTMLParser
from render_module import _figure_html,render_module
from render_index import render_index_html
from slides_course_qa import check_course
class Tags(HTMLParser):
 def __init__(self,t):super().__init__();self.video={};self.feed(t)
 def handle_starttag(self,tag,attrs):
  if tag=='video':self.video=dict(attrs)
class VideoModes(unittest.TestCase):
 def test_old_markup_defaults_and_false_flag(self):
  base={'path':'v.mp4'}
  for flag in [None,False,'false','true',1]:
   fig=dict(base)
   if flag is not None:fig['sync_to_narration']=flag
   attrs=Tags(_figure_html(fig)).video
   self.assertNotIn('data-narration-sync',attrs)
   for name in ['autoplay','loop','muted']:self.assertIn(name,attrs)
 def test_explicit_opt_in(self):
  attrs=Tags(_figure_html({'path':'v.mp4','sync_to_narration':True,'autoplay':False,'loop':False,'muted':True})).video
  self.assertEqual(attrs['data-narration-sync'],'true');self.assertNotIn('autoplay',attrs);self.assertNotIn('loop',attrs);self.assertIn('muted',attrs)
 def test_authored_legacy_settings_remain(self):
  attrs=Tags(_figure_html({'path':'v.mp4','autoplay':False,'loop':False,'muted':False})).video
  for name in ['autoplay','loop','muted','data-narration-sync']:self.assertNotIn(name,attrs)
 def test_synced_requires_boolean_and_paired_audio(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'v.mp4').touch();(root/'v.png').touch()
   fig={'path':'v.mp4','poster':'v.png','media_type':'video','alt':'Voltage rise','caption':'Charging precedes enable.','sync_to_narration':True,'autoplay':False,'loop':False,'muted':True}
   slide={'id':1,'type':'content_diagram','figure':fig};c={'modules':[{'id':1,'slides':[slide]}]};p=root/'course.json'
   def errors():p.write_text(json.dumps(c));return check_course(p,None,set())[0]
   self.assertTrue(any('paired narration' in e for e in errors()))
   slide['audio']={'wav_file':'a.wav'};self.assertEqual(errors(),[])
   fig['sync_to_narration']='true';self.assertTrue(any('must be a boolean' in e for e in errors()))
 def test_optional_local_font_delivery(self):
  c={'course_title':'Test','modules':[{'id':1,'title':'Test','slides':[{'id':1,'type':'title','title':'Test'}]}]}
  for render in [lambda:render_module(c,0),lambda:render_index_html(c)]:
   self.assertIn('fonts.googleapis.com',render());c['local_font_stylesheet']='assets/fonts/open-sans.css';t=render();self.assertNotIn('fonts.googleapis.com',t);self.assertIn('href="assets/fonts/open-sans.css"',t);del c['local_font_stylesheet']
if __name__=='__main__':unittest.main()
