// Real media regression. Usage: node test_video_modes_browser.mjs <legacy|synced> <built-course>
// Uses the first matching figure; media is muted. No network, TTS or live LMS.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {chromium} from 'playwright';
const [mode,folder]=process.argv.slice(2);
assert.ok(['legacy','synced'].includes(mode) && folder,'Provide mode and a built course');
const root=path.resolve(folder), course=JSON.parse(fs.readFileSync(path.join(root,'course.json')));
const synced=mode==='synced'; let target;
for(const module of course.modules) for(const slide of module.slides) {
 if(!target&&slide.figure?.path.endsWith('.mp4')&&(slide.figure.sync_to_narration===true)===synced) target={module,slide};
}
assert.ok(target,'Matching video');
const {module,slide}=target;
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH||undefined,args:['--mute-audio']});
let checks=0;const check=(value,message)=>{assert.ok(value,message);checks++};
try {
 const page=await browser.newPage({viewport:{width:1440,height:960}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.route(/^https?:/,route=>route.abort());
 await page.addInitScript(()=>{const Native=window.Audio;window.Audio=function(...args){const audio=new Native(...args);audio.muted=true;window.testNarration=audio;return audio};window.Audio.prototype=Native.prototype;});
 const url=pathToFileURL(path.join(root,`module${module.id}.html`)).href+`?review=1&slide=${slide.id}`;
 await page.goto(url);await page.evaluate(()=>document.querySelector('#ocpMotionIntroSkip')?.click());
 await page.waitForFunction(()=>window.testNarration?.readyState>=1&&document.querySelector('.slide.active video')?.readyState>=1);
 const state=()=>page.evaluate(()=>{const a=testNarration,v=document.querySelector('.slide.active video');const pick=v=>({time:v.currentTime,rate:v.playbackRate,paused:v.paused,duration:v.duration});return {audio:pick(a),video:pick(v),marked:v.dataset.narrationSync,loop:v.loop,clones:[...document.querySelectorAll('.lightbox-overlay video')].map(pick)}});
 const close=(a,b,t=.3)=>Math.abs(a-b)<t;
 let s=await state();check(s.audio.paused,'Review narration is paused');check(synced?s.video.paused:!s.video.paused,'Correct video entry behavior');check(s.loop===!synced,'Correct loop policy');
 await page.locator('#audioPlayBtn').click();await page.waitForTimeout(350);s=await state();check(!s.audio.paused&&!s.video.paused,'Narration starts video');
 await page.evaluate(()=>{testNarration.playbackRate=1.5;testNarration.currentTime=31});await page.waitForTimeout(300);s=await state();check(s.video.rate===1.5,'Video follows narration speed');check(close(s.video.time,synced?s.audio.time:s.audio.time%s.video.duration),'Seek uses finite or modulo time');
 await page.locator('.slide.active [data-video-zoom]').click({force:true});await page.waitForTimeout(250);s=await state();check(s.clones.length===1,'Enlarged video exists');check(s.clones[0].rate===(synced?1.5:1),'Enlarged speed preserves the mode policy');
 await page.evaluate(synced=>{const v=document.querySelector('.slide.active video'),clone=document.querySelector('.lightbox-overlay video');if(!synced)clone.pause();testNarration.currentTime=synced?45:(clone.currentTime+v.duration/2)%v.duration},synced);await page.waitForTimeout(250);s=await state();check(synced?close(s.audio.time,s.clones[0].time):!close(s.audio.time%s.video.duration,s.clones[0].time),'Enlarged seek follows only the opted-in video');
 if(synced){await page.locator('.lightbox-overlay [data-video-toggle]').click({force:true});await page.waitForTimeout(100);s=await state();check(s.audio.paused&&s.video.paused&&s.clones[0].paused,'Enlarged pause controls both');}
 await page.keyboard.press('Escape');
 // With narration enabled, the historical pause listener controls the legacy video.
 if(!synced){await page.locator('#narrationModeBtn').click();await page.waitForTimeout(150);}
 await page.evaluate(()=>testNarration.pause());await page.waitForTimeout(100);s=await state();check(s.audio.paused&&s.video.paused,'Pause preserves narration-enabled behavior');
 await page.evaluate(()=>{testNarration.currentTime=20;testNarration.dispatchEvent(new Event('waiting'))});await page.waitForTimeout(120);s=await state();check(s.video.paused,'Paused seek remains paused');
 await page.evaluate(()=>{testNarration.currentTime=testNarration.duration-.35;return testNarration.play()});await page.waitForTimeout(700);s=await state();check(s.audio.paused,'Audio completes');check(synced?s.video.paused:!s.video.paused,'Old loop continues at audio end; synced video holds');
 if(synced){
  check(s.video.time>s.video.duration-.2,'Synced final state');await page.locator('.slide.active [data-video-toggle]').click({force:true});await page.waitForTimeout(250);s=await state();check(s.audio.time<2&&!s.audio.paused&&!s.video.paused,'Replay resets both');
  await page.emulateMedia({reducedMotion:'reduce'});await page.goto(url);await page.evaluate(()=>document.querySelector('#ocpMotionIntroSkip')?.click());await page.waitForFunction(()=>document.querySelector('.slide.active video')?.readyState>=1);await page.waitForTimeout(150);s=await state();check(s.video.paused&&s.video.time>s.video.duration-.2,'Reduced motion holds conclusion');await page.locator('.slide.active [data-video-toggle]').click({force:true});await page.waitForTimeout(250);s=await state();check(!s.audio.paused&&!s.video.paused&&close(s.audio.time,s.video.time),'Explicit reduced-motion playback');
 }
 // Audio-only slide still plays, pauses and seeks normally.
 await page.goto(pathToFileURL(path.join(root,`module${module.id}.html`)).href+'?review=1&slide=1');await page.evaluate(()=>document.querySelector('#ocpMotionIntroSkip')?.click());await page.waitForFunction(()=>testNarration.readyState>=1);await page.locator('#audioPlayBtn').click();await page.waitForTimeout(180);check(await page.evaluate(()=>!testNarration.paused&&testNarration.currentTime>0),'Audio-only playback');await page.locator('#audioPlayBtn').click();check(await page.evaluate(()=>testNarration.paused),'Audio-only pause');await page.evaluate(()=>testNarration.currentTime=2);await page.waitForTimeout(100);check(await page.evaluate(()=>Math.abs(testNarration.currentTime-2)<.1),'Audio-only seek');
 assert.deepEqual(errors,[]);console.log(`PASS: ${checks} real-media ${mode} assertions: ${course.course_title}`);
} finally {await browser.close()}
