# Verification and release notes

The completed development build was checked with all thirty generated ElevenLabs clips. The source contribution retains scripts and the matching narration settings; generated audio, runtime pages, ZIPs, and original research files are excluded from Git.

The October 27, 2026 refresh regenerates all thirty clips with Eleven v4 and the existing Leo v2 voice. It updates the Open Data Center for AI destination and uses the current Slides layout and course-page review defaults. The course retains SCORM 1.2, its four syllabus entries, and its approved learner-time estimates.

## Content and media

- Three modules, thirty slides, three teaching animations, and six questions.
- Sixteen page-specific teaching/whole-document closing PDF links checked.
- Twenty-six glossary placements verified against narration, rendered text, and reviewed media inventories.
- Source Figures 5 and 19 preserve plotted evidence, units, axes, labels, and uncertainty markings. Their modeled and extrapolated scope is explained in the teaching.
- All ten scanned SVG/HTML sources pass arrow-geometry checks.
- Encodes use H.264, 1920×1080, 30 fps, silent tracks, and one complete finite master pass. Normalized comparisons exceed SSIM 0.995 and PSNR 45 dB; native and 200% detail reviews show readable edges and text.
- M1S5 has four equal illustrative 285-unit x-axis intervals. The dot turns yellow at 6.72 seconds and red at 11.62 seconds. Its 14-second encode contains 420 frames. The revised encode measures SSIM 0.999776 and PSNR 53.82 dB.
- M2S5 has 28.5 SVG units between the reference-condition text and the nearest circle outline. Its central label has a white backing and at least 19.5 units of interior clearance.
- The refresh preserves the three approved video files and the M2S5 SVG byte-for-byte. Five other static SVGs have fitted artboards, with unchanged labels and drawing geometry, audited ink bounds, and refreshed text-inventory hashes.
- The 800×400 poster was reviewed at native and reduced catalog-card size.

## Narration and browser checks

- All thirty regenerated v4 clips pass the audio signal report with zero remaining flags. Their original, unchanged Leo v2 / Multilingual v2 recordings at speed 1.18 are preserved separately as timing references. Pitch-preserving adjustment matches each reference within 7.574 milliseconds; the allowed tolerance is 50 milliseconds. Module totals are 618.499, 650.836, and 678.420 seconds.
- All thirty timing receipts match the actual output WAV hashes and original reference WAV hashes. Native masters and receipts remain outside the course runtime and ZIP.
- 188 local browser assertions cover resume, quiz selections/feedback, retry clearing, review isolation, home behavior, player controls, and real-media loop/seek behavior. The audio-pacing, chunked-audio, video-mode, and course-home unit suites pass 47 tests.
- Ninety slide views cover desktop light, desktop dark, and phone layouts, with no broken media, horizontal overflow, or JavaScript errors. Both revised figures were checked again in those views.
- The course home was checked at 1440, 1024, 640, 390, and 320 pixels, including informational tiles, the first-module start control, keyboard focus, and review behavior. Shared heading wrapping and the declared discretionary word break preserve the long course title on narrow phones.
- Thirty-three figure-caption views meet frame alignment, frame-width wrapping, at least 16px media/caption spacing, and at least 24px caption/learner-aid spacing. Actual course pages remain the primary review surface; no separate review site is produced.
- Package validation and strict ZIP integrity checks pass. All packaged files match the staged build; narration and unrelated media were unchanged by the two figure revisions.

## Acceptance boundary

A signal pass does not establish pronunciation or perceptual consistency; human listening review remains unverified. Local SCORM simulations do not establish actual LMS launch, syllabus navigation, resume, or separate module completion. Verify those behaviors in the target LMS before learner release. This refresh does not upload or replace LMS material.

## Approved LMS next-button follow-up

On October 27, 2026 the user approved direct green next-module buttons after the cross-SCO tracking limitation was explained. The course records the narrow `scorm.next_module_navigation: "direct"` override; Course Home remains guarded. The module-control regression suite passes 63 assertions, including default Syllabus layout, the narrow override, and full direct-link compatibility. Actual M1 and M2 ending pages show and navigate through the green button in four simulated LMS-context desktop/phone views. When the guarded default is used, its Syllabus instruction occupies its own line below the module heading. All thirty v4 recordings are retained unchanged.
