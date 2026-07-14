# Diablo Teaching Animations

These HTML canvas animations produce the silent WebM teaching figures and poster images referenced by `course.json`.

Run both recorders from this directory with Node.js and Playwright available:

```bash
node record_module_videos.js
node record_diablo_power_path.js
```

`record_module_videos.js` generates the Module 1, 3, and 4 assets. Set `VIDEO_FILTER` to part of a video filename to regenerate only one of them, for example:

```bash
VIDEO_FILTER=serviceable_interface_path node record_module_videos.js
```

The scripts write encoded videos and posters to the sibling `figures/` directory.
