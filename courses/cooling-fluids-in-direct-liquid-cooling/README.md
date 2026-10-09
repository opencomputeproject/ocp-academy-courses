# Cooling Fluids in Direct Liquid Cooling (DLC)

Single-phase TCS fluid guidance for direct-to-chip deployments.

The October 2026 English refresh adds the [PG25 Guidelines V1.0.0](https://www.opencompute.org/wp-content/uploads/2026/10/OCP-PG25-Guidelines-V1.0.0.pdf) as operating guidance alongside, not instead of, the two product base specifications. See [the update notes](PG25_GUIDELINES_UPDATE.md) for affected slides and source distinctions.

This course source is intended for PR-friendly editing. Change slides, quiz content, glossary links, and figure SVGs in `course.json`. Change narration in `audio/moduleN/slide_*.txt`. Generated audio and SCORM runtime files are not checked in.

English teaching-slide resource pills name the supporting PDF page or range and link directly to its first page, following the Grid Disturbance course treatment. The closing slide links to the four complete documents without page labels or fragments. Page numbers are one-based PDF viewer pages, including the cover; the PG25 base specification's printed footer is one lower. See the reference audit in [the visual review](VISUAL_REVIEW.md). This reference-only update preserves narration and media, and records the draft-only provenance of M3S8's 1000 CFU/ml water action threshold.

## Media

Course-owned SVG, PNG, and MP4 teaching assets are stored in `figures/`. Editable HTML/SVG and frame-rendering sources for the Module 3 commissioning animation are stored in `animations/m3_commissioning_sequence/`. The LMS poster is available as editable `LMS_Cooling_Fluids_800x400.svg` and upload-ready `LMS_Cooling_Fluids_800x400.png`; `thumbnail.png` contains the same 800 x 400 artwork.

The English visual refresh improves all 11 attached teaching figures and the commissioning video. See [the visual review](VISUAL_REVIEW.md) for the affected slides, instructional corrections, and validation results. The approved PG25-guideline narration is unchanged by this visual refresh.

To reproduce the silent 18-second commissioning video, run from this course folder with Node.js, Playwright, Chrome, and a full H.264-capable FFmpeg installation available:

```bash
FFMPEG_BIN="/path/to/ffmpeg" node \
  animations/m3_commissioning_sequence/render_frames.mjs \
  animations/m3_commissioning_sequence/animation.html \
  figures/commissioning_sequence.mp4 \
  figures/commissioning_sequence_poster.png
```

The encoder samples one complete master timeline into lossless PNG frames, then produces a 1920 x 1080, 30 fps H.264 video with no audio stream. The source and final encoded states must be reviewed whenever the animation changes.

## Modules

| Module | Title | Summary |
|---|---|---|
| 1 | Why Single-Phase Fluids Matter in DLC | Fluid boundaries, urgency, source discipline, and the two-phase contrast. |
| 2 | Choosing and Specifying Single-Phase Fluids | Water, PG25, chemistry windows, inhibitors, and compatibility evidence. |
| 3 | Commissioning, Filling, and Protecting the Loop | Serviceable design, compatible fill practices, filtration, startup records, and microbial control. |
| 4 | Monitoring, Maintenance, and Operational Judgment | Routine tests, lab QA, trend interpretation, adjustments, mixing, useful life, and documentation. |

## Language editions

English is the canonical source in this folder. Self-contained translated
authoring sources are available under `locales/` for:

- Korean (`ko-KR`)
- Japanese (`ja-JP`)
- Simplified Chinese (`zh-CN`)
- Traditional Chinese (`zh-TW`)
- Vietnamese (`vi-VN`)
- Brazilian Portuguese (`pt-BR`)
- Latin American Spanish (`es-419`)

Each edition preserves the English slide structure, technical facts, quiz
correctness, and reference URLs while localizing learner-facing text, narration
scripts, figures, the commissioning animation, controls, and accessibility
labels. Locale metadata records the approved ElevenLabs voice and model.

These translated editions retain the prior approved English baseline. The October 2026 PG25-guideline additions and visual refresh are currently English-only and have not yet been propagated into the seven locales.

Tracked follow-ups: [refresh all seven language editions (#83)](https://github.com/opencomputeproject/ocp-academy-courses/issues/83) and [resolve M3S8's unpublished-draft microbial action threshold (#84)](https://github.com/opencomputeproject/ocp-academy-courses/issues/84). The course owner confirmed on 9 October 2026 that the original water guideline draft remains unpublished; the approved narration is retained pending the workstream's decision.

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh cooling-fluids-in-direct-liquid-cooling
```

Build any translated edition independently:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh cooling-fluids-in-direct-liquid-cooling/locales/ko-KR
./scripts/build-course.sh cooling-fluids-in-direct-liquid-cooling/locales/ja-JP
./scripts/build-course.sh cooling-fluids-in-direct-liquid-cooling/locales/zh-CN
./scripts/build-course.sh cooling-fluids-in-direct-liquid-cooling/locales/zh-TW
./scripts/build-course.sh cooling-fluids-in-direct-liquid-cooling/locales/vi-VN
./scripts/build-course.sh cooling-fluids-in-direct-liquid-cooling/locales/pt-BR
./scripts/build-course.sh cooling-fluids-in-direct-liquid-cooling/locales/es-419
```

The finished SCORM folder and LMS zip are created under `build/`.

## Public References

The original research files are not included in this repository. Public learner/source references used by the course include:

- [Base Specification for Single Phase Water-Based Cold Plate Coolant V1.3](https://www.opencompute.org/documents/base-specification-for-single-phase-water-based-cold-plate-coolant-v1-3-final-pdf)
- [OCP Base Specification - PG25 - V1.0.0](https://www.opencompute.org/documents/ocp-base-specification-pg25-v1-0-0-final-pdf)
- [OCP PG25 Guidelines V1.0.0: operating and lifecycle guidance](https://www.opencompute.org/wp-content/uploads/2026/10/OCP-PG25-Guidelines-V1.0.0.pdf)
- [Guidelines for Using Water-based Heat Transfer Fluid in Single-Phase Cold Plate-Based Liquid-Cooled Racks](https://www.opencompute.org/documents/guidelines-for-using-water-based-transfer-fluids-in-single-phase-cold-plate-based-liquid-cooled-racks-final-pdf)
- [Guidelines for Using Dielectric Heat Transfer Fluids in Two-Phase Cold Plate-Based Liquid-Cooled Racks](https://www.opencompute.org/documents/guidelines-for-using-dielectric-heat-transfer-fluids-in-two-phase-cold-plate-based-liquid-cooled-racks-final-pdf)
