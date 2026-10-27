> Latest rebuild: see [Green next-module navigation refresh](../green-navigation-refresh/README.md). Current package-audit.json describes that delivery; older dated reports are historical.

# Final SCORM 1.2 delivery — 2026-10-27

User-approved LMS ZIP and repository publication. The manifest contains Course Home as the first SCO followed by four module SCOs (five total); current metadata, API, interaction vocabulary and saved-state behavior are SCORM 1.2. Earlier dated 2004 QA records are historical.

All 158 archived files match the validated runtime byte for byte. A fresh repository-source build with the approved audio produces identical runtime bytes. The strict ZIP excludes source scripts, narration text, editorial records and catalog sidecars.

Validation passed: package and SCORM 1.2 XML schemas; complete content/glossary audit; 33 figure/animation arrow checks; all 68 narration signal checks; 252 desktop/phone media layouts; 21 synchronized-video and 16 legacy-video playback assertions. Chromium was muted throughout.

The strict mock API verified Course Home and traversed all four modules and their questions, checked independent completion and restored attempts/bookmarks, matching response encoding, retry clearing, retired-question isolation, review isolation and visible save failures. The largest completed suspend state is 427 characters against a 4096-character limit. Oversized writes are refused without overwriting prior state. Green next-module links stay visible and clickable in local, review and LMS playback; Home initializes and completes its own SCO on launch, commits session time and finishes on exit without writing module progress. Editorial Home review makes no LMS calls.

Run `node authoring/qa/scorm12-delivery/scorm12_qa.mjs /absolute/path/to/built-course` and the sibling `media_layout_qa.mjs` with Playwright installed. See `package-audit.json` for ZIP size/hash and exact checks. Screenshots retain representative desktop and phone states.

This changes the local review build from SCORM 2004 to 1.2 at the user’s request. A deployed item may require a new upload and may not transfer attempts, bookmarks or completion history. Export any needed reports and test a separate LMS upload before retiring an existing item. No LMS upload or deletion has been performed. Local simulation is not actual target-LMS acceptance.
