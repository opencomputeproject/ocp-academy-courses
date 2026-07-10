# Introduction to Emerging Optical Technologies

An introductory-to-intermediate OCP Academy course on how new optical approaches address scale, efficiency, density, latency, and compute integration in AI infrastructure.

This standalone SCORM course belongs to the **Optical Connectivity & Reliability for AI Infrastructure** learning-plan series. Its source is intended for PR-friendly editing. Change slides, knowledge checks, glossary links, and media references in `course.json`; change narration in `audio/moduleN/slide_*.txt`.

## Modules

| Module | Title | Narrated Duration | Summary |
|---|---|---:|---|
| 1 | Why AI Infrastructure Is Changing Optics | 12 min | Accelerator fabrics, rising fiber counts, and the different pressures created by scale-up, scale-out, and scale-across. |
| 2 | Power, Thermal, and Serviceability Shifts | 14 min | Co-packaged optics, expanded beam optics, rear blind mating, and the operational constraints they address. |
| 3 | Density and Testability in the Optical Plant | 11 min | Multicore fiber, fan-in and fan-out connectivity, compact harnesses, and emerging testing considerations. |
| 4 | Latency, Quantum, and the Adoption Horizon | 14 min | Hollow-core fiber, latency-sensitive infrastructure, hybrid quantum-classical systems, and technology maturity. |

The course contains approximately 52 minutes of narration and is designed for about 60 minutes of learner time including knowledge checks and interaction.

## Media

Course-owned PNG, SVG, and MP4 teaching assets are stored in `figures/`. Editable HTML/SVG and frame-rendering sources for the custom animations are stored in `animations/` where available. Generated narration WAV files and rendered SCORM files are not checked in.

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh optics/introduction-to-emerging-optical-technologies
```

The finished SCORM folder and LMS zip are created under `build/optics/`.

For local QA with previously generated narration, set `EXISTING_AUDIO_DIR` to the existing course `audio/` folder:

```bash
EXISTING_AUDIO_DIR=/path/to/audio \
  ./scripts/build-course.sh optics/introduction-to-emerging-optical-technologies
```

## Public References

The original source deck is not included in this repository. Public references used by the course include:

- Open Rack Base Specification Version 3: https://www.opencompute.org/documents/open-rack-base-specification-version-3-pdf
- OIF 3.2T Co-Packaged Module Implementation Agreement: https://www.oiforum.com/oif-launches-the-industrys-first-co-packaging-standard-the-3-2t-co-packaged-module-implementation-agreement/
- SDM4 MCF MSA announcement: https://sumitomoelectric.com/press/2026/02/prs011
- Microsoft hollow-core fiber announcement: https://blogs.microsoft.com/blog/2022/12/09/microsoft-acquires-lumenisity-an-innovator-in-hollow-core-fiber-hcf-cable/
- Hollow-core fiber research in Nature Photonics: https://www.nature.com/articles/s41566-025-01747-5
- OCP Academy course, Integrating Quantum Processing Units into Data Center Infrastructure: https://academy.opencompute.org/learn/courses/51/integrating-quantum-processing-units-into-data-center-infrastructure
