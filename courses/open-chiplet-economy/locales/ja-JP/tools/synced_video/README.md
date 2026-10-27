# Narration-synchronized teaching sequences

The user approved Astra's M4S3, M5S3 and M9S6 storyboards and production on
23 October 2026. Sol coordinates production and final course verification.
The four translated sequences use finite narration-master timelines.

The user subsequently requested M1S3 with the same Astra support and finite
narration-synchronized treatment, plus precise M4/M9 ending underlines.
M1S3 is the fourth opted-in figure; its storyboard is in
`video_source/storyboards/M1_STORYBOARD.md`.

- `m1.py`, `m4.py`, `m5.py`, `m9.py`: deterministic SVG at any narration time.
- `produce.py`: measured WAV durations, 30 fps frame counts and QA samples.
- `rasterize.mjs`: Noto Sans JP vector-to-lossless-PNG rasterization and silent
  2560×1440 H.264 encoding, retaining white and improving fine colored edges.
  Uses the bundled Sharp library; set `SHARP_MODULE` if needed.
- `production.json`: recorded approval, source references, final audio hashes,
  cue boundaries, captions and reviewed visible-text evidence.
- `metadata.py`: preserves the approved figure configuration during authoring.
- `measure_underlines.mjs` / `font_metrics.json`: exact SVG phrase ink bounds;
  rerun the measurement if changing the font, font weight, size or wording.

Run from the course root:

```text
python3 -m tools.synced_video.produce samples
node tools/synced_video/rasterize.mjs samples m4
python3 tools/academy_wizard/scripts/check_svg_arrows.py audit/synced-video-production/native-svgs --fail-on-flags
python3 -m tools.synced_video.produce encode
node tools/synced_video/rasterize.mjs encode m4
```

Repeat Node commands for m1, m5 and m9. Results stage under `_video_work/synced-pilots/`
until native-size, displayed-size, transition, decode-quality and complete-pass
checks pass. Preserve `production.json` and the exact paired narration when
regenerating. Replacing these four media files requires synchronizing
their hashes and visible-text inventories there and in `course.json`.

Editorial authority: `video_source/storyboards/storyboards.json`. Production
evidence: `audit/synced-video-production/`. Other authored loops and original
recordings retain their existing playback modes.

## Japanese timing

The Japanese edition retains the approved scene structure and maps each phase to measured Japanese speech landmarks in `video_source/timing-ja.json`. `japanese_timing.py` applies that mapping before the scene renderer. Run `python3 tools/retime_japanese_videos.py` after re-aligning an approved script, then regenerate samples and measure underlines with `node tools/synced_video/measure_underlines.mjs`. Approved label translations are in `video_source/labels.ja.json`; do not replace them with recognition spellings.
