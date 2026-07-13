# OCP Ready™ Requirements for Energy Storage Systems

A practical guide to ESS deployment, safety, standards, and OCP Ready™ application in data centers.

This course source is intended for PR-friendly editing. Change slides, quiz content, glossary links, and figure assets in `course.json`. Change narration in `audio/moduleN/slide_*.txt`. Generated audio and SCORM runtime files are not checked in.

## Modules

| Module | Title | Summary |
|---|---|---|
| 1 | Why ESS Requirements Matter In AI Data Centers | The shift toward distributed ESS, the scope of the white paper, and the stakeholders who must align. |
| 2 | Deployment Models, Architectures, And Technologies | How ESS placement, coupling, control, and storage technology shape the compliance path. |
| 3 | Safety Hazards, Mitigation, And Operations | Electrical, thermal, gas, explosion, chemical, detection, ventilation, suppression, and response considerations. |
| 4 | Codes, Standards, And OCP Ready™ Application | How to navigate local codes, international standards, insurer guidance, and OCP Ready™ ESS parameters. |

## Media

Course-owned figures and the silent deployment-workflow animation are stored in `figures/`. The editable Python source for that animation is stored in `animations/`.

To regenerate the animation and its poster:

```bash
python -m pip install Pillow numpy imageio-ffmpeg
python courses/ocp-ready-requirements-for-energy-storage-systems/animations/build_requirement_to_evidence_workflow.py
```

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh ocp-ready-requirements-for-energy-storage-systems
```

The finished SCORM folder and LMS zip are created under `build/`.

## Public References

The original research files are not included in this repository. Public learner/source references used by the course include:

- OCP white paper: OCP Ready™ Requirements for Energy Storage Systems
- OCP Energy Storage Systems project
- 2026 OCP EMEA Summit presentation: ESS in Hyperscale & AI Data Centers: OCP Ready™ Requirements Update
