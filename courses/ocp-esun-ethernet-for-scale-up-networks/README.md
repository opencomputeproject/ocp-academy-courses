# OCP ESUN: Ethernet for Scale-Up Networks

Ethernet for Scale-Up Networks (ESUN) for tightly coupled AI fabrics.

This course source is intended for PR-friendly editing. Change slides, quiz content, glossary links, and figure assets in `course.json`. Change narration in `audio/moduleN/slide_*.txt`. Generated audio and SCORM runtime files are not checked in.

## Modules

| Module | Title | Summary |
|---|---|---|
| 1 | OCP ESUN: Ethernet for Scale-Up Networks | Why scale-up Ethernet exists, what changes at the wire, and what hardware has to do to conform. |

The module includes a knowledge check before the final course-completion slide.

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
