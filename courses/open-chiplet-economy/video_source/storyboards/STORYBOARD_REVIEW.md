# Three narration-synchronized storyboard proposals

**Open Chiplet Economy: Business and Technology of Chiplet-based Systems**

**Status: proposals for editorial review only.** No replacement video, narration, course page, player, shared skill or SCORM package is produced or changed. All three recommended treatments fit the approved scripts unchanged.

The proposal folder was absent before this pass. The current sources and sampled frames were inspected, including both contact sheets and full-resolution final frames for the three selected videos. Their existing animation is a shared eight-second opacity reveal. M4 introduces protocol first while its narration introduces the physical layer first. These proposals replace that instructional pattern with a different visual cause or comparison for each slide.

| Slide | Recommended treatment | Measured final WAV | Frames / sample rate |
|---|---|---:|---:|
| M4S3 | The same request, three different agreements | 39.522857143 s | 871479 / 22050 Hz |
| M5S3 | The connection that did not exist yet | 41.659637188 s | 918595 / 22050 Hz |
| M9S6 | Move the question; keep the model | 42.679546485 s | 941084 / 22050 Hz |

## Shared direction and review conditions

Use the existing approximately 538×302 px media surface. The visual must work there before it works in the enlarged view. Use a few large, persistent silhouettes, selective reframing and short labels; do not put the complete explanation into a miniature dashboard. The recommended treatments require no media layout change. If production finds that a larger layout is necessary, flag that choice for review rather than silently enabling media focus.

Flat vector on white; OCP green is emphasis, not a pass result. Keep text dark gray and outlines neutral. Aim for 48–52 px source labels on a 1920 px canvas, roughly 13–14 px at the current media width. Keep each scene to one focal relationship and normally three to six short labels. The labels listed below are a scene inventory, not permission to show every past label simultaneously. Replace contextual text with recognizable silhouettes during close-ups.

The proposed playback is silent, narration-synchronized and single-pass, with a concluding hold. This is a proposal for opt-in approval, not a change to current player settings. Scene boundaries follow final-v4 machine word timings; WAV duration is measured from sample counts. All timing is pedagogical, not a physical timing claim. No audible playback was performed.

No course branding, repeated slide titles, source-credit footer, edition/year badges, invented measurements, decorative gauges or arbitrary checkmarks belong inside the media. Source provenance remains in this review document. Preserve the aligned caption and the 16 px media-to-caption / 24 px caption-to-aids gaps.

## M4S3 — The same request, three different agreements

**Learning payoff.** The learner can explain how a pair can carry an electrical signal and still fail to share the meaning of a transaction. The three layers answer different compatibility questions; they are not three independent green lights that prove interoperability.

**Visual treatment.** A paired specimen under three lenses. Two persistent chiplet silhouettes sit left and right of one physical connection. The camera changes what the viewer can inspect: electrical connection, organization of transfer, then shared meaning. A single abstract read-request badge keeps its identity. A visibly separate illustrative comparison demonstrates the limitation of electrical success.

**Why motion helps.** The key motion is changing the level of inspection and preserving the same request through a representation change. The mismatch is a controlled comparison in which the electrical connection remains visible while shared meaning is missing.

**Spatial grammar and object continuity**

- Left is sender; right is receiver. These identities never swap. Bottom is the visible physical connection; higher annotations are conceptual views, not die floorplan blocks.
- Use an actual connection line only between physical endpoints. Link and protocol agreement spans are brackets between corresponding annotations, never extra wires or traffic lanes.
- The request badge means one transaction concept. Its outline can acquire a transport surround, but its central read symbol remains unchanged. No fields, bits, opcodes, addresses or wire counts.
- At 29.16 seconds a labelled comparison replaces the successful-meaning illustration. Preserve the earlier pair as a small still only if legible; otherwise use a clean cut headed “Illustrative mismatch”. Never silently mutate a working receiver into a broken one.

**Cue-aligned scene table**

Times are seconds from the beginning of the unchanged WAV, rounded to two decimals for review. Exact cue times and measured endpoints remain in `storyboards.json`; the underlying windows are contiguous and end at the measured audio duration. Quoted cues retain the approved script wording (including its pronunciation spelling where applicable).

| Window | Spoken cue | What moves or changes, and why | Labels and hold |
|---|---|---|---|
| 0.00–4.84 | “The physical layer, often called the P H Y, defines the electrical connection.” | Two facing chiplet edges are already visible. Trace their physical connection once, then send a short highlight across it. This establishes electrical transfer without inventing a waveform or startup sequence. | **Labels:** Sender; Receiver; PHY; Electrical connection. **Hold:** 4.10–4.84: connection holds. |
| 4.84–9.04 | “Pinout, voltages, timing, and the channel must be compatible.” | Keep the connection fixed; compare its endpoints. Change one focal term at each spoken cue: pinout, voltages, timing, channel. Settle on “Must be compatible”; no values or pin patterns. | **Labels:** Pinout; Voltages; Timing; Channel; Must be compatible. **Hold:** 7.94–9.04: “Must be compatible” and the connection remain still. |
| 9.04–12.26 | “The link layer organizes transfer across that connection.” | Reframe to include a plain information ribbon. Brackets close around an abstract transfer unit and cross once. This makes organization visible without prescribing a frame layout. | **Labels:** Link; Organized transfer. **Hold:** 11.40–12.26: organized unit at receiving side. |
| 12.26–16.94 | “Depending on the interface, it can include framing, error protection, and flow control.” | Stop the unit. Keep “Interface-dependent” visible while an underline follows framing, error protection and flow control. No gate, checksum, shield or retry mechanism appears. | **Labels:** Interface-dependent; Framing · error protection; Flow control. **Hold:** 16.02–16.94: qualifier and examples stay still. |
| 16.94–19.80 | “The protocol gives the transferred information meaning.” | Reframe upward to paired interpretation positions while the physical connection remains below. The same abstract information badge acquires a read symbol; it stays still until the request cue. | **Labels:** Protocol; Shared meaning. **Hold:** 18.42–19.80: hold the two corresponding interpretation positions. |
| 19.80–24.56 | “A request to read memory must be interpreted consistently by the sender and receiver.” | The “Read memory” badge crosses to the receiver; its interpretation aligns with the sender by “consistently”. Hold both meanings together. Do not invent returned data or a completed memory operation. | **Labels:** Read memory; Same interpretation. **Hold:** 22.80–24.56: the two matching meanings hold together. |
| 24.56–29.16 | “A protocol adapter can map an on-chip bus onto the die-to-die transport.” | Zoom to an explanatory sender inset. The same read symbol moves from an on-chip bus through an adapter into a transport surround. Its meaning stays unchanged while its representation changes. | **Labels:** On-chip bus; Adapter; D2D transport. **Hold:** 28.14–29.16: unchanged meaning inside the changed surround. |
| 29.16–33.06 | “A successful electrical link is therefore necessary but insufficient.” | Cut to a clearly labelled illustrative mismatch. The electrical connection remains continuous below; above, the arriving read badge meets “Meaning differs”. This is a separate comparison, not an unexplained failure. | **Labels:** Illustrative mismatch; Electrical connection; Meaning differs. **Hold:** 32.06–33.06: hold both facts in the same frame. |
| 33.06–39.52 | “The complete pair must agree on all applicable layers and options, including behavior during initialization and errors.” | Expand a requirement bracket around the whole pair: all applicable layers and options. Keep the mismatch unresolved. Initialization and errors receive timed emphasis, without a fabricated recovery or compliance result. | **Labels:** All applicable layers + options; Initialization · errors. **Hold:** 34.60–39.522857: main comparison geometry holds; only cue emphasis changes. After 38.96 all motion stops. |

Detailed intra-scene cue anchors are in `storyboards.json`.

**Caption.** An electrical connection alone does not establish a valid transaction. The pair must share the applicable transfer rules, meaning, options, and behavior during initialization and errors.

**Poster / final view (39.10 s).** Final mismatch specimen: electrically connected chiplets, visibly differing meaning, and the bracket requiring agreement on all applicable layers and options. “Illustrative mismatch” remains visible.

**Reduced motion.** A static mismatch comparison with three concise lines: “Physical: connection”, “Link: applicable transfer rules”, “Protocol: shared meaning”. Retain the complete-pair requirement and “Initialization · errors”. Use the caption for the longer explanation; no automatic motion.

**Technical limits**

- The three conceptual views are illustrative; they do not prescribe where every standard assigns functions.
- No BoW/UCIe packet layout, bit count, CRC, mandatory flow control, or startup/error-handling algorithm.
- No electrical trace with numeric axes, rates or physical timing. Motion timing is for teaching only.
- The adapter example demonstrates mapping; no performance, universal bus support, or compatibility guarantee is implied.
- The mismatch is a separate comparison case, not an unexplained failure after a successful transaction. No read response is fabricated.

**Narration change required: no.** A concrete protocol mismatch, detailed read-response exchange, CRC/retry example, or initialization state machine would need newly approved explanatory narration and interface-specific evidence. These are excluded.

**Source provenance**

- **M4-script:** `audio/module4/slide_03_a_transaction_crosses_three_agreements.txt` — Both approved paragraphs. Physical / link / protocol distinctions; consistent interpretation of a memory-read request; adapter mapping; electrical compatibility is necessary but insufficient; all applicable options, initialization and errors.
- **M4-layering:** `_research/sources/contribution-05.pdf`; PDF viewer pp. 8, 9, 14 — Section 4 Overview and Table 1; sections 5.1–5.3; section 6.1 Description. Layered relationships and protocol-variant mapping. Table 1 maps different named architectures; it does not justify a universal three-box implementation. The proposal uses three teaching questions, not a normative hardware partition.
- **M4-options:** `_research/sources/contribution-05.pdf`; PDF viewer pp. 10, 13 — Section 5.4 Functional Requirements; FDI and Error Correction passages. The described raw format bypasses UCIe adapter CRC/retry; other formats may enable it. This is evidence against illustrating mandatory universal CRC or retry, not a mechanism to teach in this clip.

## M5S3 — The connection that did not exist yet

**Learning payoff.** The learner can point to the assembled inter-die path and explain why an earlier wafer test could not have established that completed path. They can also explain why later tests add evidence without erasing the value of early screening.

**Visual treatment.** An assembly workbench with two incoming material flows and a growing test boundary. A wafer supplies identifiable dies; a separately drawn substrate arrives from a second lane. Assembly creates a new relationship between the same objects. The closing comparison uses labelled stage snapshots, not a rewind.

**Why motion helps.** Assembly itself changes the question that can be asked. The animation makes a new connection appear only when the physical objects join, then preserves that before/after fact while contrasting stage evidence. No invented defect must disappear later.

**Spatial grammar and object continuity**

- The upper incoming lane contains a circular silicon wafer and die silhouettes. The lower lane contains a long flat package substrate with a distinct outline. They do not morph into each other.
- Die A and die B retain their notches and labels through dicing, assembly and system integration. Two dies are an illustrative simplification, not a required package count.
- A thin scope bracket denotes what is being tested. It is not a test access wire, coverage map, passing result, or probe architecture.
- The inter-die path is absent before assembly. A substrate-only trace may exist beforehand, but the completed path through both die interfaces appears only after assembly.
- Closing snapshots carry “Before assembly”, “After assembly” and “System” labels. They are comparisons of evidence scope, not extra packages moving backwards through a factory.

**Cue-aligned scene table**

Times are seconds from the beginning of the unchanged WAV, rounded to two decimals for review. Exact cue times and measured endpoints remain in `storyboards.json`; the underlying windows are contiguous and end at the measured audio duration. Quoted cues retain the approved script wording (including its pronunciation spelling where applicable).

| Window | Spoken cue | What moves or changes, and why | Labels and hold |
|---|---|---|---|
| 0.00–4.54 | “Wafer-level testing probes the individual dies before the wafer is diced.” | On an intact circular wafer, a simple probe touches identifiable dies A and B, then lifts. The wafer remains intact through this sentence; no special test-access geometry appears. | **Labels:** Silicon wafer; Die A; Die B. **Hold:** 3.74–4.54: probe lifted; intact wafer holds. |
| 4.54–8.02 | “It screens functionality and electrical behavior at that stage.” | A scope bracket encloses one die on the intact wafer. Emphasize functionality and electrical behavior at this stage. Neutral interiors avoid implying complete coverage or known-good certification. | **Labels:** At this stage; Function + electrical behavior. **Hold:** 6.84–8.02: scope stays confined to the die. |
| 8.02–12.20 | “Additional die-level screening can be appropriate before expensive assembly.” | At the new sentence, separate A and B from the wafer along existing grid lines. Move them to a pre-assembly area with a dashed optional screening detour. Preserve die identities. | **Labels:** Individual dies; Screening, as appropriate. **Hold:** 10.68–12.20: separated dies hold above an empty assembly position. |
| 12.20–15.76 | “Package substrate checks can occur in a parallel manufacturing flow;” | Reveal a separate lower lane carrying a rectangular package substrate. A scope bracket inspects it independently while the dies wait above. Its origin never connects to the wafer. | **Labels:** Package substrate; Parallel flow. **Hold:** 14.04–15.76: show both incoming flows together. |
| 15.76–19.36 | “a package substrate is not the same thing as the silicon wafer.” | Hold wafer and substrate as distinct shapes with distinct origin trails. Position the dies above the substrate with a clear gap; no completed die-to-die connection exists yet. | **Labels:** Silicon wafer; Package substrate; Before assembly. **Hold:** 17.14–19.36: side-by-side distinction and separated components hold. |
| 19.36–23.28 | “After assembly, new connections and new failure opportunities exist.” | Keep a labelled pre-assembly snapshot at left. Lower the dies onto the substrate; only on “new connections” draw the complete A-to-B path. Hold the difference without inventing a defect. | **Labels:** Before assembly; After assembly; New path. **Hold:** 21.24–23.28: hold before/after comparison; the new path remains neutral, not passed. |
| 23.28–28.00 | “Package testing must address those inter-die paths and the accessible functions.” | Widen the test-scope bracket around the package. Highlight the assembled path once, then accessible functions. The bracket denotes test scope, not a universal access port or a passing result. | **Labels:** Package testing; Inter-die paths; Accessible functions. **Hold:** 26.38–28.00: hold package scope with both objects identifiable. |
| 28.00–32.82 | “System-level testing then checks integrated behavior under relevant operating conditions.” | Move the same package into a system outline and expand the test scope. A stimulus and a behavior token cross that context once; relevant conditions stay textual, without invented settings or outcomes. | **Labels:** System; Integrated behavior; Relevant conditions. **Hold:** 30.98–32.82: system context holds. |
| 32.82–34.78 | “These stages complement each other.” | Reframe to labelled snapshots of die, assembled path and system. Preserve A/B identity and the separate substrate branch. A baseline joins their evidence scopes; this is a comparison, not a rewind. | **Labels:** Before assembly; After assembly; System; Complementary evidence. **Hold:** 33.98–34.78: comparison composition is fully settled. |
| 34.78–37.66 | “Passing wafer sort does not prove the final package,” | Highlight the early die scope alongside the path that exists only after assembly. A dashed comparison connector stops short of that path. The simultaneous view explains the limit of earlier evidence. | **Labels:** Early screening; New after assembly. **Hold:** 36.30–37.66: simultaneous early-scope/new-path hold. |
| 37.66–41.66 | “and a final system test does not replace economical early defect screening.” | Keep all snapshots fixed and shift emphasis back to early screening while the system remains visible. The common evidence baseline stays; no stage is removed or bypassed. | **Labels:** Early screening still matters; Complementary evidence. **Hold:** 39.84–41.659637: all motion stops; the three scopes remain available for comparison. |

Detailed intra-scene cue anchors are in `storyboards.json`.

**Caption.** Wafer and die screening, package tests, and system tests examine different physical states. The assembled inter-die path needs later testing, while early screening still avoids spending assembly effort on identified defects.

**Poster / final view (40.50 s).** Three labelled physical-state snapshots with persistent die identities: die before assembly, new assembled path, and system context. Keep the separate substrate input visible and the baseline “Complementary evidence”.

**Reduced motion.** Use the final three snapshots. Label the die “Early screening”, the assembled path “New after assembly”, and the system “Integrated behavior”. Show the substrate on a separate incoming branch; use the caption to explain why each scope matters.

**Technical limits**

- The wafer and substrate are distinct objects and independent flows. No wafer-to-substrate morph or connecting arrow.
- No completed inter-die path exists in the pre-assembly snapshot. The substrate may contain conductors before assembly, but the full die-to-die relationship does not.
- No universal test access path, test-vector content, coverage percentage, yield statistic, or defect frequency.
- No green die stamps or known-good guarantees. “Screening” states purpose, not an assertion that all faults were found.
- The recommended sequence deliberately shows a new test obligation rather than a fault that would require an unnarrated repair or alternate-unit transition.
- A two-die package and plain board are illustrative objects, not an implied required construction or test order for every technology.

**Narration change required: no.** A specific open/short fault, repair, yield loss or defect escape story would need additional narration or an explicit comparison reset. A detailed probe/test access sequence would require technology-specific evidence. Neither is recommended for this locked clip.

**Source provenance**

- **M5-script:** `audio/module5/slide_03_test_what_exists_at_each_stage.txt` — Both approved paragraphs. Distinct parallel substrate flow; optional additional die screening; after-assembly paths and accessible functions; system operating conditions; complementary stage evidence.
- **M5-sort:** `_research/sources/contribution-12.pdf`; PDF viewer pp. 37, 38 — Section 9 Test Cost: Wafer Sort Testing; Assembly and Package Testing. Wafer probing precedes dicing and packaging; early screening avoids downstream assembly cost for identified defects; assembly/test details depend on package and flow. No yield or cost percentages are imported.
- **M5-paths:** `_research/sources/contribution-12.pdf`; PDF viewer pp. 18, 39 — Complete die-to-die link testing paragraph; Assembly and Package Testing. The assembled link includes both dies and package connections; package-level access is constrained and design-dependent. The proposal highlights scope without drawing an access architecture.
- **M5-system:** `_research/sources/contribution-12.pdf`; PDF viewer pp. 28, 29, 39 — Section 7 System Level and Functional Tests; Board Level System Testing. Integrated behavior and use-case conditions add questions beyond manufacturing tests. The animation shows no universal conditions, stress levels, or numerical results.

## M9S6 — Move the question; keep the model

**Learning payoff.** The learner can distinguish the information exchanged for shared analysis from the detailed implementation that remains supplier-controlled, and recognize that this boundary still needs policies and evidence for both accuracy and confidentiality.

**Visual treatment.** A question travels to an immovable model across a visibly labelled organizational boundary; only a permitted answer returns. The boundary is ownership, not a magical security wall. A later inspection exposes the policy questions attached to the model, incoming request and outgoing result.

**Why motion helps.** The governing visual invariant is that the model never crosses. Instead of a generic three-step workflow, the learner sees different information take different routes and then inspects where policy obligations attach to that exchange.

**Spatial grammar and object continuity**

- Integrator occupies the left side; Supplier occupies the right side. One supplier is a legibility-focused exemplar, not a mandated federation topology.
- The detailed model is a solid neutral slab with a distinct corner notch; it stays at the same supplier-relative position for the entire sequence, including camera reframing.
- Request and boundary conditions travel left-to-right; permitted results travel right-to-left on a separate clearly labelled return path. Their shapes differ from the model and never detach pieces from it.
- The vertical supplier boundary persists. No padlock, shield, encrypted tunnel or gate animation asserts security. A small “Initial proof of concept” status label is visible from the opening.
- Policy annotations use question wording and neutral outlines. No checkmark, authorization success state or guaranteed confidentiality result appears.

**Cue-aligned scene table**

Times are seconds from the beginning of the unchanged WAV, rounded to two decimals for review. Exact cue times and measured endpoints remain in `storyboards.json`; the underlying windows are contiguous and end at the measured audio duration. Quoted cues retain the approved script wording (including its pronunciation spelling where applicable).

| Window | Spoken cue | What moves or changes, and why | Labels and hold |
|---|---|---|---|
| 0.00–3.24 | “Federated simulation explores a useful idea:” | Show integrator and supplier regions separated by an ownership boundary. Keep the detailed model supplier-side and “Initial proof of concept” visible from the first frame. | **Labels:** Integrator; Supplier; Detailed model; Initial proof of concept. **Hold:** 1.82–3.24: spatial relationship holds. |
| 3.24–9.38 | “bring an agreed simulation request to the supplier's model rather than requiring the supplier to hand over the model.” | Move an agreed-request token to the supplier model. When the narration mentions handing over the model, emphasize its fixed supplier-side anchor. No model export or blocked-export animation occurs. | **Labels:** Agreed request; Model stays with supplier. **Hold:** 6.36–9.38: request beside model; model stays still. |
| 9.38–17.08 | “An integrator could exchange boundary conditions and receive permitted results while the detailed implementation remains under supplier control.” | Boundary conditions travel inward; a distinct permitted-result token returns outward. Keep model and returned result visible together. The result contains no invented values or pieces of the model. | **Labels:** Boundary conditions; Permitted results; Supplier control. **Hold:** 14.90–17.08: result at integrator, detailed model at supplier, both visible. |
| 17.08–19.76 | “That arrangement needs more than a secure container.” | Reframe around the model and two exchange paths. Settle three neutral policy-question groups before the rapid noun list: model/version, incoming requests, and outgoing results. No security seal appears. | **Labels:** Which model / version?; Who may ask / which queries?; Which outputs?. **Hold:** 19.26–19.76: all three questions settled before the rapid noun list. |
| 19.76–27.42 | “Model identity, version, authorization, query limits, and permitted outputs all affect confidentiality and trust in the result.” | Hold policy questions in fixed positions. Underline identity, version, authorization, query limits and outputs on their spoken cues. They remain obligations; no request is arbitrarily approved or denied. | **Labels:** Identity · version; Authorization · query limits; Permitted outputs. **Hold:** 24.28–27.42: all three groups remain legible together; no new motion. |
| 27.42–33.24 | “The Summit proposal describes an initial proof-of-concept direction rather than an approved universal service.” | Pull back to the original ownership view. Emphasize the existing initial-PoC status, then let it rest. Avoid a deployed portal, marketplace approval, certification or universal-service imagery. | **Labels:** Initial proof of concept. **Hold:** 30.20–33.24: full exchange relationship holds. |
| 33.24–38.34 | “Its teaching value is the relationship between shared analysis and protected implementation.” | Use open brackets to distinguish shared analysis from the supplier-controlled model. The organizational boundary stays. These two scopes explain participation without disclosure; neither bracket becomes a security seal. | **Labels:** Shared analysis; Supplier-controlled model. **Hold:** 35.50–38.34: the two scopes hold in one view. |
| 38.34–42.68 | “Accuracy and confidentiality both require explicit policies and evidence.” | Keep the exchange diagram. Add equally weighted accuracy and confidentiality requirements; both require policies and evidence. Settle geometry early and use only final-word emphasis through the ending. | **Labels:** Accuracy: policies + evidence; Confidentiality: policies + evidence. **Hold:** 40.06–42.679546: all geometry holds; final underline is complete by 42.12. |

Detailed intra-scene cue anchors are in `storyboards.json`.

**Caption.** The initial proof-of-concept direction brings agreed requests and boundary conditions to supplier-controlled models and returns permitted results. Accuracy and confidentiality still depend on explicit policies and evidence.

**Poster / final view (42.30 s).** Integrator and supplier separated by the ownership boundary; requests/conditions in and permitted results out; detailed model remains at supplier. Retain initial proof-of-concept status and the two evidence requirements.

**Reduced motion.** Use the final ownership diagram with two labelled arrow directions and the model wholly inside the supplier region. Keep the PoC status and the two concise evidence lines. Put the five policy topics in the caption or adjacent accessible description if they are too small in the poster; never shrink all of them into the image.

**Technical limits**

- This is the Summit proposal’s initial proof-of-concept direction, not a deployed or universally approved simulation service.
- The supplier boundary represents control of the model, not a proven secure execution or network mechanism.
- No normative orchestrator, network protocol, crypto scheme, simulator API, cloud topology or universal federation architecture.
- No model bytes, source, or apparent model fragments cross the boundary. Only conceptual requests, boundary conditions and permitted results move.
- No quantitative outputs or fabricated accuracy/confidentiality evidence. Any result is a labelled abstract token, not a claim of successful analysis.
- The deck’s initial PoC scope is power plus thermal; this recommendation uses domain-neutral results. It does not imply initial support for SI, PI, mechanics or functional simulation.
- Identity/version/authorization/query/output annotations remain requirements and questions; they never become arbitrary approvals.

**Narration change required: no.** A simulator workflow, worked power/thermal example, adversarial model-extraction demonstration, or policy enforcement/denial sequence would require extra approved narration and specific evidence. The locked clip does not explain these actions, so they are excluded.

**Source provenance**

- **M9-script:** `audio/module9/slide_06_from_a_catalog_to_an_evaluable_system.txt` — Both approved paragraphs. An agreed request and boundary conditions can be exchanged for permitted results while detailed implementation remains supplier-controlled; identity/version/authorization/query/output policy; initial PoC status; accuracy and confidentiality require evidence.
- **M9-poc:** `_research/sources/summit-13.pdf`; PDF viewer pp. 15, 16 — A Deliberately Simple Proof of Concept; Five Concrete Deliverables (Plus One). An initial proposal with phased scope and proposed deliverables. Phase 1 names power and thermal only; the recommendation deliberately uses domain-neutral results rather than implying all analyses already exist.
- **M9-boundary:** `_research/sources/summit-13.pdf`; PDF viewer pp. 5, 9 — Separate Ownership From Execution; Multiphysics Co-Simulation. Requests to supplier-controlled models; permitted boundary conditions and results across organizational boundaries. This supports a relationship diagram, not a fixed network topology.
- **M9-policy:** `_research/sources/summit-13.pdf`; PDF viewer pp. 7, 10 — What a Simulation Capability Manifest Describes; IP Protection Is Part of the Standard. Identity/version, validity, permissible inputs/outputs, authorization and query controls. Page 10 explicitly says federation alone does not guarantee confidentiality.
- **M9-transcript:** `_research/transcripts/summit-13.txt` — 02:50–03:35 ownership/execution; 04:22–05:13 model validity and ownership; 10:19–10:58 phased proof of concept; 12:20–12:50 invitation to demonstrate. Corroborates the proposed direction and its exploratory status. Local caption transcript identifies generated=False but states it is not independently audio-verified; deck and locked script are primary for this proposal.

## Quality and approval checklist

The following are review decisions, not claims of completed production validation.

- [ ] Approve the specific teaching relationship and visual metaphor for each slide; all three preserve locked narration.
- [ ] Approve the opt-in synchronized single-pass mode for these selected figures before production; this document records a proposal, not approval.
- [ ] M4: electrical success and differing interpretation coexist; layer/option qualifiers remain visible; no invented wire/packet/error mechanism.
- [ ] M5: substrate has its own origin; new complete path first exists after assembly; no false pass result or disappearing fault.
- [ ] M9: model stays supplier-controlled; only permitted exchange moves; initial PoC status visible from first frame; policy and evidence remain obligations.
- [ ] At current slide display size, each cue has one focal idea and short legible labels; use camera reframing before adding text.
- [ ] Final poster/reduced-motion view and caption preserve the learning payoff and technical limits.

## Implementation checks after approval

- [ ] Preserve hashes of approved scripts/WAVs; do not regenerate narration.
- [ ] Implement one deterministic master timeline equal to measured WAV duration; no internal reset or looping subordinate animations; encode within one frame of that duration.
- [ ] Inspect first/25%/50%/75%/final and both sides of every layout transition, plus a complete muted pass.
- [ ] Check current small media display, mobile, enlarged view, 0.75em text clearance, arrow endpoints, caption gaps, native-resolution linework and encoded fidelity.
- [ ] Verify pause/resume, seek, speed, replay, end hold and reduced motion for opted-in figures through the actual course. Preserve other media behavior.
- [ ] Confirm technical labels match the final visible text inventory and approved sources. Keep source credits outside media.

## Evidence and scope of this pass

- Read the installed AcademyWizard skill and its narration-synchronized-video and figure guidance. Read local approved scripts, final-v4 word timestamps, audit recommendations and preliminary storyboards; the preliminary sketches were context, not a creative constraint.
- Inspected current editable animation sources and sampled media frames. The current sources confirm opacity-only reveal mechanics and an eight-second master duration.
- Verified cited viewer-page positions directly against the PDFs for Universal D2D Transaction and Link Layer, System in Package Testing, and the Federated Chiplet Design and Simulation deck. The testing paper’s contents page has stale page references; this document uses actual PDF viewer pages.
- The M9 deck and local transcript map to the requested recording: [Federated Chiplet Design and Simulation](https://www.youtube.com/watch?v=NM_ZpSOsGYM). No new retrieval was needed. The local transcript is supporting text and was not independently checked by listening.
- The parallel substrate flow is supported directly by the locked M5 narration. The testing paper is used for wafer sort, assembled link testing and system context; its numerical claims and stronger known-good wording are not imported.
- Scene data includes final WAV sample counts, durations, source and script hashes, exact cue anchors, holds, label inventories, constraints, and future acceptance criteria. No rendered storyboard frame or video exists, so visual fit remains a production validation item.

**Deliverables:** `STORYBOARD_REVIEW.md`, `storyboards.json`, and `validation.json` in this folder. The JSON is editorial scene data for later implementation; it is not a patch to `course.json`.
