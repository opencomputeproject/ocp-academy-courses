# FCSA teaching video sources

Five deterministic vector sequences follow the measured narration in
`../../video_source/video-timing.json`. Approved source constraints and scene
plans are in `../../video_source/storyboards/`. The finished videos and posters
are in `../../figures/`.

Install Node dependencies from the course root with `npm install`, install
`requirements-media.txt` in a Python environment, and put FFmpeg with libx264
on PATH (or set `FFMPEG_BIN`). `SHARP_MODULE` can select a different Sharp path.

From the course root, sample or export a sequence with:

```sh
python3 -m tools.synced_video.produce samples --only m1
node tools/synced_video/rasterize.mjs samples m1
python3 -m tools.synced_video.produce encode --only m1
node tools/synced_video/rasterize.mjs encode m1
```

Outputs stage under ignored `audit/` and `_video_work/` folders. Review full-size
frames and transitions before replacing an approved video. If narration changes,
realign the scene timings and update the media evidence in `course.json`.
