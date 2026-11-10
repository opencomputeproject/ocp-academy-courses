# DC Basics translations — validation and review

All seven independent SCORM 1.2 editions are built and packaged. The original translation build preserved the canonical English course's 793 preexisting workspace files and its delivered ZIP. The repository addition preserves the canonical English `course.json` and its existing media.

| Check | Result |
|---|---|
| Structure | 4 teaching modules, 78 slides, Course Home first + 4 module SCOs in every edition |
| Approved content | Module/slide IDs and types, source references and URLs, all 13 question IDs and answer keys preserved |
| Narration | 476 native full Eleven v4 clips, designated locale voices, approved pitch-preserving 1.18 processing; 476 waveform checks without flags |
| Delivery audio | 68 MP3 clips per edition, 96 kbps CBR / 44.1 kHz / mono; WAV and provider masters retained outside ZIPs |
| Imported recordings | All 10 original MP4s identical to English source in each edition; original English audio, translated native captions/transcripts and English captions; no added slide narration |
| Generated videos | 8 per edition / 56 total; localized visible text and posters, measured narration beats, single pass, silent, synchronized seek/speed and final hold |
| Media layout | 217 localized figure/animation source layouts checked at narration beats; no clipping, label collisions or insufficient box padding flagged |
| Course layout | 1,092 slide/viewport cases at 1440×900 and 390×844; caption alignment and ≥16 px media gaps, ≥24 px learner-aid gaps, wrapping, scrolling and fixed-control clearance passed |
| Course Home | 14 desktop/phone cases, informational tiles, first-module launch and tracked Home completion passed |
| Module navigation | 63 local/review/simulated-LMS boundary cases; visible green next-module links reach slide 1 of the next module |
| Interactions | All 91 translated question submissions accepted canonical correct IDs, including both matching questions; native captions, separate player roles and long glossary definitions checked |
| Video fidelity | 280 full-resolution source/decoded states; minimum RGB global SSIM 0.998033 and codec-space PSNR 54.5731 dB |
| SCORM | All seven manifests pass combined IMS CP / ADL SCORM 1.2 XSD validation; Home + four module item identifiers preserved |
| Packaging | Every ZIP member declared in the manifest; CRC and every member's bytes checked against its runtime; 68 MP3s and no WAV masters, authoring scripts or LMS catalog copy in the ZIP |
| LMS information | Native formal title, ≤130-character Short Description and structured Long Description, retaining the approved 95-minute estimate and module durations; JSON/Markdown/HTML sidecars outside the ZIP |
| Posters | No foreign-language LMS catalog posters; canonical English LMS poster remains shared |
| Author credit | Original Matty Bakkeren portrait bytes and M1S2 circular author acknowledgement preserved |

Translation was machine-assisted, with technical terminology and numerical checks plus editorial corrections. Corrections included AC/DC and rectifier distinctions, RAM volatility, cooling terms, RU versus OU, software containers, electrical-source video states and conservation of heat/energy. Glossary pills follow actual first eligible use in each language; terminology aliases record real native spelling/plural variants. Source structure and answer keys stay canonical.

Video fidelity compares native 1920×1080 frames. RGB SSIM is retained separately from the PSNR comparison, which normalizes the source and decoded frames to the same 8-bit YUV420 codec space. Raw RGB PSNR includes conversion/chroma effects and is also recorded in `qa/metrics.json`. Source text, decoded labels, representative course pages and 200% video detail were visually reviewed. The last media wording refinements did not change any rendered course-page HTML; byte parity is recorded.

Native-speaker editorial approval and perceptual listening review remain pending for the final language review. No audio was played aloud. The LMS checks use a local SCORM API simulation; this workflow does not claim a live Docebo upload or acceptance test.

Retained automated records are in [authoring/translation-qa/](authoring/translation-qa/). Editable locale definitions, narration scripts, localized media and catalog exports are in `locales/<locale>/`. Every locale retains its reviewed toolchain under `authoring/toolchain/academy-wizard/`. Source publication excludes generated narration, WAV/provider masters, rendered runtime pages and ZIPs. The project-specific Docebo publishing skill and tenant/session upload records are outside this contribution.

## Repository rebuild

[authoring/build_translation.py](authoring/build_translation.py) rebuilds each locale from the repository source and the unchanged MP3s extracted from its previously delivered ZIP. The command verifies all 68 narration-file hashes, stages fonts and XML schemas, runs source/arrow/catalog checks, renders with the pinned locale toolchain and validates the package. It performs no paid generation or audio/video recompression. Supply an empty output directory and add `--zip` only when packaging is wanted. See each locale README for the exact command.

The recorded delivery audio hashes bind this release to its course source. Editing the narration or course requires deliberate media review and a new release inventory; do not bypass a failed hash check.

## Repository assembly verification

All seven locales were rebuilt from this repository source with their unchanged delivered MP3s. The course-pinned source QA, glossary/media/arrow checks, LMS export checks and strict package validation passed. Every rebuilt edition contains Course Home plus four module SCOs and matches all **174 runtime files** in its previously delivered ZIP byte for byte (**1,218 comparisons** total). The source definitions, source media, canonical answer keys and matching-pair IDs remain unchanged.

See [repository-source.json](authoring/translation-qa/repository-source.json) and [repository-rebuilds.json](authoring/translation-qa/repository-rebuilds.json). The root README translation matrix was refreshed and checked. No generated narration, LMS ZIPs, rendered course pages, global skill changes, Docebo publishing skill or tenant/session upload records are included.

### Shared-checker compatibility

The source also received a comparison audit with the current repository-wide checker. It reports **36 glossary findings** across the seven locales because its treatment of explicit orientation exclusions and native-term/acronym matching differs from the validated locale snapshot. The delivered editions retain their documented `glossary_exclude_reason` metadata and recorded aliases. This source-publication change preserves their validated toolchain and learner content; it does not claim that the newer, unpinned checker is clean. The exact findings and implementation differences are retained in [shared-checker-comparison.json](authoring/translation-qa/shared-checker-comparison.json) for a later glossary/toolchain migration review.
