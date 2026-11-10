# Introduction to Emerging Optical Technologies

An introductory-to-intermediate OCP Academy course on how new optical approaches address scale, efficiency, density, latency, and compute integration in AI infrastructure.

This standalone SCORM course belongs to the **Optical Connectivity & Reliability for AI Infrastructure** learning-plan series. Its source is intended for PR-friendly editing. Change slides, knowledge checks, glossary links, and media references in `course.json`; change narration in `audio/moduleN/slide_*.txt`.

## Modules

| Module | Title | Estimated Learner Time | Summary |
|---|---|---:|---|
| 1 | Why AI Infrastructure Is Changing Optics | 13 min | Explain how AI workload and rack architecture change optical demands. Connect networking domains, bandwidth growth, and fiber density to infrastructure-level constraints. |
| 2 | Power, Thermal, and Serviceability Shifts | 17 min | Compare pluggable, near-packaged, and co-packaged optics. Examine expanded-beam and rear blind-mate connectivity through electrical reach, power, cooling, and maintenance tradeoffs. |
| 3 | Density and Testability in the Optical Plant | 15 min | Connect physical fiber-density limits to multicore fiber and space-division multiplexing. Review fan-in/fan-out transitions and testing implications for emerging fiber systems. |
| 4 | Latency, Quantum, and the Adoption Horizon | 15 min | Explore hollow-core propagation latency and hybrid quantum-classical systems. Compare use cases, adoption horizons, and ecosystem readiness across the emerging optical approaches. |

Designed for about **60 minutes of learner time**, including narration, diagrams, knowledge checks and review. Estimated learner time is distinct from narration runtime.

## Media

Course-owned PNG, SVG, and MP4 teaching assets are stored in `figures/`. Editable HTML/SVG and frame-rendering sources for the custom animations are stored in `animations/` where available. Delivery narration is 96 kbps CBR mono MP3 at 44.1 kHz, approved for this rebuild. WAV authoring masters are retained outside Git and outside the LMS package. No narration or rendered SCORM files are checked in. Per-slide `audio.generation_provenance` records reused recordings without inventing unknown legacy model IDs.

Module 1's course overview thanks the OCP community volunteers from VIAVI Solutions, SENKO Advanced Components, and Sumitomo Electric Lightwave. Their supplied, unmodified logos are stored in `resources/images/contributors/`; this visual acknowledgment does not change the narration.

The 800 × 400 LMS catalog poster is `thumbnail.png`. Its editable copy and artwork selection are in `poster.json`; the shared Academy template supplies the layout. See the repository poster build instructions.

The English edition uses the maintained Slides player: centered responsive navigation, transcript and narration controls, per-slide bookmarks, restored quiz attempts, local glossary/resource pills, and icon-based media controls. Course Home uses informational module tiles and a first-module start action; the LMS Syllabus owns separate module launches and completion tracking. SCORM 1.2 and the existing five syllabus entries are preserved.

The three course-owned teaching animations are full-HD, finite master passes with clean final states. Their `animation.html` sources declare the duration/poster time and expose `window.renderAt(seconds)` for deterministic sampling through `skills/academy-wizard/scripts/record_css_animation.mjs`. The supplied expanded-beam video is retained unchanged. Standalone SVG figures and reviewed, hash-bound media text inventories keep glossary placement auditable.

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh optics/introduction-to-emerging-optical-technologies
```

The finished SCORM folder and LMS zip are created under `build/optics/`.

For local QA with previously generated narration, set `EXISTING_AUDIO_DIR` to the existing course `audio/` folder:

```bash
EXISTING_AUDIO_DIR=/path/to/audio \
  ./scripts/build-course.sh optics/introduction-to-emerging-optical-technologies
```

## Public References

The original source deck is not included in this repository. Public references used by the course include:

- Open Rack Base Specification Version 3: https://www.opencompute.org/documents/open-rack-base-specification-version-3-pdf
- OIF 3.2T Co-Packaged Module Implementation Agreement: https://www.oiforum.com/oif-launches-the-industrys-first-co-packaging-standard-the-3-2t-co-packaged-module-implementation-agreement/
- SDM4 MCF MSA announcement: https://sumitomoelectric.com/press/2026/02/prs011
- Microsoft hollow-core fiber announcement: https://blogs.microsoft.com/blog/2022/12/09/microsoft-acquires-lumenisity-an-innovator-in-hollow-core-fiber-hcf-cable/
- Hollow-core fiber research in Nature Photonics: https://www.nature.com/articles/s41566-025-01747-5
- OCP Academy course, Integrating Quantum Processing Units into Data Center Infrastructure: https://academy.opencompute.org/learn/courses/51/integrating-quantum-processing-units-into-data-center-infrastructure

## Catalog poster

Edit `poster.json` for wording and artwork. The shared Academy template fixes typography, gradients, logo and pill positions, and the white emblem dimensions. Rebuild from the repository root:

```sh
node skills/academy-wizard/scripts/render_lms_posters.mjs --repo-root . --course courses/optics/introduction-to-emerging-optical-technologies
```

See [the poster standard](../../../skills/academy-wizard/references/lms_poster_style.md) for dependency setup, title-fitting rules and full-catalog checks.

## LMS Catalog Metadata

Formal learner-facing LMS copy is maintained separately in [lms-catalog.md](lms-catalog.md) and [lms-catalog.json](lms-catalog.json). The course is available in English and seven self-contained language editions under `locales/`.
