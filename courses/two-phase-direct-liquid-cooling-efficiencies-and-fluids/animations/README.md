# Narration-synchronized videos

The user approved the three previously suggested single-pass videos on
2026-10-11. M1S4, M2S5, and M4S4 follow the existing approved English WAVs;
no narration was regenerated. The video is silent and the slide WAV is the
only audible track. Each conclusion holds rather than restarting.

`storyboards.mjs` is the editable visual source and sentence-boundary cue
list. `reviewed_timing.json` records the reviewed assets, measured durations,
reference narration hashes, and poster positions. The MP4s and PNG posters
are course assets, not disposable build intermediates. The original static
SVGs remain available as editable reference diagrams.

## Re-encode

Use Node.js, Playwright with an installed Chromium browser, and a full FFmpeg
build with `libx264`. From this course's source directory:

```bash
node animations/render.mjs /absolute/path/to/built-course all preview
node animations/render.mjs /absolute/path/to/built-course all encode
```

Select `M1S4`, `M2S5`, or `M4S4` instead of `all` to render one sequence.
`FFMPEG_BIN` selects FFmpeg, `PLAYWRIGHT_CHANNEL=chrome` selects installed
Chrome, and `PLAYWRIGHT_MODULE` can select an absolute Playwright module.
`ACADEMY_VIDEO_QA_DIR` selects an intermediate review folder (otherwise the
system temporary folder is used). Frame captures and encoder reports are
not public course assets.

The renderer captures native 1920x1080 browser PNGs and encodes silent H.264
at 30 fps, CRF 8, with explicit BT.709 color handling. Duration must match
the measured narration within one frame. Text inside diagram shapes is
checked for an inset of at least 20 pixels. Review the sampled and decoded
frames before updating the figure text inventory in `course.json`.

## After narration changes

The ordinary course build uses the committed MP4s. Narration timing is not
guaranteed to survive a new TTS rendering, even with unchanged text.
After regenerating the paired WAVs, remeasure their sentence boundaries,
update the cues and duration, and re-encode these videos. The renderer
rejects an unreviewed duration change. A duration match alone is not proof
of cue alignment; review narration and video together after any audio edit.
Update `reviewed_timing.json` and the hash-bound figure text inventories
after visual review. Do not commit generated narration audio.

## Technical review scope

- M1S4 arrows carry heat; they are not pipes connecting the two fluids.
  Preserve the FWS box straddling the dotted boundary and straight arrow
  approaches into the FWS and heat-rejection boxes.
- M2S5 liquid circulation is design dependent. The pump inlet subcooling
  requirement applies to pumped designs; it is not imposed on passive ones.
- M4S4 is a conceptual sequence, not an equipment-specific purge procedure.
  Hollow orange circles distinguish air from working-fluid vapor. Gas is
  removed through a dedicated system connected to a buffer port, not vented
  to the room. Bubble counts and event spacing are illustrative; there is
  no numerical alarm threshold. Follow the Treatment Plan and Owner's Manual.

Small moving markers depict continuous heat/fluid transport. They stop at
the conclusion; no fill, gas-accumulation, or purge event resets in the pass.

All three videos position moving markers on the actual displayed SVG
shafts, including rounded bends, rather than polyline approximations.
Markers fade at the ends and stay clear of boxes, arrowheads, and the
temporary pump symbol. M1S4 uses one small marker per short connector;
M2S5/M4S4 also use single markers on short feed/return connections, while
their long liquid-return and purge routes retain spaced markers. Green
liquid and purple working-fluid vapor stay solid; orange air markers stay
hollow. Run `node animations/test_motion.mjs` to check every encoded-time
frame of all three videos for centerline alignment, marker count, size,
and endpoint/pump clearance.
