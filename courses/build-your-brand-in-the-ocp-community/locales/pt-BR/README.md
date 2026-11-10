# Como construir sua marca na comunidade OCP

Brazilian Portuguese (`pt-BR`) edition of [How to Build Your Brand in the OCP Community](../../README.md).

The canonical English course is unchanged. This independent edition retains its
22 slides, two modules, SCORM 1.2 multi-SCO organization (Home plus both modules),
quiz attempts, bookmarks, source URLs, historical 1.68% versus 0.6% comparison,
current membership distinctions, and approved six-second silent animation loops.
The original April 2025 recording and updated 2026 PDF remain linked, in English.
The shared English catalog poster belongs to the canonical course.

## Narration and media

Full Eleven v4 (`eleven_v4`), voice `m151rjrbWXbBqyq56tly`, pitch-preserving
1.18 pacing; learner default speed 1.0. Delivery is 44.1 kHz, 96 kbps CBR mono MP3.
Paid provider audio, native/paced WAV masters and receipts are retained locally
outside the runtime ZIP and Git. Never regenerate just to package existing audio.
Scripts and on-screen transcripts are editable and match exactly.

`animations/labels.json` contains reviewed native-language artwork labels. Rebuild
with `python ../../scripts/build_localized_media.py pt-BR` from this locale
directory. Install Pillow, fontTools and brotli, and set `FFMPEG_BIN` to ffmpeg
with libx264. Licensed media font subsets are retained in `animations/fonts/`.
Runtime Open Sans/Noto fonts are bundled under `fonts/`; SVGs embed their fonts.
Original official membership
logos are kept in `../../scripts/membership-logos/`; the locale SVG embeds them.
The other local diagrams retain readable SVG text and accessible descriptions.

## Build and validate

From the repository root:

```sh
./scripts/build-course.sh build-your-brand-in-the-ocp-community/locales/pt-BR
python skills/academy-wizard/scripts/slides_course_qa.py courses/build-your-brand-in-the-ocp-community/locales/pt-BR/course.json --repo-root . --fail-on-flags
python skills/academy-wizard/scripts/course_delivery_summary.py courses/build-your-brand-in-the-ocp-community/locales/pt-BR/course.json --check
```

For a no-charge rebuild, set `EXISTING_AUDIO_DIR` to this edition's retained
`audio/` cache. The wrapper encodes, renders, validates and exports a strict ZIP.
The formal [LMS catalog copy](lms-catalog.md) is separate from this README.

## Review limits

Machine-assisted translation with contextual editorial corrections and automated
fact, structure, media, audio-signal and muted browser review. Native-speaker
review, human listening and target-LMS acceptance are not claimed. No LMS upload,
tracking reset or publication is performed by the translation build.
