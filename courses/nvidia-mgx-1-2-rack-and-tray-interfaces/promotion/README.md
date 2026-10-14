# LinkedIn promotion

- [30-second video with music](MGX_1.2_LinkedIn_Promo.mp4)
- [Identical silent video](MGX_1.2_LinkedIn_Promo_Silent.mp4)
- [1080-square cover](MGX_1.2_LinkedIn_Cover.png)
- [Short LinkedIn post](LinkedIn_Post.txt)

Use the post upon arrival at the 2026 OCP Global Summit's NVIDIA Reception @ MGX
Wall. It contains the live course URL. No post has been published or scheduled.
The video combines actual course footage with actual Course Home screenshots.
Large on-screen text carries the message without sound.

Both MP4s are 1080 × 1080, 30 fps, H.264 with fast-start delivery. The music
version adds AAC stereo. The source remains editable in `source/`; the frame
extraction recipe preserves the reviewed crop and time acceleration of each clip.

Install Pillow and FFmpeg, then run from the course folder:

```bash
python promotion/source/prepare_clips.py
python promotion/source/build_promo.py --preview
python promotion/source/build_promo.py
python promotion/source/verify_promo.py
```

The composer resolves the background track from the repository's AcademyWizard
bundle; set `ACADEMY_WIZARD_SKILL_DIR` or `PROMO_MUSIC_FILE` when using another
location. `FFMPEG_BIN` selects FFmpeg if needed. Decoded intermediate frames and
review images are ignored. Retained `source/verification/` reports apply to the
delivered MP4s; regenerate checks after changing the edit.

See [production notes](source/PRODUCTION_NOTES.txt) for footage, event wording,
and music attribution. The CAD separation and simultaneous-maxima force example
retain their illustrative status in the promotion.
