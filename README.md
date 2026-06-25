# OCP Academy Courses

Open source course definitions for OCP Academy SCORM courses.

This repository stores the editable course source: `course.json`, narration scripts, and lightweight course assets. It does not store generated audio, rendered HTML modules, SCORM zip files, or the original research/source materials used during course development.

## Repository layout

```text
courses/
  two-phase-direct-liquid-cooling-efficiencies-and-fluids/
    course.json
    audio/moduleN/slide_*.txt
    two_phase_dlc_mark.svg
scripts/
  build-course.sh
```

## Build a course

The build uses the local AcademyWizard Codex skill. By default the script looks for it at:

```text
~/.codex/skills/academy-wizard
```

To build the two-phase DLC course:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh two-phase-direct-liquid-cooling-efficiencies-and-fluids
```

The output is written under `build/`, including the rendered course folder and LMS-ready SCORM zip.

If you use a different skill location:

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
