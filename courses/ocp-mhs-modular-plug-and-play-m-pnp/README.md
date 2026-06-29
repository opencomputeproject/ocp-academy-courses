# OCP MHS Modular Plug-and-Play (M-PNP)

Deep-technical course on the M-PNP specifications bundle, covering the MHS interoperability problem, FRU discovery and boot, the HPM FPGA API, conformance, tooling, and adoption.

This course source is intended for PR-friendly editing. Change slides, quiz content, glossary links, and figures in `course.json`. Change narration in `audio/moduleN/slide_*.txt`. Generated audio and SCORM runtime files are not checked in.

## Modules

| Module | Title | Summary |
|---|---|---|
| 1 | Introduction to MHS & the M-PNP Vision | The interoperability problem, the three-rung ladder, and the v0.5 specifications bundle. |
| 2 | FRU, Discovery & Boot Specification | How a BMC learns the platform from a cold start. |
| 3 | M-PNP HPM FPGA Specification | A standardized API for the HPM FPGA. |
| 4 | Interop, Conformance, Tooling & Adoption | The Interop spec, the schemas, the tools, the roadmap, and how to contribute. |

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh ocp-mhs-modular-plug-and-play-m-pnp
```

The finished SCORM folder and LMS zip are created under `build/`.

For local QA with previously generated audio, set `EXISTING_AUDIO_DIR` to a folder shaped like `audio/`:

```bash
EXISTING_AUDIO_DIR=/path/to/audio ./scripts/build-course.sh ocp-mhs-modular-plug-and-play-m-pnp
```

## Public References

The original downloaded source PDFs, slide decks, transcripts, generated audio, and SCORM runtime files are not included in this repository. Public learner/source references used by the course include:

- OCP DC-MHS specifications and designs - https://www.opencompute.org/wiki/Server/MHS/DC-MHS-Specs-and-Designs
- OCP Modular Hardware System project - https://www.opencompute.org/wiki/Server/MHS
- OCP Tech Talk: M-PNP Overview and M-PNP.FRU Discovery Boot 0.5 Specification Deep Dive - https://www.youtube.com/watch?v=QapIKDsCq3E
- OCP Tech Talk: M-PNP Overview and M-PNP.FPGA 0.5 Specification Deep Dive - https://www.youtube.com/watch?v=sWQxhUJzc3k
- MHS Modular Plug-and-Play (M-PNP) Workstream Update and Guidelines For Adoption - https://www.youtube.com/watch?v=idSTvsWdLPo
- OCP M-PNP FRU Tool - https://github.com/opencomputeproject/OCP-SVR-MHS-M-PNP_FRUTool
- DMTF FRU DSP0220 - https://www.dmtf.org/dsp/DSP0220
- DMTF MMBI DSP0282 - https://www.dmtf.org/dsp/DSP0282
- DMTF SPDM standards - https://www.dmtf.org/standards/SPDM
