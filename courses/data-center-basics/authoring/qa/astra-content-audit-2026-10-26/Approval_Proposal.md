# Recommended content update for approval

Status: proposal only. The current course has not been edited for this audit.

## Recommended package

Approve the correctness repairs, two short Module 1 additions and two new teaching videos below. Preserve the four-SCO structure, all ten imported recordings, the existing five teaching videos and the Intro to OCP learning path. Imported-video slides keep their own recording audio and no separate slide narration.

The proposed course has **78 slides**, with approximately **about 94 minutes** (provisional) of estimated learner time. Each M1 addition is about a minute; the AICC video targets 50–65 seconds. The cooling video replaces an existing static figure. Final timing would be measured after the approved scripts and media are built.

All slide IDs below refer to the current 76-slide course. M1S8A and M1S8B are proposal labels.

## Correctness and teaching alignment

1. **M3S15 — make the matching question answerable from the taught example.** M3S6 shows 1U compact compute, a 2U dual-node chassis and a 4U shared multi-node platform. The current quiz instead assumes a 2U general-purpose server and a 4U storage server form one illustrated layout. Recommended repair: refer explicitly to the M3S6 examples and align the three matches and feedback with those examples. Retain the reminder that U describes height allocation, not a universal workload or performance category.
2. **Glossary — repair contextual meaning.** Review every glossary placement, including the software-container definition triggered by a shipping-container analogy at M3S3, virtual-machine terminology at M3S7 and direct-current terminology at M4S8. Move each pill to a genuine first use or remove it if no eligible use remains. Add only useful new terms introduced by the approved AI material.
3. **Imported-recording caveats — make the correction explicit where needed.** Preserve the recordings and their own audio. Strengthen written notes beside M1S5 (edge and carrier neutrality), M2S12 (server/storage generalizations and redundancy), M4S3–4 (unsupported workload percentages, DCIM and ISO terminology), and M4S6 (logical isolation versus physical high availability). Keep editorial corrections distinct from faithful transcripts/captions. Verify any suspected caption-transcription error before attributing it to the speaker.
4. **M4S22 — align trend matching with taught planning principles.** Replace unstated forecast associations with the module’s actual teaching: placement → workload/local constraints; physical deployment → modular approaches when suitable; heat reuse → suitable useful demand; energy sourcing → contracts/attribute ownership; storage planning → capacity, access, protection and service needs. Keep the five subject areas and describe this as a course-wide recap. All nine single-choice keys are defensible and can remain.
5. **M2S5/6 — explain N+1.** Add a concise written example: N is the capacity needed for the intended load; N+1 provides one additional unit of the illustrated capacity. It does not establish independent paths or guaranteed uptime. Keep imported-video slides without narration.
6. **M2S10 — complete the promised containment comparison.** Add a small static comparison and brief explanation of cold-aisle containment (cool supply side) versus hot-aisle containment (warm exhaust side). Retain the existing M2S11 causal animation.

## Two additions after current M1S8

### M1S8A — AI factories align the system around AI workloads

Teach training versus inference in plain language, then explain an AI factory as infrastructure designed around AI workloads. Connect accelerators, memory, storage, fabrics, software and facility support. Treat this as a workload/design lens that can overlap enterprise, colocation and hyperscale arrangements.

Proposed core wording:

> Training adjusts a model using data. Inference uses a trained model to produce an output. An AI factory organizes computing, data movement, software, power and heat removal around those workloads. Its useful output depends on the complete system. The term describes a purpose and design approach; it does not replace the ownership, scale or placement labels on the previous slide.

Use a clear static systems figure. A taxonomy build animation would add little learning value.

Sources: [IEA 2026 energy and AI outlook](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary), [OCP ecosystem vision](https://www.opencompute.org/news/realizing-the-ocp-open-data-center-ecosystem-vision/).

### M1S8B — place AI across the computing continuum

Connect familiar edge placement to a broader set of regional, enterprise, telco and industrial environments. Explain the choice through response needs, connectivity, data constraints and the site's available resources. Introduce the OCP AICC project and link to its existing Academy course for the deeper architecture.

Proposed core wording:

> Edge describes a relationship to the activity being served. AI inference can run at a device, an industrial or enterprise site, a regional facility or centralized infrastructure. The right placement depends on the service and its constraints. OCP's AI Computing Continuum project develops open, modular infrastructure approaches for this wider hyperscale-adjacent spectrum. The AICC course explores the architecture in more depth.

Include the [AICC project](https://www.opencompute.org/projects/aicc/) and [AICC Academy course](https://academy.opencompute.org/learn/courses/58/ai-computing-continuum-aicc-extending-ai-beyond-the-hyperscale-data-center) at this teaching point. Retain Intro to OCP as the main closing learning path; add AICC as an optional technical continuation.

## Generated videos

| Priority | Placement | Teaching sequence | Approximate duration |
|---|---|---|---|
| Recommended | Existing M2S14 — liquid cooling | Trace heat from component to cold plate, equipment coolant and a heat-transfer interface. Compare a liquid-to-liquid path with a liquid-to-air alternative. Show the continuing facility heat-rejection requirement; keep fluid and heat paths distinct. | 45–60 seconds |
| Recommended | Proposed M1S8B — AICC placement | Follow an illustrative industrial-inference scenario. Change response, connectivity or site-capacity constraints; show which placement remains feasible and what can wait. Avoid implying every request traverses every site or that an in-flight workload migrates instantly. | 50–65 seconds |
| Optional later | Existing M4S11 — PUE counterexample | Reduce IT energy while some overhead remains fixed. Show total energy fall while PUE rises, preserving useful work and service requirements as the decision context. | 30–45 seconds |

Keep the five existing narration-synchronized videos. Build the proposed videos as substantive single-pass explanations with useful final holds and shared narration controls. No new video is needed simply to introduce the AI-factory label.

## Review and implementation boundary

After approval: revise the identified slide text, affected narration, quiz wording/feedback, glossary placements and references; build the two M1 additions and two recommended videos; rebuild and validate the course. Keep the current Eleven v4/Leo pacing workflow, recording controls, four-SCO structure and editable sources. Stop before ZIP or repository publication.

The complete [Astra audit](Astra_Content_Audit.md), [issue list](Findings.json) and [coverage record](Coverage.json) accompany this proposal. The recommended content scope corresponds to findings F01–F13; the two recommended videos are V01/V02. Defer F14’s dedicated networking treatment and F15–F18’s optional refinements to keep this revision introductory and near the duration target. F17’s possible “microservers/microservices” transcription mismatch remains a verification item before changing the transcript. This is a content audit, not a perceptual listening or target-LMS certification.
