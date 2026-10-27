# Astra final review — three new teaching videos

Review date: 2026-10-26 (America/New_York). Reviewer: explicitly requested Astra subagent. Scope: M1S10, M2S14 and M4S11 in the approved 78-slide course.

**Result: pass within the scope below. No must-fix technical, causal-sequence, mathematical or sampled visual defect was found.** All three videos have meaningful teaching value. Their editable animation logic follows timestamped phrases from the final delivered narration, and their completed states remain visible through the closing speech. This is a source/word-map/representative-frame review, not an unrestricted audiovisual or integrated-player certification.

## Evidence and limits

Reviewed the three final animation HTML files, relevant builder logic in `authoring/build_approved_media.py`, all three `timeline-*.json` records and their final-WAV Scribe word maps, current course media references, `source-build-records.json`, `source-geometry.json`, and `encoded-frame-samples.json`.

Independently recomputed the hashes of each delivered WAV and approved script: all match the associated timeline records. Independently read MP4 movie durations and compared all 15 supplied source/decoded image pairs numerically. Visually inspected 10 representative decoded frames, four additional native source states, and all three posters. The detailed sample list below makes the perceptual coverage explicit. The 240-state geometry report was inspected as an automated report; it must not be read as a claim that I personally examined all 240 images. Its 78 + 78 + 84 states report no clipped text, text containment violations or text collisions.

No audio was played or perceptually listened to. Timing conclusions use the supplied Scribe word timestamps and deterministic source code, not an independent phonetic alignment or listening test. The records accurately disclose that forced alignment was unavailable. No continuous real-time playback was performed. Source/decoded agreement supports the reviewed samples; it does not establish that every encoded frame is flawless.

An attempted read of the actual `file://` module page was blocked by the browser tool's explicit URL security policy. I did not circumvent that restriction or start a server. Consequently, live player synchronization, seeking, replay, phone layout, fullscreen behavior, LMS/SCO behavior and accessibility interaction are **not independently signed off by this report**. The parent agent reports separate integrated-player/phone/harness checks; those are separate evidence, not my observations.

Only this report was written. Course content, templates, audio and media were not changed.

## M1S10 — AI placement / AICC

**Pass.** The example distinguishes a time-sensitive local inspection service from separate nonurgent regional analysis. It does not depict a running inference task instantly migrating, or imply that AICC is a mandatory ladder of network tiers. The narration conditions continued local inference on the availability of the model, data, power and computing resources. The visible title labels the constraints as illustrative, rather than a universal claim that all remote services miss inspection deadlines.

The animation adds causal value beyond a static map: it interrupts the wide-area connection while leaving a second local request/response operating, then permits separate queued work to use regional capacity after restoration. There is no transfer from the local-model box to the regional-analysis box that would suggest live-task migration. The AICC conclusion appropriately encompasses regional, enterprise, telco and industrial environments.

| Final-WAV phrase/event | Source timing and teaching check |
| --- | --- |
| Camera sends an image | Request dot travels camera → local model at 2.56–3.76 s. |
| Response deadline | Return dot travels local model → camera at 5.82–8.30 s; deadline box is highlighted. This is a conceptual request/response diagram, not a literal actuator wiring diagram. |
| Wide-area connection unavailable | WAN route fades and outage cross appears at 12.78 s. |
| Local inference can continue | Second request travels at 15.78–17.20 s; second response follows at 17.20–18.40 s, entirely inside the outage interval. Native frames at 16.500 and 17.233 s visibly confirm these two directions. |
| Separate nonurgent analysis waits | Queue is highlighted at 21.32 s while WAN remains unavailable. |
| Connectivity returns; regional capacity | Route restores at 23.76 s; only the separate batch travels to regional capacity at 25.28–27.04 s. |
| AICC and placement constraints | Project scope appears at 37.72 s; the closing constraint list appears at 50.88 s and remains to the end. |

Final narrated duration: **55.590 s**; MP4 movie duration: **55.600 s**. Closing constraint state lasts **4.710 s**. Last timestamped spoken word ends at 55.30 s. The diagram therefore remains stable throughout the closing sentence; this is not a claim of a long silent tail.

Decoded frames visually reviewed: 13.900, 27.800 and 55.557 s. Additional native states: 16.500 and 17.233 s. Poster reviewed. Text, arrows, outage mark and endpoint relationships were clear in these full-resolution images.

## M2S14 — Liquid heat path

**Pass.** The sequence traces energy from component to cold plate, through the equipment coolant to a heat-transfer interface, and onward through a distinct facility circuit and heat rejection. Warm and return arrows point in the appropriate directions. The statement that heat crosses the exchanger while the two fluids remain separate is explicit. The diagram is a conceptual heat/flow path, not a detailed piping schematic; the interface box appropriately abstracts the exchanger's internal geometry.

The later liquid-to-air example replaces the facility-loop panel instead of presenting liquid-to-liquid and liquid-to-air as consecutive physical stages. The room-air route still reaches the environment, and both narration and labels retain the need for room cooling capacity. The closing compatibility/capacity check avoids suggesting that fitting cold plates alone completes a cooling design.

Meaningful motion consists of the timed warm/return transfers and the mutually exclusive alternative heat-rejection arrangements. A static end frame alone would omit the important contrast with the earlier liquid-to-liquid example.

| Final-WAV phrase/event | Source timing and teaching check |
| --- | --- |
| Component and cold plate | Component is highlighted at 0.12 s; component → plate heat path becomes active at 1.98 s. |
| Warmed equipment coolant | Warm dot moves plate → interface at 5.34–7.14 s. |
| Liquid-to-liquid example | Facility warm path activates at 9.10 s. |
| Separate fluids | Explicit nonmixing conclusion appears at 14.98 s. Native 15.800 s frame confirms it. |
| Cooled equipment coolant returns | Return path and dot point interface → cold plate at 17.06–18.80 s; the separate facility return arrow points toward the interface. |
| Facility carries heat onward | Rejection arrow becomes active at 19.78 s. Native 20.933 s frame shows a complete path to the environment. |
| Alternative liquid-to-air arrangement | Facility-loop group is hidden and room-air group appears at 23.96 s. |
| Room cooling still removes heat | Room-air rejection path becomes active at 30.90 s. |
| Final checks | Compatibility/capacity/full-path conclusion appears at 43.78 s and remains to the end. |

The corrected rejection arrow at source x=1135 is visibly to the right of its explanatory label in both reviewed arrangements. It no longer crosses the label, and its arrowhead meets the environment-box boundary. No must-fix path or labeling collision remains in the inspected frames.

Final narrated duration: **49.135 s**; MP4 movie duration: **49.134 s**. Closing state lasts **5.355 s**. Last timestamped word ends at 49.00 s. Duration differences are negligible relative to one 30 fps frame.

Decoded frames visually reviewed: 12.300, 24.567 and 49.100 s. Additional native states: 15.800 and 20.933 s. Poster reviewed. The poster intentionally represents the final liquid-to-air alternative; the video and narration supply the earlier liquid-to-liquid comparison.

## M4S11 — Energy and PUE counterexample

**Pass.** This is an accurate controlled counterexample to treating PUE alone as an energy-performance verdict. The same useful work/service and a comparable measurement period are explicitly held constant. Facility overhead staying fixed is an assumption of this illustrative example, not a forecast that consolidation always leaves overhead unchanged.

Arithmetic checked independently:

- Before: IT 1,000 + overhead 200 = total 1,200; PUE = 1,200 / 1,000 = **1.20**.
- After: IT 800 + overhead 200 = total 1,000; PUE = 1,000 / 800 = **1.25**.
- Total energy falls by **200 units**, or about **16.7%**, despite the higher ratio. The video correctly displays the 200-unit saving without inventing a unit or percentage.

The bars share one linear scale. IT widths of approximately 583.333 and 466.667 source units preserve the 1,000:800 ratio; both overhead segments remain approximately 116.667 units wide. Before and after totals are therefore visually comparable. Ratios remain separate from energy quantities.

| Final-WAV phrase/event | Source timing and teaching check |
| --- | --- |
| Starting system | Baseline IT bar grows at 6.90–8.10 s; its numeric label is then visible for the spoken quantity. |
| Facility overhead | Baseline overhead segment grows at 10.38–12.22 s. |
| Total and baseline PUE | Total appears at 12.70 s; PUE 1.20 appears at 16.46 s. |
| After consolidation / lower IT | Lower IT bar grows at 19.24–21.18 s. Before remains visible for comparison. |
| Overhead remains 200 | Equal-width overhead segment appears at 21.42 s. |
| New total and ratio | Total 1,000 appears at 23.46 s; PUE 1.25 and the saving conclusion appear at 27.28 s. |
| Evaluation | Completed comparison remains stable during the denominator explanation and closing evaluation sentence. |

Final narrated duration: **39.524 s**; MP4 movie duration: **39.534 s**. The declared closing interval is **4.864 s**, and the complete final comparison is already visible from 27.28 s. Last timestamped word ends at 39.34 s. The final hold is ample for the spoken conclusion without a distracting loop.

Decoded frames visually reviewed: 9.900, 19.767, 29.667 and 39.490 s. Poster reviewed. Numbers, scales, colors and outcome were legible and consistent. The staged comparison earns its place as a teaching video even though its final state also works well as a static recap.

## Source/encode consistency and deliverable identity

The mean absolute RGB differences between each source image and its paired decoded frame were approximately **2.03–2.34 intensity levels on a 0–255 scale** across all 15 pairs. This is a compact numerical consistency check, not a perceptual-quality score. Representative visual inspection found no meaningful displacement, missing element or changed label. All three course entries specify muted, nonlooping video synchronized to the separate narration.

| Video | SHA-256 of reviewed MP4 |
| --- | --- |
| `figures/module1/ai-placement.mp4` | `44ee5ddd5c9461348ccfb8b4b3fef8fcc57abead30f3436f29a6c3fa6a440b54` |
| `figures/module2/liquid-heat-path.mp4` | `2885e71a9712c4438f9a67b43035c32d1197057b6f22c322c8447fb261e04584` |
| `figures/module4/energy-ratio-change.mp4` | `bacd7bfe2da4935a428fdd4d21c4a9eb9a23bb87cb75f247400c0a1a07cb148e` |

No media rework is requested by this review. Preserve the explicit conditions in the AICC narration, the separate-fluid and alternative-arrangement language in the cooling video, and the constant-useful-service assumption in the PUE example. These qualifications are essential to the accuracy of the simplified teaching diagrams.
