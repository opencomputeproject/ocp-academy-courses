# Diablo Teaching Animations

These HTML canvas animations produce the silent WebM teaching figures and poster images referenced by `course.json`.

Run the course wrapper from this directory with Node.js, the installed
AcademyWizard skill and its Playwright Chromium, and a full ffmpeg build:

```bash
node record_module_videos.js
```

`record_module_videos.js` uses the skill's deterministic 1080p recorder for
all four assets. Set `FFMPEG_BIN` if ffmpeg is outside PATH or
`ACADEMY_WIZARD_SKILL_DIR` if the skill is installed in a different location.
Set `VIDEO_FILTER` to part of a video filename to regenerate one asset:

```bash
VIDEO_FILTER=serviceable_interface_path node record_module_videos.js
```

The scripts write encoded videos and posters to the sibling `figures/` directory.
