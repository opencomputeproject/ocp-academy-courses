// Exposed Chiplet player for imported recordings only. Generated teaching videos
// retain standard figure controls and the learner narration runtime.
const videoPreferenceKey = 'ocp-academy-video-preferences';
let videoPreferences = {};
try { videoPreferences = JSON.parse(localStorage.getItem(videoPreferenceKey) || '{}'); } catch (_) {}
function saveVideoPreferences() {
  if (!reviewMode) { try {localStorage.setItem(videoPreferenceKey, JSON.stringify(videoPreferences));} catch (_) {} }
}
document.querySelectorAll('[data-video-player]').forEach(player => {
  const video = player.querySelector('video');
  if (!video || !video.classList.contains('original-video')) return;
  const options = {preferences:videoPreferences, savePreferences:saveVideoPreferences, labels:(key,fallback)=>videoUiLabels[key] || fallback};
  window.AcademyVideoPlayer(player, options);
  video.addEventListener('play', () => {
    audioPlayer.pause();setAudioPlaying(false);disarmAutoplayFallback();
    document.querySelectorAll('video.original-video').forEach(other => {if(other!==video) other.pause();});
  });
  audioPlayer.addEventListener('play', () => video.pause());
  window.addEventListener('academy:slide', () => {
    if (!video.closest('.slide.active')) video.pause();
    if (player.academyRefresh) player.academyRefresh();
  });
});

