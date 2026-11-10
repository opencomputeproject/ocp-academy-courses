# Intro to OCP — translated-edition validation

The seven translated Slides editions were built locally on 2026-11-05 through
SCORM ZIPs and separate translated LMS title/description exports. Repository
publication does not upload or replace any live LMS material.

## Scope and source preservation

- Canonical English `course.json` SHA-256:
  `017e51004e3f21ba65026ee2d0cc7cc252ccceb0cb22f669c90f121e79162940`.
- Each edition retains four modules, 52 slides, question/choice correctness,
  source references and authoritative resource URLs.
- Each SCORM 1.2 ZIP contains five tracked entries: Course Home and Modules 1–4,
  46 MP3 narration files, six imported recordings and four teaching animations.
  Archive integrity and manifest-only membership passed; zero WAV files or
  authoring receipts are included.
- All language editions share the canonical English LMS poster.
- Matty's author credit and portrait remain on Module 1, slide 2. Additional
  narration is not represented as his words or endorsement.

## Narration, dubbing and teaching media

- Fresh full `eleven_v4` narration uses the maintained locale voice profiles,
  1.18 pitch-preserving authoring tempo and 44.1 kHz / 96 kbps CBR mono MP3
  delivery. The learner dial defaults to 1.0.
- All 322 final narrated-slide masters matched their exact source scripts,
  passed waveform/tail checks, and were independently detected as the expected
  language by the local multilingual faster-whisper base model. Chinese
  detection establishes the language, not Traditional/Simplified script or
  regional pronunciation quality.
- Five recordings per locale were dubbed from reviewed translated script
  memory after verifying that the source-video hashes matched. No retired-model
  audio was reused. All 665 final utterance masters passed waveform checks.
- Language detection matched the expected language in a sample of the first
  30 seconds of each of the 35 mixed dubbed videos. This is not a transcript or
  pronunciation audit of every second of every recording.
- The dubbed recordings retain the original pictures, do not map the original
  speech soundtrack, and include timed native-language VTT captions. Background
  music uses the maintained rotation and stronger narration ducking.
- The approved `building-the-future.mp4` exception on M1S9 is byte-identical to
  the English source, with a translated on-slide notice.
- All 28 teaching animations have contextually reviewed translated labels,
  text-fit and arrow-geometry checks, and final-narration-aligned scene timing.
  They play once and hold the completed final picture.
- All seven membership reading copies retain five source-page references;
  rendered pages were inspected for layout and missing-glyph problems.

## Layout, interaction and packaging

- 1,456 actual course-page cases passed: all 52 slides in seven languages,
  desktop and phone widths, light and dark themes. No reported JavaScript
  errors, horizontal overflow or unscrollable content trapped behind controls.
- 63 browser-runtime jobs passed: seven quiz-resume/retry checks plus all 28
  teaching animations at desktop and phone sizes. Coverage includes pause,
  seek, speed, enlarged playback, end hold, replay and reduced-motion behavior.
- Quiz answer correctness, two-question interaction, dark-mode card backgrounds,
  recording controls, informational home tiles and final continuing-resource
  pills were checked.
- Formal LMS catalog exports passed metadata validation. All ZIPs passed
  integrity and manifest checks, with 46 MP3 files and zero WAV files each.
- Local/browser checks do not establish target-LMS navigation or tracking.
  Verify those during a separate LMS upload; no SCORM-version migration or
  deletion of learner history is authorized by this source contribution.

## Review limitations

Initial text drafts were machine-translated, followed by contextual technical
corrections, including cooling terminology and the engineering senses of
pilot, draft, power and product recognition. Automated ASR/language and signal
checks do not prove idiomatic wording, accurate pronunciation or complete spoken
fidelity. Native-speaker editorial review and human listening remain recommended
before publication and are not represented as completed approvals.

Generated narration, provider files, receipts, rendered runtime HTML, detailed
local QA captures and LMS ZIPs remain outside source control. The repository
contains editable locale definitions/scripts, LMS catalog JSON/Markdown,
localized teaching media, dubbed recordings, captions and reading PDFs.
