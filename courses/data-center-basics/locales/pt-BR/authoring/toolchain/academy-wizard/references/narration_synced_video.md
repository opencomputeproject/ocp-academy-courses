# Narration-synchronized teaching video

## Prefer a narration-timed single pass

For newly authored narrated Slides, prefer a substantive sequence timed to the
final narration. Use the narration clock, hold the completed conclusion, and
share pause, seek, replay and speed with narration, including the enlarged view.
Do not repeat a short reveal to fill a longer explanation or stretch an unsuitable
visual merely to meet a duration target; use a static figure when motion adds no
teaching value.

Record `narration.teaching_video_mode: "narration-synchronized"` and the explicit
per-figure settings below. These settings are essential: a duration-matched file
with `loop: true` will still cycle. Source QA must reject that mismatch.

Independent loops are exceptions for intentionally cyclic teaching that the user
has explicitly selected. Preserve an existing approved loop exception during a
rebuild unless conversion is requested. A request to time videos to narration or
hold their final scene already authorizes the corresponding conversion; do not
ask again for each clip. Original recordings remain separate and keep their own
soundtrack and player.

## Required ending for narration-timed videos

A video timed to narration plays exactly once on the narration clock, then holds
the completed final picture. It must not loop, rewind, or revert to its poster at
the end. Apply this in both the embedded and enlarged views, using the explicit
settings below; matching file durations is not enough. Pause, seek, speed and
learner-requested replay continue to follow narration. When reviewing a series,
audit every generated narration-timed video for this behavior, not just the first.

## Explicit per-figure opt-in

```json
{
  "path": "figures/controlled_connection.mp4",
  "media_type": "video",
  "poster": "figures/controlled_connection_poster.png",
  "alt": "Connection, bulk charging and load enable are separate events.",
  "caption": "Each transition needs its own readiness evidence.",
  "sync_to_narration": true,
  "autoplay": false,
  "loop": false,
  "muted": true
}
```

Pair this figure with the slide's normal `audio` block. Only the boolean `true`
enables the mode. Omitted/false flags, audio-only slides, native videos and the
Scrolling player retain their established behavior. For an explicitly retained
legacy compatibility profile, preserve that runtime and use the standard Slides
player before proposing synchronized media; do not silently replace the profile.

Review mode starts paused. In normal learner mode, narration keeps its established
autoplay preference. In reduced-motion mode, the figure shows its final summary
until the learner explicitly starts the video. Keep the transcript and a useful
caption so the learning remains available without motion.

## Produce against measured narration

Write the narrative and storyboard together; time each scene to the final WAV.
Keep the course's approved voice, model and speed. Use one audible narration
track and a silent video. Preserve editable scene timing and deterministic visual
sources. Label illustrative quantities and expanded event spacing; close circuit
paths and distinguish comparison resets from continuous events.

Match the encoded video to the measured narration within one video frame. Hold
important comparisons and the final conclusion. Follow the geometry, native-frame
and encode-quality checks in `figure_prompts.md`; add transition-adjacent frames.
Synchronize the source text, transcript, captions, references and reviewed media
inventory after any revision.

## Compatibility acceptance

Run `test_video_seek.mjs`, `test_video_playback_compatibility.mjs`, and
`test_video_modes.py` after shared player/renderer edits. Use
`test_video_modes_browser.mjs <legacy|synced> <built-course>` with real paired
media to check the first matching teaching video and an audio-only slide. Pass an
optional `M<n>S<n>` argument to select each additional video in a series. For every
narration-timed video, let narration end, wait at least one second, verify the
embedded and enlarged views stay paused on the completed picture, then verify
intentional replay. Repeat with `VIDEO_TEST_VIEWPORT=phone` for the phone layout;
`VIDEO_QA_DIR` optionally saves the completed enlarged view for visual review.
Browser checks must
cover real legacy loops, an audio-only slide, and an opted-in sequence, including
pause/resume, seeking beyond one old loop, speed, end/replay, slide return, zoom,
review mode, narration preference and reduced motion. Check buffering events do
not alter legacy playback. Run the maintained narration/control and quiz/resume
regressions against representative rebuilt courses. Test silent/muted playback.

Do not let synchronized-only listeners touch unmarked media. In particular, an
old loop must keep its historical behavior when narration ends, on metadata load,
on buffering recovery and in its independent enlarged view. A local pass does
not establish target-LMS navigation or tracking compatibility.
