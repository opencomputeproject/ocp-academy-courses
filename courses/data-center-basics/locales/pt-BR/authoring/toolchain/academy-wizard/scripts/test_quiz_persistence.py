"""Regression checks for Slides quiz persistence and resume ordering."""
import unittest

from render_module import render_module


class QuizPersistenceTests(unittest.TestCase):
    def test_local_preview_persists_and_clears_quiz_state_per_module(self):
        course = {
            "style": "Slides",
            "course_slug": "resume-test",
            "course_title": "Resume test",
            "modules": [{
                "id": 2,
                "title": "Module two",
                "slides": [
                    {"id": 1, "type": "title", "title": "Module two"},
                    {"id": 2, "type": "course_complete"},
                ],
            }],
        }

        result = render_module(course, 0)

        self.assertIn(
            'const QUIZ_STATE_KEY = "ocp:resume-test:module2:quiz-state"',
            result,
        )
        self.assertIn("localStorage.getItem(QUIZ_STATE_KEY)", result)
        self.assertIn("localStorage.setItem(QUIZ_STATE_KEY, data)", result)
        self.assertIn("clearQuizState(card.dataset.questionId)", result)
        self.assertIn("if (inLMS) data = SCORM.getSuspendData()", result)
        self.assertIn("if (inLMS) SCORM.setSuspendData(data)", result)
        self.assertLess(result.index("restoreQuizState();"), result.index("let requested = 1;"))


if __name__ == "__main__":
    unittest.main()
