# FCSA video source QA and handoff

All five deterministic render sources are stable for production. Only the five module render files and `fcsa_helpers.py` were authored; course, audio, static figures, shared primitives and runtime were not edited. Sol owns encoding, decoded-quality review and actual-course tests.

## Final audio timing

The helper reads `audit/video-timing.json`, notices when it appears or changes, and rejects mismatched scene counts. Each render uses the current aligned duration. The exported `DURATION` and `POSTER_SECONDS` constants are set at import, so use a fresh process after changing the timing file.

| Sequence | Measured WAV duration | Poster | Final two-second hold |
|---|---:|---:|---:|
| M1S3 | 51.691519 s | 50.691519 s | 49.691519 s onward |
| M2S3 | 55.546803 s | 54.546803 s | 53.546803 s onward |
| M3S5 | 52.944626 s | 51.944626 s | 50.944626 s onward |
| M4S4 | 55.683265 s | 54.683265 s | 53.683265 s onward |
| M5S3 | 55.871927 s | 54.871927 s | 53.871927 s onward |

## Checks performed

- Parsed valid SVG at every 30 fps source time plus exact scene boundaries and adjacent samples: **8,198 sample times**.
- Measured Open Sans text safe area and contained-label clearance using actual font metrics; **zero remaining flags**, minimum label font 46 px and at least 0.75 em containment clearance.
- Confirmed each final two-second interval renders the same static state, with no autonomous reset or replay.
- Inspected five contact sheets and selected full-native frames, including the revised multi-line label, Compute Tile comparison, boot image routes, final signal directions, evidence/policy convergence and aggregate-demand review.
- Generated 78 SVG/PNG keyframes at 15%, 50% and 85% of every scene. The updated `native-samples/samples.json` records exact final-timeline times.
- No audible playback, audio generation or video encoding performed. No claim is made that source checks replace complete muted playback or course-player QA.

## Intentional relationships and overlaps

### M1S3

- Solid line preserves a functional relationship across the partition.
- Dashed line in New configuration denotes a relationship still requiring review.
- Document labels are review topics, not certification results.
- Intentional overlap: At the initial partition position the two architectural unit boundaries touch; separation exposes a retained relationship. This is an architectural partition, not a manufacturing action.

### M2S3

- The Compute 1–Hub line is a generic architectural relationship.
- The memory branch illustrates direct access; it does not require on-chip DRAM.
- Open circular function bullets are not checkmarks or completion indicators.
- A second Compute 2 enters the explicit comparison view; roles do not migrate in a live system.
- No intentional occlusion.

### M3S5

- Manager left and Subordinate right are persistent throughout all named comparisons.
- Distributed image B travels through manager before subordinate; shared images fetch from one NVM; independent images fetch from separate NVMs.
- Ready/Error arrows point from subordinate to manager; Proceed points in the reverse direction.
- Error case is explicitly labelled and introduces no recovery or later Proceed.
- Intentional overlap: NVM storage is painted over emerging image papers so the paper emerges from storage. Moving papers are deliberately blank; Image A/B is labelled only on arrival, avoiding clipped text.
- Intentional overlap: An image paper crosses a component boundary during image loading; its own text remains contained by the paper.

### M4S4

- Evidence travels from chiplet B toward the primary, while local responsibilities stay at B.
- Evidence and Composition + policy converge separately on Appraisal; evidence is not depicted as overwriting policy.
- Optional Secondary RoT service points toward System RoT; composition decision stays at System RoT.
- Earlier evidence remains visible after Debug state changed; Revalidate is unresolved, not a security pass.
- No intentional occlusion.

### M5S3

- The adaptation shape change completes before transfer begins; the interface remains visibly to its right.
- Requesters A/B remain when C joins. Lines represent combined demand scope, not a mandated snoop-filter interconnect or equal demand quantities.
- Level 1 and Full in the final summary identify rule scope, not compliance achieved by the pictured design.
- Intentional overlap: The transaction paper crosses source/target silhouette edges and occludes the generic path during transfer. This is the data movement being taught; the text stays in its paper.

## Static figure review

The five main-owned statics were inspected at native resolution. Reported label-padding/size and geometry fixes are listed in `FCSA_SOURCE_QA.json`; Sol reports applying them. No other factual issue was found in these simplified views. Astra did not edit the static files.

## Production artifacts

- `tools/synced_video/m1.py` through `m5.py`: complete native SVG render functions.
- `tools/synced_video/fcsa_helpers.py`: local drawing and dynamic timing helpers.
- `FCSA_SOURCE_QA.json`: exact durations/cues, per-module text inventory, intentional overlaps, source hashes and check summary.
- `native-samples/`: source SVGs, lossless PNGs, contact sheets, sample timestamps and reproducible font checks.

The earlier storyboard JSON remains the source/provenance and narration plan. Its provisional durations are superseded by `audit/video-timing.json`; this QA manifest records the actual aligned implementation.
