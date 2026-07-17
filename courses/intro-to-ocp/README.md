# Intro to OCP

Readable source for the four-course **Intro to OCP** learning series. Each child folder is an independent OCP Academy course using the Scrolling style, with its own `course.json`, course resources, and LMS-ready build output.

The four courses are grouped here for source management, but they are not modules inside one SCORM package. Build and upload each course separately, then order them in the LMS learning plan.

## Course sources

| Order | Folder | Course | Focus |
|---:|---|---|---|
| 1 | `module-1-the-ocp-origins` | Module 1: The OCP Origins | The efficiency crisis, OCP's beginnings, Open Rack evolution, and the market impact of open infrastructure. |
| 2 | `module-2-the-ocp-ecosystem-governance` | Module 2: The OCP Ecosystem & Governance | Community participants, governance, projects, workstreams, and the contribution lifecycle. |
| 3 | `module-3-ocp-technologies-open-rack-cooling` | Module 3: OCP Technologies (Open Rack & Cooling) | ORv3 architecture, the thermal challenge, and advanced cooling solutions. |
| 4 | `module-4-today-and-tomorrow-the-journey` | Module 4: Today and Tomorrow (The Journey) | Hardware tiers, the OCP Marketplace, adoption planning, and next steps. |

## Source contract

- `course.json` is the human-readable Scrolling course definition used by AcademyWizard.
- `resources/` contains only course-owned learner media that cannot be reconstructed from readable code, including images, video, WebVTT captions, fonts, and documents.
- Rendered HTML, manifests, runtime files, and SCORM zips are generated and are not committed.

See [OCP Academy course styles](../../docs/course-styles.md) for the Scrolling format and fidelity rules.

## Build all four courses

From the repository root:

```bash
./scripts/build-course.sh intro-to-ocp/module-1-the-ocp-origins
./scripts/build-course.sh intro-to-ocp/module-2-the-ocp-ecosystem-governance
./scripts/build-course.sh intro-to-ocp/module-3-ocp-technologies-open-rack-cooling
./scripts/build-course.sh intro-to-ocp/module-4-today-and-tomorrow-the-journey
```

Each command creates a separate package folder and zip under `build/intro-to-ocp/`.
