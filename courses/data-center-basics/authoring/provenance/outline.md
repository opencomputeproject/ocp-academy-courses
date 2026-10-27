# Data Centers: From Digital Services to Physical Infrastructure

Status: outline approved October 23, 2026. Subsequent user direction: aim closer to 90 minutes while retaining source coverage.

## Agreed brief

- One Slides course with exactly four tracked SCOs, one for each original Rise course.
- Output: `DC_Basics_OCP_Academy_SCORM` in the DC Basics project.
- Introductory audience. Preserve source coverage; target approximately 90 minutes.
- Retain all ten original videos as standalone slides, including their original audio and any source captions. Do not play new narration over the original videos.
- Retain all twelve source knowledge checks, including the three matching exercises. Repair factual errors and misleading question wording in the authored adaptation, retain the untouched recovered originals, and report every substantive correction.
- Give every wrong choice an explanation of the actual misconception. Matching feedback identifies the correct pair and explains the relationship. Retain retry and saved attempts.
- Flatten the instructional content of flashcards, accordions and image markers into readable teaching slides. Their original click mechanics are unnecessary.
- Build a new glossary with authoritative sources and verified first-use placements after scripts are approved.
- Use useful references on the slides they support. No references-only lesson.
- Preserve Matty Bakkeren / Momenthesis's source contribution acknowledgment. Distinguish newly written narration and technical updates from original contributions in the authoring record.
- Use maintained OCP Academy branding, motion introduction, ElevenLabs Leo v2 (`bbGtsRRKUfYO634UxSjz`), stable `eleven_multilingual_v2`, narration rate 1.18, and pronunciation review. The supplied credential is not stored in course files.
- Stop before ZIP creation and any repository push.

## Tracking and build architecture

The source archives are SCORM 2004 3rd Edition. Preserve that version rather than silently downgrade them. The maintained Slides generator currently emits SCORM 1.2 and tracks Course Home in addition to its modules. This project therefore needs a documented, locally maintained extension for Slides with four SCORM 2004 SCOs. This is implementation work required by the supplied sources and the requested four-SCO architecture.

The manifest will contain exactly four launchable tracked module resources. Course Home may remain an untracked local asset for orientation and editorial review, but will not become a fifth syllabus item. Each module's completion, bookmark and quiz state belongs to that module. LMS-mediated navigation must launch the intended SCO rather than follow a plain hyperlink and attribute work to the old SCO. Local review links can navigate ordinary pages in isolated review mode.

Local API and browser checks will verify the adapter, manifest, per-module isolation, resume, retry, completion and navigation requests. Actual target-LMS acceptance remains a later upload test, outside this no-ZIP handoff. Do not claim that SCORM 2004 acceptance proves target-LMS sequencing behavior.

The requested reuse of all source questions governs the quiz layout: preserve source counts and matching types rather than replace them with the default Slides pattern of exactly one radio plus one checkbox question per module.

## Instructional approach and duration

The recovered courses contain 31 lessons, 125 retained resource files, ten original videos and twelve knowledge checks. The recovered video metadata totals 39:17; production QA will measure the actual files before final duration reporting.

The proposal has 76 slides. Ten are original video slides, eight are title/transition slides, four are objectives/overview slides, four are summaries, and six are source knowledge-check slides. The remaining 44 slides teach or apply source concepts and selected current updates. Slides are intentionally concise: around 30–75 seconds of new narration on most teaching slides, shorter orientation/transition narration, and concise spoken introductions to quizzes and original video playback.

Target learner time is approximately 90 minutes: about 39 minutes of original videos, 30 minutes of concise new narration, and 21 minutes for reading, reflection and knowledge checks. Keep the approved 76-slide structure and avoid repeating explanations already supplied by an original video. Final durations will come from measured audio and video; optional external reading is separate. The maintained narration speed remains 1.18.

Each module includes a new short, silent teaching animation using the maintained looping mode. Original explanatory videos are full-length, sound-on media with normal playback controls, not muted looping figure videos. Narration-synchronized full-length generated videos are not proposed at this gate.

## SCO 1 — The Digital World

Purpose: connect familiar digital services to real facilities, distinguish site types from service models, and explain where resilience comes from.

Original video time: 6:02. Proposed slides: 18. Target learner time: about 19 minutes.

| # | Slide title | Teaching purpose and source coverage | Presentation / media |
|---:|---|---|---|
| 1 | The Digital World | Introduce the learner outcome: follow a service to the physical systems behind it. | Title; new narration. |
| 2 | Follow the Service, Facility, Rack and Operations | Four-module course map; explain original videos, narration and checks. | Course overview. |
| 3 | Welcome to Data Center 101 | Preserve the original course introduction and overview. | Original video `1-1-welcome-course-overview-1080p.mp4`, 2:02. |
| 4 | One Request Depends on Many Systems | User request → network → compute/storage → response. Explain that software services depend on physical power and heat removal. | New short silent animation; distinct from a geography map. |
| 5 | What Is a Data Center? | Preserve the source explanation of the facility's role. | Original video `1-2-what-is-a-data-center-1080p.mp4`, 4:00. |
| 6 | Capacity Is More Than Floor Space | Compute, storage, networking, power and cooling; distinguish kW/MW power from kWh energy and physical area. | Simple system diagram. |
| 7 | Tiers Describe Infrastructure Capabilities | Basic capacity, redundant components, concurrent maintainability and fault tolerance. Remove the source graphic's unsupported uptime guarantees. | New Tier comparison; Uptime reference pill. |
| 8 | Enterprise, Colocation, Hyperscale and Edge | Preserve all four source definitions. Explain that the labels describe different dimensions and can overlap. | Four related cards. |
| 9 | Match the Facility to Its Role | Preserve M1-KC1: all four source type/definition pairs; improve concept feedback. | Source matching knowledge check with concise narration. |
| 10 | Location Balances Access, Energy and Risk | Connectivity, proximity, energy and water availability, resilience, costs and data requirements. Avoid equating country location with legal compliance. | Decision diagram; source location lesson. |
| 11 | Regional Hubs Serve Different Needs | Preserve Ashburn, São Paulo, Frankfurt, Johannesburg, Singapore and Sydney as illustrative regional examples, without unsupported superlatives. | Source map reused or cleaned diagram; no live market-ranking claim. |
| 12 | Remote Sites Have a Different Tradeoff | Preserve the Antarctic research example as a remote scientific use case. Distinguish local processing from a commercial hyperscale hub. | Small remote-site system diagram. |
| 13 | Fiber Connects Facilities and Users | Land fiber, submarine cables, inter-facility links, last mile and niche satellite connectivity. Avoid absolute satellite bandwidth/latency claims. | Reuse source cable map as historical illustration, not a current route inventory; preserve embedded credit. |
| 14 | Redundancy Must Survive the Same Failure | Multiple paths, load balancing, backup and continuity. Two links sharing a route can share a failure. | Simple route diagram. |
| 15 | Cloud Is a Service Model Built on Facilities | On-demand shared resources, elasticity and managed services; private/public/hybrid context. Cloud need not span many data centers or be public-internet-only. | Comparison; NIST cloud definition reference. |
| 16 | What Connects the Digital World | Summarize physical dependence, type/scale/location distinctions, resilience and cloud. | Takeaways. |
| 17 | Apply the Digital World Model | Preserve M1-KC2, KC3 and KC4; repair the cloud definition and ambiguous location-type question. | Three original single-answer questions; informative feedback per distractor. |
| 18 | Next: The Systems That Keep IT Running | Connect facility purpose to power, cooling and layout. | Module completion / next-module slide. |

## SCO 2 — Data Center Physical Infrastructure

Purpose: explain the chain of systems that delivers power, removes heat and supports reliable IT operation.

Original video time: 16:09. Proposed slides: 18. Target learner time: about 24 minutes.

| # | Slide title | Teaching purpose and source coverage | Presentation / media |
|---:|---|---|---|
| 1 | Data Center Physical Infrastructure | Introduce the connection between electricity, equipment and heat. | Title. |
| 2 | Trace Power, Heat and Physical Constraints | Source objectives: structure, power delivery, cooling, containment and integration. | Objectives. |
| 3 | A Tour of the Physical Systems | Preserve the original overview. | Original video `2-1-data-center-overview-1080p.mp4`, 4:04. |
| 4 | The Data Hall Depends on Support Systems | Facility, power plant, cooling plant and IT equipment; introduce white/grey space only as useful terminology. | Reuse source facility diagram if legibility passes. |
| 5 | How Power Reaches the Data Hall | Preserve the original power explanation. | Original video `2-2-power-infrastructure-1080p.mp4`, 3:22. |
| 6 | Follow the Power Path | Utility/distribution, backup systems, UPS, rack distribution and equipment supplies. Distinguish backup duration from uninterrupted transfer. | New short silent animation; conceptual architecture, not a wiring procedure. |
| 7 | Conversion and Expansion Happen Inside the Server | Conventional AC-input power supply → usable DC; PCIe cards add interfaces and accelerators. Teach both concepts before the source questions. Note that DC-fed rack architectures also exist. | Two-part diagram with AC/DC and PCIe terminology. |
| 8 | How Cooling Removes the Heat | Preserve the original cooling explanation. | Original video `2-3-cooling-systems-1080p.mp4`, 4:53. |
| 9 | A Cooling System Moves Heat Out | Server inlet/exhaust, room cooling and heat rejection; CRAC and CRAH are distinct technologies. | Conceptual heat-flow diagram. |
| 10 | Keep Supply Air Apart from Exhaust | Preserve hot aisle, cold aisle, containment panels, sensors and room cooling roles. Raised floor is an example, not a requirement. | Replace the dark, small-text source containment graphic with a readable diagram. |
| 11 | Containment Reduces Air Mixing | Show recirculation and its reduction with separation, using monotonic, easy-to-follow motion. | Second short silent animation if it materially improves the concept. |
| 12 | Effective Infrastructure Works as a System | Preserve the original infrastructure video. | Original video `data-center-101-2-4-effective-infrastructure-1080p.mp4`, 3:50. |
| 13 | An Empty Rack Is Not Spare Capacity | Space, electrical capacity, thermal capacity, connectivity and service access jointly limit deployment. | Capacity-constraint cards. |
| 14 | Liquid Cooling Adds a Heat-Transfer Path | Cold plates, coolant circulation, CDU and facility heat removal; air and liquid can coexist. Brief 2026 Brazos example, clearly limited to its liquid-to-air retrofit use case. | New loop diagram; OCP Cooling Environments and Google primary-source pills. |
| 15 | Open Interfaces Help Facility and IT Teams Coordinate | Introductory reason for common power and thermal interfaces. Mention emerging 800 VDC work as a specific development, not a universal installed standard. | Concise interface figure; relevant 2026 OCP blog pill. |
| 16 | Reliable Operation Requires the Whole Chain | Summarize power delivery, heat removal, separation and integrated constraints. | Takeaways. |
| 17 | Check the Function of Each Component | Preserve M2-KC1 and KC2, scoped to a conventional AC-input server and correcting `PCle` to `PCIe`. | Two original single-answer questions; choice-specific explanations. |
| 18 | Next: Put the Systems Inside the Rack | Connect supporting infrastructure to equipment organization and rack constraints. | Module completion / next-module slide. |

## SCO 3 — Inside the Rack

Purpose: use rack dimensions, equipment roles and operational constraints to interpret a practical layout.

Original video time: 4:22. Proposed slides: 16. Target learner time: about 16 minutes.

| # | Slide title | Teaching purpose and source coverage | Presentation / media |
|---:|---|---|---|
| 1 | Inside the Rack | Orient learners to the modular equipment frame. | Title. |
| 2 | Read a Rack Layout and Its Constraints | Source standards, physical arrangement and security objectives. | Objectives. |
| 3 | Rack Equipment Overview | Preserve the original equipment video. | Original video `data-center-101-3-1-rack-equipment-overview-1080p.mp4`, 4:22. |
| 4 | What the 19-Inch Dimension Measures | Equipment front-panel width, not the rail-hole center spacing, cabinet width, depth or height. | Corrected dimension diagram with primary source. |
| 5 | Rack Units Measure Vertical Allocation | 1U pitch = 1.75 inches / 44.45 mm; 2U and 4U scale vertically. U does not determine the workload or performance. | Dimension diagram. |
| 6 | Compute Comes in Many Chassis | Preserve compact compute, dual-node, multi-node, general-purpose and GPU-optimized examples. | Related equipment cards; sizes explicitly examples. |
| 7 | Storage Designs Balance Access and Capacity | Preserve NVMe enclosure, high-capacity storage and high-bay 4U+ enclosure examples. Define capacity/performance tradeoffs without universal cost claims. | Equipment comparison. |
| 8 | Shared Chassis and Utility Nodes Have Distinct Roles | Preserve blade-system and utility/management-node content. | Related cards; no universal redundancy claim. |
| 9 | Equipment Choice Consumes Several Budgets | Rack height, power, heat removal and network capacity change as equipment is added. | New short silent animation, illustrative values only. |
| 10 | Cables and Airflow Need Their Own Space | Preserve service access, front/rear orientation and the importance of orderly layout. | Clear rack front/rear diagram. |
| 11 | Physical Security Supports Serviceability | Authorized access, tenant separation and asset identification. Avoid treating a locked rack as complete security. | Rack/security layout. |
| 12 | Open Rack Is a Different Mechanical System | Brief 21-inch equipment-space / Open Unit orientation and shared power context. Reserve ORv3 architecture details for Intro to OCP. | Simple comparison; OCP Rack & Power source pill. |
| 13 | Interpret the Layout Before Adding Hardware | Mini application: identify the constraint that prevents a deployment despite free U space. | Short narrated case; not a replacement for the source checks. |
| 14 | A Rack Is More Than a Stack of Servers | Summarize dimensions, workload diversity and deployment constraints. | Takeaways. |
| 15 | Verify Dimensions and Example Form Factors | Preserve M3-KC1 with corrected width answer and M3-KC2 matching, explicitly limited to the illustrated example layout. | One single-answer and one source matching interaction; corrective per-pair feedback. |
| 16 | Next: Operate and Improve the Whole System | Connect physical arrangements to ownership, utilization and resource efficiency. | Module completion / next-module slide. |

## SCO 4 — Management and Trends

Purpose: connect management responsibilities, resource metrics and emerging infrastructure choices, then prepare learners for Intro to OCP.

Original video time: 12:44. Proposed slides: 24. Target learner time: about 31 minutes.

| # | Slide title | Teaching purpose and source coverage | Presentation / media |
|---:|---|---|---|
| 1 | Management and Trends | Set the goal: operate services responsibly as requirements change. | Title. |
| 2 | Connect Ownership, Metrics and Technology Choices | Source objectives, including the promised practical scenario. | Objectives. |
| 3 | The Changing Data Center Landscape | Preserve the original trends overview. | Original video `4-1-data-center-trends-overview-1080p.mp4`, 3:33. |
| 4 | Who Owns and Manages What? | Preserve the original ownership/management explanation. | Original video `4-2-who-owns-and-manages-what-1080p.mp4`, 4:40. |
| 5 | Responsibility Follows the Service Contract | Enterprise, colocation and cloud responsibilities; distinguish facility operation, hardware operation, service operation and customer obligations. | Responsibility matrix; qualified by contract/service model. |
| 6 | Physical Versus Virtual Infrastructure | Preserve the original physical/virtual explanation. | Original video `data-center-101-4-3-physical-vs-virtual-infrastructure-1080p.mp4`, 4:31. |
| 7 | Virtual Services Still Consume Physical Resources | Physical equipment → virtualization → workloads, with energy and heat traced back to hardware. | New short silent animation. |
| 8 | Monitor Before You Optimize | DCIM, inventory, telemetry, trends and alarms; distinguish observation from safe operational decisions. | Measurement-to-action diagram; optional timely OSPA example confined to switch platform management. |
| 9 | PUE Measures Facility Overhead | Same-boundary energy ratio, worked example and why PUE does not measure useful compute or total sustainability. | Formula and simple example; Green Grid pill. |
| 10 | Water and Carbon Need Explicit Boundaries | Site WUE versus source-inclusive water accounting; CUE emissions boundary and energy denominator. No timeless company benchmark or automatic zero-emissions claim. | Metric comparison; authoritative sources. |
| 11 | Remove Waste Without Misreading the Ratio | Zombie servers, utilization, virtualization and consolidation. Energy savings can coexist with worse PUE when fixed overhead remains. | Simple before/after example. |
| 12 | Improve Cooling and Power Together | Preserve source flashcard advice on containment, economizers, efficient conversion, UPS efficiency, monitoring and workload consolidation, with context. | Related action cards. |
| 13 | Heat Reuse Needs a Useful Heat Customer | Preserve residual-heat reuse, explain temperature, distance, demand and infrastructure constraints. Distinguish reused heat from lower facility energy/PUE. | Heat pathway diagram; OCP Heat Reuse pill. |
| 14 | Clean Energy Claims Need More Than a Contract Label | Preserve REC/PPA themes; distinguish certificates, procurement, location and timing. Avoid claiming a PPA guarantees round-the-clock physical clean supply. | Plain comparison. |
| 15 | Demand Growth Raises Local Infrastructure Questions | IEA April 2026 update: roughly 485 TWh in 2025 and a projection near 950 TWh in 2030. Clearly label estimates/projections and keep the focus on planning constraints. | One concise chart; IEA source pill. |
| 16 | Plan for Mixed Workloads and Cooling | Large centralized facilities, regional/edge use cases, modular deployment and mixed air/liquid cooling. Offshore concepts are experimental examples, not the default trajectory. | Replace speculative source trend chart. |
| 17 | Co-Design from Chip to Grid | Recent OCP examples connect accelerators, power, heat removal and management. Keep emerging 800 VDC and extreme rack densities labeled as specific developing architectures. | OCP October 2026 ecosystem blog pill; conceptual diagram. |
| 18 | Emerging Technologies Need a Readiness Test | Brief source quantum/photonic themes as emerging possibilities. No claim that quantum storage is imminent or that peer-to-peer devices eliminate facilities. | Evidence/readiness questions. |
| 19 | Choose an Improvement That Fits the Site | New scenario fulfills the source objective: a mixed-use facility must serve a denser workload within power, cooling, water and responsibility constraints. | Narrated case with learner reflection and explained decision criteria. |
| 20 | Keep the Goal Larger Than One Metric | Summarize ownership, physical dependencies, useful work, metrics and evidence-based planning. | Takeaways. |
| 21 | Check Efficiency and Operational Concepts | Preserve M4-KC1, KC2 and KC3; repair recycled heat-reuse feedback and qualify the heat-reuse claim. | Three original single-answer questions; choice-specific explanations. |
| 22 | Match Trends to Their Meaning | Preserve M4-KC4's five categories and matching interaction. Repair the location pair to reflect distributed/site-appropriate deployment; report original speculative wording. | Source matching check with per-pair explanations. |
| 23 | Continue with Intro to OCP | Explicit bridge to the repository's four courses: origins; community/governance; Open Rack/cooling; adoption journey. Keep deep details in those courses. | Four-step learning path with useful links when verified. |
| 24 | Apply the System View | Thank the learner, close this four-SCO course and encourage applying the concepts. | Course completion; continuing resources centered; no glossary pills. |

## Glossary plan

Create a course-wide inventory with concise definitions and authoritative references, then place each term at its first eligible substantive use in each module. Candidate terms include latency, colocation, hyperscale, edge computing, redundancy, concurrent maintainability, fault tolerance, power versus energy, UPS, PDU, AC, DC, CRAC, CRAH, containment, cold plate, CDU, CPU, GPU, RAM, PCIe, NVMe, rack unit, Open Unit, virtualization, hypervisor, DCIM, PUE, WUE, CUE, REC and PPA.

OCP and AI/ML are baseline audience vocabulary and will not receive glossary pills. Title, overview/objectives, quizzes, module boundaries and completion slides remain glossary-free. Candidate placements are not treated as evidence until the approved narration, visible text and reviewed media actually use each term.

## Figure plan at outline stage

- Reuse original videos verbatim. Keep source hashes, descriptive titles and any source caption tracks.
- Reuse useful source facility/rack/map artwork only when accurate and legible. Retain embedded attribution on the cable map and label it as illustrative.
- Replace the Tier graphic because it teaches fixed uptime/downtime guarantees.
- Replace the small, dark containment figure with a clear code-authored diagram.
- Replace the speculative today/tomorrow/future chart because it presents uncertain claims as expected outcomes and contains internally inconsistent storage labels.
- Create simple SVG diagrams and short HTML/CSS-derived silent animations in the Academy palette. No paid AI image generation is needed for this proposal.
- Plan motion in M1/4 (service request), M2/6 (power continuity), M3/9 (rack constraints) and M4/7 (virtual-to-physical dependence). M2/11 may add a distinct airflow animation.
- Validate arrows, label clearance, source timelines, posters and encoded visual fidelity before accepting new motion assets.

## Editorial issues for approval and final delivery

See `_knowledge_check_audit.md` for the twelve-question inventory, errors and intended adaptations, and `_research_notes.md` for source support and cautions. The untouched recovered source remains in `_recovered/` outside the final package folder.

Gate 1 has approved the structure. AcademyWizard next requires module script approval before paid narration and figure-plan approval before AI images. After those gates, complete the build, media/audio/layout/tracking QA and local review pages, stopping before ZIP creation and repository push as requested.
