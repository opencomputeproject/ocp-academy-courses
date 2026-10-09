# Two-Phase Direct Liquid Cooling Efficiencies and Fluids

Efficient phase-change cooling, dielectric fluids, and operational practices for high-density infrastructure.

This course source is intended for PR-friendly editing. Change slides, quiz content, glossary links, and figure SVGs in `course.json`. Change narration in `audio/moduleN/slide_*.txt`. Generated audio and SCORM runtime files are not checked in.

## Modules

| Module | Title | Summary |
|---|---|---|
| 1 | Why Two-Phase DLC Now | Cooling constraints, efficiency levers, and where two-phase fits. |
| 2 | Two-Phase DLC Architecture and Efficiency Mechanics | Phase-change mechanics, loop boundaries, pressure control, and scale requirements. |
| 3 | Dielectric Fluids, Selection, and Compatibility | Fluid properties, wetted materials, safety, and environmental roadmaps. |
| 4 | Deployment, Operations, Monitoring, and Lifecycle | Startup, purge, monitoring, maintenance, deployment patterns, and records. |

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh two-phase-direct-liquid-cooling-efficiencies-and-fluids
```

The finished SCORM folder and LMS zip are created under `build/`.

## Player and learner aids

This course retains SCORM 1.2 with separate Course Home and module activities.
The home tiles are informational; the LMS Syllabus owns module selection and
completion indicators. The first-module start control is a direct page link,
not an LMS request to switch tracked activities. Test its tracking behavior in
the target LMS and use the Syllabus for independently tracked module launches.

Glossary pills show definitions without opening a page. Resource pills open a
new tab; teaching-slide PDF links name the supporting viewer pages. The final
slide retains whole-document links. Knowledge checks require an attempt, not a
correct answer, and allow retries. Slide bookmarks and quiz state are saved per
module. Local editorial review uses `?review=1` to keep narration off and avoid
changing learner progress.

Figure text inventories in `course.json` record visually reviewed labels and
the exact media SHA-256. After editing a figure or video, re-review its visible
text and update the inventory before running the learner-aid check:

```bash
python3 skills/academy-wizard/scripts/slides_course_qa.py \
  courses/two-phase-direct-liquid-cooling-efficiencies-and-fluids/course.json \
  --allow-missing-module-video 1 --allow-missing-module-video 3 \
  --allow-missing-module-video 4 --fail-on-flags
```

The opt-outs preserve this course's approved one-video scope; they are not a
general waiver for newly authored courses.

## Video Opportunities

The existing silent M2S5 loop is retained. These are editorial recommendations,
not changes to the approved media:

| Priority | Slide | Opportunity |
|---|---|---|
| 1 | M4S4, Filling and Purging Non-Condensable Gases | Use the existing narration to show priming, air introduced during server service, accumulation, a non-critical purge alarm, and gas removal while cooling continues. Distinguish working-fluid vapor from non-condensable gas, and keep this a conceptual sequence rather than equipment-specific operating instructions. |
| 2 | M2S5, Inside a Controlled Two-Phase Loop | Replace the repeating 15-second loop with a narration-synced single pass through liquid feed, boiling, vapor return, condensation, inventory management, and pressure control. Pause, seek, replay, speed, and enlarged playback should follow the narration. |
| 3 | M1S4, Heat Moves Through Nested Loops | Trace heat across the TCS/CDU/FWS boundary in narration order while keeping the two fluid circuits visibly separate. Preserve the existing boundary labels and arrow geometry. |

Keep M3S6's qualification paths as a static side-by-side reference: learners
need to compare evidence and tests, not watch a repeating process. Additional
videos and narration synchronization remain subject to editorial approval.

## Public references

The original research files are not included in this repository. Public learner/source references used by the course include:

- [OCP Dielectric Coolant Fluid Base Specification V1.0](https://www.opencompute.org/documents/dielectric-coolant-fluid-base-specification-v1-0-final-pdf)
- [OCP Guidelines for Using Dielectric Heat Transfer Fluids in Two-Phase Cold Plate-Based Liquid-Cooled Racks](https://www.opencompute.org/documents/guidelines-for-using-dielectric-heat-transfer-fluids-in-two-phase-cold-plate-based-liquid-cooled-racks-final-pdf)
- [2026 OCP EMEA Summit panel recording: Revolutionizing AI Heat Management - The Superior Efficiency of Two-Phase Liquid Cooling](https://www.youtube.com/watch?v=0vxGneJ3yGo)
- [OCP Educational Webinar Program past webinars index](https://www.opencompute.org/summit/ocp-educational-webinar-program/past-webinars)
