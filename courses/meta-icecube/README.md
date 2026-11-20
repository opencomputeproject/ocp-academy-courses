# Meta IceCube: Anatomy of a 102.4 Tb/s Ethernet Switch

A 24-minute narrated OCP Academy course with 20 slides. The single SCORM 1.2 package lists Course Home and the two modules in the Docebo syllabus. [Take the course in OCP Academy](https://academy.opencompute.org/learn/courses/102/meta-icecube-anatomy-of-a-1024-tbs-ethernet-switch/lessons).

| Syllabus entry | Scope | Estimated time |
| --- | --- | ---: |
| Course Home | Course navigation | 1 min |
| 1. From ASIC to fiber | Follow Ethernet signals through the Broadcom Tomahawk6C reference design and distinguish physical OSFP connectors from logical Ethernet interfaces. Compare the NVIDIA Spectrum-6 IceCube-N preview. | 11 min |
| 2. Cooling and servicing IceCube | Locate rack power and coolant connections, follow liquid and air through the chassis, and diagnose a slow-fan warning. | 12 min |

## Editable source

- `course.json` contains the slides, knowledge checks, glossary, and page-level citations.
- `audio/module*/` contains editable narration scripts. The three teaching animations follow the narration and hold on their final frame.
- `figures/` contains specification Figures 1–4, Meta’s IcePack rack image, and the three silent teaching animations with their posters. The animation sources and timing are in `authoring/video/`.
- `poster.json` and `thumbnail.png` define the course poster. The formal LMS fields are in `lms-catalog.json` and `lms-catalog.md`.
- [Course outline](outline.md)

The course uses the [Meta IceCube OCP Design Specification v1.0.0](https://www.opencompute.org/wp-content/uploads/2026/11/Meta-IceCube-OCP-Design-Specification-v1.0.0-final.pdf) and credits the IcePack rack image to [Engineering at Meta](https://engineering.fb.com/2026/10/12/open-source/ocp-summit-2026-powering-ai-with-open-innovations-in-scale-up-scale-out-and-scale-across-networks/). The closing slide links to the [OCP Summit recording](https://www.youtube.com/watch?v=39tvEfs9LuA), [presentation](https://drive.google.com/file/d/1HBSpWnbuKEbmtQxH52qOFHcO7dnaxYLY/view), and [OSPA work stream](https://www.opencompute.org/projects/networking/open-switch-platform-architecture/).

## Build

From the repository root, build using the approved narration with FFmpeg on PATH or `FFMPEG_BIN` set.

```sh
EXISTING_AUDIO_DIR=/absolute/path/to/approved/audio \
  ./scripts/build-course.sh meta-icecube
```

The approved audio directory contains `module1/` and `module2/`. The build stages the course in `build/meta-icecube/` and produces `build/meta-icecube.zip`. For a text-and-media preview without narration, run `SKIP_AUDIO=1 ./scripts/build-course.sh meta-icecube` and open the rendered Course Home. Use the LMS syllabus to launch each tracked entry.

The source records ElevenLabs v4, the Leo voice, pitch-preserving 1.18× pacing, and 96 kbps CBR mono MP3 delivery. If narration changes, review the timing of every paired animation against the finished audio. The animation renderer uses Pillow and FFmpeg. See its docstring for the command to rebuild a silent master.

```sh
python3 skills/academy-wizard/scripts/slides_course_qa.py \
  courses/meta-icecube/course.json --repo-root . --fail-on-flags
python3 skills/academy-wizard/scripts/course_delivery_summary.py \
  courses/meta-icecube/course.json --check
```
