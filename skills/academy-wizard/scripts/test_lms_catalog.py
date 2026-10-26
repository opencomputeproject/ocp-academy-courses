"""Observable LMS metadata, localized formatting, and ZIP delivery contracts."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from course_delivery_summary import catalog_metadata, catalog_files, write_catalog, MARKDOWN_BREAK
from zip_for_lms import package


def fixture():
    return {'style':'Slides','language':'en-US','course_slug':'test','course_title':'Visible course title',
            'course_subtitle':'This is not the approved LMS short description.', 'target_duration_minutes':30,
            'modules':[{'id':11,'title':'Context'},{'id':22,'title':'Review'}],
            'lms_catalog':{'title':'Full formal LMS series title','short_description':'A concise LMS description.',
                           'overview':'An overview for prospective learners.', 'duration_minutes':30,
                           'duration_basis':'estimated_learner_time',
                           'modules':[{'id':11,'duration_minutes':10,'summary':'Explain the system context.'},
                                      {'id':22,'duration_minutes':20,'summary':'Review the integration evidence.'}]}}


class CatalogTests(unittest.TestCase):
    def test_approved_lms_fields_not_course_subtitle_or_readme(self):
        course=fixture();course['README.md']='Editorial instructions, not a description.'
        result=catalog_metadata(course)
        self.assertEqual(result['title'],course['lms_catalog']['title'])
        self.assertEqual(result['short_description'],course['lms_catalog']['short_description'])
        self.assertNotIn(course['course_subtitle'],result['long_description'])
        self.assertNotIn(course['README.md'],json.dumps(result))
        self.assertEqual(result['duration_minutes'],30)

    def test_unicode_limit_and_no_silent_truncation(self):
        course=fixture();course['lms_catalog']['short_description']='あ'*130
        self.assertEqual(catalog_metadata(course)['short_description_characters'],130)
        course['lms_catalog']['short_description']+='い'
        with self.assertRaisesRegex(ValueError,'at most 130'):catalog_metadata(course)

    def test_unit_order_ids_and_duration_reconciliation(self):
        course=fixture();course['lms_catalog']['modules'].reverse()
        self.assertEqual([r['id'] for r in catalog_metadata(course)['modules']],[11,22])
        course['lms_catalog']['modules'][0]['duration_minutes']=21
        with self.assertRaisesRegex(ValueError,'durations total'):catalog_metadata(course)
        for value in [0,-1,True,float('nan'),float('inf')]:
            bad=fixture();bad['lms_catalog']['duration_minutes']=value
            with self.assertRaises(ValueError):catalog_metadata(bad)
        bad=fixture();bad['lms_catalog']['modules'].append(copy.deepcopy(bad['lms_catalog']['modules'][0]))
        with self.assertRaisesRegex(ValueError,'Duplicate'):catalog_metadata(bad)
        bad=fixture();bad['lms_catalog']['modules'][0]['id']=99
        with self.assertRaisesRegex(ValueError,'ids must match'):catalog_metadata(bad)

    def test_module_heading_has_line_break_before_summary_in_both_formats(self):
        result=catalog_metadata(fixture())
        self.assertIn('minutes.**'+MARKDOWN_BREAK+'Explain the system context.',result['long_description'])
        self.assertIn('</strong><br>\nExplain the system context.</p>',result['long_description_html'])
        self.assertLess(result['long_description'].index('An overview'),result['long_description'].index('Overall duration'))

    def test_source_check_catches_stale_exports_without_changing_them(self):
        with tempfile.TemporaryDirectory() as temp:
            course=fixture();paths=write_catalog(course,temp)
            before={p.name:p.read_bytes() for p in paths}
            write_catalog(course,temp,check=True)
            course['lms_catalog']['modules'][0]['summary']='A revised summary.'
            with self.assertRaisesRegex(ValueError,'stale'):write_catalog(course,temp,check=True)
            self.assertEqual(before,{p.name:p.read_bytes() for p in paths})

    def test_scrolling_uses_authored_lessons(self):
        course=fixture();course['style']='Scrolling';course['lessons']=course.pop('modules')
        course['lms_catalog']['lessons']=course['lms_catalog'].pop('modules')
        result=catalog_metadata(course)
        self.assertIn('Lesson 1: Context',result['long_description'])
        self.assertIn('lessons',result)

    def test_localized_catalog_labels_and_html_escaping(self):
        course=fixture();course['language']='ja-JP'
        with self.assertRaisesRegex(ValueError,'translated'):catalog_metadata(course)
        course['lms_catalog']['labels']={'title':'タイトル','short_description':'短い説明','long_description':'詳しい説明',
                'overall_duration':'合計所要時間: {duration}分','unit_heading':'モジュール {number}: {title} — {duration}分'}
        course['lms_catalog']['title']='Chiplets <Review> & Evidence'
        result=catalog_files(course,include_html=True)
        self.assertIn('**合計所要時間: 30分**',result['lms-catalog.md'])
        self.assertIn('Chiplets &lt;Review&gt; &amp; Evidence',result['lms-catalog.html'])
        self.assertIn('<br>\n',result['lms-catalog.html'])

    def test_missing_metadata_cannot_fall_back_to_editorial_docs(self):
        course=fixture();del course['lms_catalog']
        with self.assertRaisesRegex(ValueError,'Missing'):catalog_metadata(course)


class PackagingTests(unittest.TestCase):
    def make_runtime(self,root,course):
        source=root/'course.json';source.write_text(json.dumps(course))
        (root/'README.md').write_text('Maintenance notes, not LMS catalog copy.')
        runtime=root/'SCORM';runtime.mkdir()
        (runtime/'imsmanifest.xml').write_text('<manifest xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"><resources><resource><file href="index.html"/></resource></resources></manifest>')
        (runtime/'index.html').write_text('<h1>Runtime</h1>')
        return source,runtime

    def test_zip_and_separate_sidecars_use_same_approved_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source,runtime=self.make_runtime(root,fixture())
            output,sidecars,count=package(runtime,root/'course.zip')
            self.assertEqual(count,2)
            with zipfile.ZipFile(output) as archive:
                self.assertEqual(set(archive.namelist()),{'imsmanifest.xml','index.html'})
                self.assertIsNone(archive.testzip())
            self.assertEqual({p.suffix for p in sidecars},{'.json','.md','.html'})
            delivered=json.loads((root/'course.lms-catalog.json').read_text())
            tracked=json.loads((root/'lms-catalog.json').read_text())
            self.assertEqual(delivered,tracked)
            self.assertEqual(delivered['title'],'Full formal LMS series title')
            self.assertNotIn('Maintenance notes',(root/'course.lms-catalog.md').read_text())

    def test_invalid_description_preserves_existing_zip(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);course=fixture();course['lms_catalog']['short_description']='x'*131
            source,runtime=self.make_runtime(root,course);output=root/'course.zip';output.write_bytes(b'prior delivery')
            with self.assertRaisesRegex(ValueError,'at most 130'):package(runtime,output)
            self.assertEqual(output.read_bytes(),b'prior delivery')
            self.assertFalse((root/'course.lms-catalog.md').exists())

    def test_explicit_source_for_separate_build_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source,runtime=self.make_runtime(root,fixture())
            independent=root/'other';independent.mkdir();moved=independent/'runtime';runtime.rename(moved)
            with self.assertRaisesRegex(ValueError,'course.json'):package(moved,independent/'test.zip')
            result=package(moved,independent/'test.zip',source)
            self.assertTrue(result[0].is_file())


if __name__=='__main__':unittest.main()
