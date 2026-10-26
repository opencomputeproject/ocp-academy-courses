// Event-level differential regression against the pre-sync player policy.
// No browser, audio playback, network or TTS is used.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
const current = '// ' + fs.readFileSync(fileURLToPath(new URL('../templates/learner_features.js', import.meta.url)), 'utf8').split('// The historical player remains the default.')[1];
assert.ok(current, 'Explicit playback-policy boundary');
// Frozen behavior from main before synchronized video was introduced.
const previous = `
function alignVideo(seek) {
 const video = document.querySelector('.slide.active video.figure-video'); if (!video) return;
 video.playbackRate = audioPlayer.playbackRate;
 if (seek && Number.isFinite(video.duration) && video.duration > 0) {
  const t = video.loop ? audioPlayer.currentTime % video.duration : Math.min(audioPlayer.currentTime, video.duration);
  video.currentTime = Math.max(0, Math.min(t, video.duration - 1 / 60));
 }
}
audioPlayer.addEventListener('play', () => { alignVideo(true); const v = document.querySelector('.slide.active video.figure-video'); if (v) v.play().catch(() => {}); });
audioPlayer.addEventListener('seeking', () => alignVideo(true));
audioPlayer.addEventListener('ratechange', () => alignVideo(false));
audioPlayer.addEventListener('pause', () => { if (autoPlayAudio && !audioPlayer.ended) { const v = document.querySelector('.slide.active video.figure-video'); if (v) v.pause(); } });
`;
function harness(source, {loop=true, marked, autoplay=true, reduced=false, empty=false, duration=8}={}) {
 const audioEvents={}, videoEvents={}, windowEvents={}, docEvents={};let ui=[];
 const media = (marker, listeners={}) => ({dataset:marker===undefined?{}:{narrationSync:marker}, duration, loop, paused:false, currentTime:2, playbackRate:1, plays:0, pauses:0,
  play(){this.paused=false;this.plays++;return Promise.resolve()},pause(){this.paused=true;this.pauses++},
  addEventListener(e,f){(listeners[e]??=[]).push(f)},closest(s){return s==='.slide.active'?{}:null}});
 const video=empty?null:media(marked,videoEvents), clone=empty?null:media(marked);
 const audio={currentTime:22.5,playbackRate:1.25,ended:false,paused:false,addEventListener(e,f){(audioEvents[e]??=[]).push(f)}};
 const doc={querySelector(){return video},querySelectorAll(s){return empty?[]:s.startsWith('.slide.active')?[video,clone]:[video]},addEventListener(e,f){docEvents[e]=f}};
 const ctx=vm.createContext({document:doc,audioPlayer:audio,autoPlayAudio:autoplay,window:{matchMedia:()=>({matches:reduced}),addEventListener(e,f){windowEvents[e]=f}},setAudioPlaying:x=>ui.push(x),attemptAudioPlayback:()=>ui.push('attempt')});vm.runInContext(source,ctx);
 return{video,clone,audio,ctx,fire(e){const group=e==='loadedmetadata'?videoEvents:audioEvents;for(const f of group[e]||[])f()},snap(){const pick=v=>v&&Object.fromEntries(['paused','currentTime','playbackRate','plays','pauses'].map(k=>[k,v[k]]));return{video:pick(video),clone:pick(clone),ui:[...ui]}}};
}
let checks=0;
for(const marked of [undefined,'false'])for(const loop of [true,false])for(const autoplay of [true,false])for(const reduced of [true,false])for(const empty of [true,false])for(const duration of [8,Infinity]){
 const options={marked,loop,autoplay,reduced,empty,duration},a=harness(previous,options),b=harness(current,options);
 for(const event of ['loadedmetadata','play','playing','timeupdate','waiting','playing','ratechange','seeking','pause','ended','pause']){
  if(event==='ended'){a.audio.ended=b.audio.ended=true;a.audio.paused=b.audio.paused=true;}
  if(event==='pause')a.audio.paused=b.audio.paused=true;
  a.fire(event);b.fire(event);assert.deepEqual(b.snap(),a.snap(),JSON.stringify({options,event}));checks++;
 }
}
// Opted-in sequences synchronize the main figure and enlarged view, even when
// a malformed native loop property has been set after rendering.
for(const reduced of [false,true]){
 const a=harness(current,{marked:'true',reduced});a.fire('play');
 assert.equal(a.video.playbackRate,1.25);assert.equal(a.clone.playbackRate,1.25);
 assert.ok(Math.abs(a.video.currentTime-(8-(reduced?1/24:1/60)))<.00001);checks+=3;
 a.audio.currentTime=3;a.fire('seeking');assert.equal(a.video.currentTime,reduced?8-1/24:3);assert.equal(a.clone.currentTime,a.video.currentTime);checks+=2;
 a.fire('waiting');assert.ok(a.video.paused&&a.clone.paused);checks++;
 a.fire('playing');assert.equal(a.video.paused,reduced);checks++;
 a.audio.ended=true;a.audio.paused=true;a.fire('ended');assert.ok(a.video.paused&&a.clone.paused);checks++;
}
console.log(`PASS: ${checks} legacy-equivalence and synchronized-policy assertions.`);
