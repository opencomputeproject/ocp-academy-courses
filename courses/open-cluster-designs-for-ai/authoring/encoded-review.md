# Encoded video review — baseline 29 October 2026

Accepted all five encoded assets. No blocking issues found. M3S4 was subsequently retimed for the Clos pronunciation correction; its current checks and hashes are in `clos-pronunciation-retiming-qa.json`.

Reviewed 232 decoded samples spanning the full finite timelines: 2.5-second intervals plus every cue and six cue-relative checkpoints, initial and near-final frames. Each sample was compared with a fresh source render at the same 24 fps timestamp. All five dense sheets, native final frames and paired 200% text/connector crops were visually inspected.

The encodes preserve stage order, connector meaning, label readability and complete final pictures. Mild chroma/antialias edge differences and slightly muted green are visible at 200%, but do not impair instruction. Sample RGB PSNR ranges from 37.70 to 41.50 dB. No decode errors. All encoded durations differ from their paired WAVs by less than one frame.

- M1S4: Compute domain grows into OPG-M then XOC-N; boundaries and shared resources persist. Final domain-vs-rack reminder is complete.

- M2S5: Breakout reaches N1 NIC1 and NIC5 without numbered physical legs. Distinct SOL1 port2 optical-module port1 to SO1 port1 optical-module port1 uplink and O1S1 alias are legible. Arrowheads remain outside targets and appear on completed lines.

- M3S4: Same schematic hardware retained. Clos selected hosts share Leaf A; rail1 paths share Leaf A, rail2 paths reach Leaf B; cross-rail spine path appears subsequently. No performance-superiority claim introduced.

- M3S7: Minimal omits backend while preserving gateway, front-end/storage and both management roles. Distributed panel adds backend for cross-host dependencies; no Training profile conflation.

- M4S5: One packet persists as Day0, Day1 and Day2 evidence accumulates; declared and observed columns remain distinct. Final measured-outcome comparison and reminder are complete.

## Scope limits

This was sampled whole-timeline review, not a visual watch of every frame. No narration listening or course-runtime audit was performed; those remain with parent QA. Cue timings remain editorial estimates, not forced alignment.

Detailed frame images and dense comparisons are retained in the local authoring workspace outside Git. Source and encoded hashes, scope, measurements and decisions: `encoded-review.json`. No narration, media, source, or course configuration was changed.
