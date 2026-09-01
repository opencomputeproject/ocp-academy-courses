# Two-Phase Direct Liquid Cooling Efficiencies and Fluids

Efficient phase-change cooling, dielectric fluids, and operational practices for high-density infrastructure.

This course source is intended for PR-friendly editing. Change slides, quiz content, glossary links, and figure SVGs in `course.json`. Change narration in `audio/moduleN/slide_*.txt`. Generated audio and SCORM runtime files are not checked in.

## Modules

| Module | Title | Summary |
|---|---|---|
| 1 | Why Two-Phase DLC Now | Cooling constraints, efficiency levers, and where two-phase fits. |
| 2 | Two-Phase DLC Architecture and Efficiency Mechanics | Phase-change mechanics, loop boundaries, pressure control, and scale requirements. |
| 3 | Dielectric Fluids, Selection, and Compatibility | Fluid properties, wetted materials, safety, and environmental roadmaps. |
| 4 | Deployment, Operations, Monitoring, and Lifecycle | Startup, purge, monitoring, maintenance, deployment patterns, and records. |

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh two-phase-direct-liquid-cooling-efficiencies-and-fluids
```

The finished SCORM folder and LMS zip are created under `build/`.

## Public references

The original research files are not included in this repository. Public learner/source references used by the course include:

- [OCP Dielectric Coolant Fluid Base Specification V1.0](https://www.opencompute.org/documents/dielectric-coolant-fluid-base-specification-v1-0-final-pdf)
- [OCP Guidelines for Using Dielectric Heat Transfer Fluids in Two-Phase Cold Plate-Based Liquid-Cooled Racks](https://www.opencompute.org/documents/guidelines-for-using-dielectric-heat-transfer-fluids-in-two-phase-cold-plate-based-liquid-cooled-racks-final-pdf)
- [2026 OCP EMEA Summit panel recording: Revolutionizing AI Heat Management - The Superior Efficiency of Two-Phase Liquid Cooling](https://www.youtube.com/watch?v=0vxGneJ3yGo)
- [OCP Educational Webinar Program past webinars index](https://www.opencompute.org/summit/ocp-educational-webinar-program/past-webinars)
