"""Protect Home-first syllabus ordering independently of content-module counts."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree as ET
from render_index import render_index_html,render_manifest
from slides_syllabus import include_home_sco,validate
from zip_for_lms import package

IMS='http://www.imsproject.org/xsd/imscp_rootv1p1p2'
ADL='http://www.adlnet.org/xsd/adlcp_rootv1p2'

class SlidesSyllabusTests(unittest.TestCase):
    def setUp(self):
        self.course={'style':'Slides','course_title':'Five modules','course_slug':'five-modules','motion_intro':{'enabled':False},'scorm':{'version':'1.2','organization':'multi-sco'},'modules':[{'id':n,'title':f'Topic {n}','slides':[]} for n in range(1,6)]}
    def tree(self):return ET.ElementTree(ET.fromstring(render_manifest(self.course,Path('.'))))
    def org(self,tree):return tree.find(f'.//{{{IMS}}}organization')
    def test_five_content_modules_have_six_scos_with_home_first(self):
        tree=self.tree();resources={e.get('identifier'):e for e in tree.iter(f'{{{IMS}}}resource')}
        items=self.org(tree).findall(f'{{{IMS}}}item')
        self.assertEqual([resources[e.get('identifierref')].get('href') for e in items],['index.html',*[f'module{n}.html' for n in range(1,6)]])
        self.assertEqual(items[0].findtext(f'{{{IMS}}}title'),'Course Home')
        self.assertEqual(len([e for e in resources.values() if e.get(f'{{{ADL}}}scormtype')=='sco']),6)
        self.assertEqual(validate(self.course,tree),[])
    def test_false_flag_alone_does_not_authorize_home_omission(self):
        self.course['scorm'].update(include_home_sco=False,expected_sco_count=5)
        with self.assertRaisesRegex(ValueError,'Home/index-specific'):self.tree()
    def test_generic_module_count_is_not_home_specific_authorization(self):
        self.course['scorm'].update(include_home_sco=False,home_sco_omission={'approved':True,'user_instruction':'Package five modules as five SCOs.'})
        with self.assertRaisesRegex(ValueError,'Home/index-specific'):self.tree()
    def test_authorized_home_omission_is_preserved(self):
        self.course['scorm'].update(include_home_sco=False,expected_sco_count=5,home_sco_omission={'approved':True,'user_instruction':'Omit Course Home from the syllabus; keep index.html untracked.'})
        self.assertFalse(include_home_sco(self.course));self.assertEqual(validate(self.course,self.tree()),[])
    def test_expected_sco_count_includes_home(self):
        self.course['scorm']['expected_sco_count']=5
        with self.assertRaisesRegex(ValueError,'requires 6'):self.tree()
        self.course['scorm']['expected_sco_count']=6;self.assertEqual(validate(self.course,self.tree()),[])
    def test_validator_detects_missing_home_syllabus_item(self):
        tree=self.tree();org=self.org(tree);org.remove(org.findall(f'{{{IMS}}}item')[0])
        self.assertTrue(any('order/count' in e for e in validate(self.course,tree)))
    def test_validator_detects_home_later_in_syllabus(self):
        tree=self.tree();org=self.org(tree);home=org.findall(f'{{{IMS}}}item')[0];org.remove(home);org.append(home)
        self.assertTrue(any('order/count' in e for e in validate(self.course,tree)))
    def test_validator_detects_home_downgraded_to_asset(self):
        tree=self.tree();next(e for e in tree.iter(f'{{{IMS}}}resource') if e.get('href')=='index.html').set(f'{{{ADL}}}scormtype','asset')
        self.assertTrue(validate(self.course,tree))
    def test_zipper_rejects_a_stale_five_entry_manifest(self):
        self.course['lms_catalog']={'title':'Five modules','short_description':'A five-module course.','overview':'Test overview.','duration_minutes':10,'duration_basis':'estimated_learner_time','modules':[{'id':n,'duration_minutes':2,'summary':'Learn the topic.'} for n in range(1,6)]}
        with tempfile.TemporaryDirectory() as name:
            root=Path(name);(root/'course.json').write_text(json.dumps(self.course));(root/'index.html').write_text(render_index_html(self.course))
            tree=self.tree();org=self.org(tree);org.remove(org.findall(f'{{{IMS}}}item')[0]);tree.write(root/'imsmanifest.xml',encoding='unicode')
            with self.assertRaisesRegex(ValueError,'syllabus order/count'):package(root)
    def test_single_sco_and_scrolling_organizations_are_unaffected(self):
        for style,mode in [('Slides','single-sco'),('Scrolling','single-sco')]:
            c=deepcopy(self.course);c['style']=style;c['scorm']['organization']=mode
            self.assertEqual(validate(c,self.tree()),[])

if __name__=='__main__':unittest.main()
