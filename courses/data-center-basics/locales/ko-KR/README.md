# 데이터센터: 디지털 서비스에서 물리적 인프라까지

Korean edition (`ko-KR`) of the [canonical English course](../../README.md).

This independently editable source preserves four modules, 78 slides, 13 knowledge-check questions and answer keys, and SCORM 1.2 with five tracked entries: Course Home followed by Modules 1–4. The learner-time estimate remains 95 minutes.

- [Translated LMS title and descriptions](lms-catalog.md)
- [Structured LMS catalog copy](lms-catalog.json)
- [Translation QA and review limitations](../../TRANSLATION_QA.md)

## Rebuild with the delivered audio

From the repository root, supply this language's unchanged MP3s from its delivered ZIP (the directory containing `module1/` through `module4/`):

```sh
python3 courses/data-center-basics/authoring/build_translation.py ko-KR \
  --audio-dir /path/to/ko-KR/audio
```

The command checks the recorded MP3 hashes, selects this locale's pinned renderer, stages offline fonts and schemas, and validates the generated package under ignored `build/data-center-basics/ko-KR/`. It makes no TTS requests and does not re-encode media. Add `--zip` when an LMS ZIP is wanted. Use `--output` for a different empty build directory outside the editable course source.

Narration scripts remain editable in `audio/`; generated MP3s, WAV/provider masters, provider receipts, rendered runtime pages and ZIPs are not committed. [delivery-audio.json](authoring/delivery-audio.json) identifies the delivered audio expected by this rebuild. Changing narration requires a deliberate new audio release and retiming the paired teaching video.

## Media and playback

Ten original Matty recordings keep their pictures and English audio, with translated captions/transcripts and an English caption option. Their slide narration controls remain disabled. Eight teaching videos have localized labels, editable HTML/SVG animation sources and narration-synchronized single-pass timelines with a final hold. The circular Matty Bakkeren author acknowledgement remains on M1S2.

Native full Eleven v4 narration uses the recorded locale voice, approved 1.18 pitch-preserving processing and 44.1 kHz / 96 kbps CBR mono MP3 delivery. The learner speed starts at 1.0. Reuse the shared [English LMS poster](../../thumbnail.png); there is no locale catalog poster.

Translation is machine-assisted with technical and automated review. Native-speaker editorial and human-listening approval remain pending; the retained automated evidence does not claim those approvals. No audio was played aloud during the build or repository assembly. Repository publication itself does not upload or replace LMS training material.
