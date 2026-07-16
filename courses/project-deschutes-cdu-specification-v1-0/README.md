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

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh project-deschutes-cdu-specification-v1-0
```

The finished SCORM folder and LMS zip are created under `build/`.

## Public References

The original research files are not included in this repository. Public learner/source references used by the course include:

- OCP contribution: Project Deschutes: Data Center Facilities V1.0.0
- 2025 OCP EMEA Summit recording: Project Deschutes: Google's Open Spec CDU contribution to the industry
- Google Cloud blog: AI infrastructure is hot. New power distribution and liquid cooling infrastructure can help
