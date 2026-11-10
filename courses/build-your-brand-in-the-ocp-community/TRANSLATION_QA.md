# Seven language editions — November 10, 2026

Added Korean, Japanese, Simplified Chinese, Traditional Chinese, Vietnamese,
Brazilian Portuguese and Latin American Spanish under `locales/`. The canonical
English course and its 40 existing source/assets are unchanged.

Each edition retains 22 slides, two modules, SCORM 1.2, three syllabus SCOs
(Course Home plus both modules), the approved direct navigation, quiz gates,
answer memory and completed-module resume. The April 2025 recording and updated
2026 PDF links, page anchors, membership distinctions, historical 1.68%/0.6%
comparison, contact emails and final resource choices are preserved.

Every edition has fresh full `eleven_v4` narration with its maintained locale
voice and pitch-preserving 1.18 pacing. Delivery is 44.1 kHz, 96 kbps CBR mono
MP3; the learner dial starts at 1.0. Native/provider audio, paced WAVs and receipts
are retained locally outside Git and the runtime ZIPs. One Vietnamese Marketplace
clip was revised to express the thousand-listing estimate unambiguously.

All teaching diagrams, animation labels, captions, transcripts, UI controls,
knowledge checks, glossary definitions and formal LMS metadata are localized.
The two approved silent six-second animation loops retain their geometry and
enlargement behavior. Official membership logos and the shared English catalog
poster remain unchanged. Licensed Open Sans, Noto CJK and symbol subsets support
offline playback; teaching SVGs embed their fonts. Font licenses are declared in
the manifest and included in each ZIP.

Validation completed:

- 180 shared Python regression tests.
- 3,206 desktop/mobile assertions across 1440, 1024, 390 and 320 px viewports.
- 154 real-media, touch, enlargement, cycle, embedded-font and SVG-clearance checks.
- 59 resume and 26 quiz-memory assertions with isolated local/mock-LMS state.
- 60 shared control assertions, including localized transcript and narration states.
- 10 targeted checks of the revised Vietnamese narration, transcript, seek and layout.
- 154 audio signal checks with zero flags; complete MP3 decode/duration checks.
- Source QA, PDF references, glossary first-use placement and SVG arrows for all editions.
- All seven repository rebuilds reused cached masters without TTS and reproduced
  every reviewed runtime byte. Strict ZIP membership, archive integrity and extracted
  package validation passed.

The current `main` already supplies the localized player controls, glossary fixes
and offline-font workflow. This contribution retains those implementations and
adds locale-aware control/resume regression coverage. No generated course HTML,
narration WAV/MP3 or ZIP is committed.

See [translation-release.json](translation-release.json) for source/package hashes,
voices, measured narration durations and validation details. Approved LMS estimates
remain 26 minutes overall (12 + 14); measured narration is reported separately.
Font sources are the Open Sans assets already distributed in this repository,
[Noto Sans CJK](https://github.com/notofonts/noto-cjk/tree/main/Sans) and
[Noto Sans Symbols 2](https://github.com/google/fonts/tree/main/ofl/notosanssymbols2).

Machine-assisted translation received contextual editorial and automated review.
Native-speaker review, human listening and live-LMS acceptance are not claimed.
Linked external source materials remain in their original language. No Docebo
upload, tracking reset or merge is part of this delivery.
