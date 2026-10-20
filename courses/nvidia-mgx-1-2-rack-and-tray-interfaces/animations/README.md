# Teaching media

The seven silent 1920 × 1080, 30 fps videos in `../figures/` are retained approved
outputs. `build_media.py` is the editable Pillow compositor. It reads the course
definition, local fonts, source drawing crops, and the 241 lossless HPM poses in
`assets/hpm/`. The poses were rendered from the supplied full-size fanless HPM
STEP geometry. Geometry is retained; display groups separate by height. These
positions do not describe verified disassembly, joints, or actuation.

| Video | Slide | Master duration | Playback |
|---|---|---|---|
| rack_build_up | M1S4 | 88.468 s | Narration-synchronized single pass |
| hpm_exploded | M2S4 | 92.044 s | Narration-synchronized single pass |
| bay_depth_cases | M3S5 | 20 s | Short loop |
| busbar_layers | M4S7 | 20 s | Short loop |
| blind_mate_float | M5S6 | 94.830 s | Narration-synchronized single pass |
| force_budget | M6S3 | 92.880 s | Narration-synchronized single pass |

Install Pillow and FFmpeg (`FFMPEG_BIN` can select an executable; an installed
`imageio-ffmpeg` is also supported). Run from this course folder:

```bash
python animations/build_media.py --preview
python animations/build_media.py hpm_exploded
```

With no asset name, the second command regenerates all six. Previews and logs go
to ignored `_analysis/video_review/`. When paired narration WAV files exist,
synchronized durations come from their actual frame counts. Otherwise the builder
uses the approved measurements in `reviewed_timing.json`. If narration changes,
copy the new paired WAVs into the course's ignored `audio/` paths before building.
The single-pass scenes follow paragraph-weighted landmarks and hold their final
state. The encoded duration rounds to a 30 fps frame.

Retained teaching videos are byte-identical to the delivered course. Existing
reviewed media-text inventories in `course.json` are bound to those file hashes.
After intentionally changing a figure or video, review its visible text and
refresh its inventory and hash before rerunning source QA and packaging.
`verification.json` records representative encoded fidelity from the delivered
build. It is evidence for those retained outputs, not for a future regeneration.

`lms_poster.html` is editable source for the 800 × 400 catalog thumbnail and uses
the local Open Sans stylesheet. Runtime course HTML is generated separately.

## Summit reference-design media

`build_summit_media.py` creates the 20-second `summit_power_path.mp4` loop and
`summit_power_contact_cooling.png` from editable layout source, local fonts, and
the retained exact source-view crops in `assets/summit/`. The original deck is
not required to regenerate these assets. The power path retains the separate
800 VDC strings and shared low-voltage rack busbar. The contact figure retains
the source's TBD labels and identifies the 2036 A clip as a component example.

```bash
python animations/build_summit_media.py --preview
python animations/build_summit_media.py
python animations/verify_summit_media.py
```

The verifier decodes all 600 video frames and compares seven representative
frames against the native compositor. `summit_verification.json` records the
retained output's results. Preview logs and decoded frames remain ignored.
The original media builder now resolves its target slide by the figure filename,
so an inserted slide cannot silently select a different narration timeline.
