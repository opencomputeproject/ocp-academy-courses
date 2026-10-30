# Technical teaching video plan

Final wording reviewed; phrase-position cue estimates; all durations measured or supplied

Finite deterministic window.setTeachingTime(ms); cue fades 900ms; final completed scene holds. data-duration-ms and data-poster-ms on documentElement. Preview ?play=1 runs once. No network.

## Reproducible retiming

The canonical finite HTML sources are in `../animations/` relative to the course's authoring folder. From the repository root, run `python3 courses/open-cluster-designs-for-ai/scripts/retime_videos.py /absolute/path/to/built-course` after generating changed narration. `cue-map.json` contains the exact pronunciation-aware phrase anchors. The helper uses measured PCM WAV duration and editorial word-position cue estimates, not forced alignment. Review timing against the speech and re-encode any changed source before updating MP4s, posters and media hashes. Every final picture holds at least three seconds after its last reveal; a 24 fps encoder may quantize the endpoint.


## M1S4

Build the node / pod, OPG and cluster hierarchy without equating domains with racks.

Duration: 49.560317s (measured PCM WAV duration). Completed hold: 3.000s.

### Actual spoken anchors

- 0.000s · `node` · Read the hierarchy

- 19.824s · `opg` · An Open Pod Group

- 29.053s · `cluster` · An X O C N

- 33.496s · `compose` · It combines one or more

- 44.760s · `boundary` · These are architectural domains

### Reviewed labels

XOC-N; Scale-out cluster; Shared cluster resources; OPG-M; Modular building block; Networking; Storage; Management / support; xPU-node / scale-up pod; xPU; xPU; Scale-up domain; …; OPG-M; One or more groups; Domain boundaries ≠ fixed rack boundaries

### Source pages

cluster-whitepaper PDF pp8–12; xoc-n PDF p7

### Constraints

- Ellipses and repeated symbols denote categories, not a quantity.

- Nested boundaries represent functional domains; no rack outline.

## M2S5

Preserve full endpoint identity while tracing a breakout attachment and a separate uplink.

Duration: 52.205624s (measured PCM WAV duration). Completed hold: 22.490s.

### Actual spoken anchors

- 0.000s · `base` · Follow two connections

- 2.538s · `port` · In the O P G connection map

- 10.514s · `legs` · Its two four-hundred-gigabit legs

- 18.489s · `uplink` · The next highlighted path is an uplink

- 27.916s · `alias` · In the cluster map

### Reviewed labels

January Clos example; Node attachment; Distinct leaf–spine uplink; SOL1 · port 1; 800G OSFP; N1 · NIC 1; N1 · NIC 5; 400G breakout leg; 400G breakout leg; SOL1 · port 2; Optical-module port 1; SO1 · port 1; Optical-module port 1; 400G optical; XOC map identity: O1S1 (2,1); Spine identity: SO1 (1,1)

### Source pages

opg-m PDF p29 Table10; xoc-n PDF p25 Table9

### Constraints

- Do not connect port1 breakout to spine.

- O1S1 means OPG1 SOL1, not a separate device.

- Arrows illustrate trace direction, not simplex link direction.

## M3S4

Compare traffic locality for equal-hardware Clos wiring patterns without declaring a winner.

Duration: 47.933696s (measured PCM WAV duration). Completed hold: 18.172s.

### Actual spoken anchors

- 0.000s · `hardware` · Watch where the traffic goes

- 1.816s · `clos` · With single-homed Kloh wiring

- 10.531s · `rail` · Rail-optimized wiring groups

- 17.430s · `cross` · while traffic between rails

- 27.961s · `placement` · Neither pattern wins

### Reviewed labels

Same schematic hardware · different wiring; Single-homed Clos; Spine; Leaf A; Leaf B; Host A; Host B; Rail-optimized Clos; Spine; Leaf A; Leaf B; Host A; Host B; All NICs; All NICs; Same leaf → leaf-local; r1; r2; r1; r2; Same rail + same leaf → leaf-local; Cross-rail may use spine; Co-located hosts can stay leaf-local; Traffic + placement determine the path; Selected paths only · schematic, not a complete implementation

### Source pages

training-fabric PDF pp32–37; p35 summary

### Constraints

- Both panels use identical drawn device counts.

- Only two selected rail affinities shown, not eight NICs or full cabling.

- No throughput or performance comparison.

- Cross-rail locality depends on rail domain sizing.

2026-10-30 pronunciation update: spoken Clos is Kloh; visual spelling and design unchanged.

## M3S7

Add an inference back-end only when model dependencies span hosts, retaining all shared roles.

Duration: 47.593923s (measured PCM WAV duration). Completed hold: 23.632s.

### Actual spoken anchors

- 0.000s · `minimal` · Inference uses a different decision

- 7.993s · `within` · the Minimal Inference profile omits

- 18.529s · `distributed` · Now let the model

- 22.162s · `backend` · The Distributed Inference profile adds

### Reviewed labels

Minimal Inference; Distributed Inference; Gateway; Front-end + storage; Host A; Host B; In-band management; Independent out-of-band; Gateway; Front-end + storage; Host A; Host B; In-band management; Independent out-of-band; Single-host model execution; No scale-out back-end; Scale-out back-end; Cross-host model dependencies

### Source pages

inference-fabric PDF pp14,21–22,40–41

### Constraints

- No Training Minimal/Full naming.

- The two host symbols are illustrative, not a sizing recommendation.

- Management roles remain visibly independent.

## M4S5

Accumulate enrollment, validation and operational proof in a persistent evidence packet.

Duration: 43.935556s (measured PCM WAV duration). Completed hold: 9.276s.

### Actual spoken anchors

- 0.000s · `packet` · Carry one evidence packet

- 2.954s · `day0` · At Day Zero

- 15.507s · `day1` · At Day One

- 23.998s · `day2` · At Day Two

- 32.859s · `reconcile` · A change to hardware

### Reviewed labels

Deployment evidence packet; Declared intent; Observed / tested evidence; Design + configuration version; Device and endpoint identities; Topology + tenant policy; Acceptance criteria + owner; Day 0 · Enroll; Enrollment + identity checks; Agent and platform readiness; Day 1 · Validate; Physical mapping + link checks; Logical topology + policy tests; Day 2 · Operate; Telemetry + staged-change results; Recovery drill + updated evidence; Versioned intent; Measured outcome; A declaration is not a test result

### Source pages

training-fabric PDF pp47–52; inference-fabric PDF pp35–39

### Constraints

- Evidence packet is a teaching synthesis, not a mandated upstream file format.

- No assumed automatic pass or readiness checkmark.

- Day2 changes require refreshed evidence; no looping workflow animation.

## Final measured-time QA

All five start, midpoint, final and semantic-transition checkpoint sets were rendered in Chrome and visually reviewed. No browser errors, out-of-frame labels, text collisions or incomplete final states. Arrowheads appear when their path completes. Actual visible text inventories, PCM measurements and SHA-256 input/source hashes are saved in video-plan.json.
