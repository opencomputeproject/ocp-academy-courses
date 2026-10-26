// Isolated Japanese runtime QA; no audible output or live LMS connection.
import fs from 'node:fs/promises';import path from 'node:path';import assert from 'node:assert/strict';import {pathToFileURL} from 'node:url';import {chromium} from 'playwright';
const root=path.resolve(import.meta.dirname,'..');const built=path.resolve(process.argv[2]);const out=path.join(root,'audit/japanese-browser');await fs.mkdir(out,{recursive:true});const c=JSON.parse(await fs.readFile(path.join(built,'course.json'),'utf8'));
const browser=await chromium.launch({headless:true,executablePath:process.env.ACADEMY_CHROMIUM_BIN,args:['--mute-audio']});const results=[],errors=[],english=new Set();
try{
 const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
 await context.route(/^https?:/,r=>r.abort());await context.addInitScript(()=>{const Native=window.Audio;window.Audio=function(...args){const audio=new Native(...args);audio.muted=true;window.testNarration=audio;return audio};window.Audio.prototype=Native.prototype;});
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 const open=async(m,s)=>{await page.goto(pathToFileURL(path.join(built,m?`module${m}.html`:'index.html')).href+`?review=1&slide=${s||1}`);await page.evaluate(()=>document.querySelector('#ocpMotionIntroSkip')?.click());await page.evaluate(()=>document.fonts.ready);await page.locator('#ocpMotionIntro').waitFor({state:'detached'});await page.addStyleTag({content:'.slide,.slide-content,.slide-content *{animation:none!important;transition:none!important}'});};
 for(const width of [1440,390]){
  await page.setViewportSize({width,height:1000});await open(0);assert.equal(await page.locator('article.module-card').count(),9);assert.equal(await page.locator('a.module-card,.module-card[tabindex]').count(),0);assert.equal(await page.locator('#lmsNavNote').innerText(),c.index_navigation_instruction);await page.screenshot({path:path.join(out,`home-${width}.png`),fullPage:true});
  for(const m of c.modules){
   await open(m.id,1);
   for(const s of m.slides){
    if(s.id!==1){await page.locator('#nextBtn').click();await page.waitForFunction(id=>document.querySelector('.slide.active')?.dataset.slide===String(id),s.id);}
    const state=await page.evaluate(()=>{
     const slide=document.querySelector('.slide.active');const r=slide?.getBoundingClientRect();const data={id:slide?.dataset.slide,overflow:document.documentElement.scrollWidth>innerWidth+1,inside:[],gaps:[]};
     for(const item of slide?.querySelectorAll('h1,h2,h3,p,li,.quiz-option,.reference-pill,.glossary-chip')||[]){const b=item.getBoundingClientRect();if(b.width&&b.height&&(b.left<-.5||b.right>innerWidth+.5))data.inside.push({text:item.innerText,left:b.left,right:b.right});}
     const fig=slide?.querySelector('.figure-panel');const cap=fig?.querySelector('.figure-caption');const media=fig?.querySelector('video,img');if(cap&&media){const a=media.getBoundingClientRect(),b=cap.getBoundingClientRect();data.gaps.push({frame:b.top-a.bottom,left:Math.abs(b.left-a.left),align:getComputedStyle(cap).textAlign});}
     data.text=slide?.innerText;return data;
    });
    if(state.id!==String(s.id)||state.overflow||state.inside.length)results.push({width,module:m.id,slide:s.id,state});
    for(const g of state.gaps)if(g.frame<15.5||g.left>1||g.align!=='left')results.push({width,module:m.id,slide:s.id,caption:g});
    for(const line of state.text.split('\n'))if(/[A-Za-z]{3,}\s+[A-Za-z]{3,}\s+[A-Za-z]{3,}/.test(line))english.add(line);
    if([[1,1],[3,4],[4,3],[5,3],[7,5],[9,6],[9,14]].some(([a,b])=>a===m.id&&b===s.id))await page.screenshot({path:path.join(out,`m${m.id}s${s.id}-${width}.png`),fullPage:true});
    for(const card of await page.locator('.slide.active .quiz-card').all()){await card.evaluate(el=>el.querySelectorAll('input[data-correct="true"]').forEach(i=>{i.checked=true;i.dispatchEvent(new Event('change',{bubbles:true}));}));await card.locator('.quiz-submit').click();assert.equal(await card.locator('.quiz-feedback.correct').count(),1);}

   }
  }
 }
 await fs.writeFile(path.join(out,'layout-report.json'),JSON.stringify({results,errors,latin_phrases:[...english]},null,2));
 // Native CC follows the narration clock across video loop boundaries, offline.
 await page.setViewportSize({width:1440,height:1000});await open(2,3);await page.waitForFunction(()=>window.testNarration?.readyState>=1&&document.querySelector('.slide.active video')?.readyState>=1);
 assert.equal(await page.evaluate(()=>document.querySelector('.slide.active video').textTracks[0].mode),'disabled');
 await page.locator('.slide.active [data-video-captions]').click();await page.locator('.slide.active [data-caption-index="0"]').click();
 for(const [a,v] of [[15,1],[20,7.8],[20,.1],[30,2]]){
  await page.evaluate(({a,v})=>{testNarration.pause();testNarration.currentTime=a;const video=document.querySelector('.slide.active video');video.pause();video.currentTime=v;},{a,v});await page.waitForTimeout(150);
  const check=await page.evaluate(()=>{const data=JSON.parse(document.querySelector('.slide.active [data-figure-caption-tracks]').textContent);const expected=data[0].cues.find(q=>q.start<=testNarration.currentTime&&testNarration.currentTime<q.end)?.text||'';const track=document.querySelector('.slide.active video').textTracks[0];return {expected,actual:track.cues[0].text,active:track.activeCues?.[0]?.text||'',mode:track.mode};});assert.equal(check.actual,check.expected);assert.equal(check.active,check.expected);assert.equal(check.mode,'showing');
 }
 await page.locator('.slide.active [data-video-zoom]').click();await page.waitForTimeout(100);const clone=page.locator('.lightbox-overlay video');assert.equal(await clone.count(),1);await page.keyboard.press('Escape');
 await page.locator('#transcriptBtn').click();assert.match(await page.locator('#transcriptText').innerText(),/[\u3000-\u9fff]/);await page.keyboard.press('Escape');
 await page.locator('#narrationModeBtn').click();await page.locator('#narrationModeBtn').click();assert.match(await page.locator('#narrationModeBtn').getAttribute('title'),/音声/);
 const report={slides_checked:114,viewports:[1440,390],native_narration_caption_seek_checks:4,flags:results,browser_errors:errors,latin_phrases:[...english]};await fs.writeFile(path.join(out,'report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));assert.equal(errors.length,0);assert.equal(results.length,0);
}finally{await browser.close()}
