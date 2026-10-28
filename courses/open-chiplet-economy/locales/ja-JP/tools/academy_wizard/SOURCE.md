# Validated course toolchain

This published AcademyWizard snapshot preserves the approved course rendering,
media controls, and SCORM 1.2 module organization. `course.json.authoring_toolchain`
selects it during repository builds. The shared repository builder can still be
selected explicitly with `ACADEMY_WIZARD_SKILL_DIR`.

The snapshot includes the 23 October 2026 course fixes: top-aligned Slides,
media-aligned captions and spacing, optional recording captions, the recording
player toolbar, narration-availability guards, untracked Home assets, quiz-state
restoration, contextual references, and finite narration-synchronized videos.
English narration explicitly uses ElevenLabs v4, the recorded Leo voice, and
same-text Multilingual v2 timing at 1.18. The 26 October LMS catalog exporter is
included. Compatibility tests accompany the implementation.

FCSA additionally retains its approved compact media and completion-slide layout.
Each course owns its source, media, and snapshot. Evaluate later shared-toolchain
updates against its learner and tracking behavior before changing the pin.
Background music is maintained in the repository's shared skill assets and is
not duplicated in these English course snapshots.

## Japanese locale

This locale uses Japanese controls and Noto Sans JP. Its Japanese glossary matcher supports unspaced Japanese while preserving boundaries around Latin acronyms. An opt-in `figure.captions_time_source: "narration"` keeps CC on the speech clock for short looping diagrams. All other video modes keep the normal video clock and their maintained controls. The localized mixer preserves every source video packet, including final buffered frames when rounded audio duration is slightly shorter. Narration explicitly uses the approved Japanese voice with ElevenLabs v4, paced to same-text Multilingual v2 at 1.18.

## Green next-module navigation — 27 October 2026

The installed AcademyWizard navigation fix is applied to this pinned runtime. Authored green next-module links remain visible and clickable in standalone, review and LMS playback without a special navigation override. The LMS-only click interceptor and its pop-up are removed; the maintained Course Home policy and review query propagation remain. SCORM 1.2, SCO identifiers, quizzes, bookmarks, completion and all approved content/media are preserved. `test_lms_syllabus_handoff.py` covers the shared guard across LMS/review/single-SCO/direct-link combinations.
The same maintained first-module action is also retained on untracked Home: API availability no longer cancels its click. Informational tiles and the Home asset/session policy are unchanged.

## Course Home as the first SCO — 27 October 2026

The current course source explicitly sets `scorm.include_home_sco: true`. `index.html` is a tracked Course Home item at the beginning of the manifest organization and completes when launched. The existing teaching modules retain their identifiers, numbers, quiz gates, media, bookmarks and green navigation. Course Home plus nine Chiplet modules gives ten SCOs; Course Home plus five FCSA modules gives six.
