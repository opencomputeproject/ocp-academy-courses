# Validation

The reviewed local delivery passed package validation, exact manifest/ZIP membership and CRC checks, 148 course contract/media checks, narration signal checks, and desktop/390px phone playback checks. All eight teaching videos passed single-pass, pause/seek/speed, enlarged final-frame hold and intentional replay checks. Original recordings and captions remain byte-identical to the recovered source. H.264 chroma introduces slight colored-edge differences; measured fidelity below the aspirational 45 dB threshold is retained in `authoring/video-qa.json`.

Rebuild and verify from the repository before delivery:

```sh
python3 skills/academy-wizard/scripts/slides_course_qa.py courses/open-systems-for-ai/course.json --repo-root . --fail-on-flags
python3 skills/academy-wizard/scripts/course_delivery_summary.py courses/open-systems-for-ai/course.json --check
python3 courses/open-systems-for-ai/scripts/verify_course.py
EXISTING_AUDIO_DIR=/absolute/path/to/approved/audio bash scripts/build-course.sh open-systems-for-ai
python3 courses/open-systems-for-ai/scripts/verify_course.py build/open-systems-for-ai
```

`authoring/qa/` contains historical validation evidence, not an LMS acceptance certificate. A signal pass does not establish pronunciation or human listening approval. Actual target-LMS tracking, bookmarks, assessment restoration and course completion still require acceptance testing. This contribution does not upload, publish or merge the course.
