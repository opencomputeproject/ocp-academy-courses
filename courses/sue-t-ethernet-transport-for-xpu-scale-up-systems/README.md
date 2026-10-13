# SUE-T: Ethernet Transport for XPU Scale-Up Systems

An intermediate technical OCP Academy Slides course based on the SUE-T Base Specification v1.0.0. Follow accelerator memory transactions from command mapping to Ethernet delivery, predict packet packing and recovery, map XPU and AXI interfaces, and evaluate completion, memory visibility, and error handling.

This is one standalone SCORM 1.2 course with Course Home and four tracked module syllabus entries. It contains 47 narrated slides, six silent videos synchronized to narration, worked examples, and eight knowledge-check questions.

| Module | Scope | Estimated learning time | Recorded narration |
|---|---|---:|---:|
| 1. From XPU Transactions to Ethernet Transport | Endpoint responsibilities, transaction flow, Delivery and Operational ACKs, visibility | 18 min | 13.3 min |
| 2. Efficient Packets on a Lossless Fabric | Queue service, work-conserving packing, PDC state, lossless service and optional GoBackN | 25 min | 16.8 min |
| 3. Map the XPU Interface to the Transport | Command and network interfaces, credits, AxID ordering and AXI encoding | 16 min | 12.4 min |
| 4. Define Completion and Evaluate the Design | Completion contracts, visibility, response errors, cleanup and a worked 4096B AXI write | 16 min | 10.8 min |

Allow about 75 minutes including practice and review. The approved audio build contains 53.2 minutes of narration.

## Editable source

- `course.json`: slides, scripts/transcripts, glossary evidence, source links, narration settings, SCORM organization and recorded layout overrides.
- `audio/moduleN/*.txt`: 47 narration scripts. Generated WAVs are excluded from source control.
- `figures/`: static figures, six synchronized MP4s and their posters.
- `animations/`: editable browser animation sources and measured timing data.
- `render_course.py`: course-owned layout wrapper around the maintained AcademyWizard player. It preserves the M2S3 half-size figure and aligns left-aligned caption margins with the visible figure frame, with a 12px frame gap and at least 24px before learner-aid pills.
- `suet_mark.svg` and `thumbnail.png`: course mark and exact 800×400 Academy catalog poster.
- `delivery_metadata.json` and `LMS_METADATA.txt`: LMS title, short description, complete overview and durations.

M1S2's SUE-T v1.0.0 chip links to the specification. Teaching resource links retain page-specific references and the final resource links to the complete document.

The [SUE-T Base Specification v1.0.0](https://www.opencompute.org/wp-content/uploads/2026/10/Scale-Up-Ethernet-Transport-SUE-T-Base-Specification-v1.0.0.pdf) is the authoritative source. Original research files are not committed; extracted teaching figures and source-page references are retained.

## Build

From the repository root, reuse the approved narration without contacting TTS:

```bash
EXISTING_AUDIO_DIR=/absolute/path/to/approved/audio \
  ./scripts/build-course.sh sue-t-ethernet-transport-for-xpu-scale-up-systems
```

The build script selects `authoring_renderer` from `course.json`, uses the repository's maintained AcademyWizard implementation, validates the staged package, and creates one ZIP with `imsmanifest.xml` at its root. Generated runtime HTML, audio and ZIPs stay under `build/` and are excluded from source control. A fresh narration build instead uses the recorded ElevenLabs Leo v2 voice, stable multilingual v2 model and speed 1.18; configure `ELEVENLABS_API_KEY` securely before invoking the normal build.

Check the source and catalog entries with:

```bash
python skills/academy-wizard/scripts/slides_course_qa.py \
  courses/sue-t-ethernet-transport-for-xpu-scale-up-systems/course.json \
  --repo-root . --fail-on-flags
```

## Validation and LMS use

The reviewed course passed source/reference/glossary QA, automated audio level/tail checks, real synchronized-media playback checks, quiz/resume checks, course/module navigation checks, and desktop/mobile caption geometry checks. The release ZIP is checked for CRC integrity, manifest membership, and agreement with the built runtime resources.

Use the LMS syllabus to launch each tracked module. Local file playback can continue between modules, but a direct HTML link cannot switch the active SCO in an LMS. The maintained player uses syllabus handoff instructions for those transitions. Actual target-LMS acceptance and a signed-off full human audio listening pass remain unverified; neither an LMS upload nor a merge is part of this source submission.
