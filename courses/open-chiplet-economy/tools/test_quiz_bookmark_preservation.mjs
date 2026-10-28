// Muted regression for module-specific bookmarks, quiz restore and retry.
import assert from 'node:assert/strict';import fs from 'node:fs/promises';import path from 'node:path';import {pathToFileURL} from 'node:url';import {chromium} from 'playwright';
const root=path.resolve(process.argv[2]),out=path.resolve(process.argv[3]);await fs.mkdir(out,{recursive:true});const course=JSON.parse(await fs.readFile(path.join(root,'course.json'),'utf8'));
const browser=await chromium.launch({headless:true,executablePath:process.env.ACADEMY_CHROMIUM_BIN||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--mute-audio']});const checks=[],errors=[];const check=(a,b,label)=>{assert.deepEqual(a,b,label);checks.push(label)};
async function ready(page){await page.evaluate(()=>document.querySelector('#ocpMotionIntroSkip')?.click());await page.locator('#ocpMotionIntro').waitFor({state:'detached'});}
try{
 for(const lms of [false,true]){
  const context=await browser.newContext({viewport:{width:1440,height:960},reducedMotion:'reduce'});await context.route(/^https?:/,r=>r.abort());await context.addInitScript(({lms})=>{HTMLMediaElement.prototype.play=function(){return Promise.resolve()};if(!lms)return;const key='quiz-test:'+location.pathname;const values=JSON.parse(sessionStorage.getItem(key)||'null')||{'cmi.core.lesson_status':'incomplete','cmi.core.lesson_location':'','cmi.suspend_data':''};window.API={LMSInitialize:()=> 'true',LMSGetValue:k=>values[k]||'',LMSSetValue(k,v){values[k]=v;sessionStorage.setItem(key,JSON.stringify(values));return'true'},LMSCommit:()=> 'true',LMSFinish:()=> 'true'};},{lms});
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  for(const module of course.modules){
   const quiz=module.slides.find(s=>s.type==='knowledge_check');if(!quiz)continue;
   await page.goto(pathToFileURL(path.join(root,`module${module.id}.html`)).href);await ready(page);
   for(let n=1;n<quiz.id;n++)await page.locator('#nextBtn').click();
   let card=page.locator('.slide.active .quiz-card').first();
   await card.locator('label:has(input[data-correct="false"])').first().click();await card.locator('.quiz-submit').click();
   const selected=await card.locator('input:checked').inputValue(),feedback=await card.locator('.quiz-feedback.incorrect').innerText();
   await page.reload();await ready(page);card=page.locator('.slide.active .quiz-card').first();
   check(await page.locator('.slide.active').getAttribute('data-slide'),String(quiz.id),'Own module restores its saved quiz slide');
   check(await card.locator('input:checked').inputValue(),selected,'Selected incorrect choice survives reload');check(await card.locator('.quiz-feedback.incorrect').innerText(),feedback,'Answer-specific feedback survives reload');
   await card.locator('.quiz-retry').click();await page.reload();await ready(page);card=page.locator('.slide.active .quiz-card').first();
   check(await card.locator('input:checked').count(),0,'Retry clears saved choice');check(await card.locator('.quiz-feedback').innerText(),'','Retry clears saved feedback');
   await page.locator('#nextBtn').click();check(await page.locator('.slide.active').getAttribute('data-slide'),String(quiz.id),'Retry reinstates the unattempted quiz gate');
   for(const q of await page.locator('.slide.active .quiz-card').all()){for(const label of await q.locator('label:has(input[data-correct="true"])').all())await label.click();await q.locator('.quiz-submit').click();}
   await page.locator('#nextBtn').click();await page.reload();await ready(page);check(await page.locator('.slide.active').getAttribute('data-slide'),String(quiz.id+1),'Correct attempts permit bookmarked advancement');
  }
  await context.close();console.log(`PASS: ${lms?'LMS':'local'} quiz restore, retry and independent bookmarks in ${course.modules.length} modules`);
 }
 check(errors,[],'No browser JavaScript errors');await fs.writeFile(path.join(out,'quiz-bookmark-results.json'),JSON.stringify({assertions:checks.length,modules:course.modules.length,errors,lms_scope:'API simulation, no live LMS'},null,2)+'\n');console.log(`PASS: ${checks.length} quiz/bookmark assertions`);
}finally{await browser.close()}
