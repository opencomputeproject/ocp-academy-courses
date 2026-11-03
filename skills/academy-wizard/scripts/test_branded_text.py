import unittest
from branded_text import format_trademarks

class TrademarkTests(unittest.TestCase):
    def test_visible_copy_gets_superscript(self):
        self.assertIn('OCP Ready<sup class="brand-trademark">TM</sup>',format_trademarks('<p>OCP Ready™</p>'))
    def test_metadata_and_attributes_remain_plain(self):
        source='<title>OCP Ready™</title><script>const label="OCP Ready™";</script><img alt="OCP Ready™">'
        self.assertEqual(format_trademarks(source),source)
    def test_canonical_svg_paths_and_entities_are_unchanged(self):
        source='<svg viewBox="0 0 24 24"><path d="M6 5l7 7-7 7"/></svg><p>A &amp; B &#9646;</p>'
        self.assertEqual(format_trademarks(source),source)

if __name__=='__main__':unittest.main()
