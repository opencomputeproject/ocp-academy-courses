# Optical Connectivity & Reliability for AI Infrastructure

Shared LMS descriptions and poster for the OCP Academy learning plan on optical technologies, connectivity practices, and reliability workflows for AI infrastructure.

Each course lives in its own sibling folder under `courses/`, with its own `course.json`, language editions, narration scripts, figures, and thumbnail. The LMS learning plan controls the order in which the courses appear.

## Available Course Sources

| Folder | Course | Description |
|---|---|---|
| [courses/introduction-to-emerging-optical-technologies](../introduction-to-emerging-optical-technologies/README.md) | Introduction to Emerging Optical Technologies | Emerging optical approaches for scale, efficiency, density, latency, and compute integration in AI infrastructure. |
| [courses/enhanced-telemetry-optics](../enhanced-telemetry-optics/README.md) | Enhanced Telemetry Optics | Enhanced telemetry for finding what failed, where, and why in AI optical fabrics. |

## Language Editions And LMS Copy

Both available courses have independent English, Simplified Chinese, Traditional Chinese, Korean, Japanese, Vietnamese, Latin American Spanish and Brazilian Portuguese editions. Each edition preserves SCORM 1.2 with Course Home and four module syllabus entries. Delivery uses 96 kbps MP3 narration; retained WAV authoring masters are not included in Git or the LMS packages.

Course-level formal titles, short descriptions and overview/module descriptions are maintained in each edition's `lms-catalog.json` and `lms-catalog.md`, separately from maintenance documentation. The series descriptions for all eight languages are in [lms-series-catalog.md](lms-series-catalog.md) and [lms-series-catalog.json](lms-series-catalog.json). LMS posters remain shared English assets.

## Planned Future Topics

Additional optics courses can be added directly under `courses/` as the learning plan expands.

- Introduction to Optical Fiber
- Cable Designs and Considerations
- Cable Installation and Handling
- Cable Entry and Preparation
- Splice Enclosures
- Fusion Splicing Considerations
- Fiber Panel Connectivity Considerations
- Connector Hygiene

## Catalog poster

Edit `poster.json` for wording and artwork. The shared Academy template fixes typography, gradients, logo and pill positions, and the white emblem dimensions. Rebuild from the repository root:

```sh
node skills/academy-wizard/scripts/render_lms_posters.mjs --repo-root . --course courses/optics
```

See [the poster standard](../../skills/academy-wizard/references/lms_poster_style.md) for dependency setup, title-fitting rules and full-catalog checks.
