import unittest,tempfile,pathlib,xml.etree.ElementTree as ET
from render_index import render_manifest,render_index_html
from render_module import _figure_html
class NineSCOEdition(unittest.TestCase):
 def setUp(self):self.course={'course_title':'Nine modules','style':'Slides','scorm':{'version':'1.2','include_home_sco':False},'modules':[{'id':i,'title':f'Module {i}','slides':[]} for i in range(1,10)]}
 def test_exactly_nine_scos_and_home_asset(self):
  with tempfile.TemporaryDirectory() as d:xml=ET.fromstring(render_manifest(self.course,pathlib.Path(d)))
  ns={'i':'http://www.imsproject.org/xsd/imscp_rootv1p1p2'};a='{http://www.adlnet.org/xsd/adlcp_rootv1p2}scormtype'
  resources=xml.findall('i:resources/i:resource',ns)
  self.assertEqual(9,sum(r.get(a)=='sco' for r in resources));self.assertEqual(9,len(xml.findall('.//i:organization/i:item',ns)))
  self.assertEqual('asset',next(x for x in resources if x.get('href')=='index.html').get(a))
 def test_home_does_not_take_over_module_session(self):
  h=render_index_html(self.course)
  self.assertIn('const homeIsSCO = false;',h);self.assertIn('!reviewMode && homeIsSCO && SCORM.init()',h)
  self.assertIn('!reviewMode && homeIsSCO) SCORM.setCompleted()',h)
  self.assertIn('!reviewMode && homeIsSCO) SCORM.finish()',h)
 def test_recording_controls_and_sound(self):
  h=_figure_html({'path':'original.mp4','playback_mode':'recorded','controls':True,'autoplay':False,'loop':False,'muted':False})
  video=h.split('<video ',1)[1].split('>',1)[0]
  self.assertIn('data-recorded-player',h);self.assertNotIn(' controls',video);self.assertNotIn(' autoplay',video);self.assertNotIn(' muted',video);self.assertNotIn(' loop',video)
  self.assertNotIn('figure-video-controls',h)
  self.assertEqual(h.count('data-video-action="toggle"'),1)
  self.assertEqual(h.count('data-video-action="fullscreen"'),1)
  self.assertNotIn('data-video-zoom',h)
if __name__=='__main__':unittest.main()
