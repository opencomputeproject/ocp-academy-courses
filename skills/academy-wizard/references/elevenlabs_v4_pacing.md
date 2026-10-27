# Eleven v4 with the existing Academy pacing

Read this when opting an English course or module into `eleven_v4` or
`eleven_v4_turbo`. Keep Leo (`bbGtsRRKUfYO634UxSjz`) unless another voice is
approved. The existing `stable` model policy stays on Multilingual v2 while
the English v4 pilot is reviewed; select v4 explicitly in narration metadata.

## Keep the learner and duration contracts

The learner speed dial starts at **1.0** when there is no saved preference.
Preserve the existing storage key, saved-choice restoration, slider range,
and narration/video playback behavior. Do not set the dial to 1.1 or 1.18,
clear saved learner choices, or edit catalog/course-description durations
to accommodate a model change.

Keep `narration.speed: 1.18`. With v2 this is the API synthesis speed. With v4
it specifies the speed of a **Multilingual v2 timing reference** using the
same voice, complete spoken script, stability, and similarity. Generate native
v4 without the unsupported API speed field, then use pitch-preserving
`ffmpeg atempo` on the finished audio to match that reference. A fixed 1.10
or 1.18 multiplier on native v4 is not equivalent to v2 at 1.18: native
pacing varies across scripts. Match each final clip within 50 milliseconds,
without padding silence or truncating speech. The adjusted WAV is what the
learner hears at dial 1.0 and what duration-reporting tools measure.

## Reference choices and generation

For an existing course, first verify that the old audio was generated with
Multilingual v2, the same voice, and speed 1.18. Preserve an immutable snapshot
outside the delivered package with its original `course.json` and paired
scripts/WAVs, keeping their course-relative paths. A module-only snapshot may
contain just that module's audio tree plus the original course metadata.
Reuse this first verified baseline on later retries; never replace it with
v4 output. Changed scripts cannot use old recordings as timing references.

```bash
python scripts/gen_audio.py /path/to/course/course.json --module 9 --force \
  --pacing-reference-root /path/to/module9-v2-baseline \
  --audio-work-dir /path/to/module9-v4-work
```

The generator validates the reference course's recorded voice/model/speed,
checks the paired script's spoken text, and preflights the selected jobs before
sending billable text. Supply the original verified metadata; do not relabel
unknown audio as v2 to make validation pass.

For new scripts with no verified old recording, omit `--pacing-reference-root`.
The first run synthesizes a same-text v2 timing reference **in addition to**
the native v4 narration. Budget for those two calls. The reference is cached
by script text, voice, model, speed, stability/similarity and chunk plan; later
v4 retries reuse it. Missing ffmpeg stops before either call. ffmpeg may come
from PATH or the `imageio_ffmpeg` package. The work directory defaults to
`<course>/_narration_work`; keep its references, native masters and timing
receipts out of source control and the manifest/SCORM ZIP.

The full v4 clip is assembled before time adjustment, including any approved
`audio.synthesis_chunks`. Keep complete narration and natural pauses. A failed
synthesis or adjustment leaves the previous final WAV intact. Each receipt
records target/native/final durations, the applied factor, voice/settings,
script/reference/output hashes, and the native master's path. Do not use the
processed WAV as another native source and compound speed adjustments.

## Limit a pilot to one module

A module's `narration` object overrides matching top-level narration fields.
Explicit command options still take precedence. For module 9, add:

```json
"narration": {
  "engine": "elevenlabs",
  "voice_id": "bbGtsRRKUfYO634UxSjz",
  "voice_name": "Leo v2",
  "model_id": "eleven_v4",
  "speed": 1.18
}
```

Put this on the module object, not on its slides or the course-wide object,
when other modules are to keep their current model. Whole-course rebuilds
also respect these module overrides. This setting authorizes model-specific
pacing; it does not authorize rewriting scripts, course descriptions, player
defaults, other language editions, or published LMS content.

Run `audio_tail_report.py` over the generated clips, inspect the timing
receipts against the immutable baseline, and compare the module totals at
player 1.0. Review the actual `module9.html` course page. Confirm start/middle/
end pronunciation and vocal projection, knowledge-check narration, slide
transitions, speed persistence, and any narration-synchronized video. Equal
clip duration does not guarantee equal word/cue timing. Human listening
approval remains necessary before broad adoption; do not claim that a signal
check proves the new narration sounds better. Preserve the existing SCORM
version and packaging/release gates.
