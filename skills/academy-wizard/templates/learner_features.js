// This template runs inside the module closure. Controls do not modify defaults.

// Keep desktop glossary bubbles inside the viewport, including rightmost pills.
function fitGlossaryTooltip(chip) {
  if (!chip) return;
  const style = getComputedStyle(chip, '::after');
  if (style.position !== 'absolute') return; // Mobile retains its shared fixed inset.
  const extras = style.boxSizing === 'border-box' ? 0
    : parseFloat(style.paddingLeft) + parseFloat(style.paddingRight)
      + parseFloat(style.borderLeftWidth) + parseFloat(style.borderRightWidth);
  const width = parseFloat(style.width) + extras;
  if (!Number.isFinite(width)) return;
  const anchor = chip.getBoundingClientRect().left + chip.clientLeft;
  const inset = 16;
  const left = Math.max(inset, Math.min(anchor, window.innerWidth - inset - width));
  chip.style.setProperty('--glossary-tip-offset', (left - anchor) + 'px');
}
document.addEventListener('pointerover', event => fitGlossaryTooltip(event.target.closest?.('.glossary-chip')));
document.addEventListener('focusin', event => fitGlossaryTooltip(event.target.closest?.('.glossary-chip')));
window.addEventListener('resize', () => {
  document.querySelectorAll('.slide.active .glossary-chip:hover, .slide.active .glossary-chip:focus').forEach(fitGlossaryTooltip);
});


const authoredHeadingSizes = new WeakMap();
function fitHeadingWords() {
  const canvas = document.createElement('canvas');
  const context = canvas.getContext('2d');
  if (!context) return;
  document.querySelectorAll('.slide-title, .hero-title').forEach(heading => {
    if (!authoredHeadingSizes.has(heading)) authoredHeadingSizes.set(heading, heading.style.fontSize);
    heading.style.fontSize = authoredHeadingSizes.get(heading);
    const width = heading.clientWidth;
    if (!width) return;
    const style = getComputedStyle(heading);
    context.font = `${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
    const tracking = parseFloat(style.letterSpacing) || 0;
    const words = typeof Intl.Segmenter === 'function'
      ? Array.from(new Intl.Segmenter(document.documentElement.lang || 'en', {granularity: 'word'}).segment(heading.textContent))
          .filter(segment => segment.isWordLike).map(segment => segment.segment)
      : heading.textContent.trim().split(/[\s\u2010-\u2015-]+/);
    const widest = Math.max(0, ...words.map(word => {
      const text = style.textTransform === 'uppercase' ? word.toUpperCase() : word;
      return context.measureText(text).width + Math.max(0, Array.from(text).length - 1) * tracking;
    }));
    // Preserve authored type sizes unless a single word cannot fit its container.
    if (widest > width) heading.style.fontSize = `${parseFloat(style.fontSize) * width / widest * .99}px`;
  });
}
fitHeadingWords();
document.fonts?.ready.then(fitHeadingWords);
window.addEventListener('resize', fitHeadingWords);
const transcriptPanel = document.createElement('aside');
transcriptPanel.id = 'transcriptPanel'; transcriptPanel.className = 'transcript-panel';
transcriptPanel.setAttribute('aria-label', 'Slide transcript'); transcriptPanel.hidden = true;
transcriptPanel.innerHTML = '<button id="transcriptClose" class="learner-control">Close transcript</button><h2 id="transcriptTitle" tabindex="-1"></h2><div id="transcriptText"></div>';
document.body.appendChild(transcriptPanel);
const lmsNote = document.createElement('div');
lmsNote.className = 'lms-navigation-note'; lmsNote.hidden = true; lmsNote.setAttribute('role','status');
lmsNote.textContent = 'Use the LMS course navigation to open another module so its completion is recorded correctly.';
document.body.appendChild(lmsNote);
const transcriptBtn = document.getElementById('transcriptBtn');
const narrationModeBtn = document.getElementById('narrationModeBtn');
const narrationHint = document.querySelector('.hero-start-hint span');
const narrationEnabledHint = narrationHint ? narrationHint.textContent : '';
function updateTranscript() {
  const entry = transcriptMap[String(currentSlide)] || {};
  document.getElementById('transcriptTitle').textContent = entry.title || 'Transcript';
  const body = document.getElementById('transcriptText'); body.replaceChildren();
  for (const paragraph of (entry.text || 'No narration on this slide.').split(/\n\s*\n/)) {
    const p = document.createElement('p'); p.textContent = paragraph; body.appendChild(p);
  }
}
function closeTranscript() {
  transcriptPanel.hidden = true; transcriptBtn.setAttribute('aria-expanded', 'false'); transcriptBtn.focus();
}
transcriptBtn.addEventListener('click', () => {
  const opening = transcriptPanel.hidden; transcriptPanel.hidden = !opening;
  transcriptBtn.setAttribute('aria-expanded', String(opening));
  if (opening) { updateTranscript(); document.getElementById('transcriptTitle').focus(); }
});
document.getElementById('transcriptClose').addEventListener('click', closeTranscript);
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && !transcriptPanel.hidden) { e.preventDefault(); closeTranscript(); }
});
function updateNarrationMode() {
  narrationModeBtn.setAttribute('aria-pressed', String(autoPlayAudio));
  narrationModeBtn.title = autoPlayAudio ? 'Narration on — click to turn off' : 'Narration off — click to turn on';
  if (narrationHint) narrationHint.textContent = autoPlayAudio
    ? narrationEnabledHint
    : 'Narration is off. Read the transcript or use Play for this slide.';
}
narrationModeBtn.addEventListener('click', () => {
  autoPlayAudio = !autoPlayAudio;
  if (!reviewMode) { try { localStorage.setItem('ocp-narration-enabled', String(autoPlayAudio)); } catch (_) {} }
  if (!autoPlayAudio) { audioPlayer.pause(); setAudioPlaying(false); disarmAutoplayFallback(); }
  else attemptAudioPlayback();
  updateNarrationMode();
});
function storeBookmark() {
  updateTranscript(); if (reviewMode) return;
  const value = 'module' + document.querySelector('.module-badge-text').textContent.trim().replace(/\D/g, '') + ':slide' + currentSlide;
  if (inLMS) SCORM.setLocation(value);
  else { try { localStorage.setItem(BOOKMARK_KEY, value); } catch (_) {} }
}
window.addEventListener('academy:slide', storeBookmark);
let requested = 1;
let moduleCompleted = false;
if (reviewMode) requested = Number(new URLSearchParams(location.search).get('slide') || 1);
else {
  let saved = inLMS ? SCORM.getLocation() : '';
  if (!inLMS) { try { saved = localStorage.getItem(BOOKMARK_KEY) || ''; } catch (_) {} }
  const ownModule = document.querySelector('.module-badge-text').textContent.trim().replace(/\D/g, '');
  const match = saved.match(/^module(\d+):slide(\d+)$/);
  const completed = getSuspendObject().modules;
  const hasOwnCompletion = Array.isArray(completed) && completed.includes(Number(ownModule));
  // Completion survives a later visit to earlier slides or a quiz retry.
  // In direct-link deployments, another SCO's completed flag alone is not
  // evidence that the target module is complete.
  const ownsLocation = saved === 'module' + ownModule || (match && match[1] === ownModule);
  moduleCompleted = inLMS
    ? (existingStatus === 'completed' || existingStatus === 'passed') && (ownsLocation || hasOwnCompletion)
    : hasOwnCompletion;
  if (moduleCompleted) requested = totalSlides;
  else if (match && match[1] === ownModule) requested = Number(match[2]);
}
requested = Math.min(totalSlides, Math.max(1, Number.isFinite(requested) ? requested : 1));
if (!reviewMode && !moduleCompleted) {
  const gate = Array.from(slides).find(s => Number(s.dataset.slide) < requested && s.dataset.quizSlide === 'true' && Array.from(s.querySelectorAll('.quiz-card')).some(c => c.dataset.attempted !== 'true'));
  if (gate) requested = Number(gate.dataset.slide);
}
currentSlide = requested;
slides.forEach(s => {
  const active = Number(s.dataset.slide) === currentSlide;
  s.classList.toggle('active', active); s.inert = !active; s.setAttribute('aria-hidden', String(!active));
});
storeBookmark(); updateNarrationMode();
// A multi-SCO LMS owns module changes. Replace local page-jump controls with
// honest instructions instead of presenting a button that refuses the click.
if (inLMS && !reviewMode && !SCORM.isSingleSCO && !directModuleLinks) {
  document.querySelectorAll('a[href]').forEach(link => {
  if (directNextModuleLinks && link.matches('.next-module-link')) return;
  const url = new URL(link.getAttribute('href'), location.href);
  if (url.origin === location.origin && /\/(?:module\d+|index)\.html$/.test(url.pathname)) {
    const target = url.pathname.match(/module(\d+)\.html$/);
    const note = document.createElement('p');
    note.className = 'lms-module-handoff';
    note.textContent = target
      ? 'Continue with Module ' + target[1] + ' using the Syllabus in the left sidebar.'
      : 'Open Course Home using the Syllabus in the left sidebar.';
    note.style.cssText = 'margin:16px 0;font-size:1rem;line-height:1.6;color:var(--text-secondary);';
    const heading = link.closest('.next-module-heading');
    if (heading) {
      heading.after(note);
      link.remove();
    } else {
      link.replaceWith(note);
    }
  }
  });
}
if (reviewMode) document.addEventListener('click', e => {
  const link = e.target.closest('a[href]'); if (!link) return;
  const url = new URL(link.href);
  const nextModule = link.matches('.next-module-link') && /\/module\d+\.html$/.test(url.pathname);
  const home = /\/index\.html$/.test(url.pathname);
  if (url.origin !== location.origin || (!nextModule && !home)) return;
  e.preventDefault();
  url.searchParams.set('review', '1');
  if (nextModule) url.searchParams.set('slide', '1');
  location.href = url.href;
});
// The historical player remains the default. Only explicitly marked videos
// use the narration-master timeline and synchronized enlarged view.
let motionOptIn = false;
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
function isSyncedVideo(video) { return video?.dataset.narrationSync === 'true'; }
function legacyTeachingVideo() {
  const video = document.querySelector('.slide.active video.figure-video');
  return video && !isSyncedVideo(video) ? video : null;
}
function activeSyncedVideos() {
  return Array.from(document.querySelectorAll('.slide.active video.figure-video, .lightbox-overlay video.figure-video')).filter(isSyncedVideo);
}
function motionEnabled() { return !reducedMotion.matches || motionOptIn; }
function alignVideo(seek) {
  // Preserve the old loop/finite seek and rate policy exactly for unmarked media.
  const video = legacyTeachingVideo(); if (!video) return;
  video.playbackRate = audioPlayer.playbackRate;
  if (seek && Number.isFinite(video.duration) && video.duration > 0) {
    const visualTime = video.loop
      ? audioPlayer.currentTime % video.duration
      : Math.min(audioPlayer.currentTime, video.duration);
    video.currentTime = Math.max(0, Math.min(visualTime, video.duration - 1 / 60));
  }
}
function alignSyncedVideos(seek) {
  activeSyncedVideos().forEach(video => {
    video.playbackRate = audioPlayer.playbackRate;
    if (!Number.isFinite(video.duration) || video.duration <= 0) return;
    const visualTime = !motionEnabled() ? video.duration - 1 / 24
      : Math.min(audioPlayer.currentTime, video.duration);
    if (seek || Math.abs(video.currentTime - visualTime) > .25) {
      video.currentTime = Math.max(0, Math.min(visualTime, video.duration - 1 / 60));
    }
  });
}
function updateTeachingVideoControls() {
  activeSyncedVideos().forEach(video => {
    const button = video.closest('.figure-panel')?.querySelector('[data-video-toggle]');
    if (!button) return;
    const paused = audioPlayer.paused || !motionEnabled();
    button.innerHTML = paused ? '<span class="video-icon video-icon-play" aria-hidden="true"></span>' : '<span class="video-icon video-icon-pause" aria-hidden="true"></span>';
    button.setAttribute('aria-label', paused ? 'Play narrated video' : 'Pause narrated video');
    button.title = paused ? 'Play narrated video' : 'Pause narrated video';
  });
}
function playSyncedVideos() {
  const videos = activeSyncedVideos(); if (!videos.length) return;
  setAudioPlaying(true);
  alignSyncedVideos(true);
  videos.forEach(video => {
    if (motionEnabled() && !audioPlayer.ended) video.play().catch(() => {});
    else video.pause();
  });
  updateTeachingVideoControls();
}
function pauseSyncedVideos() {
  const videos = activeSyncedVideos(); if (!videos.length) return;
  if (audioPlayer.paused) setAudioPlaying(false);
  videos.forEach(video => video.pause());
  updateTeachingVideoControls();
}
// The four legacy listeners retain their original triggers and side effects.
audioPlayer.addEventListener('play', () => {
  alignVideo(true); const video = legacyTeachingVideo();
  if (video) video.play().catch(() => {});
  playSyncedVideos();
});
audioPlayer.addEventListener('seeking', () => { alignVideo(true); alignSyncedVideos(true); });
audioPlayer.addEventListener('ratechange', () => { alignVideo(false); alignSyncedVideos(false); });
audioPlayer.addEventListener('pause', () => {
  if (autoPlayAudio && !audioPlayer.ended) { const video = legacyTeachingVideo(); if (video) video.pause(); }
  pauseSyncedVideos();
});
// These additional triggers must never act on legacy videos or audio-only slides.
audioPlayer.addEventListener('playing', playSyncedVideos);
audioPlayer.addEventListener('waiting', pauseSyncedVideos);
audioPlayer.addEventListener('timeupdate', () => alignSyncedVideos(false));
audioPlayer.addEventListener('ended', () => { alignSyncedVideos(true); pauseSyncedVideos(); });
document.querySelectorAll('video.figure-video').forEach(video => {
  if (!isSyncedVideo(video)) return;
  video.addEventListener('loadedmetadata', () => {
    if (!video.closest('.slide.active')) return;
    alignSyncedVideos(true);
    if (audioPlayer.paused || !motionEnabled()) video.pause();
    else video.play().catch(() => {});
    updateTeachingVideoControls();
  });
});
document.addEventListener('click', e => {
  const button = e.target.closest('[data-video-toggle]');
  const video = button?.closest('.figure-panel')?.querySelector('video.figure-video');
  if (!video || !isSyncedVideo(video)) return;
  e.preventDefault(); e.stopImmediatePropagation();
  if (!motionEnabled()) { motionOptIn = true; if (audioPlayer.paused) attemptAudioPlayback(); else playSyncedVideos(); }
  else if (audioPlayer.paused) { if (audioPlayer.ended) audioPlayer.currentTime = 0; attemptAudioPlayback(); }
  else audioPlayer.pause();
}, true);
window.addEventListener('academy:slide', () => { alignSyncedVideos(true); updateTeachingVideoControls(); });
