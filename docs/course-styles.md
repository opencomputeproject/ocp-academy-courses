# OCP Academy course styles

AcademyWizard supports two course formats through the top-level `style` property in `course.json`. Use the format that matches the intended learner experience; style is a structural choice, not merely a theme.

## Slides

`"style": "Slides"` is the original AcademyWizard format and remains the default when the property is absent.

- Content is organized as `modules[].slides[]`.
- Learners move backward and forward one slide at a time.
- Narration scripts and generated audio normally drive slide timing.
- Figures and code-generated teaching animations live alongside the editable source.
- The SCORM manifest exposes the course launcher and modules as separate SCOs.

Slides is appropriate when narration, paced visual explanation, and slide-level completion are central to the course.

## Scrolling

`"style": "Scrolling"` is a lesson-based, single-SCO course format.

- Content is organized as `lessons[].blocks[]`.
- A persistent left table of contents exposes lessons and completion state.
- Learners scroll through each lesson and pass Continue gates or completed-lesson links at authored milestones.
- Blocks may include rich text, images, video, quotes, accordions, process cards, flip cards, labeled graphics, knowledge checks, dividers, and other authored interactions.
- Narration is not required. Videos may carry `.vtt` caption tracks, which the renderer retains and makes available both from local files and in an LMS.
- Course-owned binary resources live below `resources/images/`, `resources/videos/`, `resources/captions/`, `resources/documents/`, and `resources/fonts/` as needed.

Each Scrolling `course.json` builds one standalone SCORM zip. When several packages form a sequence, keep their source folders under a shared series folder and manage sequence in the LMS learning plan.

## Scrolling authoring rules

The readable source must fully describe the intended learner experience, including:

- content order, wording, inline emphasis, links, and attachment behavior
- lesson widths, section backgrounds, margins, typography, colors, and responsive layout
- entrance, scrolling, card, quiz-feedback, and lesson-transition motion
- Continue gates, completion rules, table-of-contents state, and progress indicator
- interaction-specific dimensions, ordering, controls, hover states, and selected states
- designated icons and control art instead of invented approximations
- video poster frames, player controls, playback-speed options, captions, and subtitle resources

Authoring values belong in `course.json` or course-owned resources so future builds reproduce the course without one-off edits to generated HTML. Generated `index.html`, `imsmanifest.xml`, runtime scripts, and SCORM zips remain build output.

## Building

Use the same repository helper for either style:

```bash
./scripts/build-course.sh <course-folder-or-nested-path>
```

The helper reads `style`, selects the correct render path, validates the result, and creates an LMS-ready zip under `build/`. Slides builds require narration audio unless existing audio is supplied or local rendering explicitly skips audio. Scrolling builds copy retained resources and do not require a narration service.
