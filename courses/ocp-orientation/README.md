# OCP Orientation

Readable source for five independent OCP Academy orientation courses. Each child folder is a standalone Scrolling course with its own `course.json`, course-owned resources, and LMS-ready build output.

The courses are grouped here for source management, but they are not modules inside one SCORM package. Build and upload each course separately.

## Course sources

| Folder | Course | Focus |
|---|---|---|
| `understanding-and-procuring-open-technologies-and-products` | Understanding and Procuring Open Technologies and Products | Open-technology ecosystems, procurement benefits, commercial models, and adoption strategy. |
| `introduction-to-the-ocp-solution-provider-program` | Introduction to the OCP Solution Provider Program | The OCP Marketplace, product and facility recognition, agreements, and fees. |
| `ocp-volunteer-leadership-guide` | OCP's Volunteer Leadership Guide | Volunteer roles, project leadership, contribution processes, and recognition programs. |
| `ocp-ready-data-center-recognition-program` | OCP Ready™ Data Center Recognition Program | Recognition paths, site-assessment requirements, submission, and maintenance. |
| `ocp-contribution-process` | OCP Contribution Process | Contribution initiation, review, approval, publication, and supporting tools. |

## Source contract

- `course.json` is the human-readable Scrolling course definition used by AcademyWizard.
- `resources/` contains course-owned learner media, captions, fonts, and documents.
- `conversion.json` records recovery and porting provenance from the original Rise course.
- Rendered HTML, manifests, runtime files, original Rise packages, and SCORM ZIPs are not committed.

See [OCP Academy course styles](../../docs/course-styles.md) for the Scrolling format and fidelity rules.

## Build all five courses

From the repository root:

```bash
./scripts/build-course.sh ocp-orientation/understanding-and-procuring-open-technologies-and-products
./scripts/build-course.sh ocp-orientation/introduction-to-the-ocp-solution-provider-program
./scripts/build-course.sh ocp-orientation/ocp-volunteer-leadership-guide
./scripts/build-course.sh ocp-orientation/ocp-ready-data-center-recognition-program
./scripts/build-course.sh ocp-orientation/ocp-contribution-process
```
