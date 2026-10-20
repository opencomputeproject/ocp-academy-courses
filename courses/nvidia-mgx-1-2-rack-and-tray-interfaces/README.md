# NVIDIA MGX 1.2 Rack and Tray Interfaces

[Take the course on OCP Academy](https://academy.opencompute.org/learn/courses/87/nvidia-mgx-12-rack-and-tray-interfaces).

A standalone, deep technical Slides course on MGX 1.2 mechanical, electrical,
liquid, and module interfaces. Six modules contain 62 narrated slides, seven silent
teaching videos, twelve knowledge-check questions, nine first-use terminology
aids, and a fillable acceptance worksheet. Planned learner time is about 95 minutes;
measured narration is 68.18 minutes (68 minutes rounded).

| Module | Scope | Narration, nearest minute |
|---|---|---|
| 1 | Rack geometry, datums, and alignment | 11 min |
| 2 | Tray architecture, board envelopes, and DC-SCM | 11 min |
| 3 | Modular I/O bay dimensions and retention | 11 min |
| 4 | Busbar electrical design and grounding | 12 min |
| 5 | Liquid cooling and blind-mate mechanics | 12 min |
| 6 | Load cases, qualification, and integration review | 12 min |

Durations above measure narration. Module home cards allow about 15 minutes for Modules 1-3 and 6, 18 minutes for
Module 4, and 17 minutes for Module 5, including review and learner interaction.

## Editable source

- `course.json` is the authoritative content, narration, quiz, and media source.
- `audio/module*/` retains all 62 approved narration scripts; generated WAV files are excluded.
- `figures/` retains source-derived figures, seven teaching MP4s, and their posters.
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

## October 2026 Summit integration

The approved update adds M4S3 (AC/800 VDC/54 VDC conversion boundaries) and M5S5
(power-shelf contact cooling). M1S3 and the M6 qualification/capstone teaching now
include targeted context. Source metadata and affected teaching slides cite
Jared Huntington, NVIDIA, *MGX Power Rack Reference Design*, 2026 OCP Global
Summit, with page-specific deck links and timestamped recording links. The
official public PDF was checked against the supplied local copy. The full
recording remains optional.

The Summit material is a reference design and roadmap. MGX 1.2 remains the
requirements source for this course's rack/tray interfaces. No substantive
changes were made to Modules 2 or 3. See `SUMMIT_SOURCE_NOTES.txt` and
`SUMMIT_FIGURES.json` for source boundaries and figure provenance.

## Companion OCP references

The first key teaching points link to current discovery destinations instead of
pinning companion specifications to a particular revision:

| Teaching point | Companion resource |
|---|---|
| M1S4 — rack interfaces | [Open Rack / ORv3 Academy learning plan](https://academy.opencompute.org/learn/learning-plans/4/open-rack-and-orv3-past-present-and-future) |
| M2S5 — micro MGX board form factor | [M-DNO / M-SDNO contributions](https://www.opencompute.org/contributions/?s=SDNO) |
| M2S7 — management-module shape and pinout | [DC-SCM / DC-SCI contributions](https://www.opencompute.org/contributions/?s=SCM) |
| M3S5 — Type C power-supply depth option | [M-CRPS contributions](https://www.opencompute.org/contributions/?s=CRPS) |
| M5S3 — liquid connector locations | [UQD / UQDB contributions](https://www.opencompute.org/contributions/?s=UQD) and [MQD / MQDB contributions](https://www.opencompute.org/contributions/?s=MQD) |
| M5S4 — working fluid and Table 4 conditions | [Cooling Fluids in Direct Liquid Cooling (DLC) · OCP Academy](https://academy.opencompute.org/learn/courses/52/cooling-fluids-in-direct-liquid-cooling-dlc) |

These companion links appear once at the relevant teaching point. MGX 1.2's
page-specific primary citations and specified interface revisions remain
applicable; a newer catalog entry does not automatically change those requirements.
All seven destinations were verified on the official sites on October 20, 2026.

The SDNO catalog filter includes M-DNO and M-SDNO contributions. M2S5 retains
the MGX specification's DC-MHS DNO Type 2 outline/mounting reference; the related
M-SDNO catalog material does not imply an additional MGX compliance claim.
