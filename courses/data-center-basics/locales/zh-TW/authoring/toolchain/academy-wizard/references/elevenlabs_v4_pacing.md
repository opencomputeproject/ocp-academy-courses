# Full Eleven v4 narration and pacing

Use full `eleven_v4` for every new AcademyWizard narration job. Keep the approved
voice; default English voice is Leo (`bbGtsRRKUfYO634UxSjz`). Retired models and
alternate-model timing calls are not permitted. Validate the live model/language
and voice combination before sending billable text; failure stops generation.

## Pacing and learner controls

Record `narration.speed: 1.18`. Generate the native full-v4 master without an API
speed parameter, then apply that multiplier with pitch-preserving `ffmpeg atempo`.
The target finished duration is the native duration divided by 1.18. A different
multiplier requires explicit user approval. This is a v4-only pacing setting;
do not claim it reproduces a different model's exact duration or cadence.

The learner speed dial starts at 1.0 and preserves saved choices. Keep course
catalog duration estimates; report measured narration time separately. Review
internal pauses, pronunciation and sustained projection as well as total runtime.
Do not pad silence, trim speech, or raise the learner's default speed to compensate.

## Generate and retain evidence

```bash
python scripts/gen_audio.py /path/to/course/course.json --module 1 --force \
  --audio-work-dir /path/to/authoring/v4-masters
```

Each clip retains its native master and a receipt with model, voice, script hash,
native/target/final durations, tempo multiplier and output hash. Only full v4 is
synthesized. Timing processing occurs after any approved same-text paragraph
chunks are assembled, and failed processing preserves the previous recording.
Keep masters and receipts outside the SCORM runtime and release manifest.

## Staged review and migration

When the user asks for one module first, generate and review only that module,
then stop until they authorize the remainder. Preserve immutable prior files for
recovery without keeping retired model choices in active skill instructions.
Do not relabel untouched recordings as regenerated. Record the completed module
and pending modules explicitly in a mixed review build.

Run audio checks and inspect pacing receipts. Verify actual course playback,
1.0/default and saved speed behavior, knowledge checks and synchronized teaching
video in embedded and enlarged views. Retime paired video to the final audio,
matching within one encoded frame; preserve one-pass playback and final-frame hold.
Human listening approval remains necessary. Stop before ZIP creation or publishing
unless separately authorized.
