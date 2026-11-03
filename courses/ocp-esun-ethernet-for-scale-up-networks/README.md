# OCP ESUN: Ethernet for Scale-Up Networks

Ethernet for Scale-Up Networks (ESUN) for tightly coupled AI fabrics.

This course source is intended for PR-friendly editing. Change slides, quiz content, glossary links, and figure assets in `course.json`. Change narration in `audio/moduleN/slide_*.txt`. Generated audio and SCORM runtime files are not checked in.

## Modules

| Module | Title | Summary |
|---|---|---|
| 1 | OCP ESUN: Ethernet for Scale-Up Networks | Why scale-up Ethernet exists, what changes at the wire, and what hardware has to do to conform. |

The module includes a knowledge check before the final course-completion slide.

## LMS poster

[`thumbnail.png`](thumbnail.png) is the 800×400 OCP Academy catalog poster.
Its editable renderer uses the repository's shared Lato font and a cached
raster of the authoritative OCP Academy logo. The green badge is vertically
centered, and title characters share a baseline so the hyphen in `SCALE-UP`
aligns correctly.

Regenerate it from the repository root with Python and Pillow installed:

```bash
python3 courses/ocp-esun-ethernet-for-scale-up-networks/render_thumbnail.py
```

## Language editions

- English is the canonical source in this folder.
- Korean is a self-contained authoring source under `locales/ko-KR/`, including
  translated `course.json`, narration scripts, and localized figures.
- Japanese is a self-contained authoring source under `locales/ja-JP/`, including
  translated `course.json`, narration scripts, and localized figures.
- Simplified Chinese is a self-contained authoring source under `locales/zh-CN/`,
  including translated `course.json`, narration scripts, and localized figures.
- Traditional Chinese is a self-contained authoring source under
  `locales/zh-TW/`, including translated `course.json`, narration scripts, and
  localized figures.
- Vietnamese is a self-contained authoring source under `locales/vi-VN/`,
  including translated `course.json`, narration scripts, and localized figures.
- Portuguese for Latin America is a self-contained authoring source under
  `locales/pt-BR/`, including translated `course.json`, narration scripts, and
  localized figures.
- Spanish for Latin America is a self-contained authoring source under
  `locales/es-419/`, including translated `course.json`, narration scripts, and
  localized figures.

Each translated edition preserves the English structure and technical facts while
using locale-specific LMS metadata and its approved ElevenLabs narration voice.

## Build

From the repository root:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh ocp-esun-ethernet-for-scale-up-networks
```

For local QA with previously generated audio, set `EXISTING_AUDIO_DIR` to a folder shaped like `audio/`:

```bash
EXISTING_AUDIO_DIR=/path/to/audio ./scripts/build-course.sh ocp-esun-ethernet-for-scale-up-networks
```

Build the Korean edition independently:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh ocp-esun-ethernet-for-scale-up-networks/locales/ko-KR
```

Build the Japanese edition independently:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh ocp-esun-ethernet-for-scale-up-networks/locales/ja-JP
```

Build the Chinese, Vietnamese, and Latin American editions independently:

```bash
export ELEVENLABS_API_KEY="<your key>"
./scripts/build-course.sh ocp-esun-ethernet-for-scale-up-networks/locales/zh-CN
./scripts/build-course.sh ocp-esun-ethernet-for-scale-up-networks/locales/zh-TW
./scripts/build-course.sh ocp-esun-ethernet-for-scale-up-networks/locales/vi-VN
./scripts/build-course.sh ocp-esun-ethernet-for-scale-up-networks/locales/pt-BR
./scripts/build-course.sh ocp-esun-ethernet-for-scale-up-networks/locales/es-419
```

## Animated Figure

Slide 6 uses a silent, looping animation to show the standard 20-40 byte IP
header contracting into the 4-byte ESUN Header. The checked-in MP4 and poster
can be regenerated with Pillow and ffmpeg:

```bash
cd courses/ocp-esun-ethernet-for-scale-up-networks
python3 animations/header_efficiency/build_header_efficiency_video.py \
  --output figures/header_efficiency_animation.mp4 \
  --poster figures/header_efficiency_animation_poster.png
```

## Public References

The original research files are not included in this repository. Public learner/source references used by the course include:

- OCP ESUN Network Operator Requirements Base Specification Rev 1.0: https://www.opencompute.org/documents/ocp-esun-network-operator-requirements-base-specification-rev-1-0-final-pdf
- OCP announcement: Introducing ESUN: Advancing Ethernet for Scale-Up AI Infrastructure at OCP: https://www.opencompute.org/blog/introducing-esun-advancing-ethernet-for-scale-up-ai-infrastructure-at-ocp
- OCP Networking Project: https://www.opencompute.org/community/networking
- 2026 OCP EMEA Summit: https://www.opencompute.org/events/past-events/2026-ocp-emea-summit

## Catalog poster

Edit `poster.json` for wording and artwork. The shared Academy template fixes typography, gradients, logo and pill positions, and the white emblem dimensions. Rebuild from the repository root:

```sh
node skills/academy-wizard/scripts/render_lms_posters.mjs --repo-root . --course courses/ocp-esun-ethernet-for-scale-up-networks
```

See [the poster standard](../../skills/academy-wizard/references/lms_poster_style.md) for dependency setup, title-fitting rules and full-catalog checks.
