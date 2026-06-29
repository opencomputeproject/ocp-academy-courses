# OCP Academy Courses

Open source course definitions for OCP Academy SCORM courses.

This repository stores the editable course source: `course.json`, narration scripts, and lightweight course assets. It does not store generated audio, rendered HTML modules, SCORM zip files, or the original research/source materials used during course development.

It also includes the `academy-wizard` Codex skill used to build the courses so contributors can reproduce the package generation flow from a clone.

## Repository layout

```text
courses/
  cooling-fluids-in-direct-liquid-cooling/
  diablo-400-disaggregated-power-for-high-density-ai-racks/
  ocp-mhs-modular-plug-and-play-m-pnp/
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

The build script uses this repo-local copy by default, so installing the skill is optional for command-line builds. Install it into Codex when you want to use it interactively to create or revise courses:

```bash
./scripts/install-academy-wizard-skill.sh
```

If you already have a local `academy-wizard` skill and want to replace it with this repo version:

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
Use the academy-wizard skill to build the two-phase direct liquid cooling course from the course source in this repo.
```

## Available Courses

| Folder | Course |
|---|---|
| `cooling-fluids-in-direct-liquid-cooling` | Cooling Fluids in Direct Liquid Cooling (DLC) |
| `diablo-400-disaggregated-power-for-high-density-ai-racks` | OCP Diablo 400: Disaggregated Power for High-Density AI Racks |
| `ocp-mhs-modular-plug-and-play-m-pnp` | OCP MHS Modular Plug-and-Play (M-PNP) |
| `project-deschutes-cdu-specification-v1-0` | OCP Project Deschutes |
| `two-phase-direct-liquid-cooling-efficiencies-and-fluids` | Two-Phase Direct Liquid Cooling Efficiencies and Fluids |

## Build a course

The build uses the local AcademyWizard Codex skill. By default the script looks for it at:

```text
~/.codex/skills/academy-wizard
```

To build a course:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh cooling-fluids-in-direct-liquid-cooling
```

The output is written under `build/`, including the rendered course folder and LMS-ready SCORM zip.

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
- Edit narration in `courses/<course>/audio/moduleN/slide_*.txt`.
- Do not commit generated `.wav`, `module*.html`, `index.html`, `imsmanifest.xml`, or `.zip` files.
- Run the build script before opening a PR when possible.

The build regenerates audio from the checked-in narration scripts, renders the SCORM HTML, validates the package, and creates a strict LMS zip.
