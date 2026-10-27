# Data Centers: From Digital Services to Physical Infrastructure

An introductory Slides course connecting digital services to physical data-center infrastructure, then to OCP learning paths. One SCORM **1.2** package opens with **Course Home as the first SCO**, followed by **four independently tracked teaching modules**, **78 slides**, **10 preserved imported recordings**, **8 narration-synchronized teaching videos**, **68 narrated slides**, and **13 knowledge checks**. Estimated learner time is **95 minutes**; narration and recordings total **74:21** without double-counting teaching animations.

| Module | Title | Slides | Estimated time |
|---|---|---:|---:|
| 1 | The Digital World | 20 | 20 minutes |
| 2 | Data Center Physical Infrastructure | 18 | 30 minutes |
| 3 | Inside the Rack | 16 | 15 minutes |
| 4 | Management and Trends | 24 | 30 minutes |

Formal LMS copy is in [lms-catalog.md](lms-catalog.md) and [lms-catalog.json](lms-catalog.json), separate from this maintainer README. `thumbnail.png` is the separate LMS poster; its editable source is `authoring/thumbnail.svg`.

## Edit and rebuild

`course.json` is canonical. Paired narration text is in `audio/moduleN/`; editable static figures are SVGs under `figures/`. Generated videos retain deterministic HTML/SVG sources under `animations/`, with final-WAV word maps, timelines and receipts under `authoring/qa/`. All ten imported MP4 recordings, covers and caption files remain source-owned resources. Original course contributions: **Matty Bakkeren, Founder of Momenthesis**.

From the repository root, extract the approved delivery ZIP outside the checkout and run:

```sh
EXISTING_AUDIO_DIR=/absolute/path/to/approved/audio bash scripts/build-course.sh data-center-basics
```

The repository build automatically uses the validated renderer/templates in `authoring/toolchain/academy-wizard`, selected by `authoring_toolchain`. This snapshot preserves the course’s matching questions, imported captions and technical notes, Home plus four-module SCO organization, SCORM 1.2 adapter and approved media/layout overrides. Declared offline fonts and XML schemas are copied by its scaffold. The strict zipper emits runtime files only and exports LMS catalog sidecars separately.

Generated WAVs, runtime pages and ZIPs are not tracked. The approved audio is required to reproduce the tested package byte for byte. For new narration, the pinned generator supports Leo / Eleven v4, same-text Multilingual v2 timing references at 1.18, pitch-preserving duration matching and receipts. New audio requires new word alignment and re-encoded teaching videos; clip-length parity alone is insufficient. The learner speed default remains 1.0.

See [BUILDING.md](authoring/BUILDING.md) for source builders and QA. Builders are optional regeneration tools: rebuilding the runtime uses the reviewed SVG/MP4 source assets directly.

## Playback and tracking

Imported videos use their own audio and black player with exposed controls, editable captions and transcripts. Their slide narration Play control is disabled. Generated teaching videos use the standard compact Play/Pause and Enlarge controls and remain synchronized with narration through pause, seek, speed, replay and enlarged views. They are silent finite passes with useful final states.

The LMS manifest starts with Course Home (`ITEM_LAUNCHER`, launching `index.html`), followed by `ITEM_MODULE1` through `ITEM_MODULE4`: five SCOs total. Home completes on launch and each teaching module remains independent. Each module saves its own bookmark, question attempts and completion. Checks require an attempt and allow retries; no score threshold is imposed. Completed modules return to their final slide. The SCORM 1.2 adapter limits saved state to 4096 characters and exposes save failures.

Green next-module buttons remain visible and clickable in local, review and LMS playback. Review carries review=1 and starts the next module at slide 1. The LMS syllabus remains available for arbitrary module selection. These direct page links do not provide a standard SCORM 1.2 target-SCO request; target-LMS tracking should be checked separately. Local editorial review begins at generated `module1.html?review=1`, which does not write learner state.

## Validation and provenance

The [final delivery report](authoring/qa/scorm12-delivery/README.md) records package/schema validation, the strict SCORM 1.2 simulation, a fresh-source rebuild with identical runtime bytes, 252 media layouts, 68 audio signal checks and muted real-media playback checks. Representative screenshots and portable browser harnesses are retained there. Local simulations do not establish target-LMS acceptance; test a separate LMS upload before learner release.

All 31 recovered source lessons remain represented. The [source crosswalk](authoring/provenance/source_lesson_crosswalk.json), [knowledge-check audit](authoring/provenance/knowledge_check_audit.md), research notes, Astra audits and dated revision records are retained outside the runtime. Two source checks were replaced at the user’s request (rack-busbar architecture and installation fit), and power continuity was added. The two remaining matching interactions preserve their concepts. Current source has 48 glossary definitions and 59 deliberately selected placements. User-approved vendor-link and generic-link removals remain reflected in `course.json`.

**Migration notice:** the user selected SCORM 1.2 for final delivery, replacing a local 2004 review build. A deployed LMS item may require a new upload and may not transfer attempts, bookmarks or completion history. Export needed reports and test a separate upload before retiring any existing item. No LMS upload or deletion was performed. Earlier dated 2004/pre-ZIP audit notes describe historical builds.

## Maintained next-module navigation refresh

The 2026-10-27 rebuild merges the installed AcademyWizard navigation template, retaining green double-chevron next-module buttons when an LMS API is present. Course Home remains the first of five SCOs, followed by the four teaching modules. Approved content, narration, media, manifest identifiers and completion/quiz policies are preserved. See `authoring/qa/green-navigation-refresh/` for 48 navigation-parity cases, fresh package checks and screenshots. The LMS tests use an isolated persistent parent API; no live LMS upload is part of the rebuild.
