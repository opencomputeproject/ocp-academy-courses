# OCP MHS Modular Plug-and-Play (M-PNP)

Deep-technical course on the authoritative M-PNP v0.7.0 release package: MHS interoperability, FRU discovery and boot, HPM and peripheral programmable devices, conformance, tooling, and adoption. The FRU/Discovery/Boot and HPM/Peripheral PD specifications are v0.7.0 RC1; Interop is v0.3.0. Document, schema and example versions are separate identifiers.

This is a source preview, not a final production release. The four proposed teaching videos (M1S7, M2S6, M3S8 and M4S6) await review and production. Earlier figures and animation sources are preserved under `archive/pre-v0.7/` and are not copied into the active build. Missing-video QA flags are not waived. Target-LMS navigation, resume and completion still require acceptance testing.

This course source is intended for PR-friendly editing. Change slides, quiz content, glossary links, and figures in `course.json`. Change narration in `audio/moduleN/slide_*.txt`. Generated audio and SCORM runtime files are not checked in.

`authoring/source-links.json` records the release-package authority and document identities. OCP Contribution Database URLs can replace its null `canonical_url` fields when supplied; update the corresponding `course.json` links while preserving verified PDF viewer page anchors. `authoring/slide-review-plan.json` retains slide-by-slide review checks and the four video storyboards. Learner text and narration do not describe course revisions or production work.

## Modules

| Module | Title | Summary | Measured narration |
|---|---|---|---|
| 1 | Introduction to MHS & the M-PNP Vision | Interoperability definitions and the v0.7 package. | ~6.9 min |
| 2 | FRU, Discovery & Boot Specification | Qualifiers, authenticity, discovery dependencies, peripheral descriptions and BMC–BIOS exchange. | ~10.3 min |
| 3 | HPM & Peripheral Programmable Devices | Primary/peripheral roles, interfaces, the IP-block catalog, memory-map exceptions and ten power states. | ~10.3 min |
| 4 | Interop, Conformance, Tooling & Adoption | Schemas, eleven worked examples, tested compatibility, reproducible adoption and contribution. | ~6.7 min |

There are 46 slides and four narrated, two-question knowledge checks. Narration totals approximately 34.2 minutes; the 45-minute target includes interaction and reading time.

All nine course-owned hardware examples declare `hardware-component.v0_7_3`. Eight peripheral copies change only `SchemaVersion`; `authoring/source-inventory.json` records their original declarations and before/after hashes. The two programmable-device examples remain on `programmable-device.v0_7_2`. Updating a declaration does not establish schema or system validation. The sole teaching-level older-release mention is M4S5's accurate warning that a JSON tool documents v0.5/Draft 4 provenance; v0.7 compatibility must be tested. The bundled PDFs retain their genuine revision history.

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh ocp-mhs-modular-plug-and-play-m-pnp
```

The course folder and strict SCORM 1.2 preview ZIP are created under `build/`. Preserve the separate Course Home and four module syllabus entries; no SCORM-version or reporting-architecture migration is authorized. The first-module direct home action does not switch the LMS tracking context—use the LMS Syllabus for separately tracked module launches.

For local QA with previously generated audio, set `EXISTING_AUDIO_DIR` to a folder shaped like `audio/`:

```bash
EXISTING_AUDIO_DIR=/path/to/audio ./scripts/build-course.sh ocp-mhs-modular-plug-and-play-m-pnp
```

The source scripts match the reviewed local preview. A new cloud generation is not guaranteed to reproduce the same waveform and requires signal and listening review. The approved narration setup is ElevenLabs Leo v2 (`bbGtsRRKUfYO634UxSjz`), `eleven_multilingual_v2`, speed `1.18`, stability `0.55` and similarity `0.75`. M1S5 spells M-PNP as `Em P N P`; M1S6 speaks README as `reed me`. Exact visible filenames are unchanged.

M2S4 records four ordered `audio.synthesis_chunks`. The maintained generator checks that they preserve the complete narration before sending billable text, uses the same voice/settings for every part, and joins their native PCM without normalization, fades or trimming. The local repair reduced its speech-active opening/ending decline from approximately 5.0 dB to 0.6 dB; all 45 other WAVs remained identical. Measurements are retained in `authoring/narration-qa.json`, not as a claim that an arbitrary future generation is approved.

After every regeneration, run the strengthened course-wide signal report and listen across the beginning, middle and ending. Its speech-active check catches relative declines even when pauses or the former absolute-volume threshold hid them; it also surfaces borderline cases for review. Signal checks do not establish pronunciation, vocal projection or perceptual consistency.

```bash
python skills/academy-wizard/scripts/slides_course_qa.py \
  courses/ocp-mhs-modular-plug-and-play-m-pnp/course.json \
  --repo-root . --fail-on-flags
```

The current source passes PDF-link and glossary-placement checks but reports four missing-video flags. Complete and review those media, then test the target LMS before treating this preview as release-ready.

## Public References

Only the documents actually linked for learner use, the two schemas, and eleven course-owned examples are included under `resources/`; their public release-package source is recorded below. The original ZIP, Visio research files, slide decks, transcripts, generated audio and SCORM runtime files are not committed. The release README and IP Block workbook are accessed through the public package rather than republished here. `scripts/build_resources.py` creates the offline examples page in the staged build.

- [Authoritative M-PNP v0.7.0 release package](https://drive.google.com/file/d/16RsGG-KafjIRimlVTvfC0cH7lToFsSR6/view?usp=drive_link)
- [OCP DC-MHS specifications and designs](https://www.opencompute.org/wiki/Server/MHS/DC-MHS-Specs-and-Designs)
- OCP Modular Hardware System project - https://www.opencompute.org/wiki/Server/MHS
- OCP M-PNP FRU Tool - https://github.com/opencomputeproject/OCP-SVR-MHS-M-PNP_FRUTool
- DMTF FRU DSP0220 - https://www.dmtf.org/dsp/DSP0220
- DMTF MMBI DSP0282 - https://www.dmtf.org/dsp/DSP0282
- DMTF SPDM standards - https://www.dmtf.org/standards/SPDM
