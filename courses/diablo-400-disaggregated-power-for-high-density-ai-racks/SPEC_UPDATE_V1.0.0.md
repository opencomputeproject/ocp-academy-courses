# Mt. Diablo specification v1.0.0: English course refresh

Status: English content and scripts approved by the user on November 17, 2026. The notes below describe the original PR review. The November 18 local rebuild uses Leo v2 with the full Eleven v4 model and 96 kbps MP3 delivery. It rebuilds the four teaching videos at 1080p and preserves the separate syllabus entries. Human listening review and release packaging remain pending.

The local review now has 36 slides. Each module ends with a dedicated takeaways slide, a knowledge check, and a next-module or course-completion slide. Each of those slides has separate narration. Modules 1–3 retain their quiz content and audio. Question IDs remain stable across all modules.

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

## Course scope and compatibility

- Keep four modules and 32 slides, with the optional facility-LVDC module remaining distinct from base-specification requirements.
- Preserve the 35-minute core and 15-minute optional learner-time estimates. Validate timing again after narration is generated.
- Keep the stable course folder, course slug, module slugs, slide IDs, question IDs, and audio filenames. The title now uses Mt. Diablo.
- Preserve SCORM 1.2, Course Home plus four module syllabus entries, and existing independent video loops. No deployment-format migration is proposed.
- Keep WAV delivery, as requested by the user on November 17, 2026.
- Seven locale sources remain unchanged and based on v0.7.0. They must be refreshed separately before being presented as v1.0.0 editions.

## Change map

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
6. The existing Module 2 bipolar teaching clip retains its historical “Diablo 400” label. Its caption identifies that history and limits the example to bipolar output; current 800 V and grounding coverage is in the slide text and Module 3. No numerical requirement in that retained clip was changed by this refresh.

## Review and validation

- English source QA: four modules, four retained teaching videos, 23 glossary placements, and 12 page-specific PDF teaching links; zero flags.
- SVG arrow geometry: passes for active course figures. Existing canvas animations produce informational “no inline SVG” warnings.
- Separate formal LMS catalog exports regenerated and checked.
- Review pages use the maintained course renderer, with narration disabled in the review copy only. All 32 slide scripts remain available through transcripts and module-sized text exports.
- Review-package structure/media validation passes. This validates the silent review build, not final audio or LMS deployment.
- Browser spot checks: updated grounding slide, mobile PSU table (390 px; no horizontal page overflow), Module 3 question feedback and Retry reset, and all three revised static diagrams.
- Catalog poster uses the maintained template, bundled Lato/Academy logo/background and artwork. The command-line renderer could not launch its browser in this environment; the same template was checked and captured in the native review browser at 800 × 400.
- Audio generation and automated audio-tail checks are complete for all 32 clips, with zero flags. Model/voice, script/output hashes, pacing receipts, PCM format, silence and clipping checks also passed. Human pronunciation/listening approval, release packaging and target-LMS tracking verification remain pending. Script approval is now recorded from the user’s November 17, 2026 approval, rather than inherited from v0.7.0.

Narration: River (`SAz9YHcvj6GT2YYXdXww`), explicitly selected by the user after live metadata reported that the default Leo voice was unavailable. Use full Eleven v4 with the maintained pitch-preserving 1.18 tempo multiplier; learner speed remains 1.0. Keep WAV delivery. Confirm final audio and slides before release packaging.

## Narration delivery review

Measured narration time (not learner time):

- Module 1: 7.48 minutes.
- Module 2: 9.59 minutes.
- Module 3: 8.99 minutes.
- Module 4: 9.37 minutes.

Total narration: 35.42 minutes. The approved 35-minute core and additional 15-minute optional learner-time estimates remain unchanged. Native masters and per-clip receipts are retained outside the runtime. WAV delivery is decoded from ElevenLabs provider MP3 and paced with pitch preserved; it is not a lossless provider recording.

The narrated review is separate from the earlier silent review. No release SCORM ZIP has been created or uploaded, and no GitHub publication has been performed.
