# Enhanced Telemetry Optics

Enhanced telemetry for finding what failed, where, and why in AI optical fabrics.

This standalone SCORM course belongs to the **Optical Connectivity & Reliability for AI Infrastructure** learning-plan series. Its source is intended for PR-friendly editing. Change slides, knowledge checks, glossary links, and media references in `course.json`; change narration in `audio/moduleN/slide_*.txt`.

## Modules

| Module | Title | Estimated Learner Time | Summary |
|---|---|---:|---|
| 1 | The AI Fabric Visibility Problem | 10 min | Frame link reliability at fabric scale, identify the software and transceiver responsibilities, and distinguish local, remote, and breakout endpoints within the telemetry model. |
| 2 | Metrics, Flags, and Link Health | 14 min | Classify quality, error, recovery, environmental, and context metrics. Interpret link-health scores, flags, masks, thresholds, and autonomous-shutdown behavior. |
| 3 | CDB Workflows, Event Logs, and Remote Access | 14 min | Trace checked Command Data Block exchanges and persistent event logs. Distinguish remote byte and page access and connect the resulting evidence to a failure investigation. |
| 4 | Firmware, Host Software, and Deployment Readiness | 12 min | Review firmware maintenance, module-time correlation, host measurements, and command-line API categories. Connect telemetry collection and server aggregation to deployment-readiness checks. |

Designed for about **50 minutes of learner time**, including narration, diagrams, knowledge checks and review. Estimated learner time is distinct from narration runtime.

## Media

Course-owned PNG, SVG, and MP4 teaching assets are stored in `figures/`. Editable HTML/SVG and frame-rendering sources for the custom animations are stored in `animations/` where available. Delivery narration is 96 kbps CBR mono MP3 at 44.1 kHz, approved for this rebuild. WAV authoring masters are retained outside Git and outside the LMS package. No narration or rendered SCORM files are checked in. Per-slide `audio.generation_provenance` records reused recordings without inventing unknown legacy model IDs.

The 800 × 400 LMS catalog poster is `thumbnail.png`. Its editable copy and artwork selection are in `poster.json`; the shared Academy template supplies the layout. See the repository poster build instructions.

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh enhanced-telemetry-optics
```

The finished SCORM folder and LMS zip are created under `build/`.

For local QA with previously generated narration, set `EXISTING_AUDIO_DIR` to the existing course `audio/` folder:

```bash
EXISTING_AUDIO_DIR=/path/to/audio \
  ./scripts/build-course.sh enhanced-telemetry-optics
```

## Public References

The course teaches the OCP Networking Project's Optics Reliability Workstream Enhanced Telemetry Optics Product Software Specification v1.0.0. The specification is authored by Chris Collins at Credo and acknowledges community feedback from Cisco, Credo, Marvell, and Oracle.

- Enhanced Telemetry Optics Product Software Specification v1.0.0: https://www.opencompute.org/wp-content/uploads/2026/10/2026_OCP_Enhanced_Telemetry_Optics_Software_Specification_R1.0.0.pdf

## Catalog poster

Edit `poster.json` for wording and artwork. The shared Academy template fixes typography, gradients, logo and pill positions, and the white emblem dimensions. Rebuild from the repository root:

```sh
node skills/academy-wizard/scripts/render_lms_posters.mjs --repo-root . --course courses/enhanced-telemetry-optics
```

See [the poster standard](../../skills/academy-wizard/references/lms_poster_style.md) for dependency setup, title-fitting rules and full-catalog checks.

## LMS Catalog Metadata

Formal learner-facing LMS copy is maintained separately in [lms-catalog.md](lms-catalog.md) and [lms-catalog.json](lms-catalog.json). The course is available in English and seven self-contained language editions under `locales/`.
