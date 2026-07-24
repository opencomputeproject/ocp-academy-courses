# Translating an existing Scrolling course

Keep the canonical course immutable. Each translated edition lives at
`locales/<BCP-47 tag>/course.json` below the canonical Scrolling course.

## Scaffold

Run:

```bash
python scripts/scaffold_scrolling_translation.py <canonical-course-folder> <BCP-47-tag>
```

Translate learner-visible content in the locale `course.json`, preserving IDs,
block types, lesson order, styles, links, facts, and interaction structure. Set
`language`, `metadata_language_name`, localized `ui_labels`, and retain the
generated `localization` provenance object.

## Resources

The locale is a lightweight overlay. The build begins with the canonical
`resources/` tree and overlays files from `locales/<tag>/resources/` at the same
relative paths. Put only resources that differ by language in the locale:

- translated or dubbed video under `resources/videos/`;
- translated WebVTT under `resources/captions/`;
- localized images only when visible text is baked into the bitmap;
- localized documents when the learner attachment itself is translated.

Use the canonical relative filename when a localized resource replaces the
canonical one. This keeps the locale course definition readable and prevents
both language versions of a large video from entering one SCORM package.

For an intentionally untranslated video, retain the canonical media and add a
localized visible notice immediately above it explaining the limitation.

## Video dubbing

Use a natural utterance segmentation rather than synthesizing each caption cue
separately. Preserve years, values, acronyms, product names, and visual timing.
Generate a target-language VTT from the approved utterances. Never carry the
original audio stream directly into a dubbed video. Prefer a verified isolated
music/effects stem, when one exists, and mix the aligned target-language voice
over that stem.

When no isolated stem exists, use the three reusable tracks in
`assets/background-music/` unless the user requests voice only. Distribute the
tracks as evenly as possible across a training series: usage counts may differ
by at most one. Sort videos by duration and give the longest music assets to the
longest videos while preserving that balanced rotation. Keep the same track on
all language editions of a given source video.

Run `scripts/mix_localized_video.py` with the retained voice-only master. It
normalizes music to -27 LUFS, fades it in over 1.5 seconds, sidechain-ducks it
under actual narration, restores it between phrases, and fades it over the
final four seconds. Map the original video stream but never its audio stream.
Do not copy the MP3 assets or their attribution note into the course or SCORM.

Avoid repeating a track when any longer bundled track can cover the video while
maintaining balanced use. If a video is longer than every bundled track, warn
the user and select the longest track. Repeat its complete natural ending from
the beginning without an artificial crossfade; the track's built-in ending
provides the transition. Still apply the normal fade only at the video's final
end. Record the selected asset, its hash, repetition state, ducking parameters,
and the preserved voice-only master in the dubbing manifest.

Use a processed version of the original soundtrack only when the user
explicitly rejects both the bundled music and voice-only alternatives and
accepts residual source-language speech. Never describe center suppression as
speech-free.

Validate the final single audio stream, language tag, audible music before and
between narration, foreground narration level, end fade, absence of mapped
source audio, and packaged-video hash.

For Vietnamese (`vi` and regional variants), use
`eleven_flash_v2_5` or a later model with explicit Vietnamese support. Do not
use `eleven_multilingual_v2`; the API may return billable audio even though
that model does not support Vietnamese.

Before submitting any localized video script to ElevenLabs, run the shared
model/language preflight:

```bash
python scripts/elevenlabs_model_support.py <BCP-47-tag> <model-id>
```

The check uses ElevenLabs' live model catalog when credentials are available
and otherwise permits only combinations in its bundled official-documentation
table. Do not generate a paid sample when the result is unsupported or
unverifiable. When another dubbing language is added, record its model in the
dubbing manifest and run this preflight before the first segment.

For Simplified Chinese (`zh-CN` or `zh-Hans`), use the approved ElevenLabs Lan
Chen voice (`bZtjnyJAFD0Cp3lfNG5g`) unless the user selects another voice.

## Build and validate

Build the locale as its own course path, for example:

```bash
./scripts/build-course.sh intro-to-ocp/module-1-the-ocp-origins/locales/ko-KR
```

The resulting SCORM is self-contained even though the checked-in locale stores
only translated source deltas.
