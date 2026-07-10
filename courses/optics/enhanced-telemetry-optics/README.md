# Enhanced Telemetry Optics

Enhanced telemetry for finding what failed, where, and why in AI optical fabrics.

This standalone SCORM course belongs to the **Optical Connectivity & Reliability for AI Infrastructure** learning-plan series. Its source is intended for PR-friendly editing. Change slides, knowledge checks, glossary links, and media references in `course.json`; change narration in `audio/moduleN/slide_*.txt`.

## Modules

| Module | Title | Narrated Duration | Summary |
|---|---|---:|---|
| 1 | The AI Fabric Visibility Problem | 9 min | Enhanced telemetry as an operations model for local and remote optical endpoints. |
| 2 | Metrics, Flags, and Link Health | 10 min | Telemetry categories, summary flags, masks, and the worst-category link-health score. |
| 3 | CDB Workflows, Event Logs, and Remote Access | 10 min | The command-reply pattern that moves telemetry, event history, and far-end data. |
| 4 | Firmware, Host Software, and Deployment Readiness | 10 min | Lifecycle operations and host tooling that turn telemetry into fleet reliability. |

The course contains approximately 39 minutes of narration and is designed for about 50 minutes of learner time including knowledge checks and interaction.

## Media

Course-owned PNG, SVG, and MP4 teaching assets are stored in `figures/`. Editable HTML/SVG and frame-rendering sources for the custom animations are stored in `animations/` where available. Generated narration WAV files and rendered SCORM files are not checked in.

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

The course is based on the OCP Networking Project's Optics Reliability Workstream Enhanced Telemetry Spec, developed by OCP Community volunteers from Credo and Oracle.

- OCP Optics Telemetry public specification: https://www.opencompute.org/documents/2025-ocp-software-specification-optics-telemetry-rev0-9-pdf
