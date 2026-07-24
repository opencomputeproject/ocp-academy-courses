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

## Korean editions

The Korean Scrolling sources live under `locales/ko-KR/` within each course.
They retain translated `course.json` content and only the media files that
differ from the canonical English course. Build each Korean course separately:

```bash
./scripts/build-course.sh intro-to-ocp/module-1-the-ocp-origins/locales/ko-KR
./scripts/build-course.sh intro-to-ocp/module-2-the-ocp-ecosystem-governance/locales/ko-KR
./scripts/build-course.sh intro-to-ocp/module-3-ocp-technologies-open-rack-cooling/locales/ko-KR
./scripts/build-course.sh intro-to-ocp/module-4-today-and-tomorrow-the-journey/locales/ko-KR
```

## Japanese editions

The Japanese Scrolling sources live under `locales/ja-JP/` within each course.
As with Korean, the locale stores translated `course.json` content plus only
the Japanese media overrides. Build each Japanese course separately:

```bash
./scripts/build-course.sh intro-to-ocp/module-1-the-ocp-origins/locales/ja-JP
./scripts/build-course.sh intro-to-ocp/module-2-the-ocp-ecosystem-governance/locales/ja-JP
./scripts/build-course.sh intro-to-ocp/module-3-ocp-technologies-open-rack-cooling/locales/ja-JP
./scripts/build-course.sh intro-to-ocp/module-4-today-and-tomorrow-the-journey/locales/ja-JP
```

## Simplified Chinese editions

The Simplified Chinese Scrolling sources live under `locales/zh-CN/` within
each course. Each locale stores translated `course.json` content and only its
localized media overrides, including Chinese captions, dubbed videos with
AcademyWizard background music, diagrams with baked-in Chinese text, and the
translated membership PDF.
Build each Simplified Chinese course separately:

```bash
./scripts/build-course.sh intro-to-ocp/module-1-the-ocp-origins/locales/zh-CN
./scripts/build-course.sh intro-to-ocp/module-2-the-ocp-ecosystem-governance/locales/zh-CN
./scripts/build-course.sh intro-to-ocp/module-3-ocp-technologies-open-rack-cooling/locales/zh-CN
./scripts/build-course.sh intro-to-ocp/module-4-today-and-tomorrow-the-journey/locales/zh-CN
```

## Traditional Chinese editions

The Traditional Chinese Scrolling sources live under `locales/zh-TW/` within
each course. They include translated course content, Traditional Chinese
captions, and localized video narration. Build each course separately:

```bash
./scripts/build-course.sh intro-to-ocp/module-1-the-ocp-origins/locales/zh-TW
./scripts/build-course.sh intro-to-ocp/module-2-the-ocp-ecosystem-governance/locales/zh-TW
./scripts/build-course.sh intro-to-ocp/module-3-ocp-technologies-open-rack-cooling/locales/zh-TW
./scripts/build-course.sh intro-to-ocp/module-4-today-and-tomorrow-the-journey/locales/zh-TW
```

## Vietnamese editions

The Vietnamese Scrolling sources live under `locales/vi-VN/` within each
course. They include translated course content, Vietnamese captions, and
localized video narration. Build each course separately:

```bash
./scripts/build-course.sh intro-to-ocp/module-1-the-ocp-origins/locales/vi-VN
./scripts/build-course.sh intro-to-ocp/module-2-the-ocp-ecosystem-governance/locales/vi-VN
./scripts/build-course.sh intro-to-ocp/module-3-ocp-technologies-open-rack-cooling/locales/vi-VN
./scripts/build-course.sh intro-to-ocp/module-4-today-and-tomorrow-the-journey/locales/vi-VN
```
