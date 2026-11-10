# Introducción al proyecto Open Compute

Spanish (Latin America) edition.

Editable `es-419` edition of the [canonical four-module Slides course](../../README.md).
It retains 52 slides, eight knowledge-check questions and SCORM 1.2 with five
tracked entries: Course Home and Modules 1–4.

- [Translated LMS title and descriptions](lms-catalog.md)
- [Structured LMS catalog fields](lms-catalog.json)
- [Translation validation and review limitations](../../TRANSLATION_QA.md)

From the repository root, reuse approved audio for this language:

```bash
EXISTING_AUDIO_DIR=/path/to/es-419/audio ./scripts/build-course.sh intro-to-ocp/locales/es-419
```

Narration uses Ninoska, full Eleven v4, 1.18 pitch-preserving authoring pacing
and 44.1 kHz / 96 kbps CBR mono MP3 delivery. Generated narration, provider
masters, receipts, runtime HTML and ZIPs are not committed.

Five expert recordings have localized soundtracks and timed captions; their
original pictures remain unchanged. The approved English live recording on
Module 1, slide 9 retains its English audio and translated notice. All four
teaching animations have translated labels and narration-aligned timelines.
Use the shared [English LMS poster](../../thumbnail.png), not a locale poster.

The translation is machine-assisted with contextual technical corrections and
automated checks. Native-speaker editorial and human-listening approval is not
claimed; review before publishing. Repository source publication does not
upload LMS material or change learner tracking.
