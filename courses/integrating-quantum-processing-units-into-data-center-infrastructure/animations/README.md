# Quantum Teaching Animations

`render_teaching_videos.cjs` is the editable source for the course's four silent teaching videos. Checked-in WebM files and PNG posters are used by normal course builds; no animation dependencies are needed to build the SCORM package.

| Scene | Slide | Asset | Teaching Purpose |
|---|---|---|---|
| `hybrid` | M1S5 | `hybrid_infrastructure_context.webm` | Shows the QPU as a specialized resource within a classical orchestration, control, measurement, and facility context. |
| `critical` | M2S5 | `hybrid_quantum_classical_loop.webm` | Traces orchestration, control, execution, and measurement/adaptation around the low-latency round trip. This is an interpretation of whitepaper Figure 5, not a reproduction. |
| `site` | M3S3 | `quantum_site_readiness.webm` | Brings vibration, electromagnetic conditions, utilities, and physical access into the site survey. |
| `production` | M4S3 | `pilot_to_repeatable_operations.webm` | Connects a pilot deployment through a common infrastructure envelope to repeatable monitoring and service. |

## Reproduce

Use Node.js with Sharp installed and a full ffmpeg build with `libvpx-vp9`. From the course folder:

```bash
node animations/render_teaching_videos.cjs --states-only
# Run the shared arrow checker and review the updated SVG states before encoding.
node animations/render_teaching_videos.cjs
```

Set `FFMPEG_BIN` when ffmpeg is not on `PATH`. Pass one or more scene names to render only those assets, for example `node animations/render_teaching_videos.cjs critical site`. Sharp can be installed in a parent Node project or exposed through `NODE_PATH`.

Each source timeline is sampled once into lossless 1920x1080 PNG frames and encoded as lossless VP9 with 4:4:4 chroma, 15 fps, 150 frames, and no audio. Duration is exactly ten seconds. All scenes finish and hold their ending before the course player restarts the loop. The poster samples 9.9 seconds at 960x540. Narration synchronization is not enabled.

The renderer also writes the final SVG source states under `reference-states/`. These make the diagram geometry reviewable by the shared arrow checker. Fonts are Avenir Next with an Arial fallback; ensure the same font availability for matching typography.

## Review After Editing

Before encoding, refresh the source states with `--states-only`, then run the shared SVG-arrow checker against `course.json`. Inspect labels and connectors at full size. The M2 triangle markers are referenced at the midpoint of their flat backs, and each shaft stops 18 source units before the destination boundary so the tip lands on that boundary.

After encoding, review the first, 25%, 50%, 75%, final, and transition frames, then watch or scrub a complete muted loop. Verify the final second does not restart. Compare decoded frames with lossless sources at native size and 200% detail, targeting SSIM >=0.995 and PSNR >=45 dB after consistent color-range normalization.

Update the affected figure's `text_inventory` hash in `course.json` only after reviewing the visible media text. Rerun the course source QA after any media or text change. A passing geometry checker or fidelity metric does not establish browser or LMS behavior.
