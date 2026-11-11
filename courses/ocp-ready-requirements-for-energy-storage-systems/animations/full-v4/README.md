# ESS Full-v4 Teaching Animations

Four editable, shared SVG/HTML scenes, eight language editions. No tool in this
directory changes course JSON, narration scripts, audio, player code, logos, or
unrelated static figures. The previous workflow builder remains untouched for
provenance; use this implementation for the refreshed workflow.

## Teaching and Playback Contract

| Placement | Teaching sequence | Playback |
| --- | --- | --- |
| M1S3 | Centralized/distributed conceptual comparison, then deployment labels | Final-narration clock; one pass; final-frame hold |
| M2S6 | IT baseline, facility load, additive recharge; three approved illustrative comparisons | Final-narration clock; one pass; final-frame hold |
| M3S6 | Detection, ventilation, backup power, suppression, coordinated controls | Final-narration clock; one pass; final-frame hold |
| M4S8 | Eight approved workflow states and community feedback return | Existing independent 14-second loop preserved during rebuild |

M1/M2 quantities are qualitative, not site-sizing data. M2 retains the approved
relative bar heights and adds a localized illustrative-data qualifier. M3 uses
an undirected coordination spine, not an automatic trigger sequence. Explosion
control keeps its existing applicability qualifier. Backup power retains its
own spacious band. Storage remains technology-neutral.

All media is free of decorative slide headings and Academy furniture. The M1
rack nodes coincide exactly. M3's whole composition is vertically centered.
Workflow numbers do not cross arrows. Shafts meet explicit triangular heads at
the midpoint of their flat back, and tips stop at target boundaries.

## Editable Inputs

- `scene.js`: shared SVG geometry and finite deterministic timeline.
- `labels.json`: editable snapshot of approved localized labels, alt text,
  captions and source references. `extract_labels.mjs` refreshes it explicitly
  from course SVGs and existing workflow strings; never refresh silently during
  an encode. Inherited translation concerns are separate editorial issues.
- `qualifiers.json`: localized illustrative-data qualifier.
- `cue-selections.json`: reviewed semantic cue choices and their anchors.
- `alignment/<locale>/*.json`: local transcript-assisted timing evidence only.
  Recognition output is not a learner transcript and may contain ASR errors.
- `timings.final.json`: final WAV durations, course-relative paths, SHA-256s and
  selected cue times. No proportional duration guessing.
- `figure-patch-manifest.json`: figure replacements and per-asset readiness.

`final_audio_verified` means final generation was reported ready by the rebuild
owner, and local duration/hash checks bind the cues to that file. It does **not**
mean a person listened to it. `human_audio_review: "pending"` remains explicit.
Likewise, `cues_reviewed` denotes transcript-assisted semantic cue review, not
human listening approval or word-level forced alignment.

## Prerequisites

Node.js, Python 3, Playwright/Chromium, and a full FFmpeg build with libx264 and
zscale. The local alignment helper optionally uses whisper.cpp and a downloaded
multilingual model. All transcription runs locally; no keys or paid APIs.

Install a full FFmpeg build with libx264 and zscale on PATH as `ffmpeg`, or set
`FFMPEG_BIN` explicitly to select that executable. There is no private cache
fallback. Set `PLAYWRIGHT_MODULE` to
`playwright/index.mjs` and `PLAYWRIGHT_NODE_MODULES` to its containing
`node_modules` directory when not using the installed AcademyWizard dependency
tree. An optional `FFPROBE_BIN` is needed for non-WAV audio inputs; WAV durations
use Python's standard `wave` parser. The final production inputs here are WAVs.

The recorder is copied byte-for-byte from the repository's maintained
`skills/academy-wizard/scripts/record_css_animation.mjs` into ignored local cache
to resolve Playwright without modifying shared tools. Its SHA-256 is recorded.
Override its location with `--recorder` only to select another maintained copy.

## Rebuild Sources and Review Frames

Commands are relative to this directory; supply actual paths for the variables.

```sh
SOURCE=/path/to/courses/ocp-ready-requirements-for-energy-storage-systems
AUDIO_ROOT=/path/to/ESS_Full_V4_Rebuild
OUTPUT_ROOT=/path/to/review-build
export FFMPEG_BIN=/path/to/full/ffmpeg

node build.mjs --course-root "$SOURCE"
node qa.mjs --course-root "$SOURCE"
```

Without final timing inputs, the three narration scenes are clearly tagged
`preview-only`; these clocks are not encodeable. Source files open paused on the
completed picture. `?play=1` explicitly previews one finite pass, and `?time=1234`
seeks to a source time in milliseconds. Reduced motion opens the final picture.

QA materializes each SVG before running the repository arrow checker. It checks
actual glyph bounds with 0.75em clearance, five evenly spaced frames and both
sides of all transitions, all-frame reveal continuity, seek determinism, a stable
last second, overrun clamping, and mobile framing. Inspect the resulting PNGs;
automated containment is not a substitute for visual review.

## Refresh Timing Against Final Audio

External audio is resolved as:
`AUDIO_ROOT/<locale>/<course-slug>/audio/moduleN/<clip>.wav`.
Generation receipts remain external at
`AUDIO_ROOT/_narration_masters/<locale>/<generation-id>/receipt.json`.
Before encoding or reuse, the current comment-stripped script and final WAV
must both match the same full-v4 receipt. The script normalization matches the
course build guard exactly. Only the verified script digest is exported as
`figure.narration_script_sha256`; receipt paths are not copied into public source.

```sh
node measure_audio.mjs --course-root "$SOURCE" --audio-root "$AUDIO_ROOT"
node align_audio.mjs --course-root "$SOURCE" --audio-root "$AUDIO_ROOT" \
  --locale en-US --slide M1S3 --model /path/to/ggml-base.bin
```

`measure_audio.mjs` produces `timings.template.json` with deliberately empty
cues and unverified flags. For manual timing, fill those fields after review.
For transcript-assisted timing, review the local transcription against the
approved script, update `cue-selections.json`, then run:

```sh
node prepare_final_timings.mjs --audio-root "$AUDIO_ROOT"
# Update only newly verified editions while other locales remain held:
node prepare_final_timings.mjs --audio-root "$AUDIO_ROOT" --locales es-419,pt-BR
```

For newly generated WAVs, repeat alignment and semantic cue review. A changed
hash blocks encoding. Record that WAV SHA in its reviewed cue-selection entry,
so rerunning transcription alone cannot attach old cues to new narration.
Selected timing updates preserve every unselected edition. Foreign paired
encodes require locale status `verified` and zero clip flags in the external
`semantic-regeneration-summary.json`, not the superseded initial audio summary.
Reserve at least 1.5 seconds after all transitions for the
completed picture. M2 must finish each underlying layer before the next grows.
M4 always keeps its existing 14-second finite source pass; only the player loops.

## Encode

```sh
node encode.mjs --course-root "$SOURCE" --audio-root "$AUDIO_ROOT" \
  --timings timings.final.json --output-root "$OUTPUT_ROOT" \
  --locale en-US --slide M1S3

node encode.mjs --course-root "$SOURCE" --audio-root "$AUDIO_ROOT" \
  --timings timings.final.json --ready-only --resume

node encode.mjs --course-root "$SOURCE" --slide M4S8

node encode_batch.mjs --workers 3 --course-root "$SOURCE" \
  --audio-root "$AUDIO_ROOT" --timings timings.final.json --ready-only --resume

node encode_batch.mjs --workers 3 --course-root "$SOURCE" --slide M4S8 \
  --locales ko-KR,ja-JP,zh-CN,zh-TW,es-419,pt-BR --resume
```

Omitting `--output-root` writes to the source edition's `figures/` directory.
Providing it writes only animation media/source/poster/geometry assets beneath
`OUTPUT_ROOT/<locale>/<course-slug>/figures/`. Timing and manifest records stay
in this authoring directory. `--locale` and `--slide` select one edition/scene;
omitting them selects all. `--ready-only` skips narration clips without reviewed
timings. `--resume` retains matching encoded media and its reviewed compiled
source. Run `build.mjs` explicitly or omit `--resume` when applying source edits.
Reuse requires matching full-file `source_html_sha256` and
`geometry_source_sha256` values, plus the media and narration hashes. Missing
source hashes fail closed; CSS, geometry or label changes invalidate reuse.
The encoder rereads the
timing file before each asset, allowing newly ready locales to join the batch.

The maintained recorder captures lossless PNGs at 30 fps and encodes one exact
master pass: H.264, slow preset, animation tuning, CRF 8, yuv420p, BT.709, silent.
A representative-frame fidelity preflight starts at 1920x1080, then tests
2880x1620 and 3840x2160 only when fidelity requires more pixels. Valid existing
higher-resolution encodes can be retained. `--scale` explicitly
tests one supported scale, without bypassing quality checks. The encoded duration
must be within one frame of the final WAV. All subordinate animation is finite.

The encoded frame is converted from limited-range BT.709 to full-range RGB using
zscale before comparing it with the lossless PNG. Acceptance targets remain
SSIM >= 0.995 and PSNR >= 45 dB. Raw comparisons using an older swscale path
introduced a false whole-frame RGB shift and are not the acceptance metric.
Check native and 200% detail visually even when metrics pass. Partial outputs
are retained on failure and must not be integrated.

Parallel encoding uses at most three locale workers. Every locale/scene has a
private recorder copy, calibration files, and job lock under ignored `.cache/`.
Short mkdir-based locks protect shared manifest and QA-report read/modify/write
operations; whole encodes never hold the manifest lock. Atomic JSON replacement
prevents readers seeing partial writes. A dead process lock deliberately fails
closed: stop workers before removing the stale lock. Do not bypass job locks or
run independent build commands against the same scene during an encode.

Run `node --test test_*.mjs` for timing, script/source binding and cross-process
locking regressions. Working frames, ASR diagnostics and calibration caches stay
local and ignored by Git, as requested by main.

## Integrate Without Overwriting Main's Work

The manifest identifies each slide by module/slide number, ID and slug. Replace
only `figure` after that asset's encode and visual review. Do not merge a whole
saved slide or course, and do not change source references from the snapshot:
main may have updated those independently. Keep captions localized.

M1/M2/M3 explicitly require `sync_to_narration:true`, `autoplay:false`,
`loop:false`, `muted:true`. M4 explicitly requires `sync_to_narration:false`,
`autoplay:true`, `loop:true`, `muted:true`. Leave global
`narration.teaching_video_mode` unset for this mixed-mode course. The current
strict all-synchronized validator has no per-figure exception support. Do not
change M4 to satisfy that validator. This preserves the existing approved
course's `loop:true` behavior; it does not assert new user approval of a cyclic
teaching purpose.

`inventory_candidate` is hash-bound but is not automatically a completed media
review. Promote it to `figure.text_inventory` only after reviewing the encoded
visible labels. Human listening, integrated embedded/enlarged player behavior,
end/hold/replay, reduced motion, mobile, and LMS review remain separate gates.

After inspecting the decoded native, transition and 200% frames, run the full
muted playback check and record review. The export preserves the current course's
reviewed alt text and caption, never overwriting those with an older snapshot:

```sh
node verify_playthrough.mjs --locale en-US --slide M1S3
node record_visual_review.mjs --locale en-US --slide M1S3 \
  --audio-root "$AUDIO_ROOT" --record-visual-review
```

For independent loops, first run `review_encoded.mjs --locale <tag> --slide M4S8`
and `verify_playthrough.mjs --locale <tag> --slide M4S8`. Inspect the five-frame
sheet, every transition sheet, the native final frame and 200% comparison. The
playthrough check decodes a full muted 1x pass and separately crosses the loop
boundary. `record_visual_review.mjs` requires that hash-bound playback evidence
before publishing a reviewed M4S8 inventory; it needs no narration input for M4.

The review step exports measured `figure.duration_seconds` for every video and
the verified script SHA for synchronized figures. `figure-patch-<locale>.json`
contains only visually reviewed figures, with `edition_complete` and
`omitted_slides` distinguishing partial handoffs from complete editions. Main
may integrate reviewed M4S8 while the paired scenes stay held. It does not imply
human listening approval. Foreign paired scenes are enabled edition by edition
in `encoding-policy.json` only after repaired labels and fresh audio hashes/cues
are verified. Consult that policy for the current release list. The seven
semantically reviewed localized editions may encode their independent M4S8
loops without narration inputs. All seven localized paired editions now have
revised full-v4 readiness and reviewed hash-bound cues. Human listening remains
pending for every edition.

Do not package the authoring HTML, geometry snapshots, QA frames, model weights,
alignment evidence or build receipts as learner runtime assets. Runtime needs
the final MP4 and poster, plus the course's normal narration and player.
