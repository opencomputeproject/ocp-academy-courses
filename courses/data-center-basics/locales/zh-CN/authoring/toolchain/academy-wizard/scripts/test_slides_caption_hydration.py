"""Imported recording CC must contain usable, language-specific timed cues."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from render_module import _figure_html

def payload(rendered):
    match=re.search(r'<script class="academy-video__caption-data" type="application/json">(.*?)</script>',rendered,re.S)
    return json.loads(match.group(1))['tracks']

class SlidesCaptions(unittest.TestCase):
    def test_real_cli_embeds_path_only_vtt_tracks_without_modifying_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name,text in [('en','English first line.'),('ja','日本語の字幕。')]:
                (root/(name+'.vtt')).write_text('WEBVTT\n\n1\n00:00:03.660 --> 00:00:04.760\n'+text+'\n',encoding='utf-8')
            course={'style':'Slides','course_title':'Caption test','modules':[{'id':1,'title':'Recordings','slides':[{'id':1,'type':'content_diagram','title':'Original recording','audio':None,'narration_enabled':False,'transcript':'Recording transcript','figure':{'role':'original_video','path':'original.mp4','captions':[{'path':'en.vtt','language':'en'},{'path':'ja.vtt','language':'ja'}]}}]}]}
            source=root/'course.json';source.write_text(json.dumps(course));original=source.read_bytes()
            subprocess.run([sys.executable,str(Path(__file__).with_name('render_module.py')),str(source),'--module','1'],check=True,capture_output=True,text=True)
            tracks=payload((root/'module1.html').read_text())
            self.assertEqual(tracks[0]['cues'],[{'start':3.66,'end':4.76,'text':'English first line.'}])
            self.assertEqual(tracks[1]['cues'][0]['text'],'日本語の字幕。')
            self.assertEqual(source.read_bytes(),original)

    def test_per_track_cues_override_legacy_single_track_fallback(self):
        tracks=payload(_figure_html({'role':'original_video','path':'original.mp4','caption_cues':[{'start':0,'end':2,'text':'Legacy fallback'}],'captions':[{'path':'en.vtt','language':'en','_cues':[{'start':1,'end':3,'text':'English'}]},{'path':'ja.vtt','language':'ja','_cues':[{'start':1,'end':3,'text':'日本語'}]}]}))
        self.assertEqual([t['cues'][0]['text'] for t in tracks],['English','日本語'])

    def test_legacy_embedded_cues_still_render(self):
        cues=[{'start':3.66,'end':4.76,'text':'Welcome back.'}]
        tracks=payload(_figure_html({'role':'original_video','path':'original.mp4','caption_cues':cues,'captions':[{'path':'en.vtt','language':'en'}]}))
        self.assertEqual(tracks[0]['cues'],cues)

if __name__=='__main__':unittest.main()
