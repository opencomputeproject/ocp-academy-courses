# FCSA: five narration-synchronized teaching sequences

Production drafts for the five requested target slides. Each uses a distinct visual mechanism and fits its existing teaching purpose. No target-slide change is recommended. Narration is newly drafted for incorporation into the course; no audio, runtime, course metadata or video has been created or changed by this subtask.

**Timing:** these are provisional editorial windows, allocated by spoken-word share with a two-second concluding hold. They are not measured timestamps. Align the quoted narration cues to the final v4 WAVs and replace the timing before production. Approximate duration is 64–74 seconds per sequence; natural delivery governs the final duration.

| Slide | Teaching mechanism | Words | Provisional duration | Poster |
|---|---|---:|---:|---:|
| M1S3 | The moving boundary: reuse carries obligations into a new context | 137 | 64 s | 61 s |
| M2S3 | Move the responsibilities, then compare the architectural roles | 139 | 66 s | 63 s |
| M3S5 | Three image routes, one separate question about progress | 141 | 74 s | 71 s |
| M4S4 | The composition docket: state changes reopen a system decision | 138 | 68 s | 65 s |
| M5S3 | Follow one transaction, then widen the scope of the capacity question | 138 | 68 s | 65 s |

## Shared production treatment

White, flat vector with OCP green for attention and gray for structure. Keep named objects consistent; use purposeful movement and labelled comparison cuts. Avoid ornamental frames, generic box reveals, numerical gauges, decorative packets, checkmarks and pass badges. Use native 1920×1080 or larger, at least 48 px text, actual-font clearance of at least 0.75 em, and inspect the approximately 538×302 course display. Reframe dense relationships rather than shrinking them. Source credits stay outside the media.

One silent deterministic pass follows narration, holds its conclusion, and uses the existing synchronized player behavior. The final poster, caption and transcript carry the learning in reduced-motion mode. Maintain existing caption alignment and spacing. No larger player is assumed.

## Important factual decisions

- **M1:** a reused component does not make a new configuration interoperable automatically. Some FCSA mappings remain to be defined; design and profile requirements add detail. The architectural unit may itself be composite.
- **M2:** Compute 1 can contain or directly connect to memory. The comparison therefore shows required roles, not an exclusive compute-versus-memory split. Memory may be external. One primary coordinates system management/security in a multi-Hub or multi-Compute-2 system.
- **M3:** booting objects are system components and the pictured image is second-stage code. Image transfer, permission and firmware authentication are distinct. Ready/Error go toward the manager; Proceed goes toward the subordinate. No full wire protocol, universal I3C requirement or invented recovery is implied.
- **M4:** CRoT-A evidence does not make the system composition decision. Optional Secondary RoT services are separate roles. The primary is also supported by local evidence. The debug-change example ends in revalidation, without inventing an admission or rejection policy.
- **M5:** adaptation must happen before transfer over the memory traffic interface. RQLFLC/RCCBNN are Level 1; aggregate snoop-filter capacity RTPXLG is Full. Adding a requester expands the review scope; it does not prove capacity exhaustion.

## M1S3 — Reuse needs shared expectations

**Treatment:** The moving boundary: reuse carries obligations into a new context

**Learning payoff:** Learners can explain why partitioning exposes previously internal agreements and why reusing the same component still requires an integration review.

**Visual grammar:** A conceptual monolithic design has three functional glyphs on one substrate-like silhouette; the silhouette represents an architectural design, not a fabricated die. A partition seam separates compute and system resources while their identities persist. Named expectation tags attach to the now-crossing relationships. Later an explicitly labelled New configuration comparison preserves the compute unit and changes its surrounding context.

### Narration

Start with a system design whose processing, memory, and control functions were planned together. Partition that design across chiplets, and some relationships that were internal now cross independently designed boundaries.

A working physical link does not settle what each chiplet provides, what its neighbor expects, or how the complete system behaves.

FCSA makes those expectations explicit through system types, chiplet types, and interface requirements. Protocol and transport mappings add implementation detail where suitable standards exist; some mappings remain to be defined.

Now reuse the same compute chiplet in another configuration. Its identity stays the same, but the surrounding system changes. The integrator must check the applicable roles and interfaces again.

Design and profile requirements add the detail needed for the intended product. Reuse therefore begins with a shared architectural contract; it does not end with a connection.

### Provisional scene plan

The cue column quotes the opening of the exact narration segment; the JSON retains the complete cue.

| Window | Spoken cue | What changes and why | On-screen labels |
|---|---|---|---|
| 0.00–13.58 s | Start with a system design whose processing, memory, and… | One conceptual design separates at a visible partition seam. Existing processing-to-resource relationships stretch across the gap rather than disappearing. Hold the separated state for the final two seconds. | One system; Compute; System resources; Control |
| 13.58–23.08 s | A working physical link does not settle what each… | A short physical link joins the opposing edges. Three unresolved relationship tags remain above it; the link does not fill or approve them. Selectively emphasize the open tags. | Provides?; Expects?; System behavior? |
| 23.08–36.66 s | FCSA makes those expectations explicit through system types, chiplet… | Question tags become architectural topics: Roles and Interfaces. Reframe just the crossing relationship to reveal Protocol and Transport beneath it; keep an explicit Mapping may be undefined annotation. These are dependencies, not a completion pipeline. | Roles; Interfaces; Protocol / transport; Mapping may be undefined |
| 36.66–49.78 s | Now reuse the same compute chiplet in another configuration.… | Labelled cut: New configuration. Slide the same Compute object, including its distinctive notch, to a new resource counterpart. Carry its Roles / Interfaces review tags with it; keep their question marks. No automatic successful connection. | New configuration; Same compute; Review roles + interfaces |
| 49.78–64.00 s | Design and profile requirements add the detail needed for… | Add Product requirements to the open integration-obligation bracket. Hold the same component and changed context with all three topics legible; finish movement early in the closing sentence and hold through the end. | Roles; Interfaces; Product requirements |

**Caption:** Partitioning moves functional relationships across chiplet boundaries. Reuse depends on explicit roles, interfaces and product-specific requirements, not just a working physical link.

**Reduced motion / poster:** Final poster: the same reusable compute unit beside a different integration context, with a single open obligation bracket naming Roles, Interfaces and Product requirements; caption and full transcript provide the explanation.

**Final hold:** keep the settled conclusion through the end; provisional silent tail 62–64 seconds. Representative poster: 61 seconds. Adjust both after final audio alignment.

**Technical limits:**

- Partitioning and configuration change are conceptual teaching views, not manufacturing or hot-swap sequences.
- The type may describe a composite integration unit; do not assert every shape is exactly one physical die.
- Do not turn architectural alignment into universal interchangeability, certification or complete protocol coverage.
- One system means support for one system software image; avoid depicting aggregation of unrelated software systems as this example.

**Source provenance:**

- `f1-p1`: FCSA 1.1.0, 1 Introduction; printed pp. 1, PDF viewer pp. 15. Partitioned systems; single system software image; type/property/interface and implementation distinction.
- `f1-p3`: FCSA 1.1.0, 1.2 Purpose; 1.2.1 Document structure; printed pp. 3, PDF viewer pp. 17. Reuse, agreed classification, interface components and mappings that may be TO BE DEFINED.
- `f1-p4`: FCSA 1.1.0, 1.3 Using this specification; printed pp. 4, PDF viewer pp. 18. System and standalone-chiplet roles; required functionality and interfaces; reuse across configurations.
- `f1-p5`: FCSA 1.1.0, 1.3.3–1.4; printed pp. 5, 6, PDF viewer pp. 19, 20. Multiple type classification; integration-specific configuration; architectural unit may be a composite of dies.
- `f1-p2`: FCSA 1.1.0, 1.1 Layered architecture; printed pp. 2, PDF viewer pp. 16. Foundation, design and profile add requirements; no automatic complete product specification.

## M2S3 — Compute & Hub or Compute Tile?

**Treatment:** Move the responsibilities, then compare the architectural roles

**Learning payoff:** Learners distinguish system types by required functionality and coordination responsibilities, rather than by tile count or drawing arrangement.

**Visual grammar:** Use a small fixed vocabulary of role glyphs: application processing, memory access, I/O, and coordination. Place them inside large named architectural-unit silhouettes. Memory is shown externally with an access line; this avoids falsely placing all DRAM on the chiplet. A clearly labelled Compare architectures transition moves role glyphs to the alternative arrangement; it is not runtime migration or merging physical dies.

### Narration

Compare the responsibilities, not just the arrangement of rectangles. A Compute and Hub system requires at least one Compute One chiplet and at least one Hub chiplet.

Compute One supplies application processing. The Hub provides access to system memory and input-output resources. A primary Hub coordinates system management and security when there are several Hubs.

In a Compute Tile system, at least one Compute Two chiplet combines application processing with direct access to memory and input-output resources. With several Compute Two chiplets, one is primary and coordinates those system functions.

The contrast is not an absolute ban on other capabilities: Compute One can also contain or directly connect to system memory, and implementations can satisfy multiple types.

Start with the required roles, then inspect each chiplet's capabilities and required interfaces. A familiar-looking topology alone does not establish the classification.

### Provisional scene plan

The cue column quotes the opening of the exact narration segment; the JSON retains the complete cue.

| Window | Spoken cue | What changes and why | On-screen labels |
|---|---|---|---|
| 0.00–12.43 s | Compare the responsibilities, not just the arrangement of rectangles.… | Large Compute 1 and Hub silhouettes occupy left and right. Their required-role labels are anchored from the start. An open One or more caption applies to each role without spawning a decorative array. | Compute & Hub; Compute 1; Hub; One or more of each |
| 12.43–25.32 s | Compute One supplies application processing. The Hub provides access… | Application-processing glyph docks inside Compute 1; memory-access and I/O glyphs dock in Hub. One resource-access pulse travels from Compute 1 through Hub to the external memory symbol. Mark the depicted Hub Primary; explain coordination with a small anchored label, not an all-powerful control arrow. | Application processing; Memory + I/O access; Primary coordination |
| 25.32–41.44 s | In a Compute Tile system, at least one Compute… | Explicit Compare architectures cut. The same role glyphs regroup within Compute 2, and external memory stays outside. A second Compute 2 enters as the narration says several; only the first gets the Primary label. Do not animate memory-copy traffic or infer a performance gain. | Compute Tile; Compute 2; Primary; Application processing; Memory + I/O access |
| 41.44–53.87 s | The contrast is not an absolute ban on other… | Comparison cut back to Compute 1. Add a dashed optional memory-access branch labelled May also have memory; keep the required Compute 1 and Hub roles visible. A Multi-type possible note refers to the unit, with no certification seal. | May also have memory; Multiple types possible |
| 53.87–66.00 s | Start with the required roles, then inspect each chiplet's… | Settle into two uncluttered comparison rows. Retain the different required roles and one short summary: Check functions + interfaces. Hold through the end; no shrinking detailed topology into a miniature dashboard. | Compute 1 + Hub; Compute 2; Check functions + interfaces |

**Caption:** Compute & Hub requires Compute 1 and Hub roles; Compute Tile requires Compute 2. The important comparison is where application processing, resource access and primary coordination reside.

**Reduced motion / poster:** Final two-row comparison: Compute 1 — application processing; Hub — resource access and primary coordination; versus Compute 2 — application processing and resource access, with one primary coordinating the system. Include the caption and transcript; no topology interpretation depends on motion.

**Final hold:** keep the settled conclusion through the end; provisional silent tail 64–66 seconds. Representative poster: 63 seconds. Adjust both after final audio alignment.

**Technical limits:**

- Compute 1 is not prohibited from having memory. Never make a no-memory icon the defining distinction.
- Hub has no Application PEs as a Hub type, but a unit may satisfy additional types. Do not forbid composite or multi-type implementations.
- The visual is a responsibility comparison, not an exhaustive legal topology or a recipe for runtime role migration.
- Primary coordination means the system management/security functions described by the source; it does not erase local enforcement or establish trust.
- Memory may be integrated or directly connected. The external-memory drawing is an illustrative choice.

**Source provenance:**

- `f2-p18-20`: FCSA 1.1.0, 3.1 Compute and Hub System; printed pp. 18, 20, PDF viewer pp. 32, 34. Compute 1 and Hub required roles and system description.
- `f2-p25-26`: FCSA 1.1.0, 4.1 Compute 1; printed pp. 25, 26, PDF viewer pp. 39, 40. Application PEs; optional integrated or directly connected main memory.
- `f2-p30-33`: FCSA 1.1.0, 4.2 Hub; printed pp. 30, 31, 32, 33, PDF viewer pp. 44, 45, 46, 47. Resource access; no Application PEs for Hub type; primary coordinates system management/security.
- `f2-p21-23`: FCSA 1.1.0, 3.2 Compute Tile System; printed pp. 21, 23, PDF viewer pp. 35, 37. Compute 2 required role and system description.
- `f2-p36-40`: FCSA 1.1.0, 4.3 Compute 2; printed pp. 36, 37, 38, 39, 40, PDF viewer pp. 50, 51, 52, 53, 54. Application PEs and direct memory/I/O access; primary coordination.
- `f1-p5`: FCSA 1.1.0, 1.3.3–1.4; printed pp. 5, 6, PDF viewer pp. 19, 20. Multiple type classification; integration-specific configuration; architectural unit may be a composite of dies.
- `f1-p4`: FCSA 1.1.0, 1.3 Using this specification; printed pp. 4, PDF viewer pp. 18. System and standalone-chiplet roles; required functionality and interfaces; reuse across configurations.

## M3S5 — Three boot models, coordinated progress

**Treatment:** Three image routes, one separate question about progress

**Learning payoff:** Learners identify who fetches each second-stage image and distinguish image location or delivery from execution control and authentication.

**Visual grammar:** Keep Manager component left and Subordinate component right in every comparison. NVM is a storage glyph above, never confused with component memory. A folded Image token takes the delivery route; control uses separate thin directional tracks below. Every model change is a named comparison cut that visibly resets Image tokens. No clock or numeric duration suggests actual boot performance.

### Narration

Follow the second-stage boot image, then ask who controls progress. In distributed boot, the manager fetches both images from one nonvolatile memory and loads the subordinate's image into that component.

In shared boot, each component fetches its own image from the same memory. Sequence control manages access and controls when images execute.

In independent boot, each component loads from separate memory, potentially in parallel. The components still synchronize; separate storage does not remove coordination.

Ready to proceed and Error travel from subordinate to manager. Proceed travels back. Depending on the model and step, those signals govern loading, execution, or synchronization.

Keep the image path separate from permission to advance. An error reports a loading or verification problem; it is not permission to continue.

These examples concern second-stage boot. The signals alone neither authenticate the firmware nor define a complete boot protocol.

### Provisional scene plan

The cue column quotes the opening of the exact narration segment; the JSON retains the complete cue.

| Window | Spoken cue | What changes and why | On-screen labels |
|---|---|---|---|
| 0.00–15.32 s | Follow the second-stage boot image, then ask who controls… | Label Distributed. One NVM supplies an Own image token to Manager memory and a distinct Subordinate image token via Manager to Subordinate memory. Tokens remain labelled; no execution animation yet. Routes are schematic transfers, not a byte-level protocol. | Distributed; Manager; Subordinate; NVM; Image |
| 15.32–26.55 s | In shared boot, each component fetches its own image… | Labelled Shared comparison resets the two memory slots. Each component draws its own image from the same NVM. Stagger the illustrative fetches to make shared access visible without asserting fixed arbitration or universal ordering. Separate lower sequence-control line remains visible. | Shared; Shared NVM; Sequence control |
| 26.55–37.79 s | In independent boot, each component loads from separate memory,… | Labelled Independent comparison splits the storage object into NVM A and NVM B. Two image transfers occur in parallel. End at a visible Synchronize point; no fastest-model race or timing axis. | Independent; NVM A; NVM B; Synchronize |
| 37.79–51.06 s | Ready to proceed and Error travel from subordinate to… | Reframe to a labelled Sequence-control view of the same component pair. Draw Ready to proceed from Subordinate to Manager and then Proceed back on separate tracks, with each arrow terminating at the correct boundary. State tag reads Load / execute / synchronize by context, not three universal operations in a fixed sequence. | Ready to proceed; Proceed; Context sets the step |
| 51.06–62.81 s | Keep the image path separate from permission to advance.… | Explicit Error case comparison. Image token stops at subordinate memory with Load / verify issue annotation; Error travels only to Manager. No Proceed arrow follows and no repair is invented. Hold the unresolved issue for two seconds. | Error case; Load / verify issue; Error |
| 62.81–74.00 s | These examples concern second-stage boot. The signals alone neither… | Final labelled summary separates Image route from Sequence control. Include Second-stage scope as a concise qualifier. Hold through the end; poster retains the distinction and directions without needing miniature copies of all three diagrams. | Image route; Sequence control; Second-stage scope |

**Caption:** Distributed boot uses the manager to load the subordinate image; shared boot lets each component fetch from shared NVM; independent boot uses separate NVMs. Image loading and sequence-control permission remain distinct.

**Reduced motion / poster:** Use a final two-row summary: Image route — manager / shared NVM / separate NVMs; Sequence control — Ready and Error toward Manager, Proceed toward Subordinate. The caption supplies the full model names and transcript explains the second-stage scope.

**Final hold:** keep the settled conclusion through the end; provisional silent tail 72–74 seconds. Representative poster: 71 seconds. Adjust both after final audio alignment.

**Technical limits:**

- The pictured units are booting system components, not entire chiplets executing arbitrary application images.
- Ready and Error are subordinate-to-manager; Proceed is manager-to-subordinate. Maintain direction in all comparison views.
- Do not claim every model uses an identical full handshake, or that both load permission and execution permission are always separate exchanges.
- Boot Sequence Control and Boot Code Image Load protocols are TO BE DEFINED in section 7.2.1/7.2.2 (Full rules RJFNFZ/RKJVCD). A transport mapping does not complete those protocols.
- Dedicated three-wire return-to-zero transport RZGBTM and I3C image-load transport RCLTBQ are Full rules with described alternatives. They are not universal every-level requirements and are omitted from the picture.
- No firmware trust decision is inferred from delivery, storage location or Ready/Proceed. No invented error recovery.

**Source provenance:**

- `f3-p118-120`: FCSA 1.1.0, 6.1.2, figures 6.2–6.5; printed pp. 118, 119, 120, PDF viewer pp. 132, 133, 134. Three boot models, separate loading/execution when required, control directions, error and second-stage-only scope.
- `f3-p134`: FCSA 1.1.0, 7.2.1–7.2.2; printed pp. 134, PDF viewer pp. 148. Control directions and protocols TO BE DEFINED.
- `f3-p137`: FCSA 1.1.0, 7.3.1–7.3.2; printed pp. 137, PDF viewer pp. 151. Dedicated-wire and I3C mappings with stated alternatives; omitted from animation to avoid false universality.

## M4S4 — From local evidence to system trust

**Treatment:** The composition docket: state changes reopen a system decision

**Learning payoff:** Learners separate chiplet-local evidence and enforcement from the System RoT's composition decision, then explain why a security-relevant change requires new appraisal.

**Visual grammar:** Chiplet A and Chiplet B retain identities; A is the primary and contains the System RoT role with locally evidenced support. Each chiplet has a CRoT-A anchor. Evidence documents travel toward one enlarged appraisal area associated with System RoT. Policy/composition is a distinct reference document, not an output of CRoT-A. Optional Secondary RoT appears only as a subordinate service role, never a peer system decision-maker.

### Narration

A chiplet can report its identity and security state without deciding whether the whole system should trust the composition. Its chiplet root of trust for attestation, or C rot A, supplies local evidence and retains local security responsibilities.

The System Root of Trust appraises that evidence against trusted references, the intended composition, and system policy. It checks freshness and the participating chiplets' roles and topology before deciding whether the Security Platform can form or continue.

Optional Secondary Chiplet Roots of Trust can provide additional services. They do not make the system-level composition decision.

Now change a participating chiplet's debug state. The earlier evidence describes an earlier state. Revalidation is required, just as after a security-relevant update, reset, or recovery.

Keep evidence, policy, and response connected throughout operation. A valid identity alone is not a maintained system trust decision.

### Provisional scene plan

The cue column quotes the opening of the exact narration segment; the JSON retains the complete cue.

| Window | Spoken cue | What changes and why | On-screen labels |
|---|---|---|---|
| 0.00–18.17 s | A chiplet can report its identity and security state… | Start with two chiplet-local CRoT-A anchors. Chiplet B creates an Evidence paper showing Identity + state and sends it toward the primary's System RoT. A small local-enforcement bracket stays attached to B after the paper leaves. Chiplet A also has local evidence support; never imply its System RoT is exempt. | Chiplet A · primary; Chiplet B; CRoT-A; Identity + state; Local responsibility |
| 18.17–35.87 s | The System Root of Trust appraises that evidence against… | Reframe the System RoT appraisal. Evidence slides next to a separate Composition + policy document. Freshness and Roles + topology appear as two concise review dimensions. Do not draw a closed green perimeter or Accepted badge; the focus is the decision dependency. | System RoT; Evidence; Composition + policy; Freshness; Roles + topology |
| 35.87–44.48 s | Optional Secondary Chiplet Roots of Trust can provide additional… | Brief side view of an Optional secondary service attached to Chiplet B. Its service relationship leads toward System RoT, while the composition-decision label remains at the primary. Keep only the two role names and one Additional services label visible. | Secondary RoT · optional; Additional services; System RoT decides composition |
| 44.48–56.91 s | Now change a participating chiplet's debug state. The earlier… | Return to the same Chiplet B and visibly change its state tag to Debug state changed. Move its existing Evidence sheet to Earlier state; it remains visible rather than vanishing. A fresh evidence sheet enters the same appraisal location. Revalidate replaces the neutral Appraisal status, not a passing state. No automatic disable, admission or recovery action is invented. | Debug state changed; Earlier state; Revalidate |
| 56.91–68.00 s | Keep evidence, policy, and response connected throughout operation. A… | Hold a concise comparison between earlier evidence and changed state, facing the same Composition + policy reference at System RoT. Add Defined response required below the review; the result remains unresolved and product-specific. | State change → revalidation; Composition + policy; Defined response required |

**Caption:** CRoT-A supplies chiplet-local evidence and maintains local responsibilities. The System RoT appraises the composition against policy and must revalidate when security-relevant state changes.

**Reduced motion / poster:** Poster shows the same chiplet's Earlier state evidence beside Changed debug state evidence, both linked to a System RoT appraisal with Composition + policy. Final status is Revalidate; no accepted/security-pass state is implied. Caption and transcript explain optional Secondary RoT services.

**Final hold:** keep the settled conclusion through the end; provisional silent tail 66–68 seconds. Representative poster: 65 seconds. Adjust both after final audio alignment.

**Technical limits:**

- Evidence sheets are conceptual, not specified attestation packet formats, certificates, algorithms or cryptographic guarantees.
- Local enforcement remains with CRoT-A where it cannot safely be delegated. The System RoT is not depicted as bypassing the local trust boundary.
- System and optional Secondary RoT roles must be supported by or evidenced through CRoT-A as described; do not draw asymmetric trust as an evidence exemption for the primary.
- No made-up policy outcome, authorized debug state, pass level, universal security service or product certification.
- SoC-equivalent security is the analysis objective, not a demonstrated property of the illustrated product; product-specific assessment remains necessary.
- Spoken C rot A is a pronunciation aid for CRoT-A; retain CRoT-A in display text and normal written transcript if the course pipeline supports separate speech text.

**Source provenance:**

- `f4-p151-154`: FCSA 1.1.0, 9.1.4.1–9.1.4.5; figure 9.2; printed pp. 151, 152, 153, 154, PDF viewer pp. 165, 166, 167, 168. Asymmetric evidence/policy roles, optional secondary services, freshness/topology appraisal, local responsibility and revalidation triggers.
- `f4-p145-146`: FCSA 1.1.0, 9 Security introduction; printed pp. 145, 146, PDF viewer pp. 159, 160. SoC-equivalent analysis objective and need for product-specific risk assessment.

## M5S3 — Compatible types still need a system check

**Treatment:** Follow one transaction, then widen the scope of the capacity question

**Learning payoff:** Learners recognize two distinct system integration checks: adaptation before crossing an interface and snoop-filter capacity against combined demand.

**Visual grammar:** A persistent transaction token crosses from source fabric toward a target fabric. Its abstract field outline changes at an adaptation seam before the die-to-die boundary; no bit counts or byte fields are drawn. In a separately labelled Scale review, persistent requester identities A/B remain as C joins; demand lines converge on a conceptual snoop filter and the review scope expands to include C. This shows a changed evidence obligation, not a measured capacity failure.

### Narration

Matching chiplet types is only the start of an integration review. Follow a memory transaction between two chiplets whose interconnect properties differ, such as address-field or identifier-field width.

The transaction must be adapted as needed before it crosses the chiplet memory traffic interface. The relevant protocol determines the adaptation; changing the drawing's field shape does not authorize dropping information.

The differences must not prevent transmission or reception, or the required performance of related system functions. Those requirements need evidence for the actual design.

Now widen the view. A snoop filter can serve coherent caches on several chiplets. Adding a requester chiplet changes the combined demand that its capacity must support.

A chiplet-local capacity statement is therefore insufficient. Evaluate the participating system together. FCSA places transaction adaptation in Level One and the combined snoop-filter capacity rule in Full compliance.

### Provisional scene plan

The cue column quotes the opening of the exact narration segment; the JSON retains the complete cue.

| Window | Spoken cue | What changes and why | On-screen labels |
|---|---|---|---|
| 0.00–13.39 s | Matching chiplet types is only the start of an… | Track one labelled Transaction from source fabric toward the interface. Source and target property tags differ in abstract outline only; no invented binary fields, width numbers or overflowing payload. Pause the token before crossing. | Transaction; Source properties; Target properties |
| 13.39–28.22 s | The transaction must be adapted as needed before it… | A labelled Adaptation seam sits inside the sending side, before the physical interface line. The same token retains identity while its outline becomes suitable for the depicted target. It crosses only after the adaptation illustration. Keep Protocol-defined visible; do not shear bits off or imply all mismatches can be repaired. | Adapt before transfer; Protocol-defined; Interface |
| 28.22–39.70 s | The differences must not prevent transmission or reception, or… | Hold the crossed transaction while a Requirement evidence paper is placed beside the path, with Transmission + reception and Required performance. No completion stamp, throughput animation or numeric performance claim. Reserve the Level 1 label for its closing spoken cue. | Transmission + reception; Required performance; Evidence needed |
| 39.70–52.61 s | Now widen the view. A snoop filter can serve… | Labelled Scale review cut. Requester A and Requester B have demand lines into a conceptual Snoop filter. Requester C joins. Extend the Combined demand bracket to include C while retaining A/B; old capacity-review paper visibly covers only A/B and becomes Scope changed. Do not draw a fill gauge, equal demand units or an overflow result. | Scale review; Coherent caches; Snoop filter; Combined demand; Scope changed |
| 52.61–68.00 s | A chiplet-local capacity statement is therefore insufficient. Evaluate the… | Replace the review paper with a larger-scope Capacity evidence needed document, not a successful result. Finish with two clear rows: Adapt before interface — Level 1; Combined demand — Full. Reveal each level only on its spoken cue. Keep these as source requirement labels, never a compliance badge for the pictured design. Finish movement during the closing sentence and hold through the end. | Adapt before interface · Level 1; Combined demand · Full; Capacity evidence needed |

**Caption:** Adapt transactions before they cross the interface when interconnect properties differ. Evaluate snoop-filter capacity against demand from all chiplets, not a component in isolation.

**Reduced motion / poster:** Final poster has two spacious rows: Adapt before interface, with one abstract transaction on either side of an adaptation boundary; and All participating chiplets → combined demand → capacity review. No values, scale or pass result is required to understand either check.

**Final hold:** keep the settled conclusion through the end; provisional silent tail 66–68 seconds. Representative poster: 65 seconds. Adjust both after final audio alignment.

**Technical limits:**

- Adaptation occurs before transfer across the memory traffic interface (RQLFLC); placing the adapter only at the receiving endpoint would teach the wrong order.
- RQLFLC and RCCBNN are Level 1 rules; RTPXLG is Full. Do not describe all three as optional guidance or universally required at Level 0.
- Protocol-dependent adaptation can reduce, zero-extend or return an error in the source examples. The abstract animation asserts no particular valid reduction or universally successful conversion.
- No invented field widths, throughput, latency, cache sizes, capacity percentages, requester demand ratios or scalable-performance guarantees.
- A new requester changes the aggregate review scope. It does not automatically exhaust capacity, and capacity need not be illustrated as a simple sum of equal blocks.
- Snoop-filter eviction mechanics are outside this short treatment; do not silently substitute queue depth, packet buffering or cache capacity for snoop-filter capacity.

**Source provenance:**

- `f5-p143`: FCSA 1.1.0, 8.1.1.1 Transport of memory traffic; printed pp. 143, PDF viewer pp. 157. Adapt before transfer; implementation-defined significant differences; no prevention of required operation/performance.
- `f5-p144`: FCSA 1.1.0, 8.2.1.1 Snoop filters; printed pp. 144, PDF viewer pp. 158. Capacity sufficient for combined system demand; no quantified capacity model supplied.

## Production quality checklist

- Verify every spoken technical claim and visible relationship against the listed source clause; keep source links outside the media.
- Integrate narration drafts into course scripts before generating final v4 audio; preserve approved audio parameters and verify resulting text/hash provenance.
- Replace provisional times with final WAV word/phrase anchors, measure duration, and declare one master duration and representative final poster.
- Sample first, quarter, middle, three-quarter and final frames plus every movement/layout/emphasis boundary and adjacent frames; inspect source at native and displayed size.
- Check every visible label's real font clearance and every arrow's tip/back attachment. Account for intentional painter-order occlusion only where it teaches a meaningful insertion.
- Run a complete muted pass; verify comparison cuts are labelled, identities persist, no incorrect signal directions or cause/effect reversal, and final state remains held.
- Compare decoded video with lossless frames and reject ringing or block breakup; keep video silent and matched to final WAV within one frame.
- Verify real-course pause/seek/speed/end/replay, enlarged view, review mode and reduced motion; final poster plus caption/transcript must preserve the teaching.

## Evidence handling

Primary claims were checked against `_research/sources/fcsa-pages.json`, extracted from `_research/sources/FCSA-1.1.0.pdf`. The source map identifies exact viewer/printed pages and rule IDs where applicable. `_outline.md`, `_research/source-analysis.md` and `_research/transcript-analysis.md` supplied course context. Summit material is explanatory context only; no caption-derived quotation or proposed Physical AI feature has become a published FCSA requirement. No external retrieval or audible playback was needed.

The JSON is the reusable production handoff: narration segments, full cue text, provisional windows, labels, motion, poster/caption/reduced-motion text, technical limits, source IDs and QA requirements. The source constraints travel with the scene data.
