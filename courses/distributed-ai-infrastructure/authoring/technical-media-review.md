# Distributed AI Infrastructure — technical audit and teaching-animation proposals

Planning review only. No narration audio or videos have been generated. The five proposed animations are new instructional illustrations, not replacements for Ankur Sharma's eight recordings. All animation timing below is editorial timing, to be aligned to approved narration later.

## Review basis and editorial position

Reviewed the five recovered `course.json` files and all eight supplied caption tracks under `Recovered Rise`. Compared the relevant parallelism, network-domain, inference, facility, and management treatments in the adjacent Open Systems for AI and Open Cluster Designs for AI course sources. Checked the Across-model treatment in the local AICC course. Current primary technical references are linked below.

The strongest course is about identifying dependencies, measuring their cost, and operating within explicit boundaries. It should not teach that AI is one universal synchronous machine. The original recordings often use important qualifications that the surrounding Rise prose and quizzes remove. Preserve the recordings and their credit; use short framing and interpretation slides to teach their scope precisely.

Maintain the original recognition of **Ankur Sharma, Senior Principal Architect at Oracle**, as recorded in the source. This is source attribution, not a new claim that his current employment title has been independently verified. Keep his own voice and captions. Do not replace or overdub him with synthesized narration.

Working definition for new teaching: **coordination overhead** is time or resources spent satisfying communication and state dependencies. A delay can reduce throughput without corrupting state. Correctness, performance, availability, and observability are related but different outcomes.

## Technical corrections that must shape the new scripts

| Source location | Risk in recovered material | Proposed qualified teaching |
|---|---|---|
| M1 Why Distributed AI Is Different; both assessments; M2 introductory material | All AI nodes require perfect lockstep; ordinary cloud is independent and stateless. | Compare a declared synchronous training group with independent serving replicas. Both AI and conventional applications can have stateful dependencies. Architecture follows the workload's dependency graph, not its AI label. |
| M1 latency cards and assessment | Any microsecond delay breaks coherence or destroys scale efficiency. | Delay on the critical path can increase step time. Its impact depends on the step duration, communication pattern, overlap, buffering, and required participants. Do not invent a universal microsecond threshold. |
| M2 transactional/AI cards and distributed-state introduction | Distributed training always means the model is too large for one GPU and its weights are fractured across all GPUs. | Separate data parallel replication from model/state sharding. In the worked example, each participant has the same model replica and processes different data. Sharding is a different arrangement with different exchanges. |
| M2 V2, approximately 00:54–01:07 | Compute, then stop, then average parameters is presented as the general training mechanism. | Frame this as a simplified coordination picture. For the new data-parallel example, average gradients, then apply the same optimizer update to replicas. Real implementations may overlap communication with backward computation. [PyTorch DDP design](https://docs.pytorch.org/docs/stable/notes/ddp.html). |
| M2 traditional design-pattern carousel and both assessments | Load balancing, retries, and autoscaling inherently destroy AI state; dynamic membership is impossible. | Ordinary request rerouting cannot substitute for a training participant with required state. Training-aware restart and membership protocols can support elasticity; they have explicit state and restart requirements. Do not conflate service load balancing, packet forwarding, and collective membership. [PyTorch elastic launch](https://docs.pytorch.org/docs/stable/elastic/run.html). |
| M2/M3 straggler prose | A delayed packet instantly forces every GPU in a global cluster to become idle. | A required late contribution can extend a dependent operation in its participating group. Work that does not depend on it may continue. Specify the group and the assumed absence of overlap in a teaching timeline. |
| M3 event-ordering video and quiz | The GPU that finishes first must have its result applied first; reordered arrival inherently violates causality. | Earlier completion alone does not establish a dependency. Enforce the algorithm's operation/step identities and dependencies. Concurrent contributions to the same reduction do not acquire causal priority merely from finishing first. The algorithm must still use matching collective order. [DDP ordering requirement](https://docs.pytorch.org/docs/stable/notes/ddp.html); [Lamport's original paper](https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/). |
| M3 wall-clock tabs and summary | Wall clocks cannot be trusted; clock skew almost always explains GPU inefficiency. | Clock uncertainty can mislead cross-host event reconstruction. It is not proof of a compute or network bottleneck. Correlate trace/message IDs, operation IDs, timestamps with known uncertainty, and performance telemetry. A send causally precedes its receive even when local timestamps appear reversed. |
| M3 introduction | Electrons and photons both traverse fiber backplanes; propagation itself is characterized as random. | Use signals/optical propagation. Separate distance-related propagation delay from variable queuing, contention, processing, and retransmission effects. Avoid an unnecessary physics lesson or absolute simultaneity claim. |
| M4 V1, approximately 00:55–01:14 | A small bandwidth dip instantly destroys preprocessing-to-GPU efficiency. | A sustained supply deficit can drain a buffer and then starve a consumer. The depth of the buffer and rates determine when. This is a data-supply dependency, distinct from a training collective crossing regions. |
| M4 V1, approximately 01:20–01:51; M2 inference card | Every inference deployment must have the same model in all regions simultaneously. | Set a deployment/version policy appropriate to the service. Independent regional replicas can use controlled rollouts; requests may need version pinning or other service-specific consistency. Cross-host model execution has a different dependency pattern. Controlled canary and rolling deployment are concrete counterexamples to universal simultaneous replacement. [SageMaker deployment guardrails](https://docs.aws.amazon.com/sagemaker/latest/dg/deployment-guardrails.html). |
| M4 private connectivity graphics, summary, and quiz | Private links are mandatory, guarantee bandwidth, remove variability, or make dataset transfers universally fast. | Private connectivity can improve control of routing and capacity. Assess actual service terms, path diversity, congestion, failover capacity, and measured workload behavior. Dedicated links still fail and require resilience design. Avoid categorical public/private suitability or transfer-time claims without workload and bandwidth assumptions. [Direct Connect resiliency recommendations](https://aws.amazon.com/directconnect/resiliency-recommendation/). |
| M4 failure-propagation card | Component isolation is physically impossible. | Failure containment is an architectural objective. A dependency may enlarge the affected group, but does not prove that independent jobs, groups, or services must fail. |
| M4 governance tabs | Healthcare data in Europe may never cross a border; ORv3 guarantees provider independence. | Replace the legal universal with an explicit scenario policy: “For this example, the dataset is permitted only in Region A.” Determine applicable requirements outside this introductory course. Hardware interface openness does not alone guarantee software, identity, data-format, operational, or workload portability. |
| M5 physical scaling cards and first assessment | Air cooling is physically impossible at 100 kW; all AI racks need one specified liquid architecture; more sites must become one logical zone over dark fiber. | Use the selected equipment and facility's qualified load, cooling, redundancy, and service envelope. Do not infer a universal technology requirement from rack power alone. Multiple sites may host independent jobs or services rather than one stretched training group. Link deeper facility detail to the adjacent Academy courses. |
| M5 failover text and second assessment | Every failure mandates a worldwide rollback; the original video's “depending on architecture” disappears. | Show one explicit checkpoint/restart policy for one job group. Recovery scope, membership, state restoration, retry limits, and continued operation of independent groups are design choices. Framework elasticity is a concrete supported example, not a guarantee of invisible hot replacement. |
| M5 observability tabs and final guardrails | All monitoring must capture every packet; any 10 ms bottleneck destroys a cycle; absolute predictability is achievable. | Use sufficient measurement resolution to test a stated hypothesis. Combine job progress, collective duration, accelerator, network, and facility evidence as appropriate. Define measurable objectives and bounded response policies; “zero variation” is not an acceptance criterion. |

The adjacent Open Cluster Designs for AI course already teaches that independent single-host serving can omit a scale-out back-end, while cross-host dependencies add that path. Preserve that distinction. The adjacent Open Systems course distinguishes scale-up domains from rack outlines and separates power ratings by component/facility boundary. The AICC course treats Scale-Across, Sync-Across, and Reach-Across as purposes with service objectives, not mandatory network technologies. This course should apply those ideas to coordination behavior rather than repeat their full architecture surveys.

## Original recording framing and qualification map

Times below come from the supplied captions; verify against the audiovisual recordings during production review.

| Recording | Keep the original | Frame or clarify immediately around it |
|---|---|---|
| M1 V1, Introduction, about 2:30 | Ankur's motivation and authorship; “don't translate cleanly” at 00:12–00:17. | Before: “The course focuses on dependency-heavy distributed workloads, especially synchronous training.” After: compare independent inference with a coupled training group. Do not convert “don't translate cleanly” into “cloud principles never work.” |
| M2 V1, Hidden assumptions, about 4:19 | “Often cannot make progress efficiently” at 02:38–02:43; “can propagate” at 02:55–02:58. | Distinguish a slowdown from correctness loss. His 1,000-GPU and 10,000-GPU examples illustrate scale; they are not benchmark results or design requirements. The 50 ms web example is contextual, not a universal user-perception threshold. |
| M2 V2, Distributed state, about 2:58 | “May be forced to wait” at 02:10–02:13; “may need to be retried” at 02:24–02:27; “may require rolling portions” at 02:32–02:37. | Explain replicated data parallelism versus sharding, and gradients versus parameters. Preserve the conditional recovery scope in every adjacent script and quiz. |
| M3 V1, Ordering, about 2:43 | Local clocks are not a perfect shared reference; coordination protects the intended update sequence. | After: “Finish order alone does not define causal order. The required relationship comes from the algorithm, messages, and operation identities.” The animation makes this visible. |
| M3 V2, Jitter, about 2:18 | Explicit “synchronous AI training cluster” at 00:55–00:58 and “may spend time waiting” at 01:21–01:24. | Compare mean with tail and critical path. State the group and overlap assumptions. Avoid multiplying GPU-time and reporting it as elapsed wall-clock time. |
| M4 V1, Cross-region, about 2:06 | Geographic propagation and the risk of data starvation. | Separate three cases: buffered data supply, a critical-path exchange over distance, and independently serving regional model replicas. Add the version-policy qualification after the recording. |
| M5 V1, Orchestration, about 1:51 | “Depending on architecture” at 00:55–00:57 and “may need” at 00:57–01:01. | Identify the later checkpoint rollback as a specific recovery pattern. New teaching shows its scope explicitly and does not turn it into every cluster's rule. |
| M5 V2, Guardrails, about 1:46 | The goal of managing failure boundaries; “often” in the predictable-network comparison at 00:57–01:03. | Translate “absolute predictability” into measured variation limits and service objectives. Teach useful throughput and correctness together, rather than a universal rule to prefer a slower network. |

Caption QA candidates: M3 jitter track renders “GPUs 12, and 3” where “GPUs 1, 2, and 3” appears intended; M5 guardrails track has “distributed air” where “distributed AI” appears intended. Correct only after listening, while retaining the speaker's meaning and timing. No corrections have been made here.

## Shared media design and playback treatment

New animations are silent, exact technical diagrams built from reproducible vector/code primitives. They use the normal Slides figure player and the approved course narration. They need no photorealistic imagery, stock footage, animated presenters, branding inside the media, or moving decorative backgrounds.

Proposed playback is narration-synchronized, one pass, then a held final picture; obtain the user's approval of this mode with the plan. Use the standard figure controls in both inline and enlarged views. The production settings would be `sync_to_narration: true`, `autoplay: false`, `loop: false`, `muted: true`. These are proposed settings only, not changes made to a build. Keep pause, scrub, replay, captions/transcript access, and a readable final static state. Label all numerical examples “Illustrative example”; diagrams should also use shape/pattern/text distinctions so color is never the only cue.

Original recordings use the shared black media player with their own audio and supplied captions. Course narration must finish or pause before the original recording plays, and must not speak over it. Frame the recording on a separate slide or in a brief pre-play introduction; technical caveats belong in readable teaching before/after, not overlaid on Ankur's face or silently spliced into his recording.

All proposals below are new teaching scenes. No value is an OCP requirement, supplier specification, benchmark, or recommended operating threshold unless explicitly cited as such. Timeline scales are illustrative; presentation seconds are separate from simulated milliseconds/seconds/steps. The animated media must label simulated units at the point of use.

## Animation 1 — Find the dependency before counting the GPUs

**Module:** Introduction to Distributed AI Infrastructure. **Proposed duration:** 70 seconds. **Placement:** immediately after the original introduction, following the workload-scope explanation.

**Learner decision:** determine whether a slow participant delays one request, a defined training group, or unrelated work.

**Visual:** two vertically stacked lanes. Upper lane has four independent serving replicas, each completing one request. Lower lane has a four-participant synchronous training group with a clearly bounded collective gate. One unrelated job remains visible outside the group. Use request tiles, participant cards, a time ruler, and a thin bracket marking the scope of dependency. Avoid suggesting that a physical rack is the dependency boundary.

| Presentation time | Exact staged action and quantities | Voiceover beat |
|---|---|---|
| 0–10 s | Reveal four serving replicas and four training participants. Both use the same device icon. Add labels “independent requests” and “one synchronous group.” | The hardware count is the same. The dependency is different. |
| 10–23 s | Upper requests A/B/C finish at illustrative 100 ms; D finishes at 140 ms. A/B/C return independently. | A slower replica affects its assigned request in this deliberately independent example. |
| 23–39 s | Lower participants A/B/C become ready at 100 ms; D at 140 ms. A/B/C show a hatched wait region to 140 ms. Required group operation completes only after D is ready; no separate communication duration is modeled. | Here the next dependent operation requires all four participants. |
| 39–49 s | Reveal three 40 ms wait regions. Counter reads “3 × 40 ms = 120 GPU-ms waiting.” Separate ruler reads “group ready: +40 ms.” | Aggregate waiting resource-time is different from elapsed step delay. |
| 49–60 s | Illuminate unrelated Job B outside the bracket; its progress continues. Add fifth GPU outside the group without connecting it. | A new device does not remove the declared dependency; unrelated work can still progress. |
| 60–70 s | Hold final picture: independent requests; bounded training dependency; “Measure the critical path.” | Ask which operation needs which participants before drawing a scaling conclusion. |

**Illustrative assumptions:** ready times are selected for arithmetic; the training model omits communication duration and compute/communication overlap. The graphic demonstrates dependency wait only. No universal 40 ms penalty or utilization prediction is implied. The independent-serving example expressly excludes a shared downstream bottleneck.

**Why motion earns its place:** identical device layouts become two different execution patterns; the learner sees exactly which progress stops and which continues.

## Animation 2 — Follow one training update without losing the state

**Module:** Architectural Assumptions and Distributed State. **Proposed duration:** 80 seconds. **Placement:** M2S5, after the state and parallelism distinction and the first assumptions recording, before the distributed-state recording. This establishes the precise gradient mechanism before the recording's broader coordination analogy.

**Learner decision:** identify what must match before an update and why an arbitrary replacement worker cannot simply continue.

**Visual:** four model replicas in a square; each contains the same one-dimensional weight tile. Colored data tiles differ by participant. A conceptual reduction rail combines gradients and returns one result. Keep a small step/version tag attached to every gradient. This rail is an abstraction, not a claim about ring, tree, switch, or parameter-server topology.

| Presentation time | Exact staged action and quantities | Voiceover beat |
|---|---|---|
| 0–12 s | Four replicas show `step 42`, weight `w = 10`. Different input batches enter each. | This is data parallel training: replicated models, different input data. |
| 12–27 s | Gradients labeled `step 42` emerge: 2, 4, 6, 8. Show their attachment to the matching step. | The participants produce different local gradient contributions. |
| 27–41 s | Contributions combine into `(2 + 4 + 6 + 8) / 4 = 5`; the mean moves back to all four replicas. | A shared gradient result lets each replica perform the same update. |
| 41–53 s | Each replica applies simple SGD: `10 − 0.1 × 5 = 9.5`. Tags advance to `step 43`. | With the same starting state and update rule, the replicas remain aligned. |
| 53–66 s | Bring in a replacement participant showing an empty state tile. A membership gate pauses its admission; it does not receive a random request and become current. | Replacing compute is different from restoring the state needed to participate. |
| 66–74 s | Show a checkpoint bundle with labeled compartments: model, optimizer where applicable, step/progress, and other state required by the training implementation. The replacement remains “restore + validate” rather than being declared instantly safe. | Recovery must restore the state the actual training implementation requires. |
| 74–80 s | Hold the four aligned replicas and the controlled admission path. | Define the state and membership contract before automating a change. |

**Illustrative assumptions:** equal batch weighting; one scalar weight and four made-up gradient values; basic SGD with learning rate 0.1 and no momentum; one update only; no overlapped execution. Numbers teach the mechanism, not a model or tuning recommendation. Checkpoint completeness depends on implementation; do not promise the four drawn compartments form an exhaustive framework-neutral specification.

**Specified versus illustrative:** averaging gradients and applying local optimizer updates is grounded in [PyTorch's DDP design explanation](https://docs.pytorch.org/docs/stable/notes/ddp.html). The specific values, layout, step numbers, and conceptual reduction rail are authored examples.

**Why motion earns its place:** the learner can follow the same state identity through local calculation, collective result, update, and replacement admission. It also corrects the misconception that distributed training always shards the model.

## Animation 3 — Separate causal order from clock readings and waiting time

**Module:** Event Ordering, Timing, and Causality. **Proposed duration:** 90 seconds. **Placement:** after the ordering and jitter concepts, before the module's assessment.

**Learner decision:** distinguish an apparent timestamp contradiction from a real dependency and a real delay.

**Visual:** the first half uses two vertical host lifelines and one message ID. The second half transforms these into four ready-time bars for one collective. Keep separate labels for “local clock,” “causal arrow,” and “time until required contribution ready.” Use a visible transition so the two numerical examples are not mistaken for one measurement.

| Presentation time | Exact staged action and quantities | Voiceover beat |
|---|---|---|
| 0–13 s | Host A sends message `m7` at local 100 ms; B receives the same message at local 97 ms. A common reference strip, visible only as the illustrative ground truth, shows send at 100 ms and receive at 103 ms. B's offset is −6 ms. | Different local clock readings can make a valid exchange look reversed. |
| 13–26 s | Timestamp-sorted log puts receive first. Then connect send and receive by `m7`; the causal arrow stays send → receive. | The matching message provides the dependency evidence. Timestamp order alone did not. |
| 26–38 s | Add an event on B with no communication/dependency path to an independent event on A. Leave them side by side, without a causal arrow. | Independent events need not have a meaningful causal order. Do not invent one from which GPU finished first. |
| 38–48 s | Collapse the clock scene into a compact reminder. Reveal a new group labeled “required contributions for one operation.” | Correct event association and fast completion are separate questions. |
| 48–65 s | First four bars end at 10, 10, 10, 10 ms. Second set ends at 5, 5, 5, 25 ms. Both means display 10 ms; group-ready markers display 10 ms and 25 ms. | The same mean can hide a much later final required contribution. |
| 65–79 s | In second set, shade three waits from 5 to 25 ms. Show “group ready: +15 ms” and, separately, “waiting: 3 × 20 = 60 participant-ms.” | Look at the completion dependency and the distribution, not just the average. |
| 79–90 s | Hold: “Identify the operation”; “Trace dependencies”; “Measure the tail.” Keep the actual arithmetic visible. | Clocks help measurement; dependencies establish causality; late work can extend the critical path. |

**Illustrative assumptions:** fixed clock offset only, no modeled drift rate; transport itself still obeys send-before-receive. Four simultaneous participants, no overlap or other useful work, one required group operation, no separate reduction duration. The ready-time samples are not a latency distribution, p99 estimate, or benchmark. A four-sample example cannot establish a percentile service objective.

**Specified versus illustrative:** the partial-order distinction comes from [Lamport's original treatment](https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/). All clock and timing numbers are invented teaching values. Do not teach Lamport timestamps as proof of causality in both directions: a smaller logical timestamp alone does not prove one event caused another.

**Why motion earns its place:** a misleading sorted log is repaired by an explicit message relationship; then the same-average comparison makes the performance effect visible without claiming clocks caused it.

## Animation 4 — Decide what really crosses the region boundary

**Module:** Cross-Domain Architectures and Geographic Boundaries. **Proposed duration:** 95 seconds. **Placement:** after the original cross-region recording, before the private-connectivity/governance discussion.

**Learner decision:** distinguish a critical-path exchange from buffered supply and independently serving replicas.

**Visual:** two region containers separated by one explicit boundary. The middle link stays in place while three workload patterns replace one another. No map of real countries or cloud regions; use Region A/Region B. A quiet badge reads “Illustrative scenarios.”

| Presentation time | Exact staged action and quantities | Voiceover beat |
|---|---|---|
| 0–13 s | Draw a hypothetical 1,000 km optical path; declare assumed propagation speed 200,000 km/s. One signal takes 5 ms; a request/response traversal takes 10 ms before processing and queuing. | Distance sets a propagation contribution. Actual routed length and other delays still matter. |
| 13–26 s | Put that exchange on a blocking operation's critical path. Then change the link's badge to “private” without changing its length or travel time. | More control over a connection does not erase propagation delay. |
| 26–42 s | Replace blocking operation with a producer in A, buffer of 8 batches in B, and GPU consumer in B. Supply and consumption both show 4 batches/s. | A data pipeline can decouple the consumer from short supply fluctuations. |
| 42–60 s | Supply drops to 2 batches/s for 3 simulated seconds; consumption remains 4. Buffer falls 8 → 6 → 4 → 2. No starvation icon appears. | The short deficit drains six buffered batches; the GPU is still fed. |
| 60–69 s | Extend deficit to four seconds: buffer reaches zero. In the following second only 2 of 4 demanded batches arrive. Mark “consumer now supply-limited.” | A sustained deficit eventually exhausts that protection. |
| 69–83 s | Replace pipeline with independent inference replicas in both regions. Show explicit rollout policy: test v2 in B; continue approved v1 traffic in A; promote only after validation. No per-request collective arrow crosses regions. | Regional inference can follow a deliberate rollout policy instead of a universal simultaneous switch. |
| 83–95 s | Hold three small labeled diagrams: “blocking exchange,” “buffered supply,” “independent serving.” Highlight each crossing dependency. | Name the exchange, budget it, and apply the service's version and data-placement policies. |

**Illustrative assumptions:** 1,000 km is cable path length, not a straight-line separation; 200,000 km/s is a declared teaching assumption, not a measured fiber specification. The arithmetic isolates propagation, so 10 ms is not promised application RTT. The buffer example uses equal-sized batches and continuous/interval-average flow, omits serialization and scheduling, and has initial buffer 8 at the instant the deficit begins. The inference policy is a chosen example, not an OCP standard or a universal consistency rule. The diagram does not promise identical model outputs from identical versions.

**Specified versus illustrative:** controlled model deployment is supported as a real practice by [SageMaker deployment guardrails](https://docs.aws.amazon.com/sagemaker/latest/dg/deployment-guardrails.html). Dedicated connectivity still needs diversity and adequate failover capacity, as described in [Direct Connect resiliency recommendations](https://aws.amazon.com/directconnect/resiliency-recommendation/). The three staged scenes and every quantity are illustrative.

**Why motion earns its place:** retaining the same geography while changing what crosses it reveals why “multi-region AI” alone does not specify the architecture.

## Animation 5 — Recover one job without restarting the world

**Module:** Orchestration, Scaling, and Infrastructure Guardrails. **Proposed duration:** 90 seconds. **Placement:** after the orchestration recording, before the final guardrails recording or summary.

**Learner decision:** choose recovery scope and admission checks that match the job and infrastructure.

**Visual:** two explicitly separate four-participant training groups, A and B, with separate state/checkpoint tracks. A shared infrastructure envelope is visible below them. The controller has three restrained indicators: observe, decide, act. A failure pulse affects one participant, not the entire canvas.

| Presentation time | Exact staged action and quantities | Voiceover beat |
|---|---|---|
| 0–12 s | Show Job A checkpoint after step 42; completed steps 43 and 44; step 45 in progress. Job B advances on its independent track. | The recovery policy and checkpoint boundary belong to a defined job. |
| 12–25 s | Participant A3 fails in step 45. Stop the affected A group under the scenario's group-restart policy; B continues. Mark A3 unavailable. | The failed participant interrupts this group's next valid update. Independent work is outside that restart scope. |
| 25–40 s | Controller correlates job failure, device health, and network evidence. Present a compatible spare as a candidate. Hold admission while health, capacity, and state checks are incomplete. | An idle device is a candidate resource, not yet a ready participant. |
| 40–55 s | Restore Job A from the valid checkpoint after step 42. Highlight completed steps 43–44 plus partial step 45 as work to replay; do not label three completed steps lost. | Restore a known state and identify exactly which work must be repeated. |
| 55–68 s | Validate group membership and state; resume at step 43. Job B remains on its own forward track. | Resume through the framework's supported recovery mechanism. |
| 68–80 s | Add an expansion request of +40 kW to an illustrative facility envelope with only 30 kW of approved headroom. The request stays pending, even though four more devices are available. | Admission also depends on the validated facility envelope. Device availability alone is insufficient. |
| 80–90 s | Hold three checks: “right recovery group,” “valid restored state,” “approved capacity envelope.” Small counter shows “retry budget: example policy,” without recommending a universal count. | Safe automation needs explicit scope, evidence, and limits. |

**Illustrative assumptions:** separate jobs have independent restart/state semantics and no shared failure in the example; actual shared network, power, storage, or management dependencies can widen impact. Job A uses whole-group checkpoint restart; other implementations can behave differently. Step 42 is the last completed checkpoint; steps 43–44 and partial 45 are replayed. The 40 kW demand and 30 kW available headroom are fictional approved-envelope values at the same declared facility boundary, not equipment ratings, liquid-cooling thresholds, or live electrical advice.

**Specified versus illustrative:** [PyTorch elastic launch documentation](https://docs.pytorch.org/docs/stable/elastic/run.html) supplies a concrete example of worker-group restart on failures/membership changes and checkpoint-based progress recovery. The two-job layout, chosen checkpoint, failure location, and capacity numbers are authored examples. The adjacent Open Systems course provides the established boundary-based facility language.

**Why motion earns its place:** the learner sees containment, rollback distance, validated re-entry, and a separate admission limit as distinct actions. It prevents “restart every GPU” from becoming the course's default mental model.

## Proposed assessments — two questions per module

These are research alternatives for the upgraded course, not edits to the recovered source. The consolidated editorial proposal is [assessment-plan.md](assessment-plan.md), with structured keys and feedback in [assessment-plan.json](assessment-plan.json); that set is authoritative for approval. Each module has one single-choice and one multiple-select item. Narration should orient learners to the task without reading every question or giving the answer. Feedback should explain why each distractor fails in the stated scenario. Retain the course's standard attempt/retry behavior.

### Module 1

**Single choice:** Four independent inference replicas serve requests locally. A separate four-participant synchronous training group must complete a required collective before its next update. One participant in each arrangement slows down. Which conclusion is best supported?

- A. Every GPU in both arrangements must pause.
- **B. The training group's dependent update may wait; other independent requests can continue.**
- C. Inference cannot be affected by any network delay.
- D. Adding a fifth GPU automatically removes both delays.

**Feedback:** B follows the declared dependencies. A expands the failure scope without evidence; C mistakes independent request handling for immunity from delay; D does not explain how the new device satisfies the missing dependency.

**Multiple select:** Before predicting whether doubling GPUs will improve useful throughput, which evidence matters? Select all that apply.

- **A. Which operations communicate and synchronize.**
- **B. Measured communication and compute behavior at the proposed scale.**
- **C. Whether the software and workload can use the added resources.**
- D. GPU count alone, because AI speed scales linearly.

**Feedback:** A/B/C connect capacity to useful work. Device count is an input to the design, not a scaling result.

### Module 2

**Single choice:** In the illustrated equal-batch data-parallel step, four model replicas start at the same weight and produce gradients 2, 4, 6, and 8. What keeps the replicas aligned in the shown update?

- A. Each replica applies only its own gradient as soon as it finishes.
- **B. Each uses the same averaged gradient, starting state, and optimizer rule.**
- C. The first replica to finish dictates all subsequent causal ordering.
- D. Every replica must store a different shard of the model.

**Feedback:** B describes this data-parallel example. A changes the shown algorithm; C confuses completion with dependency; D describes a different distribution arrangement.

**Multiple select:** A team wants to add a participant to a running training job. Which questions must its supported change process answer?

- **A. How the participating group is re-formed.**
- **B. How the participant obtains the required model and training state.**
- **C. Whether restart, checkpoint recovery, or workload adjustment is required.**
- D. Whether an ordinary request load balancer can make membership irrelevant.

**Feedback:** A/B/C define a training-aware change. Elasticity is possible in supported designs, but an extra device does not automatically become a valid participant.

### Module 3

**Single choice:** A log records message `m7` sent on A at local time 100 ms and received on B at local time 97 ms. Clock offset is not yet known. Which inference is justified?

- A. The receive caused the send.
- B. The message traveled backward in time.
- **C. The matching send precedes the receive causally; local timestamps alone cannot establish the elapsed transit time.**
- D. The GPU hardware must be defective.

**Feedback:** The message relationship establishes the dependency. The timestamps need a shared timing interpretation before their difference is a valid transit measurement; they do not diagnose hardware failure.

**Multiple select:** For the two illustrative four-participant sets `[10,10,10,10]` and `[5,5,5,25]` ms, assume one operation needs every contribution and no overlap is available. Which statements follow?

- **A. Both sets have mean ready time 10 ms.**
- **B. The second set's operation cannot be ready before 25 ms.**
- **C. The same mean can conceal a different group completion time.**
- D. The second set proves clock skew caused the delay.

**Feedback:** A/B/C follow from the arithmetic and stated dependency. The samples show timing behavior; they do not identify its cause.

### Module 4

**Single choice:** A regional GPU consumer uses 4 equal-sized batches/s. Its buffer initially contains 8 batches. Supply falls from 4 to 2 batches/s for three seconds. Under the illustration's simplified flow assumptions, what happens?

- A. The consumer immediately loses all useful throughput.
- **B. The buffer falls to 2 batches and supplies the consumer throughout the dip.**
- C. Private connectivity would make this arithmetic irrelevant.
- D. The buffer grows to 14 batches.

**Feedback:** The deficit is 2 batches/s for three seconds, so six buffered batches are consumed. Starvation is possible if the deficit lasts longer; it is not automatic at the first bandwidth change.

**Multiple select:** What must a cross-region design review establish?

- **A. Which exchanges lie on a request or training step's critical path.**
- **B. Required data-placement and model-version policies.**
- **C. Capacity, failure behavior, and useful performance of the selected paths.**
- D. That private links remove propagation delay and all variation.

**Feedback:** A/B/C turn a geography diagram into an operational design. Link ownership alone does not establish latency, resilience, or application correctness.

### Module 5

**Single choice:** Job A has a valid checkpoint after step 42, completes steps 43 and 44, then loses a participant during step 45. Its supported policy restarts the job from that checkpoint. Job B is independent and healthy. What is the correct recovery description?

- A. Restart both jobs because they share the label “AI.”
- **B. Restore Job A after step 42 and replay subsequent work; leave Job B running under the stated independence assumption.**
- C. Insert an empty replacement directly into step 45 and assume its state matches.
- D. Declare all previously checkpointed work lost.

**Feedback:** B matches the declared recovery and failure boundaries. A invents a broader dependency; C skips restoration; D ignores the valid checkpoint.

**Multiple select:** A scale request has enough idle GPUs available. Which additional checks can still prevent admission?

- **A. Required communication and data paths cannot meet the workload's tested objective.**
- **B. The validated power/cooling envelope has insufficient headroom at the affected boundary.**
- **C. The supported membership/state transition has not been validated.**
- D. Scaling is physically impossible for all distributed AI workloads.

**Feedback:** A/B/C are concrete unmet conditions. D replaces a design assessment with an unsupported universal claim.

## Production acceptance criteria after plan approval

1. Every new narration statement retains the declared workload/group/measurement scope; no blanket “all AI” rules return in quizzes or feedback.
2. Arithmetic and units remain readable in the figure player and enlarged view; GPU-ms and wall-clock ms are never combined or mislabeled.
3. Source recordings, Ankur's attribution, own audio, and captions remain preserved. Any caption corrections receive an audio check.
4. Every stage is readable long enough to connect the cause and effect; the approved narration controls timing. The media ends in the full explanatory picture.
5. Each media item has a plain-language alt description, readable transcript, explicit illustrative status, and no unsupported supplier/OCP specification claims.
6. Sources are referenced on the relevant teaching slide; source-credit footers, title lockups, and long paragraphs stay outside the animation itself.
7. The final scripts and media plans go to editorial approval before synthesis or rendering. This document does not authorize production or modify the recovered courses.
