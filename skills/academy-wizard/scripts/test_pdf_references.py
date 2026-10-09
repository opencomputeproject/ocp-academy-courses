"""Regression tests for teaching-page PDF links and full-document closing links."""
import unittest

from slides_course_qa import audit_pdf_references


class PdfReferenceTests(unittest.TestCase):
    def audit(self, label, url, **slide_fields):
        slide = dict(id=3, type="content_bullets",
                     reference_links=[{"label": label, "url": url}], **slide_fields)
        return audit_pdf_references({"modules": [{"id": 1, "slides": [slide]}]})

    def test_teaching_single_page(self):
        self.assertEqual(self.audit("Spec · p. 5", "https://example.test/spec.pdf#page=5"), ([], 1))

    def test_teaching_ranges_open_first_viewer_page(self):
        self.assertEqual(self.audit("Spec · Table 13 · pp. 5–7, 10–11",
                                    "https://example.test/spec-final-pdf#page=5"), ([], 1))

    def test_local_pdf_range_and_query_are_preserved(self):
        self.assertEqual(self.audit("Guide · pp. 2-4", "resources/guide.PDF?download=1#page=2"), ([], 1))

    def test_generic_teaching_link_is_flagged(self):
        errors, _ = self.audit("Spec", "https://example.test/spec.pdf")
        self.assertTrue(any("#page=" in error for error in errors))

    def test_page_anchor_without_visible_pages_is_flagged(self):
        errors, _ = self.audit("Spec", "https://example.test/spec.pdf#page=5")
        self.assertTrue(any("must display" in error for error in errors))

    def test_label_and_anchor_must_match(self):
        errors, _ = self.audit("Spec · pp. 6–8", "https://example.test/spec.pdf#page=5")
        self.assertTrue(any("same PDF viewer page" in error for error in errors))

    def test_invalid_page_anchors(self):
        for fragment in ("page=0", "page=-1", "page=five", "page=2&page=3", "nameddest=scope"):
            with self.subTest(fragment=fragment):
                self.assertTrue(self.audit("Spec · p. 2", "guide.pdf#" + fragment)[0])

    def test_invalid_page_ranges(self):
        for label in ("Spec · pp. 5–3", "Spec · pp. 5–7, 10–8", "Spec · p. 0"):
            with self.subTest(label=label):
                self.assertTrue(self.audit(label, "guide.pdf#page=5")[0])

    def test_whole_document_closing_link(self):
        course = {"modules": [{"id": 4, "slides": [{
            "id": 12, "type": "course_complete",
            "reference_links": [{"label": "PG25 base specification", "url": "https://example.test/pg25-final-pdf"}],
        }]}]}
        self.assertEqual(audit_pdf_references(course), ([], 1))
        course["modules"][0]["slides"][0]["reference_links"][0].update(
            label="PG25 · Contents · pp. 2–3", url="https://example.test/pg25-final-pdf#page=2")
        self.assertTrue(audit_pdf_references(course)[0])

    def test_closing_label_and_fragment_are_independently_rejected(self):
        for label, url in (("Guide · p. 3", "guide.pdf"), ("Guide", "guide.pdf#page=3")):
            with self.subTest(label=label, url=url):
                course = {"modules": [{"id": 4, "slides": [{
                    "id": 12, "type": "course_complete",
                    "reference_links": [{"label": label, "url": url}],
                }]}]}
                self.assertTrue(audit_pdf_references(course)[0])

    def test_non_pdf_links_and_hidden_authoring_sources_are_unchanged(self):
        course = {
            "sources": [{"url": "https://example.test/spec.pdf", "kind": "pdf"}],
            "term_glossary": [{"url": "https://example.test/spec.pdf"}],
            "modules": [{"id": 1, "slides": [{
                "id": 3, "type": "content_bullets",
                "source_refs": [{"url": "https://example.test/spec.pdf"}],
                "reference_links": [{"label": "Academy course", "url": "https://academy.example.test/course#module2"}],
            }]}],
        }
        self.assertEqual(audit_pdf_references(course), ([], 0))

    def test_pdf_callout_requires_pages(self):
        course = {"modules": [{"id": 1, "slides": [{
            "id": 3, "resource_callout": {"button_text": "Guide · p. 8", "url": "guide.pdf#page=8"},
        }]}]}
        self.assertEqual(audit_pdf_references(course), ([], 1))
        course["modules"][0]["slides"][0]["resource_callout"]["button_text"] = "Read guide"
        self.assertTrue(audit_pdf_references(course)[0])

    def test_opaque_pdf_url_can_be_identified_by_source_metadata(self):
        course = {
            "sources": [{"url": "https://example.test/download/42", "path": "spec.pdf"}],
            "modules": [{"id": 1, "slides": [{
                "id": 3, "reference_links": [{"label": "Spec", "url": "https://example.test/download/42"}],
            }]}],
        }
        self.assertEqual(audit_pdf_references(course)[1], 1)
        self.assertTrue(audit_pdf_references(course)[0])

    def test_localized_document_name_keeps_page_notation(self):
        self.assertEqual(self.audit("Guia PG25 · pp. 13–16", "guia.pdf#page=13"), ([], 1))


if __name__ == "__main__":
    unittest.main()
