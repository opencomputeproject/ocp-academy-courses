# OCP L.O.C.K.: Secure Key Management for Self-Encrypting Storage

A three-module OCP Academy course based on the OCP L.O.C.K. Specification v1.1. The course explains how Layers of Cryptographic Keys creates a hardware-rooted, lifecycle-controlled key-management boundary for self-encrypting storage.

This course source is intended for PR-friendly editing. Change slides, knowledge checks, glossary links, and figure assignments in `course.json`. Change narration in `audio/moduleN/slide_*.txt`. Generated narration and SCORM runtime files are not checked in.

## Modules

| Module | Title | Estimated learner time | Narrated time | Summary |
|---|---|---:|---:|---|
| 1 | L.O.C.K.: Layered Open-source Cryptographic Key Management | 17 min | 11 min | The storage-retirement problem, threat model, security guarantees, protected key path, and relationship to Caliptra and OCP S.A.F.E.™. |
| 2 | Key Hierarchy and Lifecycle | 18 min | 13 min | Four key layers, durable/volatile/ephemeral persistence, MPK state transitions, epoch changes, and random versus derived MEKs. |
| 3 | Controller Integration and Compliance | 16 min | 13 min | Mailbox and protected-SFR interfaces, register contracts, MEK command choreography, product API mapping, reset behavior, and mandatory conformance. |

The estimated total learner time is 51 minutes, including 36.3 minutes of narration plus knowledge checks, review, and interaction.

## Media

Course-owned vector figures, seven silent teaching animations, animation posters, contributor and ecosystem logos, the L.O.C.K. course mark, and the exact 800 by 400 LMS thumbnail are included. Modules 1 and 3 each contain two teaching animations; Module 2 contains three.

Editable HTML/CSS/JavaScript animation masters and the deterministic Playwright recorder are under `animations/`. Rendered high-quality H.264 MP4 files and representative poster frames are under `figures/`.

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh ocp-lock-secure-key-management-for-self-encrypting-storage
```

The finished SCORM folder and LMS-ready ZIP are created under `build/`.

For local QA with previously generated audio, set `EXISTING_AUDIO_DIR` to a folder shaped like `audio/`:

```bash
EXISTING_AUDIO_DIR=/path/to/audio ./scripts/build-course.sh ocp-lock-secure-key-management-for-self-encrypting-storage
```

## Public references

- OCP L.O.C.K. Specification v1.1 — https://www.opencompute.org/documents/ocp-lock-specification-v1-1-final-pdf
- OCP Storage Project — https://www.opencompute.org/community/storage
- “An update on OCP L.O.C.K.”, 2026 OCP EMEA Summit — https://www.youtube.com/watch?v=a0ews3cKuQI
- Caliptra — https://chipsalliance.github.io/caliptra-web/
- OCP S.A.F.E.™ — https://www.opencompute.org/sp/about-ocp-safe
