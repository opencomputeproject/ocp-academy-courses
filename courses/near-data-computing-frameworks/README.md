# Near Data Computing: Frameworks and Open Design Questions

This OCP Academy course is for architects, engineers, and contributors in the Data Centric Computing (DCC) workstream. It takes about 40 minutes and includes 30 narrated slides, three synchronized teaching videos, six knowledge-check questions, and a contribution worksheet.

1. **Choosing Where Computation Runs** explores when moving computation closer to data could reduce data movement.
2. **Connecting Applications to NDC Devices** follows an offload request through the software stack and examines the contracts that make it work.
3. **Testing the Proposals and Contributing to DCC** compares interface approaches and turns an open question into a testable contribution.

The course was authored against a v0.1 snapshot of the NDC Framework White Paper. The workstream continues to revise the draft, so section numbers in the course source refer to the authoring snapshot. Review the [current working draft](https://docs.google.com/document/d/1gu1eheF2DapoegftHQQ8jfEBuxrLVWHQHWgM57XswEY/edit) and the [OCP DCC workstream](https://www.opencompute.org/projects/future-technologies-initiative/data-centric-computing/) when updating the course.

## Editable source

- `course.json` holds slides, quizzes, glossary, and references.
- `audio/moduleN/slide_*.txt` contains the narration scripts for all 30 slides.
- `figures/` holds diagrams, teaching videos, and video posters. `animations/` contains the editable animation HTML, timing, and narration alignment.
- `resources/dcc_contribution_worksheet.html` is an editable learner worksheet. It saves notes locally and lets learners copy or download them.
- `poster.json` and `thumbnail.png` define the shared LMS poster.
- [LMS catalog information](lms-catalog.md) is stored separately. The catalog title and descriptions identify the beta.

## Build

From the repository root, use the Academy build script. Point it at the original paced narration when rebuilding the review package.

```sh
EXISTING_AUDIO_DIR=/path/to/ndc-course/audio \
  ./scripts/build-course.sh near-data-computing-frameworks
```

For a preview of the rendered slides without audio, set `SKIP_AUDIO=1`. Narration uses ElevenLabs v4 with the Leo voice and 1.18 pacing. If you regenerate or edit narration on a video slide, check the phrase alignment and retime and re-encode the corresponding animation as needed. Each teaching video plays once with its narration and holds on the final frame. Verify pause, seek, replay, and the final hold against the audio you package.

The SCORM 1.2 package has four tracked items: Course Home and three content modules.
