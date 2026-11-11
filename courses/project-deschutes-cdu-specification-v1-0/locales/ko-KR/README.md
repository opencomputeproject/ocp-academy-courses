# OCP Project Deschutes

ko-KR edition of the Project Deschutes CDU Specification v1.0 course.

See the [canonical course README](../../README.md) for the module outline, sources, shared poster, and delivery requirements. This folder contains the localized editable course, narration scripts, teaching media, and formal LMS catalog metadata.

## Build

From the repository root, set `ELEVENLABS_API_KEY` in the environment and run:

```sh
./scripts/build-course.sh project-deschutes-cdu-specification-v1-0/locales/ko-KR
```

The recorded voice uses full `eleven_v4` with 1.18x pitch-preserving pacing. The runtime uses 96 kbps CBR mono MP3. Generated audio, native masters, receipts, HTML, and SCORM ZIPs are not source-controlled. The approved teaching videos retain independent-loop playback.

## LMS Listing

Edit `lms_catalog` in `course.json`, then regenerate and check `lms-catalog.json` and `lms-catalog.md`. Packaging creates matching JSON, Markdown, and HTML sidecars outside the SCORM ZIP. This edition shares the [English catalog poster](../../thumbnail.png).

SCORM 1.2 is preserved, with Course Home and three tracked modules. Validate the rebuilt package in the target LMS before replacing a live edition.
