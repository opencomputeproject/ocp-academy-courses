# Enhanced Telemetry Optics

Enhanced telemetry for finding what failed, where, and why in AI optical fabrics.

This standalone SCORM course belongs to the **Optical Connectivity & Reliability for AI Infrastructure** learning-plan series. Its source is intended for PR-friendly editing. Change slides, knowledge checks, glossary links, and media references in `course.json`; change narration in `audio/moduleN/slide_*.txt`.

## Modules

| Module | Title | Narrated Duration | Summary |
|---|---|---:|---|
| 1 | The AI Fabric Visibility Problem | 10 min | Enhanced telemetry as an operations model for local and remote optical endpoints. |
| 2 | Metrics, Flags, and Link Health | 12 min | Capability discovery, host/media health scores, flags, default counter masks, thresholds, and autonomous shutdown. |
| 3 | CDB Workflows, Event Logs, and Remote Access | 11 min | Checked command-reply workflows, durable 32-byte event records, and remote register read/write access. |
| 4 | Firmware, Host Software, and Deployment Readiness | 11 min | Local and remote firmware maintenance, module-time correlation, host measurements, and verified deployment behavior. |

The course contains 44.1 minutes of narration and is designed for about 50 minutes of learner time including knowledge checks and interaction. Module durations above are rounded from the generated audio.

## Media

Course-owned PNG, SVG, and MP4 teaching assets are stored in `figures/`. Editable HTML/SVG and frame-rendering sources for the custom animations are stored in `animations/` where available. Generated narration WAV files and rendered SCORM files are not checked in.

The 800 x 400 LMS catalog poster is `thumbnail.png`. Its editable source and renderer are in `poster/`; it uses the shared Academy logo and Lato font assets. Re-render it from the repository root with `node courses/optics/enhanced-telemetry-optics/poster/render_thumbnail.cjs` (requires Playwright and Chrome).

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh optics/enhanced-telemetry-optics
```

The finished SCORM folder and LMS zip are created under `build/optics/`.

For local QA with previously generated narration, set `EXISTING_AUDIO_DIR` to the existing course `audio/` folder:

```bash
EXISTING_AUDIO_DIR=/path/to/audio \
  ./scripts/build-course.sh optics/enhanced-telemetry-optics
```

## Public References

The course teaches the OCP Networking Project's Optics Reliability Workstream Enhanced Telemetry Optics Product Software Specification v1.0.0. The specification is authored by Chris Collins at Credo and acknowledges community feedback from Cisco, Credo, Marvell, and Oracle.

- Enhanced Telemetry Optics Product Software Specification v1.0.0: https://www.opencompute.org/wp-content/uploads/2026/10/2026_OCP_Enhanced_Telemetry_Optics_Software_Specification_R1.0.0.pdf
