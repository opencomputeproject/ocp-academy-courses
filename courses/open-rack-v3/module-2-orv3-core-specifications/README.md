# Module 2: ORv3 Core Specifications

The second standalone Scrolling course in the **Open Rack v3** learning series. It covers the ORv3 frame, 48V DC power shelves and busbar, cooling and manifolds, payload compatibility, accessories, cabling, transport, and sustainability.

## Lessons

1. Welcome, Intro & Learning Objectives
2. Inside the ORv3 Frame
3. Power Shelves and Busbar
4. Cooling and Manifolds
5. Liquid Cooling
6. Accessories and Sustainability
7. Payload Options and Compatibility
8. Cabling and Transport
9. Knowledge Check
10. Summary: ORv3 Core Specifications

## Review before packaging

The source of truth is `course.json`. The recovered learner media is under `resources/`, and `conversion.json` provides the conversion audit. A local, unzipped preview may be rendered for inspection; no SCORM zip should be created until the source is approved.

## Build after approval

From the repository root:

```bash
./scripts/build-course.sh open-rack-v3/module-2-orv3-core-specifications
```

That command is intentionally deferred during source review because it creates the LMS-ready package and zip under `build/open-rack-v3/`.
