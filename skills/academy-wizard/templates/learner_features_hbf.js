// This template runs inside the module closure. Controls do not modify defaults.
const transcriptPanel = document.createElement('aside');
transcriptPanel.id = 'transcriptPanel'; transcriptPanel.className = 'transcript-panel';
transcriptPanel.setAttribute('aria-label', 'Slide transcript'); transcriptPanel.hidden = true;
transcriptPanel.innerHTML = '<button id="transcriptClose" class="learner-control">Close transcript</button><h2 id="transcriptTitle" tabindex="-1"></h2><div id="transcriptText"></div>';
document.body.appendChild(transcriptPanel);
const transcriptBtn = document.getElementById('transcriptBtn');
const narrationModeBtn = document.getElementById('narrationModeBtn');
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
  const hint = document.querySelector('.hero-start-hint span');
  if (hint && !autoPlayAudio) hint.textContent = 'Narration is off. Read the transcript or use Play for this slide.';
}
narrationModeBtn.addEventListener('click', () => {
  autoPlayAudio = !autoPlayAudio;
  if (!reviewMode) { try { localStorage.setItem('ocp-narration-enabled', String(autoPlayAudio)); } catch (_) {} }
  if (!autoPlayAudio) { audioPlayer.pause(); setAudioPlaying(false); disarmAutoplayFallback(); }
  else attemptAudioPlayback();
  updateNarrationMode();
});
// Approved HBF compatibility behavior: save the module once, never a slide bookmark.
window.addEventListener('academy:slide', updateTranscript);
if (inLMS) SCORM.setLocation('module' + document.querySelector('.module-badge-text').textContent.trim().replace(/\D/g, ''));
let requested = 1;
if (reviewMode) requested = Number(new URLSearchParams(location.search).get('slide') || 1);
requested = Math.min(totalSlides, Math.max(1, Number.isFinite(requested) ? requested : 1));
if (!reviewMode) {
  const gate = Array.from(slides).find(s => Number(s.dataset.slide) < requested && s.dataset.quizSlide === 'true' && Array.from(s.querySelectorAll('.quiz-card')).some(c => c.dataset.attempted !== 'true'));
  if (gate) requested = Number(gate.dataset.slide);
}
currentSlide = requested;
slides.forEach(s => {
  const active = Number(s.dataset.slide) === currentSlide;
  s.classList.toggle('active', active); s.inert = !active; s.setAttribute('aria-hidden', String(!active));
});
updateTranscript(); updateNarrationMode();
// Keep editorial review untracked across ordinary links too.
if (reviewMode) document.addEventListener('click', e => {
  const link = e.target.closest('a[href]'); if (!link) return;
  const url = new URL(link.getAttribute('href'), location.href);
  if (url.origin === location.origin && /\/(?:module\d+|index)\.html$/.test(url.pathname)) {
    e.preventDefault(); url.searchParams.set('review', '1'); location.href = url.href;
  }
});
// Finite video timelines span the narration; honor learner speed and seeking.
function alignVideo(seek) {
  const video = document.querySelector('.slide.active video.figure-video'); if (!video) return;
  video.playbackRate = audioPlayer.playbackRate;
  if (seek && Number.isFinite(video.duration)) video.currentTime = Math.min(audioPlayer.currentTime, Math.max(0, video.duration - 1 / 30));
}
audioPlayer.addEventListener('play', () => { alignVideo(true); const v = document.querySelector('.slide.active video.figure-video'); if (v) v.play().catch(() => {}); });
audioPlayer.addEventListener('seeking', () => alignVideo(true));
audioPlayer.addEventListener('ratechange', () => alignVideo(false));
audioPlayer.addEventListener('pause', () => { if (autoPlayAudio && !audioPlayer.ended) { const v = document.querySelector('.slide.active video.figure-video'); if (v) v.pause(); } });
