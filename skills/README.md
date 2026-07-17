# Skills

This directory contains the Codex skill used to build and maintain the course source in this repository.

## AcademyWizard

`skills/academy-wizard` is the OCP Academy SCORM course authoring and rendering skill. It supports both `Slides` and `Scrolling` course sources and includes:

- the `SKILL.md` workflow playbook
- course schema and writing/design references
- SCORM rendering, validation, audio, and zip scripts
- the OCP Academy runtime assets and templates

Install it into Codex with:

```bash
./scripts/install-academy-wizard-skill.sh
```

The course build script can also use it directly from this repository without installation.

## Course styles

AcademyWizard's `Slides` style is the narrated slide-by-slide format. Its `Scrolling` style is the lesson-based format with a persistent table of contents, vertical flow, Continue gates, and block interactions. See [Course styles](../docs/course-styles.md) for the complete source and output contract.
