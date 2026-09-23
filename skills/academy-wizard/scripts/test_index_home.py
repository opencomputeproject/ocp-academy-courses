"""Regression checks for syllabus-led multi-SCO home and opt-in start control."""
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

from render_index import render_index_html, render_manifest


class Elements(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.elements = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def by_class(self, name):
        return [(tag, attrs) for tag, attrs in self.elements
                if name in attrs.get('class', '').split()]


class IndexHomeTests(unittest.TestCase):
    def setUp(self):
        self.course = {
            'style': 'Slides', 'course_slug': 'home-test',
            'course_title': 'Home Test', 'motion_intro': {'enabled': False},
            'scorm': {'version': '1.2', 'organization': 'multi-sco'},
            'modules': [{'id': n, 'title': f'Module {n}', 'subtitle': 'A topic', 'slides': []}
                        for n in range(1, 5)]}

    def render(self):
        markup = render_index_html(self.course)
        return markup, Elements(markup)

    def test_multi_sco_has_informational_tiles_without_status_or_progress_reads(self):
        markup, dom = self.render()
        self.assertEqual([tag for tag, _ in dom.by_class('module-card')], ['article'] * 4)
        self.assertFalse(dom.by_class('status'))
        self.assertNotIn('SCORM.getSuspendData()', markup)
        self.assertFalse(any('href' in attrs or 'tabindex' in attrs for _, attrs in dom.by_class('module-card')))
        self.assertIn('Use the LMS syllabus', markup)
        self.assertFalse(dom.by_class('index-start-link'))

    def test_multi_sco_ignores_stale_status_setting(self):
        self.course['index_show_module_status'] = True
        markup, dom = self.render()
        self.assertFalse(dom.by_class('status'))
        self.assertNotIn('SCORM.getSuspendData()', markup)

    def test_authorized_direct_tile_override_is_preserved(self):
        self.course['scorm']['navigation'] = 'direct'
        _, dom = self.render()
        self.assertEqual([attrs['href'] for _, attrs in dom.by_class('module-card')],
                         [f'module{n}.html' for n in range(1, 5)])

    def test_explicit_informational_tiles_override_direct_navigation(self):
        self.course['scorm']['navigation'] = 'direct'
        self.course['index_module_links'] = False
        _, dom = self.render()
        self.assertTrue(all(tag == 'article' for tag, _ in dom.by_class('module-card')))

    def test_instruction_is_escaped_and_precedes_start(self):
        self.course['index_navigation_instruction'] = 'Use the Syllabus <left> & choose.'
        self.course['index_start'] = {'enabled': True, 'navigation': 'direct', 'label': 'Start with MODULE 1'}
        markup, dom = self.render()
        self.assertIn('Use the Syllabus &lt;left&gt; &amp; choose.', markup)
        self.assertLess(markup.index('<p id="lmsNavNote"'), markup.index('<div class="index-start">'))
        self.assertLess(markup.index('<span class="index-start-label"'), markup.index('<a class="next-module-link'))
        self.assertEqual(dom.by_class('index-start-link')[0][1]['href'], 'module1.html')
        self.assertIn("'?review=1&slide=1'", markup)
        self.assertIn('M6 5l7 7-7 7', markup)
        self.assertIn('M12 5l7 7-7 7', markup)

    def test_start_does_not_enable_other_tile_links(self):
        self.course['index_start'] = {'enabled': True, 'navigation': 'direct'}
        _, dom = self.render()
        self.assertEqual(len(dom.by_class('index-start-link')), 1)
        self.assertTrue(all(tag == 'article' for tag, _ in dom.by_class('module-card')))

    def test_multi_sco_start_requires_explicit_compatibility_choice(self):
        self.course['index_start'] = {'enabled': True}
        with self.assertRaisesRegex(ValueError, 'explicitly approved'):
            self.render()

    def test_start_targets_first_authored_module_not_hardcoded_one(self):
        self.course['modules'][0]['id'] = 8
        self.course['index_start'] = {'enabled': True, 'navigation': 'direct'}
        markup, dom = self.render()
        self.assertEqual(dom.by_class('index-start-link')[0][1]['href'], 'module8.html')
        self.assertIn('Start with MODULE 8', markup)

    def test_single_sco_retains_trustworthy_progress_and_links(self):
        self.course['scorm']['organization'] = 'single-sco'
        self.course['index_start'] = {'enabled': True}
        markup, dom = self.render()
        self.assertEqual(len(dom.by_class('status')), 4)
        self.assertIn('SCORM.getSuspendData()', markup)
        self.assertTrue(all(tag == 'a' for tag, _ in dom.by_class('module-card')))

    def test_single_sco_can_hide_progress(self):
        self.course['scorm']['organization'] = 'single-sco'
        self.course['index_show_module_status'] = False
        markup, dom = self.render()
        self.assertFalse(dom.by_class('status'))
        self.assertNotIn('SCORM.getSuspendData()', markup)

    def test_home_options_do_not_change_manifest_or_version(self):
        expected = render_manifest(self.course, Path('.'))
        self.course.update(index_module_links=False, index_show_module_status=False,
                           index_start={'enabled': True, 'navigation': 'direct'})
        self.assertEqual(render_manifest(self.course, Path('.')), expected)
        self.assertIn('<schemaversion>1.2</schemaversion>', expected)
        self.assertEqual(expected.count('adlcp:scormtype="sco"'), 5)

    def test_canonical_button_styles_match_module_control(self):
        templates = Path(__file__).resolve().parent.parent / 'templates'
        index_css = (templates / 'index_styles.css').read_text()
        module_css = (templates / 'module_styles.css').read_text()
        for selector in ('.next-module-link', '.next-module-link svg',
                         '.next-module-link:hover,\n.next-module-link:focus'):
            pattern = re.escape(selector) + r'\s*\{([^}]+)\}'
            self.assertEqual(re.search(pattern, index_css)[1].strip(),
                             re.search(pattern, module_css)[1].strip())

    def test_syllabus_note_uses_body_size_and_start_label_uses_brand_indigo(self):
        css = (Path(__file__).resolve().parent.parent / 'templates/index_styles.css').read_text()

        def declarations(selector):
            body = re.search(re.escape(selector) + r'\s*\{([^}]+)\}', css)[1]
            return dict((key.strip(), value.strip()) for key, value in
                        (declaration.split(':', 1) for declaration in body.split(';')
                         if ':' in declaration))

        self.assertEqual(declarations('.index-navigation-instruction')['font-size'],
                         declarations('.module-info p')['font-size'])
        self.assertEqual(declarations('.index-start-label')['color'], 'var(--ocp-blue)')
        self.assertEqual(declarations(':root')['--ocp-blue'].lower(), '#343895')


if __name__ == '__main__':
    unittest.main()
