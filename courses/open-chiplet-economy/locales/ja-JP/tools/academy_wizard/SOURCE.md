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
