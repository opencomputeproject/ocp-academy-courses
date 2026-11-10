"""Keep transcript and narration controls localized without changing defaults."""
import json
import unittest
from render_module import render_module


class LocalizedNarrationControls(unittest.TestCase):
    def course(self, labels=None):
        return {"course_title": "Controls", "language": "ja-JP",
                "ui_labels": labels or {}, "modules": [{"id": 1, "title": "Controls",
                "slides": [{"id": 1, "type": "title", "title": "Controls"},
                           {"id": 2, "type": "course_complete"}]}]}

    def test_bootstrap_buttons_use_native_labels(self):
        result = render_module(self.course({"transcript": "文字起こし",
                                             "toggle_narration": "ナレーション切り替え",
                                             "narration_on_hint": "ナレーションをオフにする"}), 0)
        self.assertIn('id="transcriptBtn" aria-label="文字起こし" title="文字起こし"', result)
        self.assertIn('id="narrationModeBtn" aria-label="ナレーション切り替え"', result)
        self.assertIn('aria-pressed="true" title="ナレーションをオフにする"', result)

    def test_dynamic_controls_consult_the_same_native_dictionary(self):
        labels = {key: "翻訳" + str(index) for index, key in enumerate([
            "slide_transcript", "close_transcript", "lms_navigation_note", "transcript",
            "no_narration", "narration_on_hint", "narration_off_hint",
            "narration_off_message", "play_narrated_video", "pause_narrated_video"])}
        result = render_module(self.course(labels), 0)
        self.assertIn("function learnerText(key, fallback)", result)
        self.assertIn(json.dumps(labels, ensure_ascii=False), result)
        for key in labels:
            self.assertIn("learnerText('" + key + "'", result)

    def test_english_fallbacks_and_default_narration_state_survive(self):
        result = render_module(self.course(), 0)
        self.assertIn('id="transcriptBtn" aria-label="Transcript" title="Transcript"', result)
        self.assertIn('id="narrationModeBtn" aria-label="Automatic narration" aria-pressed="true"', result)
        self.assertIn("learnerText('close_transcript', 'Close transcript')", result)


if __name__ == "__main__":
    unittest.main()
