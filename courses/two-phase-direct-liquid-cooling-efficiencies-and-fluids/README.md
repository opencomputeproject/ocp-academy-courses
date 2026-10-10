# Two-Phase Direct Liquid Cooling Efficiencies and Fluids

Efficient phase-change cooling, dielectric fluids, and operational practices for high-density infrastructure.

This course source is intended for PR-friendly editing. Change slides, quiz content, glossary links, and media references in `course.json`. Static diagrams are in `figures/`; editable video storyboards are in `animations/`. Change narration in `audio/moduleN/slide_*.txt`. Generated narration audio and SCORM runtime files are not checked in.

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
  --allow-missing-module-video 3 --fail-on-flags
```

Module 3 retains its approved static qualification comparison; the opt-out is
not a general waiver for newly authored courses.

## Narration-Synchronized Videos

The three video recommendations were approved on 2026-10-11 and implemented
against the existing narration. Each silent single-pass sequence follows the
slide's audio clock, including pause, seek, replay, speed, and enlarged playback.
Review mode starts paused. Reduced-motion mode holds the final summary until
explicit playback. The narration and transcripts are unchanged.

| Priority | Slide | Sequence |
|---|---|---|
| 1 | M4S4, Filling and Purging Non-Condensable Gases | Systematic fill and priming, service-related air admission, accumulation, a non-critical alarm, and dedicated-system purging while cooling continues. Hollow orange gas markers are distinct from solid working-fluid vapor markers. This is a conceptual sequence, not an equipment-specific procedure. |
| 2 | M2S5, Inside a Controlled Two-Phase Loop | Liquid feed, boiling, vapor-rich return, condensation, inventory management, pumped/passive circulation distinctions, and pressure/saturation control. Replaces the repeating 15-second loop. |
| 3 | M1S4, Heat Moves Through Nested Loops | Heat moves from silicon through the TCS/CDU/FWS boundary to rejection or reuse. The two fluids remain separate. Boundary labels, the straddling FWS box, and straight arrow approaches are preserved. |

M3S6's qualification paths remain a static side-by-side reference. Editable
storyboards, timing provenance, and re-encoding instructions are in
[`animations/`](animations/README.md). Recheck timing after regenerating or
editing narration; a new TTS rendering can change pacing even when its text
is unchanged. The regular build includes the committed MP4s and PNG posters.

## Public references

The original research files are not included in this repository. Public learner/source references used by the course include:

- [OCP Dielectric Coolant Fluid Base Specification V1.0](https://www.opencompute.org/documents/dielectric-coolant-fluid-base-specification-v1-0-final-pdf)
- [OCP Guidelines for Using Dielectric Heat Transfer Fluids in Two-Phase Cold Plate-Based Liquid-Cooled Racks](https://www.opencompute.org/documents/guidelines-for-using-dielectric-heat-transfer-fluids-in-two-phase-cold-plate-based-liquid-cooled-racks-final-pdf)
- [2026 OCP EMEA Summit panel recording: Revolutionizing AI Heat Management - The Superior Efficiency of Two-Phase Liquid Cooling](https://www.youtube.com/watch?v=0vxGneJ3yGo)
- [OCP Educational Webinar Program past webinars index](https://www.opencompute.org/summit/ocp-educational-webinar-program/past-webinars)
