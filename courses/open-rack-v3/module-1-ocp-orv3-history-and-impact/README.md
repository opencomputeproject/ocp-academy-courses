# Module 1: OCP & ORv3: History and Impact

The first standalone Scrolling course in the **Open Rack v3** learning series. It introduces the origins of the Open Compute Project, traces Open Rack from ORv1 through ORv3, and explains ORv3's impact on efficiency, scalability, cooling, sustainability, and AI workloads.

## Lessons

1. Welcome, Introduction & Learning Objectives
2. The Open Compute Project: Origins
3. The Evolution of Open Rack: From ORv1 to ORv3
4. Key Development Milestones
5. ORv3’s Impact: Efficiency, Scalability and Flexibility
6. AI, Cooling & Sustainability
7. Knowledge Check
8. Summary

## Review before packaging

The source of truth is `course.json`. The recovered learner media is under `resources/`, and `conversion.json` provides the conversion audit. A local, unzipped preview may be rendered for inspection; no SCORM zip should be created until the source is approved.

## Build after approval

From the repository root:

```bash
./scripts/build-course.sh open-rack-v3/module-1-ocp-orv3-history-and-impact
```

That command is intentionally deferred during source review because it creates the LMS-ready package and zip under `build/open-rack-v3/`.
