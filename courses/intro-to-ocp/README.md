# Introduction to the Open Compute Project

An introductory, narrated **Slides** course about the OCP Community, open
infrastructure and practical ways to adopt, participate and contribute.
The estimated learner time is **45 minutes**, including expert videos,
narration, reading, activities and knowledge checks. Optional linked courses
are additional. No engineering prerequisites are required.

## Course structure

| Module | Focus | Estimated time |
|---|---|---:|
| 1. The OCP Origins | Origins, five tenets, open collaboration and evidence | 12 minutes |
| 2. The OCP Ecosystem & Governance | Community roles, governance and the contribution path | 10 minutes |
| 3. OCP Technologies — Open Rack & Cooling | Rack, power, cooling and facility interfaces | 14 minutes |
| 4. Today and Tomorrow — The Journey | Recognition, Marketplace discovery, pilots and further learning | 9 minutes |

The course has 52 slides, 46 MP3 narration clips, six expert recordings, four
narration-synchronized teaching animations and two knowledge-check questions
per module. Matty Bakkeren is acknowledged on Module 1 slide 2 as the original
course author and contributor, with his source portrait and Founder,
Momenthesis title. Additional narration is not represented as his words or
endorsement.

## Editable source and delivery

- `course.json` is the canonical editable definition, including transcripts,
  source references, glossary evidence, timing and formal LMS metadata.
- [LMS catalog copy](lms-catalog.md) and [structured fields](lms-catalog.json)
  are maintained separately from this README.
- `audio/moduleN/*.txt` contains the spoken scripts. Generated audio is not
  committed. Keep native provider MP3s, paced WAV masters and receipts locally.
- `figures/` contains teaching videos/posters and Matty's portrait;
  `animations/` contains their editable SVG and timed HTML source.
- `resources/` contains original recordings, captions, posters and the
  membership document. The recordings keep their original video soundtracks.
- `thumbnail.png` is the exact 800 × 400 Academy catalog poster;
  `poster.json` is its editable metadata; the shared renderer supplies the bundled logo and Lato font.

Narration uses full Eleven v4, Leo, 1.18 pitch-preserving authoring pacing,
and 44.1 kHz / 96 kbps CBR mono MP3 delivery. The learner speed dial remains
1.0 by default. WAVs are authoring masters, not runtime files. This course's
MP3 delivery is explicitly approved; no migration prompt is needed for it.

## Build

From the repository root, with existing approved audio (including WAV masters
and MP3 delivery files):

```bash
EXISTING_AUDIO_DIR=/path/to/audio ./scripts/build-course.sh intro-to-ocp
```

Set `FFMPEG_BIN` when ffmpeg is not on PATH. To generate new narration, provide
the ElevenLabs key through the environment and omit `EXISTING_AUDIO_DIR`.
Do not regenerate paid audio just for compression. New synthesis can change
timing: review and retime the paired teaching animations when necessary.
The script writes `build/intro-to-ocp/`, `build/intro-to-ocp.zip`, and separate
LMS catalog sidecars. The ZIP includes only manifest-listed runtime files;
generated HTML, audio, ZIPs and the delivery poster stay out of Git except for
the source-tracked `thumbnail.png`.

Review `index.html` and `module1.html` through `module4.html` in the generated
folder. `?review=1` isolates editorial review from saved learner progress.
Knowledge checks require an attempt on both questions, not a perfect score.

## Replacement and LMS deployment

This English course replaces the four independent Scrolling courses previously
stored beneath this folder. Their English and seven translated editions were
retired from the active source tree on 2026-11-03 at the user's request. They
remain recoverable from Git history at commit `6e3e5a2` and earlier. No new
language edition of this Slides replacement is claimed or generated.

The format remains **SCORM 1.2**, with **five tracked syllabus entries**:
Course Home, then Modules 1–4. This is one course ZIP, not four independent
packages. Consolidating the old LMS items does not transfer their tracking;
export needed reports and test a new upload before retiring them. Building
or publishing repository source does not delete anything in the live LMS.

The Docebo Syllabus remains the reliable way to select separately tracked
modules. Direct Start/Next actions require target-LMS acceptance testing;
local browser checks are not proof of separate-SCO tracking. Do not enable
forced Sequence ordering or change the SCORM version without a separate
deployment decision.

## Validation record

The 2026-11-03 reviewed delivery passed source/glossary and package validation,
ZIP integrity (46 MP3s, zero WAVs), MP3 decode/duration checks, quiz
resume/retry/navigation checks, and desktop/phone light/dark layout checks.
The final slide retains OCP Community and Contribution database resource
pills plus one Share Feedback box. Live LMS enrollment and tracking remain
to be verified during upload.

## Catalog poster

Edit `poster.json` for wording and artwork. The shared Academy template fixes typography, gradients, logo and pill positions, and the white emblem dimensions. Rebuild from the repository root:

```sh
node skills/academy-wizard/scripts/render_lms_posters.mjs --repo-root . --course courses/intro-to-ocp
```

See [the poster standard](../../skills/academy-wizard/references/lms_poster_style.md) for dependency setup, title-fitting rules and full-catalog checks.
