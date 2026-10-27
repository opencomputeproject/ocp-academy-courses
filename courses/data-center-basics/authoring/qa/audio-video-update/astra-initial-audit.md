# Initial audit: five generated teaching videos

Date: 2026-10-24. Scope: M1S4, M2S6, M2S11, M3S9, M4S7 only. This audit does not modify course content, media, player templates, imported videos or SCORM architecture. The requested upgrade is authorized; no additional narration/storyboard approval gate is required. Preserve all ten `original_video` assets and the existing SCORM 2004 four-SCO organization.

## Conclusion

All five assets should be rebuilt as narration-synchronized, single-pass explanations. Simply slowing their current 10–14 second animations to fill the narration would not satisfy the instructional goal. Service journey and virtualization mostly highlight boxes; containment never demonstrates the problem or the intervention; rack capacity changes have no visible cause. Power continuity contains a confirmed animation bug that leaves utility supply visually active after the alleged source failure.

The replacements should demonstrate a different relationship on each slide: request/response with persistent physical support; continuity through a source transition; recirculation reduced by separation; equipment additions consuming independent budgets; and additional virtual workload increasing demand on a shared physical host.

## Evidence and limitations

Read the maintained AcademyWizard `SKILL.md`, `references/narration_synced_video.md`, and `references/figure_prompts.md`, all five editable animation HTML sources, their current scripts and course metadata. Measured WAV durations directly from sample counts. Probed encoded containers: every video is silent H.264, 1920×1080, 30 fps, with one complete declared source pass. Full-duration muted browser playback reached `ended` for all five, with no backwards media-time jumps. Concurrent playback recorded 2–5 dropped frames per video; this proves basic decode/continuity, not frame-perfect rendering under all loads.

Visually inspected complete temporal contact sheets at 0.5-second intervals, including final held states, against CSS timelines. This is a temporal scrub plus full real-time browser playback check; it is not a claim of human-style continuous audiovisual listening. No audio was played aloud. Current word/phrase alignment has **not** been measured. Narration phrase anchors below are exact current script phrases; their final times must come from the final regenerated WAV. Do not reuse current timing estimates after narration regeneration.

Evidence files in this directory:

- `initial-measurements.json`: current scripts, measured audio durations, media hashes and encoded stream metadata.
- `initial-playback.json`: muted full-pass browser playback results and the power CSS diagnosis.
- `initial-frames/m*-s*-sequence.png`: decoded contact sheets, read left-to-right and top-to-bottom, one image every 0.5 s. Unused tile cells are white.

| Slide / asset | Current encoded duration | Current measured WAV | Encoded duration / WAV | Current authored behavior |
|---|---:|---:|---:|---|
| M1S4 `service-journey.mp4` | 14.000 s | 27.260 s | 51% | Independent autoplay loop |
| M2S6 `power-continuity.mp4` | 12.000 s | 25.403 s | 47% | Independent autoplay loop |
| M2S11 `containment-flow.mp4` | 10.000 s | 24.985 s | 40% | Independent autoplay loop |
| M3S9 `rack-budgets.mp4` | 12.000 s | 22.616 s | 53% | Independent autoplay loop |
| M4S7 `virtual-physical.mp4` | 12.000 s | 31.858 s | 38% | Independent autoplay loop |

All figures currently declare `autoplay:true`, `loop:true`, `muted:true` and omit `sync_to_narration`. Thus the second or third pass can be teaching an earlier event during a later narrated caveat. Source timelines themselves hold at the end; unwanted repetition comes from the player loop setting.

## Timing and visual conventions for all replacements

Use one silent video and the slide's existing narration channel. Set each of the five figures to `sync_to_narration:true`, `autoplay:false`, `loop:false`, `muted:true`; record the user's approval in editable metadata. Let D equal the **final** WAV duration. Quantize the video to the nearest 30 fps frame, so absolute duration error is at most 1/30 s. Set one source master duration from that value, and keep every animation inside it.

For each storyboard beat below, save an exact phrase anchor with aligned start and end seconds, the evidence method, animation start/end, and intended visual state. Alignment should target the explanatory verb or noun, not a uniform share of runtime. An object may be present neutrally before it is named; the meaningful change should happen while the relevant phrase is spoken. Allow roughly 0.2 s of visual anticipation where necessary, complete a simple change in 0.6–1.2 s, and hold through the rest of the phrase. A path traversal may take the length of its narrated clause. These are pacing proposals, not measured word timings.

Avoid unrelated motion while caveats are spoken. Final comparison/decision holds should normally occupy the last 3–5 seconds or the final full sentence, whichever the narration naturally supports. A longer sentence should receive meaningful supporting inspection, not a decorative perpetual loop. Motion may show one or a few finite flow cohorts; no subordinate animation restarts. Keep capacity values monotonic unless a prominently labeled comparison reset is both visible and narrated.

Use plain diagrams with large labels, minimal prose, generous whitespace, and the current OCP palette. Do not reproduce slide titles or narration paragraphs inside the videos. Every flow has a labeled meaning and attached endpoints. Use color plus labels/shape/direction, rather than color alone. If drawing a circuit, close its path; if drawing a functional one-line diagram, label it as such and do not depict literal charge moving through an open line.

## M1S4 — Service journey

**Current defect.** The marker travels horizontally at y=405 beneath boxes and arrows at y=290, so it does not physically follow the depicted network. Compute and storage are merged despite having distinct narrated roles. The response continues to a new box on the right rather than visibly returning to the originating device. Electricity/cooling are an unconnected sentence card throughout. All labels exist from t=0; boxes change fill at about 1.68, 3.92, 6.16, 8.40 and 10.64 s. The marker finishes at 12.04 s, then holds. None of those timings is tied to speech.

**Proposed storyboard.** Keep a single device on the left, network in the center, service boundary on the right containing compute and storage. Separate outbound and returning paths. Put a compact physical-support strip below the actual powered equipment, with clear power-in and heat-out connections.

| Narration phrase anchor | Instructional action and hold |
|---|---|
| “Think about opening a shared document” | Show the device/document and a neutral service layout. A single open-document action creates a request token. Brief orientation hold. |
| “Your device sends a request through networks” | The request follows the attached outbound path through the network, arriving at the service boundary as “systems providing that service” is spoken. No free-floating progress dot. |
| “Computing equipment handles the request” | The token enters compute; one finite processing indicator completes. Keep the request visibly pending until computation/data access completes. |
| “storage holds the information” | Show the document retained inside storage and a data read connecting storage to compute. The stored document remains; reading must not look like storage is emptied. |
| “a response travels back” | A distinct response token travels on the return path through the network to the original device; the opened document appears there on arrival. |
| “electricity powers the equipment” / “cooling removes the heat it produces” | Emphasize persistent power support to compute/storage/network and then a heat-removal path out of equipment. These systems were present and active from the start; the emphasis explains the dependency, not delayed activation. |
| “many connected systems … hides most of that complexity” | Hold the complete dependency map with the successful document action. Use the device/service boundary to contrast the simple user action with its underlying dependencies. |

The motion earns its place by linking request, processing/data access, response and continuously necessary physical support. No invented outage is needed.

## M2S6 — Power continuity

**Current defect and technical correction.** The `.normal` CSS rule uses `animation:normal 12s linear both`; Chromium resolves `animationName` to `none` and `animationDirection` to `normal`. The utility line therefore stays at opacity 1 throughout, including the “UPS stored energy” and “Backup supply available” states. Both source arrowheads also remain bright independently of their shafts. The intended caption switches occur at 3.00 and 6.96 s; the media text inventory records 3.2 and 7.2 s and should be refreshed after rebuilding. There is no visible stored-energy reserve, generator starting state, transfer device or equipment power trace.

The narration currently says supply passes through “distribution and an uninterruptible power supply” while the drawing shows UPS → distribution. Make the narration and a qualified functional path agree; distinguish upstream distribution/transfer from downstream distribution if both are shown. Do not imply a generator is wired directly in parallel with utility or can take over before it is ready.

**Proposed storyboard.** A compact functional flow: utility and generator feed a source-selection/transfer block, then UPS and downstream distribution, then equipment. A battery/reserve belongs to the UPS. Below, a small qualitative equipment-power trace advances once across the events. Use a quiet “Illustrative path · event spacing expanded” badge; do not imply actual transfer times.

| Narration phrase anchor | Instructional action and hold |
|---|---|
| “In a conventional example, the normal supply” | Trace the selected utility route to equipment once. Generator is visibly standby; UPS reserve is available. Equipment-power trace begins at a constant level. |
| “before reaching equipment” | Hold the complete normal route with labeled source selection, UPS and downstream distribution. Keep this map stable for the event. |
| “If the incoming source fails” | Utility availability changes to unavailable; its shaft and head deactivate together. Selection state prevents utility/generator simultaneous connection. Mark the failure on the trace while equipment output remains continuous. |
| “stored energy can bridge the transition” | UPS reserve decreases monotonically while a separate path from stored energy to the UPS output is active. The downstream route and equipment power remain visibly supplied. No full discharge or instantaneous recharge. |
| “while a backup generator starts” | Generator changes standby → starting → ready. Readiness must precede its selection. Give the start interval visible duration while stored energy continues to support equipment. |
| narration describing backup availability/transfer, added explicitly if needed | Select the ready backup, activate its complete route, and stop the illustrative reserve discharge. Show one successful transfer; hold a continuous equipment-power trace with event markers. |
| “capacity, fuel, controls and maintenance” / “A generator alone doesn't mean” | Hold the successful example while highlighting four necessary conditions around the diagram. Conclude with “Continuity depends on the complete system.” Do not show an unexplained second failure. |

The stored-energy gauge is illustrative reserve, not a literal battery state-of-charge calculation. A failure scenario comparison would require an explicit narrated reset and more time; omit it from this short version unless the script intentionally teaches it.

## M2S11 — Containment and recirculation

**Current defect.** Cool and warm tokens traverse two short straight connectors (1.1–4.5 s and 4.5–8.0 s), then vanish. No return to a cooling unit, no recirculation into an inlet, no physical separation/barrier, and no before/after effect is drawn. The central sentence asserts the lesson the motion fails to demonstrate. The final 1.9 s is the original static diagram without tokens.

**Proposed storyboard.** Show an equipment row with recognizable inlet/exhaust sides, a supply route and a return route. Use one large room section, not three disconnected boxes. Start with a clearly labeled “Mixing” condition and change to “Separated paths” on the containment phrase. This is an explicit comparison, not a spontaneous operating change.

| Narration phrase anchor | Instructional action and hold |
|---|---|
| “When exhaust mixes back into the intake stream” | One warm exhaust cohort follows a visible recirculation route into the inlet stream; a labeled inlet-condition swatch shifts warmer. Show both intended return and unwanted recirculation so the problem is spatially understandable. |
| “some equipment can receive warmer air than intended” | Hold the affected inlet and the mixed path. Avoid a numerical temperature or efficiency claim unsupported by the script. |
| “supply air through equipment” | Follow one cool cohort into the equipment and a warm cohort out. If briefly isolating the intended route, retain the mixing condition as a faint comparison; do not silently pretend it has already been solved. |
| “shows a separate return path” / “Containment supports that separation” | Introduce the physical containment boundary and visibly label the transition to the second condition. The former recirculation route becomes blocked/inactive; route warm exhaust toward the return. Supply and return remain spatially separate. |
| “appropriate airflow, cooling capacity and controls” | Hold separation and highlight those three requirements with a simple inlet-monitor symbol. Barrier presence is not presented as measured thermal compliance. |
| “every equipment inlet receives the conditions it needs” | Finish on the complete supply → equipment → return arrangement, with the inlet inspection point emphasized. Keep a small labeled before/after inset only if legible at actual slide size. |

The causal change is reduced mixing due to a barrier and controlled paths. Do not imply containment removes heat by itself, guarantees perfect isolation, or guarantees every inlet temperature. Avoid flashing an all-green “safe” gauge merely because a wall appears.

## M3S9 — Rack capacity budgets

**Current defect.** Three bars interpolate independently from 18/24/30% to 55/82/100%, with no visible rack or equipment addition. Fractions are only in source code: there is no scale, quantitative label or explanation of the denominator. Cooling reaches its limit at 9.6 s; the state is then held for 2.4 s. The relationship is relevant, but the current motion resembles a generic progress animation.

**Proposed storyboard.** Put a simplified rack and staged candidate equipment on the left; place three aligned, explicitly normalized budget bars on the right. Each insertion causes one discrete set of increments, then a hold. A quiet label says “Illustrative used share of each allocation.” Rack space, electrical capacity and cooling allocation have separate denominators; they are not interchangeable quantities.

| Narration phrase anchor | Instructional action and hold |
|---|---|
| “Adding equipment” | Insert the first visibly identifiable device into an empty rack position. The space bar increments because an actual position is filled. |
| “electrical demand, heat-removal requirements and network traffic” | Associate that same device with changes in power and cooling bars; indicate the network connection/traffic qualitatively without inventing a quantitative network limit. The three bar increments occur together, with unequal normalized amounts. |
| “at different rates” | Add another device and hold the new values long enough to compare changed shares. No free-running bars. |
| “the cooling allocation reaches its limit” | Complete a final authorized example insertion that brings cooling exactly to its allocation boundary; stop all increases. Change cooling's label to “Limit reached,” with a clear 100% tick. |
| “while mounting space remains available” | Emphasize remaining rack slots and the unfilled space budget beside the full cooling budget. This comparison must be simultaneous and remain readable. |
| “not a recommended rack design” | Keep the illustrative qualifier visible; pause the diagram rather than filling it with disclaimer prose. |
| “identify the limiting budget before deciding that another device can be installed” | Stage the next candidate outside the rack with a “Review capacity” decision; do not install it or increase any bar. Hold the complete constraint comparison to the end. |

A clean optional illustrative series is space 20→30→40→50%, power 25→45→65→85%, cooling 25→50→75→100%. If used, label it explicitly as separate illustrative allocations and update the script to explain the example. Alternatively retain the existing endpoints and choose transparent equipment increments. Never imply that electrical watts and heat watts have these different physical ratios: the bars compare fractions of independent available budgets. Keep all values constant between additions.

## M4S7 — Virtual activity and physical demand

**Current defect.** Four stacked rectangles merely change fill at 1.2, 3.6, 6.0 and 8.4 s. All arrows point down but do not distinguish dependency, work or energy. VM and hypervisor share one box; host CPU/memory/storage/network resources are not visible. There is no change in application activity, allocation or resource demand. The 12 s clip repeats while the 31.858 s narration discusses containers and physical consequences.

**Proposed storyboard.** Two guest VM boundaries above a hypervisor on one physical host. Inside the host show distinct CPU, memory, storage and network resource areas. Outside, show power entering and heat removal leaving. Use a separate short container comparison inset during its sentence, then return focus to the VM example. Preserve the container sentence's coverage.

| Narration phrase anchor | Instructional action and hold |
|---|---|
| “logical computing environments on physical resources” | Show two visibly separate guest environments sharing one physical-host boundary. Logical separation remains legible without implying separate physical machines. |
| “a hypervisor manages the guest systems and their access” | A small number of work/resource-request tokens pass through the hypervisor to host resources. Highlight mediation and sharing; do not animate decorative arrows between generic layers. |
| “Containers provide another arrangement” / “share the kernel” | Show a compact clearly labeled alternative with two containers over a shared host kernel. This is an explicit comparison, not VMs morphing invisibly into containers. Do not put the hypervisor label under this alternative or imply every VM shares the same guest kernel. |
| “The animation traces a virtual machine’s physical dependency” | Return the visual emphasis to the labeled VM example. Keep the main host topology stable. |
| “More activity in an application” | Increase a finite visible batch of pending application work. The increase is the cause of the next changes. |
| “more demand on processors, memory, storage and networks” | Raise corresponding qualitative/illustrative host resource use by different amounts as work is processed. These are four distinct requirements, not one interchangeable reservoir. Avoid unexplained exact percentages or a claim of identical linear growth. |
| “consequences for electricity and heat” | Show a modest increase in illustrative power demand and heat-removal demand after the workload/resource change. Do not imply memory allocation alone causes an immediate fixed power increment. |
| “doesn't remove their physical limits” | Hold the higher-demand state with finite host capacity clearly bounded. Leave visible headroom or a neutral capacity marker; do not introduce an unspoken overload/failure. |

Meaningful motion requires a workload change propagated through the virtualization layer to resource demand, not just another sequence of highlighted architecture boxes.

## Final review required after implementation

Send Astra the final scripts/WAV hashes, measured WAV durations, aligned phrase timings (including the alignment method and uncertainty), editable timeline definitions, encoded MP4s/posters, current figures' flags/text inventories, and player test results. Include before/after transition frames at native resolution plus the complete playback evidence. Review the actual generated module pages at desktop and narrow widths and in enlarged-media view.

Acceptance is two-dimensional: each narrated causal claim must have a corresponding visible cause/change/result, and each major change must land on its correct spoken clause. A technically synchronized but instructionally empty stretched loop fails. A good explanation drifting ahead of or behind the narration also fails.

Check start, pause/resume, arbitrary seek into every scene, speed changes, end hold, replay, slide leave/return, zoom synchronization, review-mode pause, narration preference, and reduced-motion final-summary behavior. Seeking must reconstruct the full appropriate visual state without requiring earlier scenes to have played. Reduced-motion and muted viewing must retain a useful caption and static conclusion. Keep imported videos and an audio-only slide as regression controls.

After shared player/renderer edits, run the maintained `test_video_seek.mjs`, `test_video_playback_compatibility.mjs`, `test_video_modes.py`, and `test_video_modes_browser.mjs` checks, plus the applicable narration/control and quiz/resume checks. Verify exactly five figures opt into sync, all ten imported originals are preserved, and four-SCO SCORM identity/architecture is unchanged. Run media geometry, source/course QA and package validation; do not create a ZIP, commit or push as part of this audit.

At 30 fps, check duration within one frame and sample first/25%/50%/75%/final plus both sides of every transition. Inspect native/200% decoded detail against lossless source frames, with target SSIM ≥ 0.995 and PSNR ≥ 45 dB when measured; reject visible artifacts regardless of score. Verify the final encoded frame is the true held conclusion with no partial second pass. Refresh visible media text inventory/hashes and any glossary first-use evidence after the video changes.
