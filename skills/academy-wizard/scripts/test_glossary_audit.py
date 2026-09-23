"""Regression tests for actual glossary usage, not metadata keyword presence."""
import hashlib
import tempfile
import unittest
from pathlib import Path
from glossary_audit import audit_glossary, match_term


class GlossaryAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.term = {'id': 'fungibility', 'term': 'Fungibility', 'tooltip': 'Fungibility explained.'}

    def slide(self, **kwargs):
        return dict({'id': 1, 'type': 'content_bullets', 'title': 'Facility interfaces', 'bullets': [], 'term_refs': ['fungibility']}, **kwargs)

    def audit(self, *slides, term=None, boundaries=True):
        if boundaries:
            slides = [self.slide(id=0, type='title', term_refs=[]), *slides,
                      self.slide(id=999, type='up_next', term_refs=[])]
        course = {'course_title': 'Test', 'term_glossary': [term or self.term], 'modules': [{'id': 1, 'title': 'Test', 'slides': list(slides)}]}
        return audit_glossary(course, self.root)[0]

    def media(self, text='CDU', video=True):
        path = 'media.mp4' if video else 'figure.svg'
        (self.root/path).write_bytes(b'reviewed test media')
        entry = {'text': text}
        if video: entry['at_seconds'] = 1.5
        return {'path': path, 'media_type': 'video' if video else 'image', 'alt': 'Diagram', 'caption': '',
                'text_inventory': {'sha256': hashlib.sha256((self.root/path).read_bytes()).hexdigest(), 'entries': [entry]}}

    def test_pill_cannot_justify_itself(self):
        self.assertTrue(any('absent' in x for x in self.audit(self.slide())))

    def test_visible_text_and_caption_are_evidence(self):
        self.assertEqual([], self.audit(self.slide(bullets=[{'text': 'Fungibility preserves choice.'}])))
        fig = self.media(text='A rack', video=False); fig['caption'] = 'Fungibility needs evidence.'
        self.assertEqual([], self.audit(self.slide(type='content_diagram', figure=fig)))

    def test_current_script_not_stale_transcript(self):
        (self.root/'script.txt').write_text('# pronunciation: Fungibility\nCheck the physical interfaces.')
        s = self.slide(audio={'script_file':'script.txt'}, transcript='Fungibility is mentioned only in this stale transcript.')
        self.assertTrue(any('absent' in x for x in self.audit(s)))
        (self.root/'script.txt').write_text('Fungibility requires interface evidence.')
        self.assertEqual([], self.audit(s))

    def test_absent_script_is_a_failure(self):
        self.assertTrue(any('missing narration script' in x for x in self.audit(self.slide(audio={'script_file':'missing.txt'}, transcript='Fungibility'))))

    def test_metadata_unused_fields_and_alt_do_not_count(self):
        fig = self.media(text='Rack', video=False); fig['alt'] = 'Fungibility'
        s = self.slide(type='content_diagram', figure=fig, slug='fungibility',
                       bullets=[{'text':'Fungibility in a non-rendered field'}],
                       source_refs=[{'source':'fungibility.pdf'}],
                       reference_links=[{'label':'Fungibility', 'url':'https://example.test/fungibility'}])
        self.assertTrue(any('absent' in x for x in self.audit(s)))

    def test_hidden_markup_is_not_evidence(self):
        from glossary_audit import ReadingText
        parser = ReadingText(); parser.feed('<div><span hidden>Fungibility</span><span data-tooltip="Fungibility">A rack</span><script>Fungibility</script></div>')
        self.assertIsNone(match_term(self.term, ''.join(parser.parts)))

    def test_real_video_only_term_and_first_use(self):
        term = {'id':'cdu','term':'CDU'}
        early = self.slide(term_refs=[], type='content_diagram', figure=self.media())
        later = self.slide(id=2, title='CDU review', term_refs=['cdu'])
        self.assertTrue(any('first appears on M1S1' in x for x in self.audit(early,later,term=term)))
        early['term_refs']=['cdu']; later['term_refs']=[]
        self.assertEqual([], self.audit(early,later,term=term))

    def test_changed_media_invalidates_inventory(self):
        fig = self.media('Fungibility')
        (self.root/fig['path']).write_bytes(b'changed media')
        self.assertTrue(any('stale' in x for x in self.audit(self.slide(type='content_diagram',figure=fig))))

    def test_unreviewed_earlier_media_is_not_silently_skipped(self):
        fig = self.media(); del fig['text_inventory']
        early = self.slide(term_refs=[],type='content_diagram',figure=fig)
        later = self.slide(id=2,title='Fungibility')
        self.assertTrue(any('missing reviewed' in x for x in self.audit(early,later)))

    def test_media_locator_required(self):
        fig = self.media('Fungibility'); del fig['text_inventory']['entries'][0]['at_seconds']
        self.assertTrue(any('at_seconds' in x for x in self.audit(self.slide(type='content_diagram',figure=fig))))

    def test_variants_and_boundaries(self):
        term = {'term':'SLA','aliases':['SLAs','service-level agreements']}
        for phrase in ['S L A', 'S.L.A.', 'Open SLAs', 'Service‑level agreements']:
            self.assertIsNotNone(match_term(term,phrase))
        self.assertIsNone(match_term(term,'slanted'))
        self.assertIsNotNone(match_term({'term':'kW/ft'}, '25 kW / ft'))
        self.assertIsNone(match_term(self.term,'Compatible implementations'))
        self.assertIsNone(match_term(self.term,'https://example.test/fungibility'))

    def test_preview_is_not_first_substantive_use(self):
        preview = self.slide(type='objectives',title='Fungibility',objectives=['Understand fungibility'],term_refs=[])
        teaching = self.slide(id=2,title='Fungibility in practice')
        self.assertEqual([], self.audit(preview,teaching))

    def test_completion_and_baseline_vocabulary_are_rejected(self):
        self.assertTrue(any('not course_complete' in x for x in self.audit(self.slide(type='course_complete'))))
        self.assertTrue(any('Excluded baseline vocabulary' in x for x in self.audit(self.slide(term_refs=['ocp'],title='OCP'),term={'id':'ocp','term':'OCP'})))

    def test_quiz_pill_is_rejected_even_when_term_is_spoken(self):
        quiz = self.slide(type='knowledge_check', transcript='Fungibility')
        self.assertTrue(any('not knowledge_check' in x for x in self.audit(quiz)))

    def test_quiz_is_not_first_substantive_use(self):
        quiz = self.slide(type='knowledge_check', transcript='Fungibility', term_refs=[])
        teaching = self.slide(id=2, title='Fungibility in practice')
        self.assertEqual([], self.audit(quiz, teaching))

    def test_first_and_last_excluded_by_position_not_id_or_type(self):
        first = self.slide(id=8, title='Fungibility')
        middle = self.slide(id=1, title='Fungibility', term_refs=[])
        last = self.slide(id=3, type='takeaways', items=['Fungibility'])
        flags = self.audit(first, middle, last, boundaries=False)
        self.assertEqual(2, len(flags))
        self.assertTrue(any('first slide' in x for x in flags))
        self.assertTrue(any('last slide' in x for x in flags))
        first['term_refs'] = []; middle['term_refs'] = ['fungibility']; last['term_refs'] = []
        self.assertEqual([], self.audit(first, middle, last, boundaries=False))

    def test_single_slide_module_has_no_glossary(self):
        self.assertTrue(self.audit(self.slide(title='Fungibility'), boundaries=False))

    def test_renderer_rejects_excluded_pills_without_mutating_source(self):
        import copy
        from render_module import render_module
        for kind, position in [('content_bullets', 0), ('takeaways', 2), ('knowledge_check', 1)]:
            slides = [self.slide(id=i+1, term_refs=[]) for i in range(3)]
            slides[position].update(type=kind, term_refs=['fungibility'], transcript='Fungibility')
            course = {'course_title':'Test', 'modules':[{'id':1, 'title':'Test', 'slides':slides}]}
            before = copy.deepcopy(course)
            with self.assertRaisesRegex(ValueError, 'Glossary pills are prohibited'):
                render_module(course, 0)
            self.assertEqual(before, course)


if __name__ == '__main__':
    unittest.main()
