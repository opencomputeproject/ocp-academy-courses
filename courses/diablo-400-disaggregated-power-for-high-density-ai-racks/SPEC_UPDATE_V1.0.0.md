# Mt. Diablo specification v1.0.0: English course refresh

## Release status

The English content and scripts were approved on November 17, 2026. The release merged in [PR #148](https://github.com/opencomputeproject/ocp-academy-courses/pull/148) on November 18. The same day, [PR #150](https://github.com/opencomputeproject/ocp-academy-courses/pull/150) merged the seven v1.0.0 translations, which were also published to the existing language editions on OCP Academy course 49. See the [course README](README.md#v100-refresh) for the current edition and narration settings.

The released course has 36 slides and four teaching videos per edition. Each module ends with separately narrated takeaways, a knowledge check, and a next-module or completion slide. Question IDs remain stable across all modules.

## Optional Module 4 source audit

Module 4 now follows the 239-page [OCP DCF Power Distribution LVDC white paper v1.1.0](https://www.opencompute.org/wp-content/uploads/2026/10/DCF-Power-Distribution-LVDC-white-paper-version-1.1.0.pdf), dated September 2, 2026. The 15-minute estimate is unchanged. The white paper describes architecture options and draft criteria; the Mt. Diablo base specification remains the authority for Modules 1–3.

| Slides | What changed | v1.1.0 evidence (PDF viewer pages) |
| --- | --- | --- |
| 1–3 | Refresh the version and objectives. Verify the three adoption stages, distinguish the facility stages from the two rack conversion placements, and label rack-input voltage criteria preliminary. Remove the older deployment-metric examples from the short overview. | pp. 1, 7–8, 25–31, 166–174 |
| 4 | Teach the difference between the nominal label, equipment rating, and operating limits. Qualify proposed voltage bands and explain why the selected polarity and earthing matter. | pp. 51–74, 80–98 |
| 5 | Explain the existing conceptual video using the updated paper's protection, conversion, and tiered storage treatment. Avoid a universal timing or grid-recovery target. | pp. 111–128, 144–150, 182–187 |
| 6 | Add operating sequences, control responsibilities, and EMC under representative loads. Retain DC arc-flash and applicable-code verification. | pp. 133–135, 188–200, 203–230 |
| 7–9 | Summarize what to verify, test equipment compatibility and system behavior, then link to the complete paper. | Chapters 5–7, 10–12 |

Baseline: the repository's English Diablo 400 course, based on v0.7.0 (March 1, 2026). Target: **Mt. Diablo Disaggregated Power Rack Specification v1.0.0**, effective October 8, 2026.

Source: https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Specification-Mt.-Diablo-Disaggregated-Power-Rack-Specification-v1.0.0.pdf

Page numbers below are one-based PDF viewer pages. The final specification has 37 pages; the earlier specification has 36. Both full texts were extracted and compared, and the changed grounding diagrams, PSU table, and interconnect tables were checked against their rendered pages.

## Original review scope and compatibility

The original English review used 32 slides and WAV audio. The release added four dedicated takeaways slides and switched delivery to MP3. The 35-minute core and 15-minute optional learner-time estimates are unchanged. The course retained its stable folder and slugs, SCORM 1.2, and Course Home plus four module syllabus entries. Localization was handled separately after the English review and is now complete.

## Original English change map

Slide numbers below refer to the original English review. The final optional module uses the v1.1.0 audit above.

| Course location | Change | v1.0.0 evidence |
| --- | --- | --- |
| Home, titles, catalog, scripts, poster | Use Mt. Diablo and the final version/effective date. Retain historical project-video titles. | Cover p. 1; revision history pp. 3–4 |
| Module 1, slides 3–6 | Refresh naming and supporting specification links; retain density, current/copper, sidecar and OCP tenet concepts. | §§4–5, pp. 10–11 |
| Module 2, slide 3 | Retain implementation-specific rack envelopes and 6000 lb target; distinguish 1 OU PSU modules from shelves up to 2 OU. Add three PSU solution families, input-dependent ratings, Solution 1 A/B dimensions, and handle exclusions. | §6/Table 1 p. 12; §8.2.1/Table 10 pp. 23–24 |
| Module 2, slide 4 | Preserve AC voltage, frequency and power-quality requirements. Tighten spoken THD load boundaries to match Table 3. | §7.1/Tables 2–3 p. 13 |
| Module 2, slide 5 | Preserve holdup and 45–90 second BBU support. Add the 820 V no-load/800 V full-load row, ±0.5% regulation, and the resolved ±1% peak-to-peak ripple/noise value. Distinguish differential voltage from earth reference. | §§7.1.3–7.3.1/Table 4, pp. 14–15 |
| Module 2, slide 6 | Explain TDP as defined for continuous 100% rated electrical output under specified conditions. Preserve dynamic tests and end-to-end efficiency; distinguish short peaks from continuous ratings. | §7.3.2/Table 5 p. 16; Tables 6–9 pp. 16–18 |
| Module 2, slide 7 | Replace the first question with a differential-voltage/earth-reference check. Preserve the dynamic-load multiple-select question. | §§7.3.1, 8.1.4 |
| Module 3, slide 3 | Replace 12×200 A cords with up to 16×200 Aac or 24×100 Aac. Clarify shelf versus PSU serviceability. Explain current DC and AC interconnect locations and preliminary connector part numbers. | §8.1.1 pp. 18–19; §8.2 pp. 23–24; §§9–10 pp. 25–28 |
| Module 3, slide 4 | Expand midpoint/return reference and 2-wire/3-wire options. Make ground-fault detection mandatory for both solid and high-resistance midpoint grounding, with HRG voltage-balance detection and residual-current detection per output connection. | §8.1.4, pp. 19–22; Appendix A pp. 34–35 (non-normative) |
| Module 3, slide 5 | Remap management/environment sources to §§11–12. Distinguish required internal communication from external interface choices; show required and preferred temperature ranges. | pp. 29–30 |
| Module 3, slide 6 | Remap safety, EMC and sustainability references to §13; retain the established requirement categories. | pp. 30–32 |
| Module 3, slide 7 | Test the changed cord counts, mandatory detection, and preliminary connector qualification, with updated feedback and narration. | §8.1.1, §8.1.4.2.3, §§9–10 |
| Module 4 | Update links back to Mt. Diablo and course naming. Retain the original LVDC white-paper scope and historical context. | Separate OCP DCF Power Distribution LVDC white paper v1.0; not new base-specification requirements |

## PSU Table 10 values carried into the course

Ratings are up-to average DC load, without redundancy. Voltage order: 480 / 415 / 400 Vac.

| Solution | Ratings | Dimensions L × H × W |
| --- | --- | --- |
| 1 | 30 / 26 / 25 kW | A: 848 × 40 × 170 mm; B: 875 × 42.2 × 163 mm, both without handle |
| 2 | 27 / 27 / 27 kW | 945 × 45 × 134 mm; length without handle 933 mm |
| 3 | 26 / 26 / 26 kW | 898.8 × 40 × 170 mm without handle |

## Source qualifications requiring implementation review

1. The revision-history references to sections 14.1 and 15.1 are stale after reorganization. The actual DC and AC interconnect sections are **9 and 10**. Management is now 11, environment 12, compliance 13, and references 14.
2. The final release still explicitly says connector part numbers are preliminary in §§9–10. The course teaches option selection and complete mating-set verification; it does not turn those numbers into procurement approvals.
3. Section 8.1.4 describes solid-return 800 V grounding, while §8.2.1 describes a differential 800 V option isolated from PE and downstream input-isolation requirements. These architecture-specific statements need to be reconciled for the selected implementation; the course does not prescribe a universal bond location.
4. Table 12's 96/100 kW row mixes “3W to 2W” assembly wording with a two-wire electrical-source description. The course reports a two-wire option without inventing adapter wiring or pin assignments.
5. Appendix A is non-normative and contains strong touch-safety assertions. The course retains qualified fault/service tradeoffs and explicitly preserves pole-to-pole shock risk.

## Original English review and validation

These checks describe the original 32-slide review, not the released packages.

- English source QA: four modules, four retained teaching videos, 23 glossary placements, and 12 page-specific PDF teaching links; zero flags.
- SVG arrow geometry: passes for active course figures. Existing canvas animations produce informational “no inline SVG” warnings.
- Separate formal LMS catalog exports regenerated and checked.
- Review pages use the maintained course renderer, with narration disabled in the review copy only. All 32 slide scripts remain available through transcripts and module-sized text exports.
- Review-package structure/media validation passes. This validates the silent review build, not final audio or LMS deployment.
- Browser spot checks: updated grounding slide, mobile PSU table (390 px; no horizontal page overflow), Module 3 question feedback and Retry reset, and all three revised static diagrams.
- Catalog poster uses the maintained template, bundled Lato/Academy logo/background and artwork. The command-line renderer could not launch its browser in this environment; the same template was checked and captured in the native review browser at 800 × 400.
- Audio generation and automated audio-tail checks passed for all 32 review clips. Model, voice, script and output hashes, pacing receipts, PCM format, silence, and clipping were checked. The review audio settings were superseded by the release settings in the README.

## Original review narration timing

Measured narration time for the pre-release audio (not learner time):

- Module 1: 7.48 minutes.
- Module 2: 9.59 minutes.
- Module 3: 8.99 minutes.
- Module 4: 9.37 minutes.

Total pre-release narration: 35.42 minutes. The review WAVs were decoded from ElevenLabs provider MP3 and paced with pitch preserved. This timing does not describe the released narration.
