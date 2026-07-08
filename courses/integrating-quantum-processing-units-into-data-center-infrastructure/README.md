# Integrating Quantum Processing Units into Data Center Infrastructure

An OCP Academy course on deploying QPUs as hybrid data center infrastructure.

This course source is intended for PR-friendly editing. Change slides, knowledge checks, glossary links, and figure assets in `course.json`. Change narration in `audio/moduleN/slide_*.txt`. Generated audio and SCORM runtime files are not checked in.

## Modules

| Module | Title | Summary |
|---|---|---|
| 1 | Why Quantum Belongs in the Data Center | Market context, OCP workstream goals, and the hybrid infrastructure framing. |
| 2 | The Logical QPU and Its Classical Stack | Reference architecture, classical dependencies, storage growth, and deployment coupling. |
| 3 | Facility Readiness by Modality | Site selection, service boundaries, environmental controls, and modality-specific requirements. |
| 4 | From Pilot Deployment to OCP Practice | Operational maturity, shared infrastructure, existing OCP domains, and learner next steps. |

Each module includes a two-question knowledge check before the final wrap-up slide: one single-choice question followed by one multi-select question.

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh integrating-quantum-processing-units-into-data-center-infrastructure
```

The finished SCORM folder and LMS zip are created under `build/`.

For local QA with previously generated audio, set `EXISTING_AUDIO_DIR` to a folder shaped like `audio/`:

```bash
EXISTING_AUDIO_DIR=/path/to/audio ./scripts/build-course.sh integrating-quantum-processing-units-into-data-center-infrastructure
```

## Public References

The original research files are not included in this repository. Public learner/source references used by the course include:

- OCP whitepaper: Integrating Quantum Processing Units into Data Center Infrastructure: https://www.opencompute.org/documents/integrating-qpus-into-dc-infrastructure-pdf
- OCP FTI workstream: Data Center Integration of Quantum Information Infrastructure: https://www.opencompute.org/community/data-center-integration-of-quantum-information-infrastructure
- 2026 OCP EMEA Summit FTS Quantum Track: https://www.opencompute.org/events/past-events/2026-ocp-emea-summit#fts-quantum
- YouTube playlist: 2026 OCP EMEA Summit FTS Quantum Track: https://www.youtube.com/playlist?list=PLAG-eekRQBSgWit1dUFGB4vbjs7FstsXy
