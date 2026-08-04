# High Bandwidth Flash: Bridging SSD Capacity and HBM Performance

A three-module OCP Academy course on the OCP HBF Architecture Specification v0.7.0. The course explains why AI serving needs a memory layer between HBM and SSDs, how HBF connects high-capacity Nand flash to an xPU, and how software should handle its read-optimized behavior.

This course source is intended for PR-friendly editing. Change slides, knowledge checks, glossary links, and figure assignments in `course.json`. Change narration in `audio/moduleN/slide_*.txt`. Generated narration and SCORM runtime files are not checked in.

## Modules

| Module | Title | Narrated time | Summary |
|---|---|---:|---|
| 1 | Why AI Needs a New Memory Layer | 9.6 min | The AI memory wall, HBF's position between HBM and SSDs, the open OCP architecture, and the v0.7.0 performance envelope. |
| 2 | How HBF Connects Capacity to the xPU | 9.8 min | The base die and 16-die Nand stack, independent UCIe channels, AXI flash geometry, and address interleaving for parallel bandwidth. |
| 3 | Programming HBF for AI Serving | 12.0 min | Independent linear spaces, parallel reads, structured writes, reliability responsibilities, model-serving patterns, and deliberate placement of weights and KV cache. |

The total narrated runtime is 31.4 minutes. Allow additional time for the knowledge check in each module and learner interaction.

## Media

Course-owned vector figures, three silent teaching animations, animation posters, the HBF course mark, and the 800 by 400 LMS thumbnail are included. Each module contains one teaching animation.

Editable HTML sources and the Playwright recorder for the animations are under `animations/`. The rendered H.264 MP4 files and their poster frames are under `figures/`.

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh high-bandwidth-flash
```

The finished SCORM folder and LMS zip are created under `build/`.

For local QA with previously generated audio, set `EXISTING_AUDIO_DIR` to a folder shaped like `audio/`:

```bash
EXISTING_AUDIO_DIR=/path/to/audio ./scripts/build-course.sh high-bandwidth-flash
```

## Public references

- OCP HBF Architecture Specification v0.7.0 - https://www.opencompute.org/documents/ocp-hbf-architecture-specification-v0-7-0-final-pdf
- OCP Storage Project - https://www.opencompute.org/community/storage
- SK hynix, "HBF at FMS 2026" - https://news.skhynix.com/en/hbf-at-fms-2026/
- Sandisk, "Scaling Beyond the Wall: Inside Sandisk's High Bandwidth Flash for AI" - https://www.sandisk.com/company/newsroom/blogs/2025/scaling-beyond-the-wall-inside-sandisks-high-bandwidth-flash-for-ai
- Sandisk HBF Fact Sheet - https://documents.sandisk.com/content/dam/asset-library/en_us/assets/public/sandisk/collateral/company/Sandisk-HBF-Fact-Sheet.pdf

The Sandisk fact sheet is used only as background context and is not quoted directly in the course.
