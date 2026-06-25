# Cooling Fluids in Direct Liquid Cooling (DLC)

Single-phase TCS fluid guidance for direct-to-chip deployments.

This course source is intended for PR-friendly editing. Change slides, quiz content, glossary links, and figure SVGs in `course.json`. Change narration in `audio/moduleN/slide_*.txt`. Generated audio and SCORM runtime files are not checked in.

## Modules

| Module | Title | Summary |
|---|---|---|
| 1 | Why Single-Phase Fluids Matter in DLC | Fluid boundaries, urgency, source discipline, and the two-phase contrast. |
| 2 | Choosing and Specifying Single-Phase Fluids | Water, PG25, chemistry windows, inhibitors, and compatibility evidence. |
| 3 | Commissioning, Filling, and Protecting the Loop | Serviceable design, compatible fill practices, filtration, startup records, and microbial control. |
| 4 | Monitoring, Maintenance, and Operational Judgment | Routine tests, lab QA, trend interpretation, adjustments, mixing, useful life, and documentation. |

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh cooling-fluids-in-direct-liquid-cooling
```

The finished SCORM folder and LMS zip are created under `build/`.

## Public References

The original research files are not included in this repository. Public learner/source references used by the course include:

- OCP contribution: Guidelines for Using Water-based Heat Transfer Fluid in Single-Phase Cold Plate-Based Liquid-Cooled Racks
- OCP contribution: Guidelines for Using Dielectric Heat Transfer Fluids in Two-Phase Cold Plate-Based Liquid-Cooled Racks
