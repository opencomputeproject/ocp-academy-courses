import json,unittest,tempfile,pathlib,xml.etree.ElementTree as ET
from render_index import render_manifest,render_index_html
from render_module import _figure_html
class CourseHomeSCO(unittest.TestCase):
 def setUp(self):self.course={'course_title':'Nine teaching modules','style':'Slides','scorm':{'version':'1.2','include_home_sco':True},'modules':[{'id':i,'title':f'Module {i}','slides':[]} for i in range(1,10)]}
 def test_current_source_includes_home(self):
  source=pathlib.Path(__file__).resolve().parents[3]/'course.json'
  self.assertIs(json.loads(source.read_text())['scorm'].get('include_home_sco'),True)
 def test_home_is_first_of_ten_scos(self):
  with tempfile.TemporaryDirectory() as d:xml=ET.fromstring(render_manifest(self.course,pathlib.Path(d)))
  ns={'i':'http://www.imsproject.org/xsd/imscp_rootv1p1p2'};a='{http://www.adlnet.org/xsd/adlcp_rootv1p2}scormtype'
  resources=xml.findall('i:resources/i:resource',ns);items=xml.findall('.//i:organization/i:item',ns)
  self.assertEqual(10,sum(r.get(a)=='sco' for r in resources));self.assertEqual(10,len(items))
  self.assertEqual('ITEM_LAUNCHER',items[0].get('identifier'));self.assertEqual('RES_LAUNCHER',items[0].get('identifierref'))
  self.assertEqual('Course Home',items[0].find('i:title',ns).text)
  self.assertEqual('index.html',resources[0].get('href'));self.assertEqual('sco',resources[0].get(a))
  self.assertEqual([f'RES_MODULE{i}' for i in range(1,10)],[item.get('identifierref') for item in items[1:]])
 def test_home_initializes_completes_and_finishes(self):
  h=render_index_html(self.course)
  self.assertIn('const homeIsSCO = true;',h);self.assertIn('!reviewMode && homeIsSCO && SCORM.init()',h)
  self.assertIn('!reviewMode && homeIsSCO) SCORM.setCompleted()',h);self.assertIn('!reviewMode && homeIsSCO) SCORM.finish()',h)
 def test_home_start_remains_clickable_with_an_api(self):
  h=render_index_html(self.course)
  self.assertIn('index-start-link',h);self.assertIn('href="module1.html"',h)
  self.assertNotIn('if (startLink && !homeIsSCO && !reviewMode)',h);self.assertNotIn('if (SCORM.isAvailable())',h)
 def test_recording_controls_and_sound(self):
  h=_figure_html({'path':'original.mp4','playback_mode':'recorded','controls':True,'autoplay':False,'loop':False,'muted':False})
  video=h.split('<video ',1)[1].split('>',1)[0]
  self.assertIn('data-recorded-player',h);self.assertNotIn(' controls',video);self.assertNotIn(' autoplay',video);self.assertNotIn(' muted',video);self.assertNotIn(' loop',video)
  self.assertNotIn('figure-video-controls',h);self.assertEqual(h.count('data-video-action="toggle"'),1)
  self.assertEqual(h.count('data-video-action="fullscreen"'),1);self.assertNotIn('data-video-zoom',h)
if __name__=='__main__':unittest.main()
