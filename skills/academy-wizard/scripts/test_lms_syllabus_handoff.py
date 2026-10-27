"""Shared Slides handoff checks with isolated DOM mocks, never a live LMS."""
import shutil
import subprocess
import unittest
from pathlib import Path
from render_module import render_content_grid


class SyllabusHandoffTests(unittest.TestCase):
    def test_module_links_survive_all_lms_and_review_modes(self):
        node = shutil.which('node')
        if not node:
            self.skipTest('Node.js is required for the isolated JavaScript guard test')
        template = (Path(__file__).resolve().parent.parent/'templates/learner_features.js').read_text()
        start = template.index('if (inLMS && !reviewMode && !SCORM.isSingleSCO')
        end = template.index("if (reviewMode) document.addEventListener('click'", start)
        result = subprocess.run([node, '-e', r'''
const fs = require('fs'), vm = require('vm'), assert = require('assert/strict');
const code = fs.readFileSync(0, 'utf8');
for (const inLMS of [false,true]) for (const reviewMode of [false,true])
for (const isSingleSCO of [false,true]) for (const directModuleLinks of [false,true]) {
  const links = ['module3.html?review=1','index.html','resources/guide.pdf','https://example.org/module3.html']
    .map(href => ({getAttribute: () => href, replaceWith(note) {this.note=note;}}));
  const document = {querySelectorAll: () => links, createElement: () => ({style:{}})};
  vm.runInNewContext(code, {inLMS,reviewMode,SCORM:{isSingleSCO},directModuleLinks,document,URL,
    location:{origin:'https://lms.test',href:'https://lms.test/module2.html'}});
  const shouldReplace = inLMS && !reviewMode && !isSingleSCO && !directModuleLinks;
  assert.equal(links[0].note,undefined);
  assert.equal(Boolean(links[1].note),shouldReplace);
  assert.equal(links[2].note,undefined);
  assert.equal(links[3].note,undefined);
  if(shouldReplace) {
    assert.equal(links[1].note.textContent,'Open Course Home using the Syllabus in the left sidebar.');
  }
}
'''],input=template[start:end],text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertNotIn('preventDefault',template[start:end])

    def test_card_trademark_is_superscript_without_unescaping_other_content(self):
        markup = render_content_grid({'id':3,'title':'Storage','cards':[
            {'title':'ESS','body':'OCP Ready™ evidence. <script>unsafe</script>'}]},{},{})
        self.assertIn('OCP Ready<sup>TM</sup> evidence.',markup)
        self.assertIn('&lt;script&gt;unsafe&lt;/script&gt;',markup)
        self.assertNotIn('<script>unsafe</script>',markup)


if __name__ == '__main__':
    unittest.main()
