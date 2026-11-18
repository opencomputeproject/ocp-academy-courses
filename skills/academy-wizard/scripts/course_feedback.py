"""Keep the Academy feedback destination current in new and pinned course builds."""
import argparse
from pathlib import Path
import re

FEEDBACK_URL = "https://opencomputeproject.github.io/ocp-academy-courses/feedback/"
_LEGACY_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSf-IDIuFSXbRk-nks90x7J_4-iiZ6vEvmmNQoVps3ySP6UFmg/viewform"
_LEGACY_HREF = re.compile(
    r"""(\bhref\s*=\s*)(["'])""" + re.escape(_LEGACY_FORM) + r"""(?:[?#][^"']*)?\2""",
    re.IGNORECASE,
)


def update_rendered_feedback(folder):
    for page in [folder / "index.html", *folder.glob("module*.html")]:
        if page.is_file():
            original = page.read_text(encoding="utf-8")
            updated = _LEGACY_HREF.sub(lambda m: m[1] + m[2] + FEEDBACK_URL + m[2], original)
            if updated != original:
                page.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    update_rendered_feedback(parser.parse_args().folder)
