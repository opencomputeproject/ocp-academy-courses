# Narration-synchronized teaching video

## Recommend, then obtain approval

Prefer recommending a substantive timed sequence when the lesson benefits from
following a circuit, changing quantity, comparison case or operating decision.
Do not lengthen a simple loop just to fill time or impose a video where a static
comparison teaches better.

The established default remains a silent short video with `autoplay: true`,
`loop: true`, `muted: true`, and no `sync_to_narration` flag. Explain the proposed
single-pass alternative before producing it: it follows the narration clock,
holds its conclusion, and shares pause, seek, replay and speed with narration,
including the enlarged view. Obtain user approval for the course or selected
slides and record that approval in editable course metadata or the figure plan.
An existing recorded approval is sufficient; do not ask again. A general rebuild,
permission to finish, or a request for a video alone does not approve conversion
of existing loops. Preserve their authored settings unless conversion is requested.

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
media to check the first matching teaching video and an audio-only slide. Browser checks must
cover real legacy loops, an audio-only slide, and an opted-in sequence, including
pause/resume, seeking beyond one old loop, speed, end/replay, slide return, zoom,
review mode, narration preference and reduced motion. Check buffering events do
not alter legacy playback. Run the maintained narration/control and quiz/resume
regressions against representative rebuilt courses. Test silent/muted playback.

Do not let synchronized-only listeners touch unmarked media. In particular, an
old loop must keep its historical behavior when narration ends, on metadata load,
on buffering recovery and in its independent enlarged view. A local pass does
not establish target-LMS navigation or tracking compatibility.
