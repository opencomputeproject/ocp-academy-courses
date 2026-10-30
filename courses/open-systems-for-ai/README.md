# Open Systems for AI

An updated derivative of the OCP Community's 2025 Open Systems for AI white paper, recovered from six Rise modules and rebuilt as narrated Slides. The six-module structure is retained with current OAC, AICC, MGX, LVDC/Diablo, HBF and Caliptra/LOCK context. Learner references point to live Academy courses and official project/specification pages. The older Academy learning plan is excluded.

One SCORM **1.2** package contains **exactly six module SCOs**. Course Home is an untracked asset, as requested for this course; this is an explicit override of the shared tracked-Home default. Each module retains its own bookmark, two-question assessment and completion. Both questions require an attempt; correctness is not a completion gate. The Start Module 1 and module-end links remain available, but direct HTML navigation does not switch the LMS tracking context. Use LMS syllabus launches for separately tracked modules and verify this in the target LMS.

The course has 72 slides: 66 full Eleven v4 narration scripts, six intact original recordings with captions, eight silent narration-synchronized teaching videos and 23 editable static SVG diagrams. Each teaching video plays once and holds its final picture, including when enlarged. Estimated learner time is 99 minutes; optional external reference recordings do not determine this estimate. Formal LMS copy is in [lms-catalog.md](lms-catalog.md) and [lms-catalog.json](lms-catalog.json). `thumbnail.png` is the 800×400 LMS poster.

## Edit and build

`course.json` is canonical. Edit the matching script in `audio/moduleN/` when narration changes, retaining pronunciation hints. Static diagrams are in `figures/`; finite HTML/SVG animation sources are in `animations/`. `authoring/video-plan.json` describes the eight sequences. Original recordings, posters and captions are in `resources/`. Poster source and branding provenance are in `authoring/`.

From the repository root, reuse the approved narration held outside Git:

```sh
EXISTING_AUDIO_DIR=/absolute/path/to/approved/audio bash scripts/build-course.sh open-systems-for-ai
python3 courses/open-systems-for-ai/scripts/verify_course.py build/open-systems-for-ai
```

The course resource hook stages local fonts and branding. Reuse matching approved audio for text-only changes; regenerate changed scripts with the recorded Leo voice, full `eleven_v4` and pitch-preserving 1.18 tempo. Keep native masters/receipts outside the runtime and Git. The learner speed default remains 1.0× with saved preferences retained. A changed script requires new listening/signal checks; changed paired audio requires animation cue review and re-encoding. Animation cues are estimated from narration word fractions, not forced alignment. Use the shared animation recorder and review the full pass and final-frame hold.

`authoring/media-integrity.json` records the reviewed media, narration and script hashes. After an intentional media or script revision, review it and update this inventory before rerunning verification. Generated WAVs, rendered module/home HTML, original Rise archives and SCORM ZIPs are deliberately excluded from Git. Do not rebuild from obsolete intermediate generator scripts; edit this source directly.

## Companion course

[Open Cluster Designs for AI](../open-cluster-designs-for-ai/README.md) is the four-module companion for Academy course 93. It builds on this course's system-level context with cluster hierarchy, equipment and connection records, fabric choices and deployment evidence. Its estimated learner time is 55 minutes. Historical planning snapshots under this course's authoring folder are superseded by the companion's canonical source.

See [QA.md](QA.md) for checks and acceptance limits.
