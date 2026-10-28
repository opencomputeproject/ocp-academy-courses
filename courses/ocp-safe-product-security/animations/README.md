# Teaching animation sources

These four finite, editable HTML/SVG timelines correspond to M1S4, M2S5, M3S4 and M3S6. Each diagram remains on its final state after a single pass. Scene timing comes from measured approved narration, recorded in the `.timing.json` sidecars and `../authoring/animation-sync.json`.

Edit a timing sidecar, then run `python3 animations/apply_timing.py animations/<name>.timing.json`. The maintained `record_css_animation.mjs` captures lossless PNG frames at 1080p and encodes high-quality H.264. Use a full ffmpeg build and explicit dependency paths when needed. Inspect transition frames, the full timeline and encoded final state with playback muted; align the encode with the matching approved WAV within one frame. Do not restore provisional storyboard defaults or regenerate narration solely to fit a visual.

Local Lato WOFF assets are licensed under SIL OFL; see `fonts/OFL.txt`. Learner teaching remains available in slide text, figure descriptions and narration transcripts without motion.
