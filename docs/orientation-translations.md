# OCP Community Orientation translations

The five canonical English courses have seven independently editable Slides
editions each: `es-419`, `ja-JP`, `ko-KR`, `pt-BR`, `vi-VN`, `zh-CN`, and `zh-TW`.
All 35 editions were published to OCP Academy on November 10, 2026.

| Academy course | Canonical source | Language editions |
|---|---|---|
| [2 — Volunteer Leadership](https://academy.opencompute.org/course/edit/2) | [Volunteer Leadership](../courses/ocp-orientation/ocp-volunteer-leadership-guide/) | [Seven locales](../courses/ocp-orientation/ocp-volunteer-leadership-guide/locales/) |
| [14 — Solution Provider](https://academy.opencompute.org/course/edit/14) | [Solution Provider](../courses/ocp-orientation/introduction-to-the-ocp-solution-provider-program/) | [Seven locales](../courses/ocp-orientation/introduction-to-the-ocp-solution-provider-program/locales/) |
| [25 — OCP Ready](https://academy.opencompute.org/course/edit/25) | [OCP Ready](../courses/ocp-orientation/ocp-ready-data-center-recognition-program/) | [Seven locales](../courses/ocp-orientation/ocp-ready-data-center-recognition-program/locales/) |
| [26 — Contribution Process](https://academy.opencompute.org/course/edit/26) | [Contribution Process](../courses/ocp-orientation/ocp-contribution-process/) | [Seven locales](../courses/ocp-orientation/ocp-contribution-process/locales/) |
| [28 — Open Procurement](https://academy.opencompute.org/course/edit/28) | [Open Procurement](../courses/ocp-orientation/understanding-and-procuring-open-technologies-and-products/) | [Seven locales](../courses/ocp-orientation/understanding-and-procuring-open-technologies-and-products/locales/) |

Each edition remains one content module in one SCORM 1.2 tracked activity,
including Course Home. The original recording visuals and screenshots are
retained. Spoken recordings have native voice-over and captions; Contribution
Process's silent demonstrations retain their original footage and use separate
narration timed to the caption windows. Teaching videos play once and hold their
final frame.

The source folders include `course.json`, narration scripts, editable animation
art, reviewed encoded media, original-recording sources, captions, offline fonts
and licenses, prepared poster sources, and the separate LMS catalog exports.
Generated slide narration MP3/WAV files, rendered course pages, private production
reports, and SCORM ZIPs remain outside Git under the repository's source policy.
The native poster assets predate the shared English poster default; preserve them
when reviewing these existing editions with `--allow-localized-poster`.

Narration uses full ElevenLabs v4 and the recorded locale voice, with a
pitch-preserving 1.18 authoring pace. Delivery uses 44.1 kHz, 96 kbps CBR mono MP3;
the learner's playback dial starts at 1.0. Reuse the approved narration when
rebuilding the published editions:

```bash
EXISTING_AUDIO_DIR=/path/to/approved/audio \
  ./scripts/build-course.sh \
  ocp-orientation/ocp-contribution-process/locales/ja-JP
```

Without `EXISTING_AUDIO_DIR`, the normal build can make paid speech-generation
requests. Keep an API key in the environment only. The Contribution Process
generation hook uses its reviewed `scripts/narration-cue-plan.json`; do not add
another baked narration track to those silent demonstration videos.

The [publication inventory](orientation-translations.json) records source and
delivered ZIP hashes, Docebo library material IDs, versions, and course-folder
organization IDs. All translated packages are library items in
**Docebo / OCP Orientation** (folder 19), assigned once to their matching course
language. English materials, summaries, and course settings were preserved.
Titles and descriptions match the prepared `lms-catalog` exports, including the
replacement of the older Rise descriptions.

Repository validation covered all 35 source/metadata/arrow checks and runtime
builds. The six generated runtime/control/manifest files per edition matched the
published build byte for byte when reusing approved audio. The shared regression
suite passed 180 tests. Earlier production validation covered all slides at
desktop and phone widths, teaching-video playback/final holds, and mock-LMS
bookmark, quiz, and completion behavior. Human listening review remains recorded
as pending in the locale README files; LMS publication is not a listening audit.
