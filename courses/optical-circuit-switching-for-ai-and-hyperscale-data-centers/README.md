# Optical Circuit Switching for AI and Hyperscale Data Centers

An introductory AcademyWizard Slides course rebuilt from five Rise courses based on the April 2026 OCP OCS whitepaper. Estimated learner time is 75 minutes. Course Home and the five modules are separately tracked: six SCORM 1.2 syllabus entries in total.

The editable source retains all 32 original lessons' scope and seven original recordings with their soundtracks, supplied caption tracks and transcripts. The course adds 55 narration scripts, 15 editable technical SVG figures, five narration-timed teaching videos, 14 glossary terms and ten new questions. See [formal LMS catalog fields](lms-catalog.md) for the approved title, short description and module descriptions.

## Modules

| Module | Learner time |
|---|---|
| Introduction to OCS | 12 minutes |
| The OCS Technology Landscape | 16 minutes |
| OCS in Action: Current AI Data Center Deployments | 18 minutes |
| Emerging OCS Use Cases | 18 minutes |
| What's Next for the OCS Ecosystem | 11 minutes |

Optional external viewing is excluded from these estimates. Required narration and original recordings take approximately 55 minutes; reading, interaction and reflection account for the remaining learner time. Teaching-video duration overlaps narration.

## Editable source and media

`course.json` is the content source of truth. Edit it and the paired `audio/moduleN/*.txt` scripts rather than generated module HTML. `figures/` contains new SVG figures, five silent H.264 teaching videos and their posters. `animations/` contains the deterministic HTML/SVG master timelines. `resources/` contains the seven preserved recordings, caption tracks and posters.

Original recordings play manually with their soundtracks in the shared recording player. They have no additional slide narration. New teaching videos follow their paired narration, play once and hold their final frame in both normal and enlarged views. Changing that narration requires updating alignment and re-encoding the corresponding video.

Learner narration uses ElevenLabs Leo, full Eleven v4, pitch-preserving 1.18 pacing, and 44.1 kHz, 96 kbps CBR mono MP3 delivery. Generated MP3s, WAV masters, provider receipts and rendered HTML remain outside Git. No API credential is stored here.

The series poster is `thumbnail.png` with editable `poster.json` and `ocp-ocs-mark.svg`. Five additional module posters and their editable SVG artwork are under `posters/`. Offline Open Sans fonts and their license are under `assets/fonts/`.

## Build and review

From the repository root, reuse approved narration masters and delivery files:

```sh
EXISTING_AUDIO_DIR=/path/to/approved/audio \
FFMPEG_BIN=/path/to/ffmpeg \
bash scripts/build-course.sh optical-circuit-switching-for-ai-and-hyperscale-data-centers
```

`EXISTING_AUDIO_DIR` must contain module subfolders with the approved WAV masters and MP3 delivery files. Without it, the standard build generates narration using `ELEVENLABS_API_KEY`; do not regenerate approved audio unnecessarily. A source-only preview is available with `SKIP_AUDIO=1` and no existing audio directory; it does not create a delivery ZIP or validate audio.

The source pins its reviewed AcademyWizard build files through `authoring_toolchain`. This keeps reviewed layout, narration/video synchronization and SCORM behavior reproducible while the shared repository toolchain evolves. File hashes and the reviewed release checksum are recorded in `authoring/toolchain/provenance.json`. An explicit `ACADEMY_WIZARD_SKILL_DIR` build override takes precedence. Course-owned `scripts/build_resources.py` stages declared fonts and caption assets using the repository's resource hook.

Review the generated `build/optical-circuit-switching-for-ai-and-hyperscale-data-centers/index.html` and `module1.html` through `module5.html`. Append `?review=1` for an editorial pass without saving learner progress. Use normal playback to check bookmarks, assessment attempts and completion.

To rebuild teaching media, install the shared tool dependencies with `npm ci --prefix skills/academy-wizard`, install its Playwright Chromium browser, and provide an ffmpeg build with libx264. Then run `authoring/astra-media/build_animations.py` and `authoring/astra-media/encode_all.py`. The course-local recorder preserves the explicit RGB-to-BT.709 conversion used for reviewed colors. `authoring/align-teaching-narration.py` can request updated phrase timings using `ELEVENLABS_API_KEY` when approved audio changes. Static SVG sources can be regenerated with `authoring/astra-media/build_figures.py`; review inventories and refresh affected hashes after any media edits.

## Source fidelity and references

The primary reference is the [April 2026 OCP OCS whitepaper](https://www.opencompute.org/documents/ocp-ocs-white-paper-april-2026-final-pdf/). `authoring/content/source-fidelity.json` maps all 32 source lessons and archives the 18 replaced questions. Recovered lesson and conversion records are under `authoring/source-inventory/`. Original-media SHA-256 hashes cover all 21 recording, caption and poster files.

Three 2026 OCP Global Summit presentations are referenced contextually: [Interoperable Multi-Vendor OCS Use Cases](https://www.youtube.com/watch?v=LQJmCZUTHic), [Standardizing OCS Interfaces](https://www.youtube.com/watch?v=_TBtUSijLAM), and [Zero-Touch OCS Fabrics](https://www.youtube.com/watch?v=XjJ8sXzr-Oc). Research covers all 47 presentation pages. Full video links are used because topic start times could not be verified. Evidence and limitations are in `authoring/summit-research/reference-map.json`.

[Fast Optical Circuit Switching for Dynamic AI Fabrics](https://academy.opencompute.org/learn/courses/79/fast-optical-circuit-switching-for-dynamic-ai-fabrics) is an optional continuation for workload timing and complete reconfiguration readiness. It remains a separate course.

New explanations qualify optical budgets, technology timing, quantum transport, research maturity and recovery dependencies without editing the original recordings. Active assessment has one new single-answer and one new multi-select question per module. Learners submit both questions to continue; correctness is not a passing threshold. Individual contributor acknowledgements are omitted from all five objectives slides and their narration at the user's request; historical attribution remains in editorial provenance.

## Validation and delivery

Run the pinned `scripts/course_delivery_summary.py course.json --check` and the shared `skills/academy-wizard/scripts/slides_course_qa.py <course.json> --repo-root . --fail-on-flags` from the repository root with the appropriate paths. Review receipts are under `authoring/qa/`; the publication audit records source/media integrity and a rebuild comparison with the approved runtime.

Keep generated narration, rendered module/home HTML, SCORM ZIPs and local caches outside Git. Packaging validates and exports the same LMS copy as JSON, Markdown and HTML sidecars. The six-entry SCORM 1.2 package has been built and checked locally; a target-LMS session test remains outstanding. Use the LMS syllabus for tracked module navigation: a direct home Start link cannot itself switch SCORM 1.2 tracking context.

The five original SCORM 2004 activities become one six-SCO SCORM 1.2 course under the approved conversion scope. Existing attempts, bookmarks and completion history may not transfer. Test a separate import before replacing deployed material. This repository contribution does not upload, delete or reset any LMS item.
