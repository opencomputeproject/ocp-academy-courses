# Open Cluster Designs for AI

A narrated Slides course on reading OCP cluster contributions, tracing pod groups into complete clusters, comparing training and inference fabric choices, and assembling deployment evidence. Academy destination: [course 93](https://academy.opencompute.org/learn/courses/93/open-cluster-designs-for-ai/). The prerequisite is [Open Systems for AI](https://academy.opencompute.org/learn/courses/92/open-systems-for-ai/).

Four modules contain 45 narrated slides, eighteen editable SVG diagrams and two original XOC-N figures, five Astra-directed teaching videos, four scenario activities and eight assessment questions. Estimated learner time is **55 minutes**; narration runs **24.43 minutes**. The estimate includes diagram reading, decisions, reflection and assessments. External reading and Summit recordings are optional and excluded from that estimate. Formal LMS copy is in [lms-catalog.md](lms-catalog.md) and [lms-catalog.json](lms-catalog.json); `thumbnail.png` is the 800×400 poster.

The SCORM **1.2** organization contains **Course Home plus four module SCOs**. Home remains at `index.html` with a Start Module 1 action and informational module cards. Modules retain separate bookmarks, two-question assessments and completion. Both questions require an attempt; correctness is not a completion threshold. Direct HTML links do not switch LMS tracking context: launch separately tracked modules from the LMS syllabus and verify the behavior in the target LMS.

## Edit and rebuild

`course.json` is canonical. Narration scripts are paired with WAV filenames under `audio/moduleN/`; pronunciation-aware spoken text and formal transcripts are intentionally separate. Static diagrams are in `figures/`, and deterministic finite animation sources are in `animations/`. See [source audit](authoring/source-audit.md), [video plan](authoring/video-plan.md), [credits](NOTICE.md) and [QA](QA.md).

From the repository root, reuse the current approved or review narration held outside Git:

```sh
EXISTING_AUDIO_DIR=/absolute/path/to/review/audio bash scripts/build-course.sh open-cluster-designs-for-ai
python3 courses/open-cluster-designs-for-ai/scripts/verify_course.py build/open-cluster-designs-for-ai
```

The resource hook stages local fonts and branding. Retain the Leo voice, full `eleven_v4`, pitch-preserving 1.18 tempo, and the learner speed default of 1.0×. Native masters and unmodified synthesis receipts remain outside the runtime and Git. Regenerate only changed narration, then review its level, tail, pauses and pronunciation. No further editorial production gates were requested for this review build; human listening review is still pending.

For a video narration change, edit the pronunciation-aware TXT and formal transcript, generate its WAV, then run `python3 courses/open-cluster-designs-for-ai/scripts/retime_videos.py /absolute/path/to/built-course`. The helper uses measured WAV duration and editable phrase anchors; cue timing is an editorial word-position estimate, not forced alignment. Review cue timing against speech, re-encode the affected HTML using the shared animation recorder, replace its MP4/poster, and refresh the figure text inventory and reviewed hashes. All five videos play once with narration and hold the final picture, including in the enlarged player. Keep `sync_to_narration: true`, `autoplay: false`, `loop: false`, `muted: true`.

`authoring/media-integrity.json` binds the reviewed scripts, audio and media. After an intentional revision, review the result before updating hashes. Generated WAVs, rendered Home/module HTML, source research PDFs and ZIPs are excluded from Git. Rebuild from this course source rather than initial planning or staging generators.

Pronunciation correction: the spoken scripts render Clos as `Kloh` (rhymes with go/slow; silent s). The conventional spelling remains in visible labels and display transcripts. M2S6 and M3S4 were re-recorded, and M3S4 was retimed to its new WAV.
