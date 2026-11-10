"""Shared learner controls consume course-localized labels without changing defaults."""
import unittest

from render_module import render_module, render_takeaways


class LocalizedLearnerControlTests(unittest.TestCase):
    def course(self, labels=None):
        return {
            'style': 'Slides', 'course_slug': 'localized-control-test',
            'course_title': 'Test', 'language': 'ja-JP',
            'motion_intro': {'enabled': False}, 'ui_labels': labels or {},
            'modules': [{'id': 1, 'title': 'Test', 'slides': [
                {'id': 1, 'type': 'title', 'title': 'Test'}]}],
        }

    def test_localized_control_labels_are_escaped_and_available_to_runtime(self):
        markup = render_module(self.course({
            'transcript': '文字起こし & 記録', 'toggle_narration': '音声を切り替え',
            'narration_on_hint': '音声オン', 'close_transcript': '閉じる',
        }), 0)
        self.assertIn('aria-label="文字起こし &amp; 記録"', markup)
        self.assertIn('aria-label="音声を切り替え"', markup)
        self.assertIn('title="音声オン"', markup)
        self.assertIn('"close_transcript": "閉じる"', markup)
        self.assertIn("learnerText('close_transcript', 'Close transcript')", markup)

    def test_current_labels_take_precedence_over_earlier_translation_keys(self):
        markup = render_module(self.course({
            'automatic_narration': 'Current narration label',
            'toggle_narration': 'Earlier narration label',
            'narration_on': 'Current on title',
            'narration_on_hint': 'Earlier on title',
        }), 0)
        self.assertIn('aria-label="Current narration label"', markup)
        self.assertIn('title="Current on title"', markup)

    def test_english_fallbacks_remain_available(self):
        markup = render_module(self.course(), 0)
        self.assertIn('id="transcriptBtn" aria-label="Transcript" title="Transcript"', markup)
        self.assertIn('id="narrationModeBtn" aria-label="Automatic narration"', markup)
        self.assertIn("learnerText('narration_off_message', learnerText('narration_off_hint', 'Narration is off.", markup)

    def test_takeaway_teaching_slide_keeps_authored_learner_aids(self):
        course = self.course()
        course['term_glossary'] = [{'id': 'dlc', 'term': 'DLC', 'tooltip': 'Direct Liquid Cooling'}]
        markup = render_takeaways({
            'id': 10, 'type': 'takeaways', 'title': 'Apply the guidance',
            'items': ['Monitor DLC fluid condition.'], 'term_refs': ['dlc'],
            'reference_links': [{'label': 'Guideline · p. 8', 'url': 'https://example.org/spec.pdf#page=8'}],
        }, course, course['modules'][0])
        self.assertIn('class="glossary-chip"', markup)
        self.assertIn('https://example.org/spec.pdf#page=8', markup)
        self.assertLess(markup.index('</ul>'), markup.index('class="learner-aids"'))


if __name__ == '__main__':
    unittest.main()
