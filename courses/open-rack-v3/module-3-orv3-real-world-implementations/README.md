# Module 3: ORv3 Real World Implementations

The third standalone Scrolling course in the **Open Rack v3** learning series. It covers ORv3 case studies, community contributions, the OCP Marketplace, and deployment-oriented comparisons.

## Lessons

1. Welcome, Intro & Learning Objectives
2. ORv3 in Practice: Case Studies
3. Marketplace & Community Contributions
4. Compare and Choose
5. Knowledge Check
6. Summary

## Review before packaging

The source of truth is `course.json`. The recovered learner media is under `resources/`, and `conversion.json` provides the conversion audit. A local, unzipped preview may be rendered for inspection; no SCORM zip should be created until the source is approved.

## Build after approval

From the repository root:

```bash
./scripts/build-course.sh open-rack-v3/module-3-orv3-real-world-implementations
```

That command is intentionally deferred during source review because it creates the LMS-ready package and zip under `build/open-rack-v3/`.
