# OCP Project Deschutes

Coolant Distribution Unit (CDU) Specification v1.0.

This course source is intended for PR-friendly editing. Change slides, quiz content, glossary links, and figure assets in `course.json`. Change narration in `audio/moduleN/slide_*.txt`. Generated audio and SCORM runtime files are not checked in.

## Modules

| Module | Title | Summary |
|---|---|---|
| 1 | Why Deschutes, Why Now | Motivation, the FWS -> CDU -> TCS architecture, and the v1.0 headline specs. |
| 2 | CDU Architecture & Performance | Inside the v1.0 CDU: physical envelope, fittings, pump/HX/sensor suite, controls, electrical, hot-swap. |
| 3 | Deployment, Supply Chain & Call to Action | Redmond HAC, rack power architecture, the three-tier supplier model, FRUs, contained pump service, and how to get involved. |

## Teaching animations

Each module includes one short, silent teaching animation that plays alongside the narrated lesson:

| Module | Concept |
|---|---|
| 1 | The CDU as the thermal bridge between facility water and the technology cooling system |
| 2 | Concurrent PLC control loops for pump speed, valve position, and redundant power |
| 3 | Contained pump service while the redundant pump maintains coolant flow |

The rendered WebM files and poster images are in `figures/`. Their editable HTML animation sources are in `animations/`.

`animations/render_animation.js` delegates to the maintained deterministic recorder: lossless PNG frames, a 1920x1080 viewport, and high-quality VP9 WebM or H.264 MP4 output. Locale wrappers use the same recorder. Set `FFMPEG_BIN` when a full ffmpeg build is not on the system path. Keep the recorded cyclic playback mode and finite source timeline when editing these animations.

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh project-deschutes-cdu-specification-v1-0
```

The finished SCORM folder and LMS zip are created under `build/`.

Narration uses full Eleven v4 with the recorded language-specific voice and 1.18x pitch-preserving pacing. Delivery audio is 96 kbps CBR, 44.1 kHz mono MP3; WAV authoring masters and generation receipts stay outside the runtime ZIP. The existing approved teaching animations retain their independent-loop playback.

The course remains SCORM 1.2 with four tracked activities: Course Home and three modules. The separate first-module and next-module page links do not switch the LMS tracking context; verify launch, bookmarks, quizzes, and completion in the target LMS syllabus before replacing a live edition.

## LMS Metadata And Translations

`lms_catalog` in each `course.json` is the editable LMS listing source. Its checked `lms-catalog.json` and `lms-catalog.md` exports contain the title, short and long descriptions, learner-time estimate, and module summaries. Packaging writes JSON, Markdown, and HTML catalog sidecars beside each ZIP, not inside it.

The seven translated editions are in `locales/`: `es-419`, `ja-JP`, `ko-KR`, `pt-BR`, `vi-VN`, `zh-CN`, and `zh-TW`. All editions share the English catalog poster. The 40-minute catalog estimate is learner time, not a promise that every language has the same measured narration duration.

## Public References

The original research files are not included in this repository. Public learner/source references used by the course include:

- OCP contribution: Project Deschutes: Data Center Facilities V1.0.0
- 2025 OCP EMEA Summit recording: Project Deschutes: Google's Open Spec CDU contribution to the industry
- Google Cloud blog: AI infrastructure is hot. New power distribution and liquid cooling infrastructure can help

## Catalog poster

Edit `poster.json` for wording and artwork. The shared Academy template fixes typography, gradients, logo and pill positions, and the white emblem dimensions. Rebuild from the repository root:

```sh
node skills/academy-wizard/scripts/render_lms_posters.mjs --repo-root . --course courses/project-deschutes-cdu-specification-v1-0
```

See [the poster standard](../../skills/academy-wizard/references/lms_poster_style.md) for dependency setup, title-fitting rules and full-catalog checks.
