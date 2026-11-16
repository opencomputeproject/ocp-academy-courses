# Falcon Transport

A technical OCP Academy narrated Slides course based on the [Falcon Transport Specification v1.2.0](https://www.opencompute.org/wp-content/uploads/2026/11/Falcon-Networking-Transport-Protocol-v1.2.0.pdf). Follow worked packet exchanges from transaction boundaries through delivery recovery, congestion feedback and path decisions.

This is **one approximately 60-minute course**, with 33 slides, nine silent animations synchronized to narration, and six page-cited knowledge-check questions. Its single SCORM 1.2 package has **four tracked SCOs**: Course Home first, followed by the three modules below. Optional external recordings are outside the duration estimate.

| Module | Scope | Estimated learner time |
|---|---|---:|
| 1. Transaction Architecture | Roles, connection/transaction/packet identities, ordered push and pull flows, resource independence and compatibility | 20 min |
| 2. Reliable Delivery and Loss Recovery | Receiver state, EACK feedback, selective repair, RACK, TLP, retry ownership and CIE/Resync | 20 min |
| 3. Congestion Control and Multipathing | Delay measurement, Swift control roles, CSIG, per-path credit, Max-Open-Window scheduling and PLB | 20 min |

Learners should know Ethernet, RDMA and basic congestion control. ULP mappings, application APIs, drivers, RTL, register programming and NIC microarchitecture are excluded. Numerical timing and window examples illustrate protocol behavior, not recommended deployment settings. The course distinguishes v1.1 features from v1.2 additions and preserves the older-peer interoperability limits.

## Editable source

- `course.json`: teaching content, transcripts, glossary, page references, quizzes, narration settings and four-SCO structure.
- `audio/moduleN/*.txt`: 33 readable narration scripts, including pronunciation guidance.
- `figures/moduleN/`: reviewed SVGs, nine silent MP4s and their posters.
- `animations/`: editable browser scenes and frozen narration-aligned cue data; see its [rebuild instructions](animations/README.md).
- `poster.json`, `thumbnail.png` and `falcon-series.svg`: one shared English catalog poster and the Falcon course mark. The mark's historical filename does not indicate a separate course series.
- `lms-catalog.json` and `lms-catalog.md`: formal LMS information exported from the editable source, separately from this README.
- [Outline](outline.md), [related-course and recording references](references.md), and `qa/`: authoring scope, overlap review and compact validation evidence.

Original research PDFs/decks, provider recordings, generated narration, rendered course pages, SCORM ZIPs and large review captures are not committed. Source references use the public specification URL. Page citations use physical PDF pages matching the footers; the specification's contents-page references are stale.

## Build

Install the repository build dependencies, including FFmpeg on PATH (or set `FFMPEG_BIN`). From the repository root, reuse approved narration without making TTS requests:

```sh
EXISTING_AUDIO_DIR=/absolute/path/to/approved/audio \
  ./scripts/build-course.sh falcon-transport
```

The audio directory must contain `module1/`, `module2/` and `module3/`, with the matching paced WAV masters and/or approved MP3 delivery files. The build stages source and media under `build/falcon-transport/`, validates the package and creates `build/falcon-transport.zip` with matching LMS metadata sidecars. The generated files remain outside source control.

For fresh narration, configure `ELEVENLABS_API_KEY` securely and use the ordinary build command. Source records full `eleven_v4`, the Leo technical voice, pitch-preserving base pacing of **1.18×**, and 96 kbps CBR mono MP3 delivery. The learner's **1.0×** dial plays this already-paced recording; their 1.2× and 1.3× selections multiply it further. No key is stored in the course source.

Changing narration requires reviewing and retiming the paired animations against the new final audio. Preserve single-pass playback, completed final-frame hold, and hash-bound visible-text inventories. Regeneration alone does not validate synchronization.

Run source and LMS metadata checks before contribution:

```sh
python3 skills/academy-wizard/scripts/slides_course_qa.py \
  courses/falcon-transport/course.json --repo-root . --fail-on-flags
python3 skills/academy-wizard/scripts/course_delivery_summary.py \
  courses/falcon-transport/course.json --check
```

Rebuild the catalog poster using the [shared poster workflow](../../skills/academy-wizard/references/lms_poster_style.md):

```sh
node skills/academy-wizard/scripts/render_lms_posters.mjs \
  --repo-root . --course courses/falcon-transport
```

## Validation and LMS behavior

The reviewed build passed source/reference/glossary checks, SVG arrow checks, all 33 narration-quality checks, desktop/phone layout inspection, package validation and ZIP integrity checks. Real-media playback, synchronized enlargement, seeking, end holds, quiz resume and navigation passed 470 assertions. A further 18 real-time measurements confirmed 1.0×, 1.2× and 1.3× playback across all three modules; native/paced duration and package-file identity were checked for all 33 narration clips.

[Published course](https://academy.opencompute.org/learn/courses/99/falcon-transport/lessons). Docebo readback verified the Networking category, 60-minute average time, poster, Certificate of Completion - Single Course, OCP Data Center Technologies catalog, and the library-backed material in Courses Made with AI. The learner syllabus was checked for the exact four-SCO order.

Launch each SCO through the LMS syllabus to establish its tracking context. Direct links between HTML pages cannot themselves switch SCORM 1.2 tracking context. Preserve the SCORM version, SCO identifiers, Home-first order and separate module tracking when refreshing the deployed material.

Docebo's material-level desktop view mode was left at its Theater/Lightbox default; this creates the large overlay on launch. Browser fullscreen inside the course requires the learner's fullscreen control or F shortcut. Course Focus mode and autoplay inherit disabled defaults. These settings belong to the LMS and are not changed by this source contribution.
