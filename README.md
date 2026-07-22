# OCP Academy Courses

Open source course definitions for OCP Academy SCORM courses.

This repository stores editable course source: `course.json`, narration scripts when applicable, and course-owned media. It does not store generated audio, rendered HTML, SCORM zip files, or the original research materials used during course development.

The courses in this repository are generally hosted on [OCP Academy](https://academy.opencompute.org/learn), primarily in its catalog of [Data Center Technology courses](https://academy.opencompute.org/learn/public/catalog/view/3).

It also includes the `academy-wizard` Codex skill used to author and rebuild courses so contributors can reproduce the package generation flow from a clone.

## Course styles

AcademyWizard supports two explicit values for the top-level `style` property in `course.json`:

| Style | Learner experience | Source shape | Typical media |
|---|---|---|---|
| `Slides` | Narrated, previous/next slide navigation | `modules[].slides[]` | Narration scripts, generated audio, figures, and teaching animations |
| `Scrolling` | Lesson table of contents, vertical content, Continue gates, and in-page interactions | `lessons[].blocks[]` | Images, videos, captions, documents, and course-specific interaction settings |

`Slides` remains the default when `style` is omitted. `Scrolling` courses are emitted as one standalone SCORM course per `course.json`; a multi-course learning sequence is assembled in the LMS rather than combined into one package.

See [Course styles](docs/course-styles.md) for the authoring and fidelity contract.

## Repository layout

```text
courses/
  <slides-course>/
    course.json                 # canonical English source
    audio/
    figures/
    locales/
      ko-KR/                    # self-contained translated source
      fr-FR/
  cooling-fluids-in-direct-liquid-cooling/
  diablo-400-disaggregated-power-for-high-density-ai-racks/
  integrating-quantum-processing-units-into-data-center-infrastructure/
  intro-to-ocp/
    module-1-the-ocp-origins/
    module-2-the-ocp-ecosystem-governance/
    module-3-ocp-technologies-open-rack-cooling/
    module-4-today-and-tomorrow-the-journey/
  multipath-reliable-connection-mrc/
  ocp-esun-ethernet-for-scale-up-networks/
  ocp-mhs-modular-plug-and-play-m-pnp/
  ocp-nic-3-0-technical-overview/
  ocp-ready-requirements-for-energy-storage-systems/
  open-rack-v3/
    module-1-ocp-orv3-history-and-impact/
    module-2-orv3-core-specifications/
    module-3-orv3-real-world-implementations/
    module-4-orv3-high-power-racks/
    module-5-orv3-future-trends/
    module-6-the-open-rack-wide-orw-expansion/
    module-7-advanced-orw-liquid-cooling-practice/
  optics/
    enhanced-telemetry-optics/
    introduction-to-emerging-optical-technologies/
  project-deschutes-cdu-specification-v1-0/
  two-phase-direct-liquid-cooling-efficiencies-and-fluids/
scripts/
  build-course.sh
  install-academy-wizard-skill.sh
skills/
  academy-wizard/
```

## Install the AcademyWizard skill

The bundled skill lives at:

```text
skills/academy-wizard
```

The build script uses the repo-local AcademyWizard copy by default, so installing the skill is optional for command-line builds. Install it into Codex when you want to interactively create or revise courses:

```bash
./scripts/install-academy-wizard-skill.sh
```

Add `--force` to replace an existing local copy:

```bash
./scripts/install-academy-wizard-skill.sh --force
```

The installer copies the skill to:

```text
${CODEX_HOME:-$HOME/.codex}/skills/academy-wizard
```

Restart Codex or start a new Codex session after installing so the skill list refreshes.

To use the skill interactively, ask Codex for AcademyWizard work, for example:

```text
Use AcademyWizard to build a Scrolling course from the course source in this repository.
```

## Available Courses

| Folder | Course |
|---|---|
| `cooling-fluids-in-direct-liquid-cooling` | Cooling Fluids in Direct Liquid Cooling (DLC) |
| `diablo-400-disaggregated-power-for-high-density-ai-racks` | OCP Diablo 400: Disaggregated Power for High-Density AI Racks |
| `integrating-quantum-processing-units-into-data-center-infrastructure` | Integrating Quantum Processing Units into Data Center Infrastructure |
| `intro-to-ocp/module-1-the-ocp-origins` | Module 1: The OCP Origins |
| `intro-to-ocp/module-2-the-ocp-ecosystem-governance` | Module 2: The OCP Ecosystem & Governance |
| `intro-to-ocp/module-3-ocp-technologies-open-rack-cooling` | Module 3: OCP Technologies (Open Rack & Cooling) |
| `intro-to-ocp/module-4-today-and-tomorrow-the-journey` | Module 4: Today and Tomorrow (The Journey) |
| `multipath-reliable-connection-mrc` | OCP Academy - MRC Technical Overview |
| `ocp-esun-ethernet-for-scale-up-networks` | OCP ESUN: Ethernet for Scale-Up Networks |
| `ocp-mhs-modular-plug-and-play-m-pnp` | OCP MHS Modular Plug-and-Play (M-PNP) |
| `ocp-nic-3-0-technical-overview` | OCP NIC 3.0 Technical Overview |
| `ocp-ready-requirements-for-energy-storage-systems` | OCP Ready™ Requirements for Energy Storage Systems |
| `open-rack-v3/module-1-ocp-orv3-history-and-impact` | Module 1: OCP & ORv3: History and Impact |
| `open-rack-v3/module-2-orv3-core-specifications` | Module 2: ORv3 Core Specifications |
| `open-rack-v3/module-3-orv3-real-world-implementations` | Module 3: ORv3 Real World Implementations |
| `open-rack-v3/module-4-orv3-high-power-racks` | Module 4: ORv3 High Power Racks |
| `open-rack-v3/module-5-orv3-future-trends` | Module 5: ORv3 Future Trends |
| `open-rack-v3/module-6-the-open-rack-wide-orw-expansion` | Module 6 - The Open Rack Wide (ORW) Expansion |
| `open-rack-v3/module-7-advanced-orw-liquid-cooling-practice` | Module 7 - Advanced ORW Liquid Cooling & Practice |
| `optics/enhanced-telemetry-optics` | Enhanced Telemetry Optics |
| `optics/introduction-to-emerging-optical-technologies` | Introduction to Emerging Optical Technologies |
| `project-deschutes-cdu-specification-v1-0` | OCP Project Deschutes |
| `two-phase-direct-liquid-cooling-efficiencies-and-fluids` | Two-Phase Direct Liquid Cooling Efficiencies and Fluids |

## Build a course

The build uses the bundled AcademyWizard skill by default and selects the Slides or Scrolling pipeline from `course.json`.

To build a narrated Slides course:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh cooling-fluids-in-direct-liquid-cooling
```

The output is written under `build/`, including the rendered course folder and LMS-ready SCORM zip.

### Translate a Slides course

Keep the existing course root as the canonical English source. Scaffold each
additional language beneath a BCP 47 locale folder:

```bash
python skills/academy-wizard/scripts/scaffold_slides_translation.py \
  courses/ocp-esun-ethernet-for-scale-up-networks/course.json ko-KR \
  --language-name Korean
```

This creates a self-contained editable source under
`courses/ocp-esun-ethernet-for-scale-up-networks/locales/ko-KR/`. Translate its
`course.json`, narration scripts, and text-bearing media, then build it as an
independent package:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh ocp-esun-ethernet-for-scale-up-networks/locales/ko-KR
```

The visible course title remains unchanged. The SCORM manifest title adds the
English language name, such as `OCP ESUN (Korean)`, so LMS asset lists can
distinguish editions. See
`skills/academy-wizard/references/slides_translation.md` for the complete
translation and QA workflow.

#### Translations

Published editions are available on the
[OCP Academy Translated Learning](https://academy.opencompute.org/pages/25/ocp-academy-translated-learning)
page.

<!-- translations-table:start -->
| Course | Chinese (Simplified) | Japanese | Korean | Portuguese (Brazil) | Spanish (LATAM) |
|---|---|---|---|---|---|
| [Intro to OCP - Module 1: The OCP Origins](courses/intro-to-ocp/module-1-the-ocp-origins/) | [`zh-CN`](courses/intro-to-ocp/module-1-the-ocp-origins/locales/zh-CN/) | [`ja-JP`](courses/intro-to-ocp/module-1-the-ocp-origins/locales/ja-JP/) | [`ko-KR`](courses/intro-to-ocp/module-1-the-ocp-origins/locales/ko-KR/) | [`pt-BR`](courses/intro-to-ocp/module-1-the-ocp-origins/locales/pt-BR/) | [`es-419`](courses/intro-to-ocp/module-1-the-ocp-origins/locales/es-419/) |
| [Intro to OCP - Module 2: The OCP Ecosystem & Governance](courses/intro-to-ocp/module-2-the-ocp-ecosystem-governance/) | [`zh-CN`](courses/intro-to-ocp/module-2-the-ocp-ecosystem-governance/locales/zh-CN/) | [`ja-JP`](courses/intro-to-ocp/module-2-the-ocp-ecosystem-governance/locales/ja-JP/) | [`ko-KR`](courses/intro-to-ocp/module-2-the-ocp-ecosystem-governance/locales/ko-KR/) | [`pt-BR`](courses/intro-to-ocp/module-2-the-ocp-ecosystem-governance/locales/pt-BR/) | [`es-419`](courses/intro-to-ocp/module-2-the-ocp-ecosystem-governance/locales/es-419/) |
| [Intro to OCP - Module 3: OCP Technologies (Open Rack & Cooling)](courses/intro-to-ocp/module-3-ocp-technologies-open-rack-cooling/) | [`zh-CN`](courses/intro-to-ocp/module-3-ocp-technologies-open-rack-cooling/locales/zh-CN/) | [`ja-JP`](courses/intro-to-ocp/module-3-ocp-technologies-open-rack-cooling/locales/ja-JP/) | [`ko-KR`](courses/intro-to-ocp/module-3-ocp-technologies-open-rack-cooling/locales/ko-KR/) | [`pt-BR`](courses/intro-to-ocp/module-3-ocp-technologies-open-rack-cooling/locales/pt-BR/) | [`es-419`](courses/intro-to-ocp/module-3-ocp-technologies-open-rack-cooling/locales/es-419/) |
| [Intro to OCP - Module 4: Today and Tomorrow (The Journey)](courses/intro-to-ocp/module-4-today-and-tomorrow-the-journey/) | [`zh-CN`](courses/intro-to-ocp/module-4-today-and-tomorrow-the-journey/locales/zh-CN/) | [`ja-JP`](courses/intro-to-ocp/module-4-today-and-tomorrow-the-journey/locales/ja-JP/) | [`ko-KR`](courses/intro-to-ocp/module-4-today-and-tomorrow-the-journey/locales/ko-KR/) | [`pt-BR`](courses/intro-to-ocp/module-4-today-and-tomorrow-the-journey/locales/pt-BR/) | [`es-419`](courses/intro-to-ocp/module-4-today-and-tomorrow-the-journey/locales/es-419/) |
| [OCP ESUN: Ethernet for Scale-Up Networks](courses/ocp-esun-ethernet-for-scale-up-networks/) | [`zh-CN`](courses/ocp-esun-ethernet-for-scale-up-networks/locales/zh-CN/) | [`ja-JP`](courses/ocp-esun-ethernet-for-scale-up-networks/locales/ja-JP/) | [`ko-KR`](courses/ocp-esun-ethernet-for-scale-up-networks/locales/ko-KR/) | [`pt-BR`](courses/ocp-esun-ethernet-for-scale-up-networks/locales/pt-BR/) | [`es-419`](courses/ocp-esun-ethernet-for-scale-up-networks/locales/es-419/) |
| [Open Rack: Module 1: OCP & ORv3: History and Impact](courses/open-rack-v3/module-1-ocp-orv3-history-and-impact/) | [`zh-CN`](courses/open-rack-v3/module-1-ocp-orv3-history-and-impact/locales/zh-CN/) | [`ja-JP`](courses/open-rack-v3/module-1-ocp-orv3-history-and-impact/locales/ja-JP/) | [`ko-KR`](courses/open-rack-v3/module-1-ocp-orv3-history-and-impact/locales/ko-KR/) | [`pt-BR`](courses/open-rack-v3/module-1-ocp-orv3-history-and-impact/locales/pt-BR/) | [`es-419`](courses/open-rack-v3/module-1-ocp-orv3-history-and-impact/locales/es-419/) |
| [Open Rack: Module 2: ORv3 Core Specifications](courses/open-rack-v3/module-2-orv3-core-specifications/) | [`zh-CN`](courses/open-rack-v3/module-2-orv3-core-specifications/locales/zh-CN/) | [`ja-JP`](courses/open-rack-v3/module-2-orv3-core-specifications/locales/ja-JP/) | [`ko-KR`](courses/open-rack-v3/module-2-orv3-core-specifications/locales/ko-KR/) | [`pt-BR`](courses/open-rack-v3/module-2-orv3-core-specifications/locales/pt-BR/) | [`es-419`](courses/open-rack-v3/module-2-orv3-core-specifications/locales/es-419/) |
| [Open Rack: Module 3: ORv3 Real World Implementations](courses/open-rack-v3/module-3-orv3-real-world-implementations/) | [`zh-CN`](courses/open-rack-v3/module-3-orv3-real-world-implementations/locales/zh-CN/) | [`ja-JP`](courses/open-rack-v3/module-3-orv3-real-world-implementations/locales/ja-JP/) | [`ko-KR`](courses/open-rack-v3/module-3-orv3-real-world-implementations/locales/ko-KR/) | [`pt-BR`](courses/open-rack-v3/module-3-orv3-real-world-implementations/locales/pt-BR/) | [`es-419`](courses/open-rack-v3/module-3-orv3-real-world-implementations/locales/es-419/) |
| [Open Rack: Module 4: ORv3 High Power Racks](courses/open-rack-v3/module-4-orv3-high-power-racks/) | [`zh-CN`](courses/open-rack-v3/module-4-orv3-high-power-racks/locales/zh-CN/) | [`ja-JP`](courses/open-rack-v3/module-4-orv3-high-power-racks/locales/ja-JP/) | [`ko-KR`](courses/open-rack-v3/module-4-orv3-high-power-racks/locales/ko-KR/) | [`pt-BR`](courses/open-rack-v3/module-4-orv3-high-power-racks/locales/pt-BR/) | [`es-419`](courses/open-rack-v3/module-4-orv3-high-power-racks/locales/es-419/) |
| [Open Rack: Module 5: ORv3 Future Trends](courses/open-rack-v3/module-5-orv3-future-trends/) | [`zh-CN`](courses/open-rack-v3/module-5-orv3-future-trends/locales/zh-CN/) | [`ja-JP`](courses/open-rack-v3/module-5-orv3-future-trends/locales/ja-JP/) | [`ko-KR`](courses/open-rack-v3/module-5-orv3-future-trends/locales/ko-KR/) | [`pt-BR`](courses/open-rack-v3/module-5-orv3-future-trends/locales/pt-BR/) | [`es-419`](courses/open-rack-v3/module-5-orv3-future-trends/locales/es-419/) |
| [Open Rack: Module 6 - The Open Rack Wide (ORW) Expansion](courses/open-rack-v3/module-6-the-open-rack-wide-orw-expansion/) | [`zh-CN`](courses/open-rack-v3/module-6-the-open-rack-wide-orw-expansion/locales/zh-CN/) | [`ja-JP`](courses/open-rack-v3/module-6-the-open-rack-wide-orw-expansion/locales/ja-JP/) | [`ko-KR`](courses/open-rack-v3/module-6-the-open-rack-wide-orw-expansion/locales/ko-KR/) | [`pt-BR`](courses/open-rack-v3/module-6-the-open-rack-wide-orw-expansion/locales/pt-BR/) | [`es-419`](courses/open-rack-v3/module-6-the-open-rack-wide-orw-expansion/locales/es-419/) |
| [Open Rack: Module 7 - Advanced ORW Liquid Cooling & Practice](courses/open-rack-v3/module-7-advanced-orw-liquid-cooling-practice/) | [`zh-CN`](courses/open-rack-v3/module-7-advanced-orw-liquid-cooling-practice/locales/zh-CN/) | [`ja-JP`](courses/open-rack-v3/module-7-advanced-orw-liquid-cooling-practice/locales/ja-JP/) | [`ko-KR`](courses/open-rack-v3/module-7-advanced-orw-liquid-cooling-practice/locales/ko-KR/) | [`pt-BR`](courses/open-rack-v3/module-7-advanced-orw-liquid-cooling-practice/locales/pt-BR/) | [`es-419`](courses/open-rack-v3/module-7-advanced-orw-liquid-cooling-practice/locales/es-419/) |
<!-- translations-table:end -->

To build one standalone course in the Intro to OCP Scrolling series, no narration API key is required:

```bash
./scripts/build-course.sh intro-to-ocp/module-1-the-ocp-origins
```

This writes the package folder and zip beneath `build/intro-to-ocp/`. Run the same command with each sibling folder to produce the four independent LMS packages.

The script defaults to the bundled skill under `skills/academy-wizard`. If you use a different skill location:

```bash
ACADEMY_WIZARD_SKILL_DIR=/path/to/academy-wizard ./scripts/build-course.sh two-phase-direct-liquid-cooling-efficiencies-and-fluids
```

For local QA with previously generated audio, set `EXISTING_AUDIO_DIR` to a folder shaped like `audio/`:

```bash
EXISTING_AUDIO_DIR=/path/to/audio ./scripts/build-course.sh two-phase-direct-liquid-cooling-efficiencies-and-fluids
```

## Contributing

Use pull requests for course improvements.

- Edit slide text, quiz content, figures, and structure in `course.json`.
- For Slides courses, edit narration in `courses/<course-path>/audio/moduleN/slide_*.txt`.
- Store translated course sources in `courses/<course-path>/locales/<BCP-47 tag>/`; Slides locales are self-contained, while Scrolling locales overlay language-specific resources on the canonical course.
- When committing a translated course source, run
  `python skills/academy-wizard/scripts/update_translation_catalog.py` to refresh
  the root README translation table.
- For Scrolling courses, retain learner media under `resources/` and preserve source-specific interaction, typography, spacing, motion, control-art, and caption metadata in `course.json`.
- Do not commit generated `.wav`, `module*.html`, `index.html`, `imsmanifest.xml`, or `.zip` files.
- Run the build script before opening a PR when possible.

The build renders the selected style, validates the package, and creates a strict LMS zip. Slides builds also regenerate audio from checked-in narration scripts unless existing audio or `SKIP_AUDIO=1` is supplied.
