# Astra source-scene review

2026-10-24. Review of the first narration-aligned SVG/JavaScript source build, before encoding. No narration was played aloud. No source, script, media asset, or player template was edited by this review.

## Method and overall assessment

Inspected `source-build-records.json`, all five timeline files, word timestamp schemas, the generator `_work/build_synced_media.py`, 139 native-resolution screenshots covering first/final and every narration anchor's start/mid/end, and per-video contact sheets. Screenshots and state records are in `source-audit/`; `box-clearance.json` records measured local SVG clearances. All five final → zero → final renders reproduced identical SVG state. These are deterministic sources, not playback loops; arbitrary-time reconstruction is credible from source inspection. Final encoded video/runtime acceptance remains outstanding.

The timing source is ElevenLabs Scribe v2 timestamped transcription checked against the approved scripts, **not** forced alignment. Its provenance is correctly recorded inside timeline beats; the generator's introductory docstring still calls the inputs forced alignments and should be corrected. Any regenerated narration needs new timestamps and hashes before rendering. The timestamp values are measured ASR estimates, not independently listened-to phonetic boundaries.

This is a substantive upgrade. Rack insertion now causes unequal capacity changes; power has a source loss, declining reserve, generator readiness and selected backup; the service sequence returns a response to the origin; the virtualization scene introduces increased work before increased physical-resource demand. These are more than timed box builds. Containment and the final power/heat consequences initially remained too dependent on labels/opacity; specific fixes are below.

## First-pass findings sent to the builder

### M1S4 — topology and icon placement

- **Required:** the original replacement's request path at y195 and response path at y390 bypassed the `Network` rectangle (x390–590, y225–350). Highlighting the box did not make it part of the route. Each path must visibly enter and leave the network; active tokens must follow that route.
- **Required:** the returned document at x127,y285 overlapped the centered “Your device” label, visible from response completion through the final hold. Use a dedicated label row and icon area.
- **Required:** the stored-document bottom at y332 exceeded the storage card's bottom y305. Keep the persistent document inside an enlarged/rearranged card with clearance.
- The correct principle is a retained source document plus a returned view/result, not moving the sole document out of storage. The current opacity change preserves that principle.
- Physical support is present before it is emphasized, which avoids implying that electricity/cooling only become necessary after the request completes. Consider a support connection to the network too if the drawing is intended to describe all depicted infrastructure.

### M2S6 — reserve continuity and readability

- **Required:** source loss initially occurred at8.72s, but the reserve route/discharge started10.42s. During that1.70s interval neither input source nor reserve was visibly active, despite a continuous equipment-supply trace. Activate reserve when the utility fails; use the “stored energy” phrase for emphasis rather than delayed operation.
- **Required:** the reserve-level gauge crossed the second line “reserve.” Separate title and gauge vertically.
- **Required:** “Upstream distribution / and source selection” had only6.34 SVG px left/right clearance at23px type; the maintained0.75em minimum is17.25px. Increase available width or use a more compact multiline label at readable size.
- **Recommended:** add event markers or a short maintained-supply label to the equipment trace so it is unmistakably a qualitative continuity trace, rather than a generic progress line. Mark utility loss and backup selection at their real timeline positions; no literal seconds are needed because event spacing is explicitly expanded.
- Correctly distinguishes starting, ready-but-unselected and selected backup. No utility/generator parallel connection is implied once source opacity works. The upstream/downstream distribution distinction reconciles the unchanged narration.

### M2S11 — physical intervention and its timing

- **Required:** the first replacement still depicted three functional boxes plus a small floating horizontal green patch over a dashed recirculation line. It named containment but did not clearly show a partition separating inlet and exhaust regions. Place a recognizable boundary beside/around equipment or its return region; attach it spatially to the separation being taught.
- **Required:** barrier, “separated” state and blue inlet changed instantaneously at11.82s (“a separate return path”). The containment phrase13.66–15.68s triggered no change at all. Use11.82–12.96s to inspect/highlight the intended return, then introduce the physical separation across the containment phrase and suppress the recirculation route as that intervention occurs. A finite redirected warm cohort would make the cause and result visible.
- **Required:** move the long state label away from the vertical recirculation segment; it currently crosses the label region. Keep text and flow paths disjoint.
- Keep the good caveat: “Reduced recirculation · verify inlet conditions” plus airflow/capacity/controls avoids claiming that a barrier guarantees acceptable inlet conditions. A blue qualitative inlet indication should mean less mixing, not a certified temperature. No numeric thermal reduction is justified by this narration.

### M3S9 — strong cause/result, improve explanation timing

- The rack and normalized budgets now tell a meaningful story: two installed devices initially, one addition changes all three budgets by unequal amounts, a second reaches cooling100% while space50% and power82%, and the next device remains outside the rack as a review decision. The arithmetic agrees with eight rack positions and four filled final slots. The independent-allocation qualifier prevents interpreting the bars as direct power-to-heat ratios.
- **Required for close narration alignment:** the first addition and all its budget increases finished at1.40s, while “electrical demand…” begins4.26s and “at different rates” begins7.66s. Stage the candidate at the opening and perform its insertion/unequal increments during the demand clause, or retain insertion but add explicit delta comparisons/attention while the consequences are spoken. Avoid a6-second early reveal with no visual emphasis during the explanatory phrase.
- The second addition correctly occurs10.64–12.32s, on “cooling allocation reaches its limit.” Final hold and review decision are clear. No unnecessary extra rack animation is needed.

### M4S7 — physical demand and alternative architectures

- **Required:** the first replacement's “consequences for electricity and heat” only recolored the two bottom boxes at about25.69s. Show an actual qualitative increase in power and heat-removal demand after the application/host-resource change. Use bounded illustrative bars or flow thickness, not exact unsupported physical numbers.
- The labels “Guest VM A/B,” “Hypervisor mediates access,” “Container A/B,” and “Shared host kernel” are individually appropriate for the stated examples. No container is incorrectly labeled as a VM, and the container label does not claim separate guest kernels.
- **Required for clarity:** the full-strength VM panel and container panel simultaneously fed “One physical host,” which can look like one combined deployment rather than another arrangement. Label the container view as an alternative, fade the VM teaching focus during its comparison sentence, and restore VM focus at16.40s. This can preserve the shared physical-dependency lesson without asserting a particular combined stack.
- Connect both container boxes to the shared kernel. They initially floated above it without an explicit relationship. Guest B can also have an access connector to make shared hypervisor mediation clear; distinguish the active workload path for A.
- The application work batch rises19.52–21.16s and distinct physical-resource bars rise22.08–24.38s. This gives the quantitative/causal sequence the old loop lacked. Keep those bars as illustrative demand; do not imply identical units or exact proportional electricity scaling.
- `hypervisor` box vertical clearance was18.5px against18.75px required, a minor geometry adjustment rather than a pedagogical defect.

## Builder updates during review

The builder reported and source inspection confirmed an interim repair of network traversal, storage containment, immediate reserve activation on utility failure, reserve-label/gauge separation, trace completion before the conclusion, and quantitative/qualitative M4 power/heat demand bars with increased flow width. The returned-document label overlap, upstream text clearance, containment intervention/timing, rack first-addition timing, and explicit alternative-arrangement treatment were communicated in the consolidated follow-up. Recheck the final regenerated sources after those repairs; do not treat first-pass screenshots as evidence of the latest state.

## Source acceptance still requires

Re-render all repaired states at1920×1080 and at actual slide size, check transition-adjacent frames, and confirm source final hold stops all unrelated motion. Verify that every important change agrees with the narration clause, with ASR uncertainty stated honestly. Then encode exactly one complete source pass to match the current final WAV within one video frame; perform decoded-frame quality, muted full-pass playback and synchronized actual-player checks. Source-scene success alone is not approval of an MP4 or the runtime.

## Focused source acceptance after consolidated repairs

**Result: design and instructional source scenes accepted; no remaining design blocker.** This acceptance covers the explicitly labeled `interim v2 geometry review` sources and their causal structure. It does not approve the forthcoming v4 timestamps, encoded MP4s, or integrated player.

Re-rendered91 native anchor midpoint/end/final states from the regenerated sources, inspected their contact sheets and the important repaired states at1920×1080, and replayed those states in reverse seek order. All91 reverse-order renders matched their corresponding forward-order SVG exactly. Evidence and source SHA-256 values are in `source-acceptance/frames.json`.

- M1: request/response visibly traverse the network; response returns to the source device; the stored document remains inside storage and the returned icon clears the device label. Physical-support emphasis remains available for the narration.
- M2: source failure immediately activates reserve delivery and discharge, preserving the visible supply chain. Generator readiness and selection remain distinct. Reserve title/gauge and distribution labels are legible. The illustrative equipment-supply trace stops before the final hold.
- M2 containment: the room, inlet/return regions and physical return-side enclosure now make the spatial relationship understandable. The enclosure installs during the containment phrase while recirculation fades. Earlier supply/return inspection phrases retain their matching flow tokens. The final state retains inlet verification and the airflow/capacity/control caveat; it does not assert a numerical temperature result.
- M3: the candidate is staged outside, and insertion plus unequal budget increases occur during the demand clause. The second addition reaches the cooling allocation on its corresponding phrase, with mounting space visibly remaining. One final draw-order defect was found and repaired: incoming devices had been partially hidden by later slot backgrounds. The builder moved all devices above slot backgrounds. Six fresh25%/50%/75% insertion captures were produced; the native demand-mid and limit-mid frames confirm complete, intact moving devices. See `source-acceptance/m3-layer-fix.json` for the repaired source hash and evidence.
- M4: the container panel is explicitly an alternative, both containers connect to the shared kernel, VM focus dims during that comparison, and the main VM path remains separate. Added application work precedes distinct host-resource increases, followed by power/heat-demand bar increases. The bottom cards and conclusion are separated. This is now a visible cause-and-result explanation, not a sequence of box highlights.

The proposed optional event labels on the M2 supply trace would be a useful refinement, but are not a blocker: the active source/reserve routes and state labels already establish the continuity relationship.

Next review must use newly transcribed word timestamps from the final v4 WAVs, verify unchanged script coverage and duration/frame agreement, then inspect actual encoded frames and synchronized playback. Reusing the interim-v2 timing is not covered by this design acceptance.
