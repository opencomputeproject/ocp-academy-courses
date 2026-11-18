import tempfile
import unittest
from pathlib import Path
from html.parser import HTMLParser

from course_feedback import FEEDBACK_URL, update_rendered_feedback, _LEGACY_FORM
from render_module import render_course_complete


class FeedbackButton(HTMLParser):
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a" and values.get("class") == "survey-btn":
            self.href = values["href"]


class CourseFeedbackTests(unittest.TestCase):
    def test_new_and_rebuilt_completion_ignore_stale_course_url(self):
        for slide in [{}, {"survey": {"url": _LEGACY_FORM, "button_text": "Comentarios"}}]:
            markup = render_course_complete({"id": 4, **slide}, {"course_title": "Sample"}, {"title": "Lesson", "id": 1})
            button = FeedbackButton()
            button.feed(markup)
            self.assertEqual(button.href, FEEDBACK_URL)

    def test_pinned_render_preserves_other_forms_and_link_attributes(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            page = folder / "module1.html"
            original = f'<a target="_blank" href="{_LEGACY_FORM}?usp=header">Feedback</a><a href="https://example.org/survey">Survey</a>'
            page.write_text(original)
            update_rendered_feedback(folder)
            update_rendered_feedback(folder)
            self.assertEqual(page.read_text(), original.replace(_LEGACY_FORM + '?usp=header', FEEDBACK_URL))


if __name__ == "__main__":
    unittest.main()
