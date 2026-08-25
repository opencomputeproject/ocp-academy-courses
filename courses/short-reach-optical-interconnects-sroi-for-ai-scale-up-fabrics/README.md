# Short-Reach Optical Interconnects for AI Scale-Up Fabrics

A four-module OCP Academy course based on the OCP Short Reach Optical Interfaces 1.0.0 contribution paper. The course connects scale-up workload behavior and copper reach limits to reliability targets, optical placement choices, signaling options, and an ecosystem roadmap for links of 30 meters or less.

This course source is intended for PR-friendly editing. Change slides, knowledge checks, glossary links, and figure assignments in `course.json`. Change narration in `audio/moduleN/slide_*.txt`. Generated narration and SCORM runtime files are not checked in.

## Modules

| Module | Title | Narrated time | Summary |
|---|---|---:|---|
| 1 | Why Scale-Up Needs a New Optical Reach Class | 9.1 min | Load/store semantics, synchronized accelerator behavior, switch radix, copper limits, multi-rack geometry, and the definition of SROI. |
| 2 | Finding the Copper-to-Optics Crossover | 9.2 min | Complete channel loss budgets, reach, retiming, optical placement, and the system thresholds that determine where copper gives way to optics. |
| 3 | Engineering for Reliability at Pod Scale | 10.5 min | Transient and hardware failures, FEC, CRC, retries, temperature, laser strategy, diagnostics, repair, redundancy, and qualification. |
| 4 | Choosing an Optical Architecture and Roadmap | 12.0 min | Pluggable, near-package, and co-packaged optics; optical circuit switching; PAM4 and slow-and-wide WDM; the 400G copper boundary; and ecosystem action. |

The total narrated runtime is 40.8 minutes. Allow approximately 50–55 minutes for knowledge checks, review, and learner interaction.

## Media

Course-owned vector figures, five silent teaching animations, animation posters, the SROI course mark, and the 800 by 400 LMS thumbnail are included.

Editable HTML sources and the Playwright renderer for the animations are under `animations/`. The rendered H.264 MP4 files and poster frames are under `figures/`.

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh short-reach-optical-interconnects-sroi-for-ai-scale-up-fabrics
```

The finished SCORM folder and LMS zip are created under `build/`.

For local QA with previously generated audio, set `EXISTING_AUDIO_DIR` to a folder shaped like `audio/`:

```bash
EXISTING_AUDIO_DIR=/path/to/audio \
  ./scripts/build-course.sh short-reach-optical-interconnects-sroi-for-ai-scale-up-fabrics
```

## Public links

- OCP Short Reach Optical Interfaces 1.0.0 contribution paper - https://www.opencompute.org/documents/sroi-white-paper-1-0-0-pdf
- OCP Short Reach Optical Interconnect Workstream - https://www.opencompute.org/community/short-reach-optical-interconnect
- OCP Optical Circuit Switching Subproject - https://www.opencompute.org/community/optical-circuit-switching
- OCP Academy course - https://academy.opencompute.org/learn/courses/66/short-reach-optical-interconnects-sroi-for-ai-scale-up-fabrics
- OCP Data Center Technologies catalog - https://academy.opencompute.org/pages/21/ocp-data-center-technologies
