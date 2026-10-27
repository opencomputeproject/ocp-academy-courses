import {chromium} from 'playwright';import fs from 'node:fs/promises';import path from 'node:path';import assert from 'node:assert/strict';import {pathToFileURL} from 'node:url';
const root=path.resolve(process.argv[2]),out=path.resolve(process.argv[3]);await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true,args:['--mute-audio'],executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH});
let checks=0;const errors=[],layouts=[],playbacks=[];const check=(a,b,msg)=>{assert.deepEqual(a,b,msg);checks++};
const url=(m,s)=>pathToFileURL(path.join(root,`module${m}.html`)).href+`?review=1&slide=${s}`;
async function ready(p){await p.evaluate(()=>document.getElementById('ocpMotionIntroSkip')?.click());await p.waitForFunction(()=>!document.getElementById('ocpMotionIntro'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(200)}
async function context(viewport){const c=await browser.newContext({viewport,reducedMotion:'reduce'});await c.route(/^https?:/,r=>r.abort());await c.addInitScript(()=>{const Native=window.Audio;window.Audio=function(...args){const a=new Native(...args);a.muted=true;window.testNarration=a;return a;};window.Audio.prototype=Native.prototype});return c}
const buttonStyle=async p=>p.locator('#audioPlayBtn').evaluate(b=>{const s=getComputedStyle(b),r=b.getBoundingClientRect();return{disabled:b.disabled,opacity:s.opacity,background:s.backgroundColor,borderRadius:s.borderRadius,width:r.width,height:r.height,pointerEvents:s.pointerEvents}});
try{
 const referenceStyle=JSON.parse(await fs.readFile(new URL('../authoring/qa/recording-player-reference.json',import.meta.url),'utf8')).referenceStyle;
 for(const viewport of [{width:1440,height:960},{width:390,height:844},{width:320,height:640}])for(const theme of ['light','dark']){
  const c=await context(viewport),p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));
  for(let m=1;m<=4;m++){
   await p.goto(url(m,9));await ready(p);await p.evaluate(theme=>document.documentElement.setAttribute('data-theme',theme),theme);await p.waitForTimeout(150);
   const player=p.locator('.slide.active [data-video-player]'),v=p.locator('.slide.active video.original-video');await v.waitFor();await p.waitForFunction(()=>document.querySelector('.slide.active video.original-video').readyState>=1);
   const style=await buttonStyle(p);check(style.opacity,referenceStyle.opacity,'Disabled opacity matches DC Basics');check(style.disabled,true,'Narration play is disabled');check(style.background,referenceStyle.background,'Narration button treatment matches DC Basics');
   check(await p.locator('#audioPlayBtn').getAttribute('aria-disabled'),'true','Disabled narration is accessible');check(await p.locator('#audioSpeedBtn').isDisabled(),true,'Narration speed is disabled');check(await p.evaluate(()=>testNarration.hasAttribute('src')),false,'Narration source is cleared');
   const state=await v.evaluate(v=>({autoplay:v.autoplay,loop:v.loop,muted:v.muted,paused:v.paused}));check(state,{autoplay:false,loop:false,muted:false,paused:true},'Recording uses its own audio and manual playback');
   for(const selector of ['.academy-video__controls [data-video-action="toggle"]','[data-video-progress]','[data-video-menu-button="rate"]','[data-video-menu-button="captions"]','[data-video-action="picture-in-picture"]','[data-video-action="fullscreen"]','[data-video-action="mute"]','[data-video-volume]'])check(await player.locator(selector).isVisible(),true,'Video control remains exposed: '+selector);
   const geometry=await player.evaluate(el=>{const r=el.getBoundingClientRect(),video=el.querySelector('video').getBoundingClientRect(),bar=el.querySelector('.academy-video__controls').getBoundingClientRect();const children=[...el.querySelectorAll('.academy-video__controls button,.academy-video__controls input')].filter(e=>e.getBoundingClientRect().width>0&&getComputedStyle(e).display!=='none'&&!e.closest('[hidden]')).map(e=>({label:e.getAttribute('aria-label'),left:e.getBoundingClientRect().left,right:e.getBoundingClientRect().right}));return{left:r.left,right:r.right,barBelowVideo:bar.top>=video.bottom-.5,children}});
   check(geometry.left>=-.5&&geometry.right<=viewport.width+.5,true,'Player fits viewport');check(geometry.barBelowVideo,true,'Black control bar sits below the recording');check(geometry.children.every(x=>x.left>=-.5&&x.right<=viewport.width+.5),true,'Wrapped controls fit viewport');
   await p.screenshot({path:path.join(out,`${viewport.width}-${theme}-m${m}-top.png`)});
   const bottom=await p.evaluate(()=>{const s=document.querySelector('.slide.active');s.scrollTop=s.scrollHeight;const controlTop=document.querySelector('.controls').getBoundingClientRect().top;const last=[...s.querySelectorAll('p,h2,a,button,input,video')].map(e=>e.getBoundingClientRect()).filter(r=>r.width>0&&r.height>0).sort((a,b)=>b.bottom-a.bottom)[0];return{wide:s.scrollWidth>s.clientWidth+1,gap:controlTop-last.bottom}});
   check(bottom.wide,false,'No horizontal slide overflow');check(bottom.gap>=12,true,'Video and context can scroll clear of fixed controls');
   if(viewport.width<500)await p.screenshot({path:path.join(out,`${viewport.width}-${theme}-m${m}-bottom.png`)});
   layouts.push({viewport:viewport.width,theme,module:m,button:style,...bottom});
  }
  await c.close();console.log(`PASS layout: ${viewport.width}px ${theme}, all four recordings`);
 }
 await fs.writeFile(path.join(out,'layout-stage-results.json'),JSON.stringify({checks,referenceStyle,layouts,errors},null,2));
 for(let m=1;m<=4;m++){
  const c=await context({width:1440,height:960}),p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));
  await p.goto(url(m,8));await ready(p);await p.locator('#audioPlayBtn').click();await p.waitForFunction(()=>!testNarration.paused&&testNarration.currentTime>.1);
  await p.locator('#nextBtn').click();await p.waitForFunction(()=>document.querySelector('.slide.active')?.dataset.slide==='9');
  check(await p.evaluate(()=>testNarration.paused&&!testNarration.hasAttribute('src')),true,'Entering recording stops and clears prior narration');check(await p.locator('#audioPlayBtn').isDisabled(),true,'No overlay narration on recording');
  const player=p.locator('.slide.active [data-video-player]'),v=p.locator('.slide[data-slide="9"] video.original-video');await p.waitForFunction(()=>document.querySelector('.slide.active video.original-video')?.readyState>=2);
  await v.evaluate(v=>{v.muted=true;v.currentTime=4});await p.waitForTimeout(150);
  await player.locator('[data-video-menu-button="captions"]').click();await player.locator('[data-video-caption-index="0"]').click();await p.waitForTimeout(100);check(await player.locator('[data-video-caption-text]').innerText().then(x=>x.length>5),true,'File-based caption fallback displays the selected language');
  const toggle=player.locator('.academy-video__controls [data-video-action="toggle"]');await toggle.click();await p.waitForFunction(()=>!document.querySelector('.slide.active video.original-video').paused);await p.waitForTimeout(200);
  await p.keyboard.press('p');check(await v.evaluate(v=>v.paused),false,'P does not interfere with recording audio');await p.locator('#narrationModeBtn').click();check(await p.evaluate(()=>testNarration.hasAttribute('src')),false,'Narration preference cannot start a second audio source');
  await player.locator('[data-video-menu-button="rate"]').click();await player.locator('[data-video-rate="1.5"]').click();check(await v.evaluate(v=>v.playbackRate),1.5,'Recording speed control works');
  await toggle.click();check(await v.evaluate(v=>v.paused),true,'Recording pause works');await v.evaluate(v=>{v.currentTime=12;v.dispatchEvent(new Event('timeupdate'))});check(await v.evaluate(v=>v.paused),true,'Paused seeking stays paused');
  await toggle.click();await p.waitForTimeout(100);await p.locator('#nextBtn').click();await p.waitForFunction(()=>document.querySelector('.slide.active')?.dataset.slide==='10');
  check(await v.evaluate(v=>v.paused),true,'Leaving the recording pauses its audio');check(await p.locator('#audioPlayBtn').isEnabled(),true,'Following slide restores narration play');check(await p.evaluate(()=>testNarration.hasAttribute('src')),true,'Following slide loads its original narration');
  playbacks.push({module:m,recording_slide:9,next_slide:10,captions:true,narration_disabled:true,adjacent_narration_restored:true});await c.close();console.log(`PASS native playback: module ${m}`);
 }
 check(errors,[],'No player JavaScript errors');await fs.writeFile(path.join(out,'player-results.json'),JSON.stringify({checks,referenceStyle,layouts,playbacks,errors,scope:'Actual local-file pages and muted native media; no localhost server or live LMS'},null,2));console.log(`PASS: ${checks} original-recording player assertions`);
}finally{await browser.close()}
