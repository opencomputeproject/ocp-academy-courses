# Verification and release notes

The completed development build was checked with all thirty generated ElevenLabs clips. The source contribution retains scripts and the matching narration settings; generated audio, runtime pages, ZIPs, and original research files are excluded from Git.

## Content and media

- Three modules, thirty slides, three teaching animations, and six questions.
- Sixteen page-specific teaching/whole-document closing PDF links checked.
- Twenty-six glossary placements verified against narration, rendered text, and reviewed media inventories.
- Source Figures 5 and 19 preserve plotted evidence, units, axes, labels, and uncertainty markings. Their modeled and extrapolated scope is explained in the teaching.
- All eleven scanned SVG/HTML sources pass arrow-geometry checks.
- Encodes use H.264, 1920×1080, 30 fps, silent tracks, and one complete finite master pass. Normalized comparisons exceed SSIM 0.995 and PSNR 45 dB; native and 200% detail reviews show readable edges and text.
- M1S5 has four equal illustrative 285-unit x-axis intervals. The dot turns yellow at 6.72 seconds and red at 11.62 seconds. Its 14-second encode contains 420 frames. The revised encode measures SSIM 0.999776 and PSNR 53.82 dB.
- M2S5 has 28.5 SVG units between the reference-condition text and the nearest circle outline. Its central label has a white backing and at least 19.5 units of interior clearance.
- The 800×400 poster was reviewed at native and reduced catalog-card size.

## Narration and browser checks

- All thirty clips pass the audio signal report with zero remaining flags. Targeted retries preserved Leo v2, Multilingual v2, and speed 1.18.
- Eighty-one local browser assertions cover resume, quiz selections/feedback, retry clearing, review isolation, and looping/finite video seek behavior.
- Ninety slide views cover desktop light, desktop dark, and phone layouts, with no broken media, horizontal overflow, or JavaScript errors. Both revised figures were checked again in those views.
- The course home was checked at 1440, 1024, 640, 390, and 320 pixels, including informational tiles, the first-module start control, keyboard focus, and review behavior. Shared heading wrapping and the declared discretionary word break preserve the long course title on narrow phones.
- Package validation and strict ZIP integrity checks pass. All packaged files match the staged build; narration and unrelated media were unchanged by the two figure revisions.

## Acceptance boundary

A signal pass does not establish pronunciation or perceptual consistency; human listening review remains unverified. Local SCORM simulations do not establish actual LMS launch, syllabus navigation, resume, or separate module completion. Verify those behaviors in the target LMS before learner release. This PR adds course source and does not upload or replace LMS material.
