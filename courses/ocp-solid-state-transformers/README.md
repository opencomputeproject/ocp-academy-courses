# OCP Solid State Transformers: From Medium Voltage to 800 VDC

A five-module OCP Academy course on the OCP SST v0.3 design envelope, grid behavior, coordinated energy storage, and LVDC data center integration.

This course source is intended for PR-friendly editing. Change slides, knowledge checks, glossary links, and figure assignments in `course.json`. Change narration in `audio/moduleN/slide_*.txt`. Generated narration and SCORM runtime files are not checked in.

## Modules

| Module | Title | Narrated time | Summary |
|---|---|---:|---|
| 1 | Why SSTs, Why Now | 13 min | AI rack density, current and copper constraints, the 800 VDC transition, and the complementary boundaries of the SST, Diablo 400, and ESS courses. |
| 2 | The Technology Inside the SST Black Box | 12 min | The conversion path from MVAC to regulated 800 VDC, including active power conversion, high-frequency isolation, wide-bandgap devices, magnetics, controls, and topology-neutral tradeoffs. |
| 3 | The OCP SST v0.3 Design Envelope | 12 min | Input classes, power ratings, output regulation, fault and overload behavior, efficiency, environment, communications, standards, and the boundary between requirements and open work. |
| 4 | Grid Interaction, Ride-Through, and State Behavior | 11 min | Grounding, voltage and frequency ride-through, coordinated SST–ESS response, recovery pacing, alarms, and the six-state operating model. |
| 5 | Integrating SSTs into LVDC Data Centers | 13 min | Redundancy, selective DC protection, SST and ESS timescales, storage placement, verification, pilot deployment, and the path toward v1.0. |

The total narrated runtime is 59.9 minutes. Allow additional time for the two-question knowledge check in each module, review, and learner interaction.

## Media

Course-owned vector figures, four silent teaching animations, animation posters, and the LMS thumbnail are included. Regenerate the four animations with:

```bash
python -m pip install Pillow imageio-ffmpeg
python courses/ocp-solid-state-transformers/animations/build_teaching_animations.py
```

Two credited SemiAnalysis figures are included as learner media for market context and the four-phase transition lens. The article HTML and other downloaded research material are not stored in this repository. The ESS deployment architecture is reused from the OCP Ready Requirements for Energy Storage Systems course.

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh ocp-solid-state-transformers
```

The finished SCORM folder and LMS zip are created under `build/`.

For local QA with previously generated audio, set `EXISTING_AUDIO_DIR` to a folder shaped like `audio/`:

```bash
EXISTING_AUDIO_DIR=/path/to/audio ./scripts/build-course.sh ocp-solid-state-transformers
```

## Public references

- OCP SST Design Specification v0.3 - https://www.opencompute.org/documents/ocp-sst-design-specification-v0-3-final-pdf
- OCP Power Distribution Sub-Project - https://www.opencompute.org/community/power-distribution
- DCF Power Distribution LVDC White Paper Version 1.0 - https://www.opencompute.org/documents/dcf-power-distribution-lvdc-white-paper-version-1-0-final-pdf-1
- SemiAnalysis, “Inside the 800VDC Revolution - Part 1” - https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part
- OCP Diablo 400 course - https://academy.opencompute.org/learn/courses/49/ocp-diablo-400/
- OCP Ready Requirements for Energy Storage Systems course - https://academy.opencompute.org/learn/courses/50/ocp-ready-requirements-for-energy-storage-systems
