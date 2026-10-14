# NVIDIA MGX 1.2 Rack and Tray Interfaces

[Take the course on OCP Academy](https://academy.opencompute.org/learn/courses/87/nvidia-mgx-12-rack-and-tray-interfaces).

A standalone, deep technical Slides course on MGX 1.2 mechanical, electrical,
liquid, and module interfaces. Six modules contain 60 narrated slides, six silent
teaching videos, twelve knowledge-check questions, nine first-use terminology
aids, and a fillable acceptance worksheet. Planned learner time is about 90 minutes;
measured narration is 64.71 minutes (65 minutes rounded).

| Module | Scope | Narration, nearest minute |
|---|---|---|
| 1 | Rack geometry, datums, and alignment | 11 min |
| 2 | Tray architecture, board envelopes, and DC-SCM | 11 min |
| 3 | Modular I/O bay dimensions and retention | 11 min |
| 4 | Busbar electrical design and grounding | 10 min |
| 5 | Liquid cooling and blind-mate mechanics | 11 min |
| 6 | Load cases, qualification, and integration review | 11 min |


Durations above measure narration. Module home cards allow about 15 minutes each
for playback, drawing review, quizzes, and acceptance work.

## Editable source

- `course.json` is the authoritative content, narration, quiz, and media source.
- `audio/module*/` retains all 60 approved narration scripts; generated WAV files are excluded.
- `figures/` retains source-derived figures, six teaching MP4s, and their posters.
- `animations/` retains the media builder, measured master timelines, and 241
  source-derived HPM poses needed to reproduce the CAD sequence.
- `assets/fonts/` supplies local Open Sans fonts and their OFL license.
- `resources/documents/mgx_acceptance_worksheet.pdf` is the learner worksheet.
- `thumbnail.png` is the exact 800 × 400 catalog poster; editable poster source
  is `animations/lms_poster.html`.
- [Course outline](OUTLINE.md), [LMS metadata](LMS_METADATA.md),
  [media notes](animations/README.md), [attribution](ATTRIBUTION.md), and
  [validation record](QA.md) accompany the source.
- [Promotion assets](promotion/README.md) include the 30-second LinkedIn videos,
  cover, post, actual index screenshot, and editable composer.

Original research PDFs, the CAD download, generated course HTML, generated
narration, and LMS ZIPs are intentionally outside source control.

## Rebuild from the repository root

Use Python 3.10+ and the repository's bundled AcademyWizard. Reuse a retained
narration directory to reproduce the approved package without another TTS call:

```bash
EXISTING_AUDIO_DIR=/path/to/retained/audio \
  ./scripts/build-course.sh nvidia-mgx-1-2-rack-and-tray-interfaces
```

Alternatively, set `ELEVENLABS_API_KEY` in the environment and run the same build
without `EXISTING_AUDIO_DIR` to regenerate narration from the approved scripts.
Never commit keys. New narration may have different durations; regenerate and
review the four synchronized videos against those measured WAVs before release.
`SKIP_AUDIO=1` produces a visual review build only. Outputs go under `build/`.
The course-local resource hook stages the fonts and poster before rendering.

The existing deployment uses SCORM 1.2 with separate Course Home/module SCOs.
Preserve this format and organization on rebuild. Home tiles are informational;
the first-module start action is a direct link and cannot itself switch the LMS's
tracking context. Test navigation and separate completion in the target LMS.

## Source and interpretation

The source is the [MGX Rack and Tray Specification 1.2.0](https://www.opencompute.org/wp-content/uploads/2026/10/MGX-Accelerated-Computing-Rack-and-Trays-Specification-1.2.0-Final.pdf)
and its [2D/3D design files](https://www.opencompute.org/wp-content/uploads/2026/10/MGX-V1.2-2D-and-3D-Design-Files.zip).
The PDF has 92 viewer pages; [SOURCE_FIGURES.json](SOURCE_FIGURES.json) indexes
84 source figures. Teaching references use PDF viewer pages, including the cover.

The design archive contains native Creo parts, 251 drawing PDFs, and one STEP
model of a full-size fanless HPM. The course uses that supplied geometry for an
illustrative layer separation. Display offsets, alignment silhouettes, and the
595.7 lb simultaneous-maxima arithmetic are explanatory examples, not verified
assembly motion, force measurements, or structural qualification.

Keep source conditions distinct: the parasitic-load current in Table 3 is not
the same rating as the wider busbar envelope; the source's Table 4 maximum-burst
and Table 9 minimum-burst wording require implementation clarification. The course
preserves those qualifications and does not invent an unprovided brass zinc limit.

Automated QA does not substitute for technical review, narration listening, or
target-LMS acceptance. See [QA.md](QA.md) for the evidence and remaining review.
