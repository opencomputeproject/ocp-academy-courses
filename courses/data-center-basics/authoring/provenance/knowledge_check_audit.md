# Source knowledge-check audit

Status: all twelve source interactions have been authored and exercised in the final Slides build. Substantive corrections are recorded below; the original recovered interactions remain available for comparison. The exact recovered interactions are retained in `_source_knowledge_checks.json` and the four recovered `course.json` files.

The source contains twelve interactions: nine single-answer multiple-choice questions and three matching exercises. Preserve all twelve in the Slides adaptation. The explicit reuse request takes precedence over the new-course default of eight questions (one radio and one checkbox per module).

| ID | Source reference | Finding | Implemented authored treatment |
|---|---|---|---|
| M1-KC1 | M1/L5/B8 | Four facility-type pairs are useful introductory associations. The categories are not mutually exclusive: edge describes placement/use, while colocation describes an operating model. | Retain all pairs. Explain the characteristic each pair tests and that a facility may fit more than one label. |
| M1-KC2 | M1/L7/B3 | Physical hardware storing/processing data is the correct answer. Existing distractors are weak, and fallback feedback is generic. | Retain the tested concept/key. Improve distractors where useful and explain why cloud is a service model, app development is a workload, and customer support is an organizational function. |
| M1-KC3 | M1/L7/B5 | The intended key is closest, but it defines cloud as interconnected data centers. A private cloud can serve one organization, and cloud characteristics do not require multiple facilities. | Reword the keyed answer around on-demand access to pooled configurable resources. Preserve the physical-infrastructure teaching point; cite NIST. Flag the substantive wording correction. |
| M1-KC4 | M1/L7/B7 | "Location type" is ambiguous. An underground bunker can genuinely house a data center, so the keyed Edge answer is not uniquely defensible with that wording. | Ask which type is specifically placed near users to reduce latency; keep Edge as the key. Replace or explain misleading distractors. |
| M2-KC1 | M2/L7/B3 | AC-to-low-voltage-DC is correct for conventional AC-input server supplies, but not every server/rack power architecture uses that input. | Scope the prompt to a conventional AC-input server. Explain storage, networking and airflow functions separately in wrong-choice feedback. |
| M2-KC2 | M2/L7/B5 | Correct intended key. `PCle Card` uses a lowercase L instead of the I in PCIe. | Correct to `PCIe card`; explain CPU execution, RAM working memory, disk storage and expansion-card roles. Teach the concept within Module 2 before the check. |
| M3-KC1 | M3/L4/B3 | The key and feedback say 19 inches is the width between mounting rails. This is inaccurate. The nominal 19-inch dimension is the equipment front-panel width; horizontal hole centers are about 18.312 inches / 465.1 mm. | Replace the keyed answer with "the nominal width of the equipment front panel, including its mounting ears." Keep height, capacity and depth distractors, each with precise explanation. This is a factual correction to the original answer. |
| M3-KC2 | M3/L4/B7 | 1U/2U/4U associations are plausible examples, not a general mapping from server role to size. Source prose itself gives general-purpose servers as 2U or 4U. | Keep all three pairs but scope the prompt to the illustrated example layout; explain that vendors offer other sizes and U is only vertical allocation. |
| M4-KC1 | M4/L7/B3 | Heat reuse is the intended key. It can improve useful energy recovery and wider-system outcomes, but it need not lower facility energy or PUE. It is already deployed in some places, so "emerging" needs context. | Ask about putting otherwise rejected heat to productive use. Retain heat reuse as the key; explain demand, temperature and distance constraints. |
| M4-KC2 | M4/L7/B5 | Correct zombie-server key, but both success and failure feedback are copied from the heat-reuse question. "Zombie" can also mean malware-controlled equipment outside this energy-management context. | Keep the energy-management context. Explain powered-on equipment doing no useful work; distinguish it from standby redundancy, infection and productive high utilization. |
| M4-KC3 | M4/L7/B7 | Mixed air/liquid cooling is a defensible trend, but both feedback strings are copied from the heat-reuse question. | Keep the key. Explain workload-dependent cooling and why the three sweeping alternatives do not follow. |
| M4-KC4 | M4/L7/B10 | Five pairs are recoverable. Location → "Small and offshore deployments" overstates speculative offshore deployment. Incorrect feedback also says the learner matched the categories successfully. Other categories are broad trends rather than universal requirements. | Preserve five categories and matching format; change the location description to "Distributed or regional deployment matched to local constraints." Explain each category, and identify the correct partner for an incorrect pair. Record the wording change. |

## Feedback standard

Each wrong radio choice receives its own explanation of the misconception. Do not use praise-only, apology-only or answer-repetition-only messages. Correct-answer feedback explains why the function or relationship fits. Matching feedback shows the expected pair and explains its concept; the learner can retry. Narration orients the learner and does not read every answer aloud.

## Related teaching corrections

- The source Tier image embeds availability percentages and maximum annual downtime. Replace it: Uptime Institute removed expected-downtime predictions from its Tier Standard in 2009. Teach maintainability/fault behavior rather than a guaranteed service-level agreement.
- Distinguish site WUE from water used to generate purchased energy. Do not silently mix accounting boundaries.
- Remove universal "good/bad" PUE bands and undated company WUE benchmarks. PUE needs boundaries, climate/load context and complementary measures.
- Workload consolidation or zombie-server removal may lower total energy while increasing PUE because fixed facility overhead remains. Do not promise that every beneficial action lowers the ratio.
- Preserve remote and regional source examples without legal-compliance guarantees, absolute connectivity claims or unsupported city rankings.
- Replace the future-trends graphic's "no data centers at all" and quantum-storage inevitability with clearly qualified emerging-technology discussion.
- Keep original video binaries unchanged. Speech transcripts and 471 sampled video frames were reviewed; material corrections and qualifications are visible beside the preserved recordings. This does not claim continuous human playback review.

## Evidence

- [NIST cloud definition](https://www.nist.gov/publications/nist-definition-cloud-computing?pub_id=909616) and [NIST private cloud definition](https://csrc.nist.gov/glossary/term/Private_cloud).
- [METCASE 19-inch front panel](https://www.metcaseusa.com/en/19-Front-Panels/M6019010.htm) and [CyberPower rack-hole spacing](https://www.cyberpowersystems.com/faqs/what-is-the-standard-rack-horizontal-hole-spacing/). The CyberPower statement was available in the primary-source search excerpt; direct retrieval returned HTTP 405.
- [Uptime Institute Tier explanation](https://journal.uptimeinstitute.com/explaining-uptime-institutes-tier-classification-system/). Primary-source search excerpt explicitly states the removal of expected downtime; direct retrieval returned HTTP 403.
- [The Green Grid PUE definition](https://www.thegreengrid.org/node/372) and [OCP Heat Reuse](https://www.opencompute.org/projects/cooling-environments/heat-reuse/).
