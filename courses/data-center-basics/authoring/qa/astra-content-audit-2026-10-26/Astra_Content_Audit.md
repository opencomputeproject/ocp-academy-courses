# Astra content audit — Data Center Basics

Audit date: 26 October 2026 (America/New_York). Course snapshot: `2921de71109bba941c28b65e9ff9eede2d65fec1b7f1564496c7c86b3500666e`.

The course has a sound introductory core. Its authored explanations already correct several common errors: power versus energy, Tier capability versus uptime percentages, nominal rack dimensions, finite resources behind virtualization, and the limits of PUE. I recommend a targeted revision, not a technical expansion. Preserve all ten imported recordings and their own-audio/no-separate-slide-narration treatment.

The essential repairs are the unsupported rack-example matching question, three incorrect glossary placements, the second trend-matching question, and more specific editorial corrections to a few retained recordings. No single-choice answer key was found to be factually wrong. The two matching repairs are alignment/precision problems, not evidence that the listed hardware or trend associations can never occur.

For current coverage, add AI factories as a workload/purpose lens and introduce AICC as the broader continuum beyond centralized hyperscale facilities. Keep M1S8’s uncluttered four-card comparison. Two short following slides are preferable to squeezing ownership, scale, proximity, AI lifecycle and an OCP project into one grid. Keep Intro to OCP as the main onward path; AICC is an additional optional deep dive.

## Approval-ready choices

| Choice | Concrete scope | Slide count | Estimated effect |
|---|---|---:|---|
| A — Essential repairs | F01–F08 and F13: assessment alignment, three glossary placements, precise adjacent recording notes. Preserve recordings; no new standalone narration on them. | 76 | Mostly text/feedback; approximately 0–1 minute additional reading. |
| B — Recommended content update | A plus two short M1 slides (F09/F10), N+1 and containment clarifications (F11/F12), AICC project/course links and a small recap change. | 78 | About 2–3 minutes additional media; roughly 3–4 minutes additional learner time. Plan around 93–94 minutes until measured. |
| C — Recommended motion enhancement | B plus V01 on existing M2S14 and V02 on the new AICC slide. Seven generated videos total; AI-factory terminology stays static. | 78 | V02 is within the new slide’s time, not additive. V01 may add about 20–35 seconds over its current short narration; final timing must be measured. |

F14 networking is the strongest further coverage option, but it can wait if preserving the introductory duration is the priority. F15–F18 are optional refinements, verification or assessment coverage. Do not add five AICC project-domain lessons, detailed AI fabrics, electrical design, exhaustive cloud taxonomies, Tier uptime tables, or a quantum roadmap. Do not change voice, speed, LMS architecture or source recordings to meet a time target. The existing “about 90 minutes” is an estimate; a claim of an unchanged exact duration would be unwarranted.

## What was reviewed and what was not

- Every slide was reviewed as text using the current full-content packets, including complete active script bodies, imported transcripts, all quiz choices/keys/feedback, static-figure labels and available video text inventories. Duplicate transcript/cue forms were compared programmatically; their only differences were line-wrap hyphen spacing.
- No perceptual listening of narration or imported audio was performed, and no audio was played aloud. Audio realization, pronunciation, transcription fidelity and timing are not certified by this audit.
- One representative current frame from each of the five generated teaching videos was viewed, plus the M2S6 editable state/timing source. This is conceptual sampling, not a complete encoded-frame, continuity, timing or fullscreen/playback audit.
- No source-recording frames were newly viewed in this audit; original-video visual conclusions rely on the supplied reviewed inventories. Static figures were text-reviewed, not visually re-approved here.
- Primary sources were opened and read for material corrections and selected numerical/current claims. No exhaustive link, copyright, electrical design, environmental compliance, legal or product-specification certification is claimed.
- No LMS session, SCORM completion, mobile UI, quiz persistence or accessibility behavior was tested. Earlier timing-only and connector audits are not treated as proof of content accuracy.
- The live Academy URL returned a JavaScript shell; local adjacent AICC course/scripts verified scope. Enrollment and live course equivalence were not verified.

The four full-content packets were parsed and read in module-sized, deduplicated chunks. The repeated VTT text was compared against all ten full transcripts; differences were only hyphenation across caption line wraps. This comparison does not establish that the transcription matches the recorded voice. All forty glossary definitions were inspected in course.json, with direct semantic placement checks on the suspect slides.

| Module | Slides | Measured narrated + imported media | Existing learner estimate |
|---|---:|---:|---:|
| 1 — The Digital World | 18 | 13.95 min | 17 min |
| 2 — Data Center Physical Infrastructure | 18 | 21.92 min | 28 min |
| 3 — Inside the Rack | 16 | 10.90 min | 15 min |
| 4 — Management and Trends | 24 | 22.49 min | 30 min |

Total media is about **69.26 minutes** at normal speed. The five silent teaching videos share their narration time and are not counted twice. The 90-minute learner estimate therefore leaves about 20.74 minutes for reading, reflection, navigation and twelve questions. Timing was measured from WAV headers and MP4 movie headers without playback; this is a duration inventory, not a pacing/listening approval.

## Findings for approval

High priority means repair before approving this revision; medium means a material clarification or targeted gap; low means optional precision or verification. Categories distinguish factual errors, misleading simplifications, coverage gaps and assessment alignment. All wording below is proposed, not implemented.

### F01 — Align the form-factor matching exercise to examples actually taught

**High · assessment alignment · M3S6, M3S7, M3S15 · confidence: high**

M3S15 m3_kc2 keys 1U to compact compute, 2U to general-purpose enterprise, and 4U to high-density storage while referring to an illustrated example layout. M3S6 instead names 2U dual-node and 4U shared multi-node examples; M3S7 has a 4U-plus high-bay enclosure. No single current illustration supplies the tested mapping.

Evidence: The current cards, figure labels, active scripts and question pairs directly establish the mismatch. These are possible products, so the key is not universally factually false; it is insufficiently grounded in the current teaching.

Proposed wording or repair: Prompt: “Match the three named compute examples from ‘Compute Comes in Many Chassis’ to their illustrated vertical allocations.” Pairs: 1U → Compact compute server; 2U → Dual-node chassis; 4U → Multi-node platform with shared chassis infrastructure. Feedback: “These are the examples used here. A workload or server role does not imply one universal U height.”

Scope: Revise this question, its feedback and matching narration only after approval. Keep the separate storage example and general-purpose/GPU discussion. Alternative if original keys must remain: show an explicitly labeled second example table before testing it.

### F02 — Remove three glossary matches with the wrong meaning

**High · factual error in learner aid · M3S3, M3S7, M4S8, M4S17 · confidence: high**

M3S3 attaches the software Container definition to a shipping-container analogy. M3S7 attaches Virtual machine where the content discusses NVMe storage and never teaches a VM. M4S8 attaches DC (direct current) to a DCIM explanation with no direct-current use.

Evidence: course.json term_refs and the complete same-slide scripts/media inventories confirm these mismatches. VM and DC resemble substrings of NVMe and DCIM; that is not usage evidence. The precise mechanism that produced the pills was not audited.

Proposed wording or repair: Remove container from M3S3 and virtual_machine from M3S7. Remove dc from M4S8; its eligible first use in Module 4 is the spoken “direct current” on M4S17. Keep valid software-container and VM aids on M4S6.

Scope: Update only placements, then review all term_refs semantically for word boundaries, meaning and first eligible use. Do not add invented aliases or narration just to justify a pill.

Sources: [CNCF container glossary](https://glossary.cncf.io/container/); [NIST hypervisor glossary](https://csrc.nist.gov/glossary/term/hypervisor).

### F03 — Correct the division between DCIM and workload management

**High · misleading simplification · M4S4, M4S8 · confidence: high**

The imported M4S4 recording says BMS manages the environment and DCIM manages the workload. DCIM does not generally replace application monitoring, operating-system management or workload orchestration. The current “roles depend on implementation” caption is too vague to replace this false mental model.

Evidence: M4S4 transcript explicitly assigns these roles; M4S8 already provides a much sounder physical-assets/capacity definition. The opened Vertiv definition describes convergence between physical IT infrastructure and facility management.

Proposed wording or repair: “BMS monitors or controls building services. DCIM brings together information about physical assets, capacity, power and cooling. Application and workload tools manage software services; integrations and responsibilities vary by site.”

Scope: Put a concise editorial clarification next to M4S4 and reinforce it with one sentence on M4S8 if narration is revised. Preserve the recording and its verbatim transcript.

Sources: [Vertiv DCIM and IT management](https://www.vertiv.com/en-us/learn-about/dcim/).

### F04 — Identify ISO/IEC 27001 accurately

**Medium · misleading simplification · M4S4 · confidence: high**

The recording lists “ISO 27000 for data security” and says the frameworks ensure an efficient, secure, sustainable and accountable facility. The generic applicability caption does not distinguish an overview standard from requirements or explain that a standard is not a guaranteed outcome.

Evidence: ISO now identifies ISO/IEC 27000:2026 as an ISMS overview; ISO/IEC 27001:2022 specifies ISMS requirements. The 2026 27000 edition should not be described using the older “overview and vocabulary” title.

Proposed wording or repair: “ISO/IEC 27001 specifies requirements for an information security management system; ISO/IEC 27000 provides an overview of the family. Management standards support defined practices and assessment, but do not guarantee every service outcome. Applicable reporting obligations depend on the organization and jurisdiction.”

Scope: Use an editorial note or short supporting text. Do not add a detailed CSRD/legal lesson; this audit does not determine applicability to any organization.

Sources: [ISO/IEC 27000:2026 overview](https://www.iso.org/standard/27000); [ISO/IEC 27001:2022 requirements](https://www.iso.org/standard/27001).

### F05 — Make the market-share correction more decisive

**Medium · unsupported quantitative claim · M4S3, M4S4 · confidence: high**

M4S4 states that about 60% of global IT workload was in hyperscale facilities in 2024. The current caption calls the percentages unverified, but learners may still retain the figure. M4S3 also says the majority of workloads are in centralized hyperscale data centers without a defined workload measure.

Evidence: Synergy’s 2024 release reports 41% of worldwide data-center capacity and forecasts over 60% for 2029. Its June 2025 release reports 44% capacity and forecasts 61% for 2030. Neither supports the recorded 2024 workload claim. Similar figures suggest a forecast/measurement confusion, but the original chart’s provenance was not established.

Proposed wording or repair: “Do not use the recording’s 60% figure as a 2024 workload statistic. Facility capacity, workload counts and forecasts are different measures. The teaching point here is how ownership and contracts divide responsibility.”

Scope: Replace the existing uncertainty-only caption with this explicit note; avoid adding another dated share statistic. Keep the ownership teaching and all recordings.

Sources: [Synergy: hyperscale and colocation capacity trends](https://www.srgresearch.com/articles/hyperscale-operators-and-colocation-continue-to-drive-huge-changes-in-data-center-capacity-trends); [Synergy: capacity shifting to hyperscale operators](https://www.srgresearch.com/articles/the-worlds-total-data-center-capacity-is-shifting-rapidly-to-hyperscale-operators).

### F06 — Make the server/storage caveat specific enough to counter the recording

**Medium · misleading simplification · M2S12 · confidence: high**

The recording calls 2U two-socket servers the most common today, describes HDDs as requiring more power and failing sooner because of moving parts, and ends by saying redundancy ensures continuous uptime. The existing variation caption is directionally correct but leaves these stronger claims insufficiently qualified.

Evidence: Current transcript and on-screen inventory contain the broad claims. SNIA describes SSD product segmentation and workload-dependent endurance; form factor, endurance and reliability cannot be ranked universally from one media label. No market-share evidence for the 2U/two-socket assertion is supplied.

Proposed wording or repair: “The 2U, two-socket server is an example, not a verified majority. SSDs and HDDs have different failure modes; neither medium is always more reliable or lower-power. Compare product specifications and workload needs. Redundancy supports availability only within its designed failure coverage.”

Scope: Expand the adjacent editorial note, ideally with the reliability correction visible before playback. Preserve original caption text as a record of what was said, clearly separated from editorial corrections.

Sources: [SNIA, What is an SSD?](https://www.snia.org/education/what-is-ssd); [Uptime Institute Tier Classification explanation](https://journal.uptimeinstitute.com/explaining-uptime-institutes-tier-classification-system/).

### F07 — Explain that logical isolation does not create physical redundancy

**Medium · misleading simplification · M4S6, M4S7 · confidence: high**

M4S6’s caption already corrects the one-application bare-metal model and fixed utilization percentages. However, the recording also presents virtualization/containerization as inherently smarter redundancy with less hardware and implies a universal progression from bare metal to VMs to containers.

Evidence: M4S7 correctly shows a shared finite host. If that host fails, environments on it share the failure unless additional architecture provides continuity. This is an inference from the shared-host model, not a claim that all virtualized services lack resilience.

Proposed wording or repair: “Bare metal can run multiple applications, and containers can run on bare metal or inside virtual machines. Neither VMs nor containers automatically provide high availability. Several logical environments on one host still share that host’s failure; continuity needs suitable placement, spare capacity and recovery mechanisms.”

Scope: Strengthen the adjacent M4S6 note; add the one-host failure sentence to M4S7 only if the script update is approved. No container orchestration tutorial is needed.

Sources: [NIST hypervisor glossary](https://csrc.nist.gov/glossary/term/hypervisor); [NIST SP 800-190, Application Container Security Guide](https://csrc.nist.gov/pubs/sp/800/190/final).

### F08 — Qualify the recorded edge and connectivity definitions

**Medium · misleading simplification · M1S5, M1S8 · confidence: high**

M1S5 defines edge data centers as smaller modular units, implies redundant infrastructure is universal and explains carrier neutrality only as having multiple providers. M1S8 improves the edge definition, but the recording’s adjacent caption is generic.

Evidence: The current recording transcript is categorical; the current M1S8 definition and OCP AICC project scope accommodate many site forms. A carrier-neutral provider makes provider choice available to customers; presence of multiple carriers alone is an incomplete definition.

Proposed wording or repair: “These are examples, not requirements for every facility. Edge describes proximity to the workload, not a required size or modular building. Carrier-neutral facilities allow customers to choose among network providers. Redundancy and connection options depend on the site.”

Scope: Add this short editorial note next to the preserved recording. Keep M1S8’s overlapping-dimensions explanation.

Sources: [Flexential carrier-neutral data centers](https://www.flexential.com/resources/blog/carrier-neutral-data-center).

### F09 — Add AI factories as a workload lens, with training and inference

**Medium · coverage gap · M1S8, M1S16, M2S12, M4S16 · confidence: high**

AI workloads appear later, but Module 1 never names AI factories or explains training versus inference. Adding “AI factory” as another exclusive ownership/location type would undermine M1S8’s correct statement that labels describe different dimensions.

Evidence: NVIDIA uses the term for purpose-built infrastructure across the AI lifecycle; the IEA uses it for AI-focused data centers; the European Commission also uses it for a computing/data/expertise ecosystem. These usages justify acknowledging the term, not declaring one universally standardized taxonomy.

Proposed wording or repair: Proposed new M1S8A title: “AI Workloads Add Another Design Lens.” Script: “Some data centers are designed around AI workloads. You may hear these called AI factories: infrastructure and software organized to develop and run AI at scale. Training adjusts a model using data; inference uses a trained model to produce a result. Their requirements vary. Accelerators, memory, storage and the connections between systems must work together, with suitable power and cooling. AI factory describes a purpose and operating approach. It does not tell you who owns the building or where it sits. An enterprise, a colocation customer or a hyperscale operator can run AI infrastructure.”

Scope: Recommend a new short slide after M1S8, with a static workload-versus-facility comparison. Keep the four-card M1S8 unchanged. Add workload/purpose to the M1S16 recap. Do not teach model internals, vendor products, token economics or rack-density thresholds.

Sources: [NVIDIA AI factory glossary](https://www.nvidia.com/en-us/glossary/ai-factory/); [European Commission AI Factories](https://digital-strategy.ec.europa.eu/en/policies/ai-factories); [IEA, Key Questions on Energy and AI, executive summary](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary).

### F10 — Connect edge placement to the broader AICC learning path

**Medium · coverage gap · M1S8, M1S12, M4S16, M4S23 · confidence: high**

Edge is taught, but neither the AICC project nor the existing Academy course is named. AICC must not be reduced to “OCP’s edge tier” or presented as a completed universal platform.

Evidence: The live OCP project covers hyperscale-adjacent environments and constraints, including regional colocation, enterprise, telco and industrial settings. The supplied local AICC Module 1 explicitly treats a continuum rather than a fixed ladder.

Proposed wording or repair: Proposed new M1S8B title: “AI Can Run Across a Computing Continuum.” Script: “Some AI services benefit from running near the people or equipment they serve. Others need more capacity at a regional or large central site. Consider a factory inspection system: a local model may keep making time-sensitive decisions, while selected information goes elsewhere for deeper analysis. OCP’s AI Computing Continuum, or AICC, explores open infrastructure for AI beyond centralized hyperscale facilities. The sites have different limits on power, cooling, space and connectivity. This is broader than one edge category. Placement follows the service’s needs, and a distant connection does not automatically meet them.” Resource text: “Explore the AICC project” and “Optional deep dive: AI Computing Continuum.”

Scope: Use a second short slide rather than crowd M1S8. Add the project link there and on M4S16; add the exact Academy course link as an optional path on M4S23 alongside the existing Intro to OCP path. Leave the five domains and Across models to the dedicated course.

Sources: [OCP AI Computing Continuum project](https://www.opencompute.org/projects/aicc/); [AI Computing Continuum: Extending AI Beyond the Hyperscale Data Center](https://academy.opencompute.org/learn/courses/58/ai-computing-continuum-aicc-extending-ai-beyond-the-hyperscale-data-center).

### F11 — Define N+1 where the original power graphic introduces it

**Medium · coverage gap · M2S5, M2S6 · confidence: high**

The imported M2S5 text inventory contains N+1 SETUP, but the current course provides no N+1 definition. The general redundancy glossary does not decode the notation.

Evidence: The reviewed inventory establishes a visible unexplained term. N+1 expresses additional capacity relative to the amount needed; it does not establish independent distribution paths or guarantee uptime.

Proposed wording or repair: “N is the capacity needed to support the intended load. N+1 adds one extra capacity unit so the load can still be supported when one unit is unavailable, if the rest of the design permits it. It does not mean that every path is independent.”

Scope: Add a short explanation near M2S5 or in M2S6 supporting text, with a small static two-needed-plus-one example if desired. A glossary entry can support, but should not replace, the explanation. Keep any numbers illustrative.

Sources: [LBNL/EPRI UPS report](https://datacenters.lbl.gov/sites/default/files/UPS_Report_2005.pdf).

### F12 — Close the promised hot-versus-cold containment comparison

**Medium · coverage gap · M2S2, M2S10, M2S11 · confidence: high**

M2S2 narration promises a comparison of hot and cold aisle containment. Later slides explain hot/cold aisles and general separation, while the generated video shows a contained return side. They do not clearly contrast which aisle is enclosed.

Evidence: This is a teaching-objective alignment issue, not an error in the existing airflow sequence.

Proposed wording or repair: “Cold-aisle containment encloses the cool supply side. Hot-aisle containment encloses the warm exhaust side. Both aim to reduce mixing; their suitability depends on the room’s supply, return and operating arrangements.”

Scope: Add one sentence and a small static side-by-side to M2S10, or narrow the M2S2 promise to “explain containment.” Prefer the small comparison if maintaining the original learning intent. Keep M2S11’s substantive causal video.

Sources: [DOE Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/sites/default/files/2024-07/best-practice-guide-data-center-design.pdf).

### F13 — Replace the trend-matching exercise’s unstated or ambiguous associations

**Medium · assessment alignment · M4S16, M4S22 · confidence: high**

M4S22 tests a shift toward modular and hybrid architectures, direct investment, and storage-capacity growth without clearly teaching those exact developments. “Energy Efficiency → Recycling residual heat” also blurs the distinction that M4S13 carefully makes between facility electricity and wider-system useful heat.

Evidence: All pairs are plausible associations, not proven wrong answer keys. The problem is instructional support and precision: hybrid is not defined here, and the current module does not establish a storage-growth forecast.

Proposed wording or repair: Prompt: “Match each area to the planning consideration taught in this course.” Pairs: Location → Match placement to workload and local constraints; Physical deployment → Use modular construction where it fits the site; Heat reuse → Connect recoverable heat to suitable useful demand; Energy sourcing → Check contracts and energy-attribute ownership; Storage planning → Balance capacity, access performance, protection and service needs.

Scope: Preserve all five subject areas, but align labels, keys, feedback and narration with taught principles instead of adding several forecast lessons. The storage principle is covered in M3S7; identify this as a course-wide recap or briefly reprise it before the question.

### F14 — Give networking a small, explicit equipment-role treatment

**Medium · coverage gap · M2S12, M3S7, M3S10 · confidence: medium-high**

Compute and storage get dedicated explanation in Module 3. Networking is repeatedly named as a capacity constraint, but switch/router/interface roles are compressed into one sentence in the imported server recording.

Evidence: This is a proportional coverage gap for a course organized around compute, storage and networks. It is not necessary to add protocol design or detailed AI fabrics.

Proposed wording or repair: “A network interface connects a server to a network. Switches connect devices and carry traffic within the facility; routing functions move traffic between networks. Some equipment combines these functions. Check compatible interfaces, link capacity and the complete path: more compute is useful only if information can reach it.”

Scope: Optional one 45–60-second slide near M3S7–M3S10 with a static server → switch → other network illustration. If strict duration is preferred, add a compact panel to the existing equipment-role discussion instead. Keep Ethernet, InfiniBand, RDMA and topology tuning for a later course.

Sources: [Cisco switch versus router](https://www.cisco.com/site/us/en/learn/topics/small-business/network-switch-vs-router.html).

### F15 — Add one concrete operations loop

**Low · optional enrichment · M3S11, M4S8, M4S19 · confidence: medium**

Management is sensibly framed around evidence and responsibility but stays abstract about what an operator does between an alarm and an improvement.

Evidence: The current M4S8 figure already contains measure, context, procedural action and verification. A brief scenario would make the existing concept transferable without expanding into an operations manual.

Proposed wording or repair: “If inlet temperature rises after equipment is added, first identify the affected assets and confirm the reading. The responsible teams review airflow, cooling capacity and the approved operating limits. Any change follows the site’s authorized procedure, and the team checks service performance and temperatures afterward.”

Scope: Optional 20–30 seconds within M4S8 or M4S19; no new slide needed. Mention trained/authorized work without adding technical switching, electrical or maintenance procedures.

### F16 — Make the temperature correction explicitly about equipment inlets

**Low · optional precision · M2S8 · confidence: high**

The recording moves from higher cooling setpoints to “up to 27 degrees” as though this could be a universal setting. The existing equipment-requirements caption already provides the necessary caveat; a more concrete sentence would reduce misreading.

Evidence: ASHRAE’s air-cooled classes use different envelopes: the commonly cited 18–27 °C recommended range applies to A1–A4, while H1 is narrower. Recommended inlet conditions are not a universal thermostat setpoint.

Proposed wording or repair: “The temperature example concerns equipment inlet conditions, not a universal room setpoint. The applicable equipment class and manufacturer limits govern; some dense systems require lower inlet temperatures. Cooling stages alone do not create redundancy.”

Scope: Optional refinement to the existing adjacent caption; keep numerical class tables out of the beginner narrative. The current caption is textually adequate if read, so this is not a release-blocking new error.

Sources: [ASHRAE 2023 Applications Handbook, Chapter 20](https://handbook.ashrae.org/Handbooks/A23/SI/A23_Ch20/a23_ch20_si.aspx).

### F17 — Verify “microservers” versus “microservices”

**Low · transcription verification · M4S6 · confidence: medium**

The preserved transcript and cues at 163.72–167.62 seconds say “microservers,” while the reviewed visible-text inventory says MICROSERVICES. This may be an ASR error or the speaker’s actual word; this audit did not listen to adjudicate it.

Evidence: Direct comparison of transcript/cue text and the supplied visible-text inventory. No audio claim is made.

Proposed wording or repair: If the spoken word is “microservices,” correct the transcript/cue transcription. If it is actually “microservers,” retain the verbatim speech record and add “Here, the intended software concept is microservices.” as an editorial note.

Scope: Targeted listening by an authorized reviewer or a non-audible independent transcription comparison before any change. Do not silently rewrite a verbatim transcript as though the speaker said something else.

### F18 — Consider one check on the module’s power or thermal path

**Low · optional assessment coverage · M2S2, M2S17 · confidence: high**

Module 2’s two retained source questions assess server PSU and PCIe functions rather than its main facility power-continuity and cooling outcomes.

Evidence: The current objectives and both questions were compared directly. This is a coverage opportunity, not an incorrect answer key.

Proposed wording or repair: Optional added question: “In the conventional example, what supports the equipment while the backup generator starts?” Correct: “Stored energy through the UPS.” Distractors: “Extra empty rack positions”; “The generator before it is ready and selected”; “Containment alone.” Feedback: “Stored energy can bridge the source transition for the supported load; the actual duration and coverage depend on the design.”

Scope: If approved, add this as a formative item while retaining the twelve source questions. It would bring the question count to thirteen and require matching knowledge-check narration; do not silently substitute it for an existing source question.

## Retained-recording correction assessment

“Sufficient in text” means the adjacent written correction and later teaching address the misconception. It does not certify the unmodified recording as factually clean or prove learners see the correction during fullscreen playback. Keep editorial corrections visibly distinct from verbatim transcripts and captions; where the misconception matters, expose the note before playback and reinforce it in the next authored explanation.

| Recording slide | Disposition | What remains |
|---|---|---|
| M1S3 | No material factual correction required at this level. | Systems overview is broad and examples should not be read as a universal facility bill of materials. Generic supporting caption is adequate for the role. |
| M1S5 | Strengthen correction: F08. | Edge/modularity and carrier-neutral shorthand remain misleading; later M1S8 helps but the immediate caption does not counter them. |
| M2S3 | Existing correction is substantially sufficient in text. | The recording conflates air handlers with CRACs and UPSs with battery banks. The adjacent caption explicitly distinguishes CRAC/CRAH and a complete UPS, and M2S6/M2S9 reinforce the system roles. A named environmental goal is not proof of lower lifecycle emissions. |
| M2S5 | Existing correction is substantially sufficient; add definition F11. | The adjacent note directly corrects continuously-running generators, qualifies startup/supported load, treats rack densities as examples and qualifies fuel emissions. M2S6 gives a sound backup sequence. N+1 remains unexplained. |
| M2S8 | Existing correction is substantially sufficient; optional F16. | The note explicitly rejects the claim that each cooling level creates redundancy and conditions temperature/efficiency claims. Clarifying inlet conditions would help. Immersion benefits remain design-dependent. |
| M2S12 | Strengthen correction: F06. | The current variation caveat is useful but should explicitly counter the failure/power ranking and unsupported server-majority claim; redundancy is not a guarantee. |
| M3S3 | Existing correction is strong in text; glossary error F02 is separate. | The source says 44.45 centimeters for 1U and treats 19 inches as rail separation. Adjacent caption plus M3S4/M3S5 clearly correct both, including U versus performance. This audit does not assert that every viewer notices an outside-video note in fullscreen. |
| M4S3 | Existing correction is mostly sufficient; F05 also applies. | Heat reuse does not recover every kWh usefully; M4S13 fixes this well. Quantum requirements differ by platform, and local hosting is not automatic compliance or resilience. The unsupported majority-of-workloads statement should not be retained as a fact. |
| M4S4 | Strengthen correction: F03–F05. | Current caveats are too generic for DCIM workload-management and ISO distinction; market-share claims need a decisive non-use note. |
| M4S6 | Existing correction partly sufficient; strengthen via F07; verify F17. | Bare-metal multiple-app support and variable utilization are already corrected. Shared-host failure, coexistence of containers and VMs, and the microservers/microservices discrepancy remain. |

## Quiz correctness and ambiguity

All nine single-choice items have a defensible best answer; no corrected item requires a mastery gate. Existing attempt/retry policy is outside this content audit and should remain as approved. Three matching items were reviewed; one is acceptable with caveats and two need teaching alignment.

| Question | Slide | Result | Reason |
|---|---|---|---|
| m1_kc1 | M1S9 | acceptable with caveat | Four associations are distinguishable; global cloud is a hyperscale example, not an exclusive definition. Existing feedback appropriately allows overlap. |
| m1_kc2 | M1S17 | correct | Choice c is the best answer; feedback also includes networking and facility support. |
| m1_kc3 | M1S17 | correct | Choice b matches the core cloud definition; public internet and multiple sites are correctly not mandatory. |
| m1_kc4 | M1S17 | correct | Choice d; distractors are weak but unambiguous. No need to add difficulty merely for its own sake. |
| m2_kc1 | M2S17 | correct | Choice b; conventional AC-input scope avoids falsely excluding DC-fed architectures. |
| m2_kc2 | M2S17 | correct | Choice c; expansion card role is accurate for the stated examples. |
| m3_kc1 | M3S15 | correct | Choice b; distinguishes panel width from hole spacing, depth and height. |
| m3_kc2 | M3S15 | alignment repair | Possible hardware sizes, but the stated illustrated mapping is not supplied by current teaching; F01. |
| m4_kc1 | M4S21 | correct | Choice c; feedback correctly conditions useful heat on temperature, distance and infrastructure and does not promise lower PUE. |
| m4_kc2 | M4S21 | correct | Choice b; context distinguishes energy-management zombies from malware and legitimate standby capacity. |
| m4_kc3 | M4S21 | correct | Choice b; workload-dependent mixed cooling is defensible. Distractors are broad but not ambiguous. |
| m4_kc4 | M4S22 | alignment repair | Plausible associations, but several exact trends are not taught and heat reuse is awkwardly categorized; F13. |

The quiz distribution is uneven: Module 2 checks server PSU/PCIe functions more than its central power-continuity/cooling objectives. This is the low-priority F18 assessment opportunity, not a wrong-key finding. If one additional formative item is desired, use an unscored scenario on why a generator needs a bridging source or why a liquid-cooled rack still needs facility heat rejection. Do not replace the twelve retained source questions merely to improve balance; get approval for an additional item and its narrated treatment.

## Teaching video opinion

Keep the current five. They cover distinct relationships: M1S4 service dependency, M2S6 source transfer and UPS bridge, M2S11 mixing versus containment, M3S9 independent capacity budgets, and M4S7 virtual-to-physical demand. One representative current frame from each was viewed; M2S6 state logic was also inspected. No sampled conceptual error justifies replacing them. This is not a renewed timing or continuous-frame signoff.

Prefer at most two additional narration-timed, single-pass causal sequences in this revision. Do not animate a taxonomy, acronym list, formula reveal or decorative loop merely to increase the video count. Each new sequence needs an approved script/storyboard, measured final narration, useful final still and one audible track.

### 1. Follow two coolant loops and the heat path — V01

**Placement:** M2S14. **Approximate length:** 45–60 seconds.

**Learning gain:** Separates coolant circulation from heat transfer and shows why a cold plate does not eliminate facility heat rejection.

**Sequence:** Component generates heat; the equipment loop carries it to a heat exchanger. → Show heat crossing the interface while the two fluids remain in separate closed paths in this example. → Compare liquid-to-liquid facility transfer with a liquid-to-air retrofit. → Trace the heat onward to the environment and hold the remaining facility-capacity requirement.

**Static alternative:** A properly labeled two-loop static diagram is sufficient for recognition; motion materially helps trace flow, transfer and the retrofit consequence.

**Recommendation:** Recommended first new video if approved. Replace the existing static figure; retain one silent video with the approved narration clock.

### 2. Place an AI task when conditions change — V02

**Placement:** proposed M1S8B, M4S16. **Approximate length:** 50–65 seconds.

**Learning gain:** Makes the AICC bridge a service-placement decision rather than a map or a fixed hierarchy.

**Sequence:** A local inspection request has a short response deadline. → A wide-area link becomes unavailable; the defined local service continues with its local model. → A separate, non-urgent analysis task uses regional capacity when connectivity permits. → Hold latency, connectivity and site limits as the decision criteria; do not route every request through every site.

**Static alternative:** A static continuum is enough to introduce the project; the conditional decision sequence adds genuine causal teaching when the new slide is approved.

**Recommendation:** Recommended second only with the AICC addition. Do not reproduce the dedicated AICC course’s deeper architecture.

### 3. Total energy falls while PUE rises — V03

**Placement:** M4S11. **Approximate length:** 35–45 seconds.

**Learning gain:** Makes the denominator effect visible and prevents equating a better ratio with all energy improvements.

**Sequence:** Begin with same-period IT energy 1000, overhead 200 and total 1200; calculate 1.20. → Hold useful work constant in the stated example; reduce IT energy to 800 while overhead remains 200. → Recalculate total 1000 and PUE 1.25 together. → Hold the lower total energy beside the higher ratio.

**Static alternative:** The existing before/after figure already teaches this correctly. Video is optional, not needed to repair a defect.

**Recommendation:** Next optional choice after the top two; add the same-useful-work assumption explicitly if animating consolidation.

### 4. One excavation defeats two services — V04

**Placement:** M1S14. **Approximate length:** 35–45 seconds.

**Learning gain:** Shows common-cause failure and why provider count is not physical path diversity.

**Sequence:** Two labeled service links use a common trench. → One excavation interrupts both. → Reset to a separate comparison with physically diverse routes. → The same event interrupts only one path; continued service is conditional on an appropriate working alternate and failover.

**Static alternative:** The existing paired static routes are already sufficient. Motion adds a memorable failure event but overlaps the current resilience explanation.

**Recommendation:** Optional; do not imply separation alone guarantees uninterrupted application service.

### 5. A host failure affects its logical guests — V05

**Placement:** M4S7. **Approximate length:** 30–40 seconds.

**Learning gain:** Reinforces the corrected distinction between logical isolation and physical redundancy.

**Sequence:** Several guests share one physical host. → A host failure affects those guests together. → Reset to a deliberately separate, designed recovery example with another host, available capacity and recoverable state. → Hold that recovery may take time and is not an inherent property of containers or VMs.

**Static alternative:** One clear shared-host diagram plus a sentence is sufficient for this introductory course.

**Recommendation:** Defer unless users still misunderstand resilience. Do not lengthen or replace the existing resource-demand animation just to increase the video count.

## Glossary and reference implications

- Apply F02 before adding terms. Also review first-use placement: containment is already spoken in M2S3, while its pill currently appears at M2S10; move it only after confirming the eligible, rendered first use and accepted plural variant. Do not turn substring matches into evidence.
- Add AI factory, inference or N+1 only where the approved revised content actually uses them. AICC needs a project/resource link; a tooltip is optional. Do not create glossary entries for baseline AI/ML or OCP.
- Put the AICC project link with the new continuum explanation and the exact Academy course link with the optional learning path. The old community URL redirects to the current project URL. Do not remove Intro to OCP or substitute the separate OCP Orientation series without a requested curriculum decision.
- Keep current, well-supported references: the 2026 IEA demand outlook; the October 12, 2026 OCP ecosystem article; the developing 800 VDC context; Google’s June 16, 2026 Brazos example; PUE and DOE water/carbon boundaries. M4S10’s DOE PDF viewer pages 39–40 are the correct supporting range.
- The audit did not refresh every city example, every cable on the historical map, the McMurdo service page, every glossary URL or every external enrollment route. Do not turn this audit into a blanket link or source-video signoff.

## Coverage ledger

Coverage.json accounts for all 76 current slides and records a per-slide disposition, findings, review mode and limitations. The list below is a concise content ledger; “no additional issue identified” is limited to the reviewed material, not a certification of every real-world implementation.

### Module 1: The Digital World

| Slide | Topic | Audit note |
|---|---|---|
| M1S1 | The Digital World | Orientation is appropriately foundational. |
| M1S2 | Follow the Service, Facility, Rack and Operations | Four-module course overview fits scope; 90 minutes is estimated learner time. |
| M1S3 | A First Look at Physical Infrastructure | Imported systems overview checked textually. |
| M1S4 | One Request Depends on Many Systems | Service-request sequence and persistent physical dependencies are coherent. |
| M1S5 | What Is a Data Center? | Imported edge/connectivity generalizations need a clearer note. |
| M1S6 | Capacity Is More Than Floor Space | Power/energy distinction and 1 kW × 1 h arithmetic are correct. |
| M1S7 | Tiers Describe Infrastructure Capabilities | Capability-based Tier framing is sound; retain the no-uptime-guarantee distinction. |
| M1S8 | Enterprise, Colocation, Hyperscale and Edge | Overlapping dimensions are sound; add AI/AICC on separate short slides. |
| M1S9 | Match the Facility to Its Role | Matching is acceptable with existing overlap feedback. |
| M1S10 | Location Balances Access, Energy and Risk | Latency, resources, hazards and location constraints are appropriately conditional. |
| M1S11 | Regional Hubs Serve Different Needs | Six city examples are illustrative; no current market ranking or detailed site suitability independently certified. |
| M1S12 | Remote Sites Have a Different Tradeoff | Remote/local capability example is appropriate; precise McMurdo program/site facts not independently refreshed. |
| M1S13 | Fiber Connects Facilities and Users | Historical map is explicitly not a current cable inventory; geography not audited cable by cable. |
| M1S14 | Redundancy Must Survive the Same Failure | Common-trench example correctly distinguishes nominal and independent redundancy. |
| M1S15 | Cloud Is a Service Model Built on Facilities | Cloud/facility distinction is sound; this is not an exhaustive NIST deployment/service-model lesson. |
| M1S16 | What Connects the Digital World | Retain recap; add workload/purpose if AI-factory slide approved. |
| M1S17 | Apply the Digital World Model | Three single-choice keys and feedback are correct. |
| M1S18 | Data Center Physical Infrastructure | Module boundary is coherent. |

### Module 2: Data Center Physical Infrastructure

| Slide | Topic | Audit note |
|---|---|---|
| M2S1 | Data Center Physical Infrastructure | Power and heat-removal framing is appropriate. |
| M2S2 | Trace Power, Heat and Physical Constraints | Promised containment comparison needs one explicit distinction or narrower objective. |
| M2S3 | A Tour of the Physical Systems | Imported CRAC/UPS misconceptions have explicit adjacent corrections. |
| M2S4 | The Data Hall Depends on Support Systems | White/grey space is introduced as coordination vocabulary, not absolute architecture. |
| M2S5 | How Power Reaches the Data Hall | Generator/density/emissions caveats are useful; N+1 is unexplained. |
| M2S6 | Follow the Power Path | Conventional functional power/backup sequence is sound and clearly illustrative. |
| M2S7 | Conversion and Expansion Happen Inside the Server | AC/DC conversion and PCIe roles are sound within the stated scope. |
| M2S8 | How Cooling Removes the Heat | Cooling-level redundancy is corrected; temperature specificity is optional. |
| M2S9 | A Cooling System Moves Heat Out | Heat must leave the room/facility; basic CRAC/CRAH distinction is appropriately restrained. |
| M2S10 | Keep Supply Air Apart from Exhaust | Add explicit cold- versus hot-aisle containment comparison if objective retained. |
| M2S11 | Containment Reduces Air Mixing | Mixing/return-side video supports the concept; no new content error identified. |
| M2S12 | Effective Infrastructure Works as a System | Recorded storage/server generalizations need a sharper editorial correction. |
| M2S13 | An Empty Rack Is Not Spare Capacity | Space is not enough; concurrent resource limits are well stated. |
| M2S14 | Liquid Cooling Adds a Heat-Transfer Path | Liquid-to-air retrofit explanation is correct; strongest new motion candidate. |
| M2S15 | Open Interfaces Help Teams Coordinate | 800 VDC is properly described as developing community work, not mandatory conversion. |
| M2S16 | Reliable Operation Requires the Whole Chain | System-wide constraints recap is coherent. |
| M2S17 | Check the Function of Each Component | Both single-choice keys and scope are sound. |
| M2S18 | Next: Inside the Rack | Transition to rack interpretation is coherent. |

### Module 3: Inside the Rack

| Slide | Topic | Audit note |
|---|---|---|
| M3S1 | Inside the Rack | Rack overview fits introductory scope. |
| M3S2 | Read a Rack Layout and Its Constraints | Objectives are consistent with later material, aside from the example-matching repair. |
| M3S3 | Rack Equipment Overview | Unit/width errors are explicitly corrected; software-container pill is wrong. |
| M3S4 | What the 19-Inch Dimension Measures | Nominal front-panel versus hole-center dimensions are correct at introductory precision. |
| M3S5 | Rack Units Measure Vertical Allocation | U allocations and clearance distinction are correct; U is not performance. |
| M3S6 | Compute Comes in Many Chassis | Current compute examples differ from the later quiz mapping. |
| M3S7 | Storage Designs Balance Access and Capacity | Storage roles are sound; virtual-machine pill is unsupported. |
| M3S8 | Shared Chassis and Utility Nodes Have Distinct Roles | Shared-chassis dependencies are accurately conditional. |
| M3S9 | Equipment Choice Consumes Several Budgets | Independent percentage budgets are illustrative; no equation of electrical and thermal allocations implied. |
| M3S10 | Cables and Airflow Need Their Own Space | Airflow/cabling/access discussion allows non-front-to-rear equipment. |
| M3S11 | Physical Security Supports Serviceability | Access-control teaching is useful; not a complete physical/security operations course. |
| M3S12 | Open Rack Is a Different Mechanical System | U versus Open Unit and equipment-space vocabulary are sound; version-specific dimensions deferred appropriately. |
| M3S13 | Interpret the Layout Before Adding Hardware | Scenario correctly requires review of cooling and connectivity rather than spare U alone. |
| M3S14 | A Rack Is More Than a Stack of Servers | Recap maintains dimensional and functional distinctions. |
| M3S15 | Verify Dimensions and Example Form Factors | Dimension key correct; example-matching alignment needs repair. |
| M3S16 | Next: Management and Trends | Transition to responsibility/resource outcomes is coherent. |

### Module 4: Management and Trends

| Slide | Topic | Audit note |
|---|---|---|
| M4S1 | Management and Trends | Management/resource framing is appropriate. |
| M4S2 | Connect Ownership, Metrics and Technology Choices | Objectives fit content; scope is foundational rather than operator qualification. |
| M4S3 | The Changing Data Center Landscape | Context caveats correct most trends; avoid unsupported workload-majority claim. |
| M4S4 | Who Owns and Manages What? | DCIM, ISO and market-share editorial corrections need strengthening. |
| M4S5 | Responsibility Follows the Service Contract | Responsibility follows actual service contract; no fixed universal matrix is asserted. |
| M4S6 | Physical Versus Virtual Infrastructure | Bare-metal and utilization caveats help; physical redundancy and transcription need attention. |
| M4S7 | Virtual Services Still Consume Physical Resources | Shared physical-resource model is sound; optional one-host failure sentence reinforces correction. |
| M4S8 | Monitor Before You Optimize | DCIM definition is sound; direct-current glossary pill is not. |
| M4S9 | PUE Measures Facility Overhead | PUE 1200/1000 = 1.20 is correct and limits are clear. |
| M4S10 | Water and Carbon Need Explicit Boundaries | WUE/CUE boundaries and units are appropriate; PDF viewer pp. 39–40 support them. |
| M4S11 | Remove Waste Without Misreading the Ratio | PUE 1000/800 = 1.25 while energy falls is correct; state same useful work explicitly if animating. |
| M4S12 | Improve Cooling and Power Together | Efficiency improvements are conditional; economizer is named without a deep explanation, acceptable optional vocabulary. |
| M4S13 | Heat Reuse Needs a Useful Heat Customer | Heat reuse is correctly conditional and not equated with lower PUE. |
| M4S14 | Clean Energy Claims Need More Than a Contract Label | Energy attributes, contract ownership and annual-versus-hourly claims are distinguished. |
| M4S15 | Demand Growth Raises Local Infrastructure Questions | 485/950 TWh and April 2026 attribution independently verified; preserve estimate/projection labels. |
| M4S16 | Plan for Mixed Workloads and Cooling | Mixed deployment/cooling discussion is sound; natural AICC return point. |
| M4S17 | Co-Design from Chip to Grid | October 2026 chip-to-grid context verified; no universal 800 VDC claim. |
| M4S18 | Emerging Technologies Need a Readiness Test | Readiness framework appropriately avoids a speculative quantum/photonics roadmap. |
| M4S19 | Choose an Improvement That Fits the Site | System-view scenario is useful; optional concrete operations example. |
| M4S20 | Keep the Goal Larger Than One Metric | Recap correctly keeps useful work and multiple resource measures in view. |
| M4S21 | Check Efficiency and Operational Concepts | All three keys and feedback are defensible. |
| M4S22 | Match Trends to Their Meaning | Matching associations need clearer taught scope and category wording. |
| M4S23 | Continue with Intro to OCP | Retain Intro to OCP; add AICC as an optional separate deep dive. |
| M4S24 | Apply the System View | Completion is appropriate; keep glossary-free. |

## Primary-source register

All access dates are 26 October 2026. Dates below are publication dates only when established; otherwise the page is treated as a live, undated source. Evidence was not adopted solely from a search snippet. Some source pages are commercial primary descriptions; their marketing promises are not treated as universal technical rules.

- **AICC — [OCP AI Computing Continuum project](https://www.opencompute.org/projects/aicc/)**. Undated live project; accessed 2026-10-26. Full project text read. The older /index.php/community/aicc URL redirects here.
- **AICC_COURSE — [AI Computing Continuum: Extending AI Beyond the Hyperscale Data Center](https://academy.opencompute.org/learn/courses/58/ai-computing-continuum-aicc-extending-ai-beyond-the-hyperscale-data-center)**. Existing course; accessed 2026-10-26. Public URL returned a JavaScript loading shell. Course title, scope and introductory scripts verified in the supplied local AICC course; live enrollment/playback not verified.
- **AI_FACTORY — [NVIDIA AI factory glossary](https://www.nvidia.com/en-us/glossary/ai-factory/)**. Undated live glossary; accessed 2026-10-26. Full definition and lifecycle sections read. A vendor usage of the term, not a universal facility classification.
- **EU_FACTORY — [European Commission AI Factories](https://digital-strategy.ec.europa.eu/en/policies/ai-factories)**. Undated live policy page; accessed 2026-10-26. Opening definition read; demonstrates broader ecosystem/program usage. No counts or investment forecasts are proposed for this course.
- **OCP_VISION — [Realizing the OCP Open Data Center Ecosystem Vision](https://www.opencompute.org/news/realizing-the-ocp-open-data-center-ecosystem-vision/)**. Published 2026-10-12; accessed 2026-10-26. Full article read. Publication date verified in page metadata and visible date.
- **OCP_LVDC — [OCP: Powering the Next Era of AI](https://www.opencompute.org/news/powering-the-next-era-of-ai-how-google-microsoft-and-nvidia-are-standardizing-and-accelerating-the-industry-transition-to-lvdc/)**. Publication date not established; accessed 2026-10-26. Opened article body supports developing 800 VDC community interfaces; do not infer universal deployment.
- **IEA — [IEA, Key Questions on Energy and AI, executive summary](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary)**. Report published 2026-04-16; accessed 2026-10-26. Full executive summary read; 485 TWh in 2025 and 950 TWh in 2030 verified. Date from report landing page.
- **UPTIME — [Uptime Institute Tier Classification explanation](https://journal.uptimeinstitute.com/explaining-uptime-institutes-tier-classification-system/)**. April 2021 update; accessed 2026-10-26. Web reader returned 403; full article retrieved through ordinary HTTP and parsed. Capability definitions and removal of expected-downtime predictions read.
- **NIST_CLOUD — [NIST SP 800-145, The NIST Definition of Cloud Computing](https://csrc.nist.gov/pubs/sp/800/145/final)**. Published September 2011; accessed 2026-10-26. Official publication page and full abstract read.
- **NIST_VM — [NIST hypervisor glossary](https://csrc.nist.gov/glossary/term/hypervisor)**. Undated glossary linked to NIST publications; accessed 2026-10-26. Definitions read. Shared-host failure consequences are an architectural inference, not a quoted availability guarantee.
- **NIST_CONTAINER — [NIST SP 800-190, Application Container Security Guide](https://csrc.nist.gov/pubs/sp/800/190/final)**. Published September 2017; accessed 2026-10-26. Official publication page/abstract read; not claimed to be a full line-by-line review of the publication.
- **CNCF — [CNCF container glossary](https://glossary.cncf.io/container/)**. Undated live glossary; accessed 2026-10-26. Technical definition read; used to distinguish software containers from shipping containers.
- **DCIM — [Vertiv DCIM and IT management](https://www.vertiv.com/en-us/learn-about/dcim/)**. Undated live vendor source; accessed 2026-10-26. Body definitions and linked-topic descriptions read; establishes overlap of IT physical infrastructure and facilities.
- **ISO27000 — [ISO/IEC 27000:2026 overview](https://www.iso.org/standard/27000)**. Edition 6, July 2026; accessed 2026-10-26. Official definition and FAQ read; the 2026 edition is an overview, not the older overview-and-vocabulary title.
- **ISO27001 — [ISO/IEC 27001:2022 requirements](https://www.iso.org/standard/27001)**. Edition 3, October 2022; accessed 2026-10-26. Official standard summary read; one amendment noted on the page. No certification or legal advice is inferred.
- **SYNERGY24 — [Synergy: hyperscale and colocation capacity trends](https://www.srgresearch.com/articles/hyperscale-operators-and-colocation-continue-to-drive-huge-changes-in-data-center-capacity-trends)**. Published 2024-08-07; accessed 2026-10-26. Full research release read: 41% worldwide capacity then; over 60% forecast for 2029. Capacity is not workload share.
- **SYNERGY25 — [Synergy: capacity shifting to hyperscale operators](https://www.srgresearch.com/articles/the-worlds-total-data-center-capacity-is-shifting-rapidly-to-hyperscale-operators)**. Published 2025-06-24; accessed 2026-10-26. Full research release read: 44% capacity at Q1 2025, 61% forecast for 2030. Original recording chart provenance not proven.
- **SNIA — [SNIA, What is an SSD?](https://www.snia.org/education/what-is-ssd)**. Undated live source; accessed 2026-10-26. Definition, product segmentation and workload-dependent endurance discussion read.
- **CARRIER — [Flexential carrier-neutral data centers](https://www.flexential.com/resources/blog/carrier-neutral-data-center)**. Published 2025-12-23; accessed 2026-10-26. Provider definition and carrier-choice discussion read; promotional resilience claims are not adopted.
- **ASHRAE — [ASHRAE 2023 Applications Handbook, Chapter 20](https://handbook.ashrae.org/Handbooks/A23/SI/A23_Ch20/a23_ch20_si.aspx)**. 2023 chapter incorporating 2021 thermal guidance; accessed 2026-10-26. Relevant definitions, rack dimensions, airflow and environmental tables read. Not a full standards compliance review.
- **DOE — [DOE Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/sites/default/files/2024-07/best-practice-guide-data-center-design.pdf)**. Revised July 2024; accessed 2026-10-26. Relevant text: containment PDF pp. 18–21; WUE/CUE PDF pp. 39–40. PDF text inspected; no PDF page-image QA performed.
- **UPS — [LBNL/EPRI UPS report](https://datacenters.lbl.gov/sites/default/files/UPS_Report_2005.pdf)**. December 2005; accessed 2026-10-26. Section 3.2.3, PDF pp. 30–31, read for N+1 conceptual example only. Old numerical efficiency and uptime predictions are not recommended for reuse.
- **RACK — [Canford rack dimensional data](https://www.canford.co.uk/TechZone/Article/19InchRackDimensions)**. Undated dimensional guidance; accessed 2026-10-26. Dimension table read. The page cites older mechanical standards; manufacturer drawings remain appropriate for actual fit.
- **CISCO — [Cisco switch versus router](https://www.cisco.com/site/us/en/learn/topics/small-business/network-switch-vs-router.html)**. Undated live page; accessed 2026-10-26. Functional descriptions read. Data-center switches may perform routing too; no universal box-per-function rule proposed.
- **PUE — [The Green Grid PUE definition](https://www.thegreengrid.org/node/372)**. Undated glossary; accessed 2026-10-26. Definition read; worked arithmetic independently checked.
- **BRAZOS — [Google: Brazos liquid-to-air cooling](https://cloud.google.com/blog/topics/systems/brazos-liquid-cooling-system-for-air-cooled-data-centers)**. Published 2026-06-16; accessed 2026-10-26. Full relevant product/design explanation read; used as one retrofit example, not a universal solution.
- **HEAT — [OCP Heat Reuse project](https://www.opencompute.org/projects/cooling-environments/heat-reuse/)**. Undated live project; accessed 2026-10-26. Project overview read; useful-heat demand and complete-system accounting remain contextual requirements.
- **REC — [US EPA renewable energy certificates](https://www.epa.gov/green-power-markets/renewable-energy-certificates-recs)**. Undated live guidance; accessed 2026-10-26. Definitions, attributes and ownership discussion read; US instrument context.
- **PPA — [US EPA physical PPA](https://www.epa.gov/green-power-markets/physical-ppa)**. Undated live guidance; accessed 2026-10-26. Contract, attribute ownership and physical/financial distinction read; no legal conclusion proposed.
- **EIA — [EIA measuring electricity](https://www.eia.gov/energyexplained/electricity/measuring-electricity.php)**. Undated live educational page; accessed 2026-10-26. Power/energy unit explanation checked.

Local cross-course evidence: `<local-user>/Documents/Academy Course Work/AICC/AICC_OCP_Academy_SCORM/course.json` and its Module 1 paired scripts; the other module titles/scope were inspected for continuation context. This is not a fresh content audit of the entire AICC course.

No course, script, recording, generated media, installed skill, repository state or LMS package was changed. No server was started; no audio was played; no ZIP, commit, push or external message was produced. Only audit deliverables were written.
