# OCP Diablo 400: Disaggregated Power for High-Density AI Racks

Disaggregated plus-minus 400 volt rack power, sidecar architecture, safety interfaces, and future LVDC context.

This course source is intended for PR-friendly editing. Change slides, quiz content, glossary links, and inline SVG figures in `course.json`. Change narration in `audio/moduleN/slide_*.txt`. Generated audio and SCORM runtime files are not checked in.

## Modules

| Module | Title | Summary |
|---|---|---|
| 1 | Why Diablo 400 Exists | AI rack density, higher-voltage distribution, the sidecar model, and the OCP Rack & Power context. |
| 2 | Diablo 400 Architecture and Power Path | Rack envelope, AC input, DC output, ride-through, storage options, dynamic loading, and efficiency. |
| 3 | Interfaces, Safety, Telemetry, and Adoption | PDUs, shelves, cables, grounding choices, Redfish telemetry, safety, EMC, and implementation boundaries. |
| 4 | Optional: Future Work - Facility LVDC Power Distribution | Facility LVDC architectures, voltage bands, grounding topologies, protection, ESS, SST, standards, and future OCP work. |

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh diablo-400-disaggregated-power-for-high-density-ai-racks
```

The finished SCORM folder and LMS zip are created under `build/`.

For local QA with previously generated audio, set `EXISTING_AUDIO_DIR` to a folder shaped like `audio/`:

```bash
EXISTING_AUDIO_DIR=/path/to/audio ./scripts/build-course.sh diablo-400-disaggregated-power-for-high-density-ai-racks
```

## Public References

The original research files, downloaded PDFs, generated audio, and captured paid article assets are not included in this repository. Public learner/source references used by the course include:

- OCP specification: Diablo 400 v0.7.0 FINAL - https://www.opencompute.org/documents/ocp-specification-diablo-400-v0-7-0-final-pdf
- OCP white paper: DCF Power Distribution LVDC White Paper Version 1.0 - https://www.opencompute.org/documents/dcf-power-distribution-lvdc-white-paper-version-1-0-final-pdf-1
- OCP Rack & Power Project - https://www.opencompute.org/community/rack-and-power
- OCP Diablo 400 Project, HVDC Industry Standardization Effort - https://www.youtube.com/watch?v=OvrZR2Sp2aw
- Meta, Google, and Microsoft implementation comparison, starting at 12:17 - https://youtu.be/OvrZR2Sp2aw?si=NIwuLbVCDniyOjNZ&t=737
- Microsoft: Mt Diablo - Disaggregated Power Fueling the Next Wave of AI Platforms - https://techcommunity.microsoft.com/blog/azureinfrastructureblog/mt-diablo---disaggregated-power-fueling-the-next-wave-of-ai-platforms/4268799
- Google Cloud: Enabling 1 MW IT racks and liquid cooling at OCP EMEA Summit - https://cloud.google.com/blog/topics/systems/enabling-1-mw-it-racks-and-liquid-cooling-at-ocp-emea-summit
- Meta: Meta's open AI hardware vision - https://engineering.fb.com/2024/10/15/data-infrastructure/metas-open-ai-hardware-vision/
- OCP: Realizing the Open Data Center Ecosystem Vision - https://www.opencompute.org/blog/realizing-the-open-data-center-ecosystem-vision
- SemiAnalysis: Inside the 800VDC Revolution - Part 1 - https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part
