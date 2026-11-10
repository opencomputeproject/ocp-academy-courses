# MP3 narration for new courses and updates

The default learner narration is 44.1 kHz, 96 kbps CBR mono MP3. Record
`narration.delivery` with `format: "mp3"`, `approved: true`, `bitrate_kbps: 96`,
`sample_rate_hz: 44100`, `channels: 1`, and `bitrate_mode: "CBR"`.
Every narrated slide keeps `audio.wav_file` for its paced authoring WAV and
uses `audio.delivery_file` for the MP3. Original recordings keep their own audio.
Explicit course delivery overrides remain authoritative.

Request `output_format=mp3_44100_96` directly from ElevenLabs using full
`eleven_v4` and the approved voice. Keep the provider MP3. Decode it to a native
WAV for the existing pitch-preserving 1.18 pacing and quality workflow. This is
a decoded master, not a lossless original. Retain native and paced WAVs and
receipts outside the release ZIP. Because v4 does not accept a speed field,
post-generation pacing still requires a final MP3 encode; do not claim the
provider bytes are unchanged in learner delivery.

## Existing WAV courses: ask before migration

On every rebuild, inspect `narration.delivery` and slide audio paths before
scaffolding, TTS, rendering or packaging. WAV-only sources without delivery
metadata count as previously defaulted to WAV, even if their generated audio
is absent from the repository. Ask: “Convert all course narration to 96 kbps
MP3 for smaller files and faster learner downloads? I'll retain the WAV masters
and reuse approved audio without new ElevenLabs charges.” A generic request to
rebuild with the updated skill is not consent; an explicit MP3 request is.

After agreement, record the decision in the canonical source:

```bash
python scripts/audio_delivery_defaults.py course.json --audio-delivery-choice mp3
```

If declined, use `--audio-delivery-choice keep-wav`. The decision is saved as
`narration.delivery.migration_decision`; a recorded decline avoids repeated
prompts on unchanged rebuilds. A later explicit MP3 request supersedes it.
The source and build preflight stop without mutation when a WAV decision is
missing. `new_course.py` and `encode_delivery_audio.py` also accept the flag;
when staging into a separate folder, persist the same decision in source.
The repository wrapper accepts
`./scripts/build-course.sh <course> --audio-delivery-choice mp3` and records it
before staging or any paid requests. Do not bypass a pinned course toolchain
without reviewing its compatibility requirements.

New authoring declares the MP3 settings above before adding narrated slides;
this distinguishes a new course from ambiguous older WAV-only sources.
Keep original-video soundtracks, Scrolling courses without narration, model,
voice, pacing, SCORM organization, and explicit non-WAV codec overrides unchanged.

## Encode and validate

Run `encode_delivery_audio.py` after pacing or approved migration. It encodes
from paced masters, fully decodes the result and checks duration parity.
Existing approved WAV recordings may be
compressed without new TTS calls. Do not regenerate them solely for a format
change. Module/manifest rendering selects only delivery audio, excluding WAVs.

Do not change model, voice, pacing, SCORM version, captions or animation timing
to achieve compression. Revalidate seeking and synchronized animations against
the delivered MP3. A codec test does not establish listening quality.

Sources: https://elevenlabs.io/docs/api-reference/text-to-speech/convert and
https://github.com/elevenlabs/elevenlabs-python/blob/main/src/elevenlabs/types/output_format.py
