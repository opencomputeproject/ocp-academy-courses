# OCP S.A.F.E.: Product Security Reviews and S.O.L.I.D. Requirements

An introductory Slides course with three modules, 31 slides, 30 narration scripts, four synchronized teaching videos and the intact 5:25 program overview recording. Estimated learner time is 35 minutes (16, 11 and 8 minutes per module). This is a standalone course, not part of an orientation meta-series.

One SCORM **1.2** activity launches through `launch.html`, keeping a single LMS session across Course Home and all three internal modules. Completion requires all modules and an attempt on each of six formative questions; correctness is not a completion gate. Bookmarks and quiz attempts are retained within the activity. Index cards are informational, without progress labels or click actions; the separate start control opens module 1.

Formal LMS fields are in [lms-catalog.md](lms-catalog.md) and [lms-catalog.json](lms-catalog.json). `thumbnail.png` is the exact 800×400 LMS poster, with editable source at `authoring/thumbnail.svg`. The supplied official outlined trademark SVG is used on M2S7 and the poster, including its TM artwork. The separate course mark is retained in `safe_mark.svg`.

## Edit and build

`course.json` is canonical. Spoken TXT scripts in `audio/moduleN/` preserve pronunciation choices, including the added “And next” on M1's final slide and unhyphenated spoken “AI assisted” on M2's final slide. Visible transcripts retain conventional spelling. Narration uses ElevenLabs Leo v2, Multilingual v2 and synthesis speed 1.18; the learner playback default is 1.0.

From the repository root, reuse approved narration stored outside source control:

```sh
EXISTING_AUDIO_DIR=/absolute/path/to/approved/audio bash scripts/build-course.sh ocp-safe-product-security
python3 skills/academy-wizard/scripts/slides_course_qa.py courses/ocp-safe-product-security/course.json --repo-root . --fail-on-flags
node courses/ocp-safe-product-security/scripts/check_visual_layout.cjs build/ocp-safe-product-security /tmp/ocp-safe-layout
```

The resource hook stages offline fonts and the poster. If generating new narration, use the recorded provider/voice/model/pacing and valid credentials in the process environment; no credentials belong in source. Generated WAVs, runtime HTML, SCORM ZIPs and original research/Rise archives are intentionally omitted from Git. The build command emits a strict runtime ZIP and separate LMS catalog sidecars.

Review from the generated `index.html` and `moduleN.html` files; `?review=1&slide=N` isolates editorial review and starts narration off. The full single-session shell can be tested in an LMS or through local HTTP. A server is not required for individual module review. Keep QA playback muted.

Editable static figures are in `figures/`. The four finite HTML/SVG animation sources, measured timing sidecars, local Lato fonts and timing updater are in `animations/`; the final MP4s are silent, single-pass, 1080p, and follow the narration clock. Do not regenerate them against unmeasured audio durations. `authoring/animation-sync.json` records the approved narration hashes and beat timing. Re-encode only when content/timing changes, using the maintained lossless-frame recorder.

For the logo/diagram composite, edit `authoring/build_marketplace_figure.py`, render and review it, then pass `--reviewed` to bind the text inventory. The original outlined logo remains unchanged in `authoring/ocp_safe_official_tm.svg`. For poster edits, use `python3 authoring/build_static_art.py --poster-only`, then export `authoring/thumbnail.svg` at exactly 800×400. Preserve the trademark paths and the course mark.

## Source and review context

The original Rise source contained 17 lessons, 146 blocks, 11 questions and 37 resources; local recovery retained all source media. Foundational course contributors Roy Albert and Ilja Van Sprundel of IOActive remain credited here; this does not imply their approval of later changes. The original recording is byte-identical, with editable English machine-transcribed captions and a transcript. Its historical framing is bounded by current guidance on the slide. Source/media hashes are in `authoring/media-provenance.json`.

The update uses the 2026 Summit session “Upgrading OCP S.A.F.E. and S.O.L.I.D. for the AI age” and current OCP framework, review-scope, product requirements and AI review guidance. Applicable S.O.L.I.D. gaps are reported in long-form reports from October 1, 2026; AI-assisted review is mandatory for audit completion dates on/after January 1, 2027. The checked guidance gives no effective date for short-form S.O.L.I.D. gap reporting. The independent provider remains responsible for the review.

M2S7 links to the verified OCP Marketplace recognition filter and vendor listing guidance. Listings support product discovery and promotion; the identified product/firmware, review evidence and deployment fit govern interpretation. URLs remain in `course.json` rather than duplicating live product lists.

This intentionally migrates a SCORM 2004 3rd Edition source to user-selected single-activity SCORM 1.2. Existing LMS attempts, bookmarks and completion history may not transfer. Test a separate upload and preserve needed reports before replacing old material. No upload, deletion or tracking reset is part of this source contribution.

See [QA.md](QA.md) for verification scope and target-LMS acceptance limits.
