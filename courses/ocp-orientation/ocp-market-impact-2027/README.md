# OCP Market Impact: What We’re Building in 2027

This standalone OCP Orientation course looks back at the 2026 Global Summit and invites learners to join the work ahead. One narrated module includes seven interactive videos and a two-question knowledge check. Estimated learner time is 22 minutes. Course Home and Module 1 are separate SCORM 1.2 syllabus entries.

## Build and maintain

The editable content is in `course.json`. The HTML renderer and `assets/player/` add the prediction pause, project choices and closing actions to the Academy player. The recorded voice is Eleven v4, Leo. The public references are in the slide data. The November 2026 Academy participation figures were supplied by the Academy team.

From the repository root, set `EXISTING_AUDIO_DIR` to the approved narration audio directory (containing `module1/`) and run `./scripts/build-course.sh ocp-orientation/ocp-market-impact-2027`. The committed videos are timed to that recording. Narration masters are retained by the Academy production team.

For a new take, edit `authoring/Narration.md` and run `authoring/record.py` with the affected slide numbers and the ElevenLabs key in the environment. Use `authoring/compile_media.py prepare` and then `encode` with the same temporary work directory and slide numbers to rebuild the video against its word timings. This requires FFmpeg and the Node sharp library. Run `authoring/assemble.py` to refresh the transcripts, interaction timings and media inventories before building with the revised audio. Open the course Home and module pages to verify the forecast pause and final-frame holds.

Use `thumbnail.png` for the Academy course poster and `lms-catalog.json` for the approved Docebo metadata.
