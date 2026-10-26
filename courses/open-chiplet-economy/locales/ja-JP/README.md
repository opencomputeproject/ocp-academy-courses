# Open Chiplet Economy：チップレットシステムのビジネスと技術

Japanese narrated Slides source for nine independently tracked SCORM 1.2 modules: 114 slides, 100 slide narrations, 19 questions, nine teaching videos and 14 dubbed recordings. Home remains an untracked asset. Formal LMS copy is maintained separately in [lms-catalog.md](lms-catalog.md).

## Source layout

- `course.json`: Japanese content, questions and feedback, glossary, media evidence, narration settings and LMS catalog metadata.
- `audio/module*/`: approved Japanese scripts; generated WAVs stay outside Git.
- `figures/`: localized teaching videos and PNG figures, posters and Japanese dubbed recordings.
- `media_source/figures/`: editable Japanese SVG figures.
- `animation_sources/`: five Japanese looping teaching diagrams.
- `tools/synced_video/`: four finite teaching sequences; Japanese timing, labels and production evidence are in `video_source/`.
- `captions/`: 23 optional Japanese VTT tracks. The five short looping diagrams use the slide narration clock for captions.
- `video_source/narration/`: approved full Japanese recording scripts.
- `tools/academy_wizard/`: locale toolchain, including Japanese controls, offline CC and SCORM 1.2 generation.
- `fonts/`: bundled Open Sans and [Noto Sans JP](https://github.com/google/fonts/tree/main/ofl/notosansjp), with OFL licenses.
- `thumbnail.svg` / `thumbnail.png`: editable artwork and 800 × 400 LMS poster.

## Build

From the repository root, reuse the approved local audio:

```sh
EXISTING_AUDIO_DIR=/path/to/approved/Japanese/audio bash scripts/build-course.sh open-chiplet-economy/locales/ja-JP
```

To generate missing slide narration, run `python3 tools/generate_narration.py` from this locale folder, then rebuild with its `audio/` folder. The secure launcher uses an environment key or hidden prompt; credentials are never saved. Japanese ElevenLabs voice `b34JylakFZPlGS0BnwyY` uses `eleven_v4`, paced against same-text, same-voice Multilingual v2 at speed 1.18 with pitch-preserving duration matching. Player speed stays 1.0.

Install media tools with `npm install` and `python3 -m pip install -r requirements-media.txt`; FFmpeg with libx264 is required only when changing media. Source-owned videos and captions can be packaged directly. Japanese vectors render with `node tools/render_japanese_static.mjs`; loops with `node tools/render_animations.mjs`. See [finite video production](tools/synced_video/README.md). Always review new text and native-size samples before updating a media inventory hash.

The repository builder exports a strict runtime-only ZIP and matching LMS catalog JSON, Markdown and HTML sidecars. Catalog exports are LMS fields; this README is maintenance documentation. Narration masters, raw timing responses, intermediate frames and built packages are ignored.

To reproduce changed recording audio from the approved Japanese scripts, run the following from this locale folder (the first and third steps use ElevenLabs):

```sh
python3 tools/japanese_video_audio.py synthesize
python3 tools/japanese_video_audio.py prepare
python3 tools/japanese_video_audio.py align
python3 tools/japanese_video_audio.py captions
python3 tools/japanese_video_audio.py mix
python3 tools/build_teaching_captions.py
```

Retain the ignored `_narration_work/` pacing receipts, native v4 and v2 reference masters, voice-only dubs and timing caches. Re-align and retime teaching sequences after changing their narration. Normal package builds use the checked-in finished videos and captions and require only generated slide WAVs.

## Recordings and verification

The [Academy source recordings](https://academy.opencompute.org/learn/learning-plans/1/open-chiplet-economy-business-and-technology-of-chiplet-based-systems) retain every original video packet. Their audio is replaced by complete Japanese v4 narration and the maintained three-track music rotation, balanced 5/5/4. Music is normalized, ducked during speech, faded in and out. Voice-only masters remain in local production storage. The longest recording naturally repeats its music near the end. Raw music and its attribution are not included in the learner package.

Japanese captions use approved script orthography with measured Japanese speech timings. Captions start off. Recording visuals retain their source labels; authored figures, teaching videos, controls, transcripts, alt text, glossary and LMS descriptions are localized. Question IDs, choices, correct answers, technical values, URLs and module tracking match the canonical English source.

Source QA, audio-level/tail checks, caption and media validation, muted browser review and strict package checks are recorded in production evidence. Translation and speech recognition were reviewed by the authoring model; no native-speaker listening review or target-LMS acceptance is claimed. Launch, resume and separate module reporting in the target LMS remain deployment acceptance checks.
