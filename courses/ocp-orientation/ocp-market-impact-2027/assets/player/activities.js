// Course-specific activities share the Academy player's audio clock.
const marketData = MARKET_ACTIVITY_DATA;
function marketStillTime(video) {
  const lastFrame = video.duration - 1 / 24;
  if (currentSlide !== 3 || audioPlayer.ended) return lastFrame;
  if (!document.querySelector('.prediction-result').hidden) {
    return audioPlayer.currentTime >= marketData[3].horizon_at ? lastFrame : marketData[3].reveal_at;
  }
  return marketData[3].pause_at;
}
const projectStore = 'ocp:market-impact-2027:project';
let projectIndex = null;
try {
  const stored = localStorage.getItem(projectStore);
  if (stored !== null && /^[0-3]$/.test(stored)) projectIndex = Number(stored);
} catch (_) {}
function seekNarratedScene(number, time) {
  const seek = () => {
    if (currentSlide === number && Number.isFinite(audioPlayer.duration)) {
      audioPlayer.currentTime = Math.min(time, audioPlayer.duration);
    }
  };
  if (audioPlayer.readyState >= 1) seek();
  else audioPlayer.addEventListener('loadedmetadata', seek, {once:true});
}
function chooseOption(area, index) {
  const number = Number(area.dataset.activity);
  const item = marketData[number].options[index];
  area.querySelectorAll('[data-option]').forEach((button,i)=>button.setAttribute('aria-pressed',String(i===index)));
  const result = area.querySelector('.activity-result');
  result.hidden = false;
  result.querySelector('p').textContent = item.text;
  const link = result.querySelector('a');
  link.hidden = !item.url;
  if (item.url) { link.href=item.url; link.textContent=item.action; }
  if (item.listen_at != null && currentSlide === number) {
    seekNarratedScene(number, audioPlayer.paused ? item.look_at : item.listen_at);
  }
  if (number === 10) {
    try { localStorage.setItem(projectStore,String(index)); } catch (_) {}
  }
}
document.querySelectorAll('[data-option]').forEach(button=>{
  button.addEventListener('click',()=>chooseOption(button.closest('[data-activity]'),Number(button.dataset.option)));
});
if (projectIndex !== null) chooseOption(document.querySelector('[data-activity="10"]'),projectIndex);

const forecastBox=document.querySelector('[data-activity="3"]');
const guess=forecastBox.querySelector('input');
const output=forecastBox.querySelector('output');
const waitPoint=marketData[3].pause_at;
let predictionDone=false;
let waiting=false;
let lastNarrationTime=0;
const response=forecastBox.querySelector('.prediction-result');
guess.addEventListener('input',()=>{output.textContent='$'+guess.value+'B';guess.setAttribute('aria-valuetext',guess.value+' billion dollars');});
function resetForecast() {
  predictionDone=false; waiting=false; lastNarrationTime=0;
  forecastBox.querySelector('.guess-controls').hidden=false;
  response.hidden=true;
  forecastBox.querySelector('.extra-forecast').open=false;
}
forecastBox.querySelectorAll('[data-reveal]').forEach(button=>{
  button.addEventListener('click',()=>{
    const shouldPlay=waiting;
    predictionDone=true;waiting=false;
    response.hidden=false;
    const preface=button.dataset.reveal==='guess'?'Your estimate was $'+guess.value+'B. ':'';
    response.textContent=preface+'IDC’s new forecast was about $800B for 2029, roughly 2.7 times its prior $295B estimate.';
    forecastBox.querySelector('.guess-controls').hidden=true;
    response.focus({preventScroll:true});
    if (shouldPlay) attemptAudioPlayback();
    else if (audioPlayer.currentTime < waitPoint) {
      seekNarratedScene(3, audioPlayer.paused ? marketData[3].reveal_at : waitPoint);
    }
  });
});
window.addEventListener('academy:slide',e=>{if(e.detail===3) resetForecast();});
audioPlayer.addEventListener('timeupdate',()=>{
  if(currentSlide!==3)return;
  const now=audioPlayer.currentTime;
  if(!predictionDone && !waiting && !audioPlayer.paused && !audioPlayer.seeking && lastNarrationTime<waitPoint && now>=waitPoint && now<waitPoint+.9) {
    waiting=true;
    audioPlayer.pause();
    audioPlayer.currentTime=waitPoint;
    setAudioPlaying(false);
    document.querySelector('.lightbox-overlay')?.click();
    guess.focus({preventScroll:true});
    forecastBox.scrollIntoView({block:'nearest',behavior:'instant'});
  }
  if(now<.2 && lastNarrationTime>waitPoint && !waiting)resetForecast();
  lastNarrationTime=now;
});
audioPlayer.addEventListener('play',()=>{
  if(currentSlide===3 && waiting) {
    waiting=false;predictionDone=true;
    forecastBox.querySelector('.guess-controls').hidden=true;
    response.textContent='IDC projected about $800B for 2029.';response.hidden=false;
  }
});
