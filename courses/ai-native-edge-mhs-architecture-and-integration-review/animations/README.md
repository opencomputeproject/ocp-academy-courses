# Teaching video authoring

These sources rebuild the three silent, narration-synchronized teaching videos. The committed HTML, SVG and timeline files are sufficient; no provider account, narration regeneration, original PDF or original CAD download is required for a video-only rebuild.

| Stem | Slide | Encoded duration |
|---|---|---:|
| `video_m1s6_fixed_floating` | M1S6 | 78.733333 s |
| `video_m2s3_datum_interfaces` | M2S3 | 84.400000 s |
| `video_m3s6_evidence_debrief` | M3S6 | 84.133333 s |

The videos play alongside narration, not as additional learner time. Keep `sync_to_narration: true`, `autoplay: false`, `loop: false`, and `muted: true` in the course source. Each encoded asset contains one master pass and holds its completed final state. Preserve `narration.teaching_video_mode: "narration-synchronized"`.

## Setup and rebuild

Run the following from this `animations/` directory. Use Python 3.9 or newer and Node.js 18 or newer. The lockfile pins Playwright 1.61.1, the authoring version used for these assets. Install an FFmpeg build with `libx264` and put it on `PATH`, or set `FFMPEG_BIN` to its executable. The original build used FFmpeg 4.4. Do not rely on the limited FFmpeg bundled with browser-test tools.

```sh
npm ci
npx playwright install chromium
python3 build_video_sources.py

for stem in video_m1s6_fixed_floating video_m2s3_datum_interfaces video_m3s6_evidence_debrief; do
  node record_css_animation.mjs "$stem.html" "../figures/$stem.mp4" "../figures/${stem}_poster.png"
done
```

The local encoder is a snapshot of AcademyWizard's `record_css_animation.mjs`; only the workstation-specific FFmpeg fallback was removed. It captures lossless 1920×1080 PNG frames at 30 fps and encodes silent H.264 at CRF 8. Duration and poster time come from the HTML, which is generated from the saved timeline. Do not pass an arbitrary duration override. The timeline remains the authority when rebuilding existing media.

Font rendering can differ across operating systems: the sources use Arial with Helvetica and sans-serif fallbacks. Review text fitting and visual fidelity on the rebuild host. Identical source and timing do not guarantee a byte-identical encode across browser, font or FFmpeg versions.

## Review a rebuilt asset

```sh
python3 ../authoring/toolchain/scripts/check_svg_arrows.py . --fail-on-flags
node qa_media.mjs video_m1s6_fixed_floating video_m2s3_datum_interfaces video_m3s6_evidence_debrief
node playback_qa.mjs video_m1s6_fixed_floating video_m2s3_datum_interfaces video_m3s6_evidence_debrief
```

The arrow checker is the pinned AcademyWizard helper in the course's authoring toolchain. `qa_media.mjs` captures source checkpoints and reports visible text. `playback_qa.mjs` plays each encoded file once, muted and at normal speed, retaining progression frames, monotonic-time checks and an end-hold check. `inspect_sources.mjs` is a smaller five-checkpoint source-only inspection helper. These helpers create the ignored `qa/` directory themselves.

Inspect the actual encoded first, quarter, middle, three-quarter and final frames; inspect transition-adjacent frames and scrub a complete pass. Check label containment, geometry, continuity, final-state hold and representative native/200% details. Compare decoded quality with the lossless source in a consistent color space. Recheck the actual course player, including narration seeking, speed, enlarged view and ending. Do not treat source-text extraction as proof of encoded text legibility.

`video_media_inventory.json` records reviewed asset hashes, visible phrases at verified readable times, durations and QA summaries. Any changed MP4 requires visual review and a new matching inventory digest; never refresh the digest automatically to silence QA. Keep the course figure's `text_inventory` and `duration_seconds` synchronized after review. The existing inventory remains valid for the unchanged delivered media.

## Optional source-input workflows

The frozen timeline files contain the measured narration durations and scene times. `narration_master` is a course-relative reference to the WAV used during original authoring; that WAV need not be bundled with this repository. Receipt/alignment paths are provenance references to external authoring records, not claims that those provider records are committed. None of these external files is needed for the normal rebuild above.

Only retime when narration actually changes. Supply an external directory containing `v4-masters/*/receipt.json` and `narration-alignments/<text_sha256>.json`:

```sh
python3 sync_narration_timing.py --authoring-root /path/to/authoring-inputs video_m1s6_fixed_floating video_m2s3_datum_interfaces video_m3s6_evidence_debrief
```

Receipts must provide the matching output filename, `text_sha256`, `output_sha256`, `final_seconds` and `tempo_factor`. Alignment files must contain `alignment.characters` and `alignment.character_start_times_seconds`. The helper matches the scripted phrases and divides native provider timestamps by the receipt's measured tempo factor. A missing phrase or non-unique receipt stops the operation. Rebuild and review the media after retiming; do not retain old hashes.

The checked-in `cad_class_l_top.svg` is an edge projection of the supplied Class L STEP assembly, not invented hardware. It is needed by M2S3. No original STEP file is needed unless the projection itself must be regenerated. Optional extraction uses `cadquery-ocp` (original version 7.7.2):

```sh
python3 -m venv .cad-env
.cad-env/bin/python -m pip install cadquery-ocp==7.7.2
.cad-env/bin/python extract_cad_projection.py --cad-dir /path/to/extracted-official-cad --class l
```

The external directory must contain `edge_mhs_class_l_hpm_asm.stp`; `--class n` uses `edge_mhs_classn_hpm_asm.stp`, and `--class all` processes both. On Windows, use the virtual environment's `Scripts/python.exe`. The Class N projection is not used by any delivered video and is not required in Git. The models contain board and connector/interface geometry, not a populated computer or chassis. Projection/import success does not establish dimensional or engineering conformance. Keep any teaching derivative explicitly labeled.

## Tracked files

`tracked-files.txt` is the exact minimal file list for this authoring folder. It includes the used Class L SVG, three HTML masters, three timeline records, the portable encoder, source/retiming/CAD/QA helpers, package manifests and the small hash-bound media inventory. Keep the delivered MP4s and posters in the course's `figures/` directory separately.

Do not commit `qa/`, `node_modules/`, virtual environments, original STEP/PDF downloads, provider recordings, authoring WAVs or caches as part of this folder. Large historical review captures remain local; the small inventory preserves the review summary. Video rebuilding does not authorize packaging or publishing a new LMS revision.
