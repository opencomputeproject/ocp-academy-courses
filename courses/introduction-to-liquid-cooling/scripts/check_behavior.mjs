import assert from 'node:assert/strict';import fs from 'node:fs/promises';import path from 'node:path';import {pathToFileURL} from 'node:url';import {chromium} from 'playwright';
const root=path.resolve(process.argv[2]),dest=path.resolve(process.argv[3]);
await fs.mkdir(dest,{recursive:true});
const course=JSON.parse(await fs.readFile(path.join(root,'course.json'),'utf8'));
const firstQuiz=course.modules[0].slides.find(s=>s.type==='knowledge_check').id;
const firstEnding=course.modules[0].slides.at(-1).id;
const url=n=>pathToFileURL(path.join(root,n)).href;
const browser=await chromium.launch({headless:true,args:['--mute-audio'],executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH});
let count=0;const checks=[],errors=[];const check=(a,b,msg)=>{assert.deepEqual(a,b,msg);checks.push(msg);count++;};
const context=await browser.newContext({reducedMotion:'reduce'});
await context.route(/^https?:/,r=>r.abort());
await context.addInitScript(()=>{
 HTMLMediaElement.prototype.play=function(){return Promise.resolve()};
 window.calls=[];const key='isolated-sco:'+location.pathname;
 const values=JSON.parse(sessionStorage.getItem(key)||'null')||{'cmi.core.lesson_status':'not attempted'};
 window.API={LMSInitialize(){calls.push(['init']);return 'true'},LMSGetValue(k){calls.push(['get',k]);return values[k]||''},LMSSetValue(k,v){calls.push(['set',k,v]);values[k]=v;sessionStorage.setItem(key,JSON.stringify(values));return'true'},LMSCommit(){calls.push(['commit']);return'true'},LMSFinish(){calls.push(['finish']);return'true'}};
});
const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
try{
 await page.goto(url('index.html'));await page.waitForFunction(()=>!document.getElementById('ocpMotionIntro'));
 check(await page.evaluate(()=>calls.filter(c=>c[0]==='init').length),1,'Course Home initializes its own LMS session');
 check(await page.evaluate(()=>calls.some(c=>c[0]==='set'&&c[1]==='cmi.core.lesson_status'&&c[2]==='completed')),true,'Course Home completes on launch');
 check(await page.locator('.index-start:visible').count(),1,'Tracked Course Home retains its first-module start button in LMS playback');
 await page.goto(url('module1.html'));await page.waitForFunction(()=>!document.getElementById('ocpMotionIntro'));
 for(let s=1;s<firstQuiz;s++)await page.locator('#nextBtn').click();
 check(await page.locator('.slide.active').getAttribute('data-slide'),String(firstQuiz),'Learner reaches the module quiz');
 await page.locator('#nextBtn').click();
 check(await page.locator('.slide.active').getAttribute('data-slide'),String(firstQuiz),'Both quiz questions must be attempted');
 const cards=page.locator('.slide.active .quiz-card');
 await cards.nth(0).locator('input:not([data-correct="true"])').first().check();await cards.nth(0).locator('.quiz-submit').click();
 await page.locator('#nextBtn').click();
 check(await page.locator('.slide.active').getAttribute('data-slide'),String(firstQuiz),'One attempted question does not release the quiz gate');
 await cards.nth(1).locator('input:not([data-correct="true"])').first().check();await cards.nth(1).locator('.quiz-submit').click();
 check(await cards.locator('.quiz-feedback.incorrect').count(),2,'Both incorrect attempts receive feedback');
 await page.locator('#nextBtn').click();
 check(await page.locator('.slide.active').getAttribute('data-slide'),String(firstEnding),'Final slide opens after both attempts');
 check(await page.evaluate(()=>calls.some(c=>c[0]==='set'&&c[1]==='cmi.core.lesson_status'&&c[2]==='completed')),true,'Only the launched module is completed');
 check(await page.locator('.slide.active .next-module-link:visible').count(),1,'LMS ending retains the authored next-module button');
 check(await page.locator('.slide.active .syllabus-navigation:visible').count(),0,'LMS ending does not substitute a syllabus message for the button');
 await page.locator('.slide.active .next-module-link').click();await page.waitForURL(url('module2.html'));check(await page.locator('.slide.active').getAttribute('data-slide'),'1','The LMS-mode next button opens module two');
 check(await page.evaluate(()=>calls.some(c=>c[0]==='set'&&c[1]==='cmi.core.lesson_status'&&c[2]==='completed')),false,'Module-one completion does not complete module two');
 await page.goto(url('module4.html')+'?review=1&slide='+course.modules.at(-1).slides.at(-1).id);
 check(await page.locator('.slide.active').innerText().then(t=>t.toLowerCase().includes('continue your learning')),true,'Final module offers follow-on learning without claiming all four modules are complete');
 check(await page.evaluate(()=>calls),[],'Editorial review remains isolated from LMS state');
 await context.close();
 const mobile=await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'});await mobile.route(/^https?:/,r=>r.abort());
 const p=await mobile.newPage();p.on('pageerror',e=>errors.push(e.message));
 const bottom=[];
 for(const m of course.modules){
  await p.goto(url(`module${m.id}.html`)+'?review=1&slide=1');await p.waitForFunction(()=>!document.getElementById('ocpMotionIntro'));
  for(const s of m.slides){
   await p.waitForTimeout(450);
   check(await p.locator('.slide.active').getAttribute('data-slide'),String(s.id),`M${m.id}S${s.id}: mobile check is on the intended slide`);
   const r=await p.evaluate(()=>{
    const slide=document.querySelector('.slide.active');slide.scrollTop=slide.scrollHeight;
    const controls=document.querySelector('.controls').getBoundingClientRect();
    const last=[...slide.querySelectorAll('h1,h2,h3,p,li,td,a,button,input,img,video')].map(e=>({e,r:e.getBoundingClientRect()})).filter(x=>x.r.width>0&&x.r.height>0).sort((a,b)=>b.r.bottom-a.r.bottom)[0];
    return {maxContentBottom:last.r.bottom,controlsTop:controls.top,gap:controls.top-last.r.bottom,scrollable:slide.scrollHeight>slide.clientHeight+1};
   });bottom.push({module:m.id,slide:s.id,...r});
   check(r.gap>=12,true,`M${m.id}S${s.id}: all mobile content can scroll clear of the bottom controls`);
   if([2,7,11,12].includes(s.id))await p.screenshot({path:path.join(dest,`mobile-bottom-m${m.id}-s${s.id}.png`)});
   if(s.type==='knowledge_check')await p.evaluate(()=>document.querySelectorAll('.slide.active .quiz-card').forEach(c=>{c.querySelector('input').checked=true;c.querySelector('.quiz-submit').click()}));
   if(s.id<m.slides.length)await p.locator('#nextBtn').click();
  }
 }
 await p.goto(url('module2.html')+'?review=1&slide=7');await p.waitForFunction(()=>!document.getElementById('ocpMotionIntro'));await p.locator('#themeToggle').click();await p.waitForTimeout(500);await p.screenshot({path:path.join(dest,'mobile-dark-m2-s7.png')});
 await mobile.close();
 check(errors,[],'No JavaScript errors in home, quiz, LMS navigation or mobile checks');
 await fs.writeFile(path.join(dest,'behavior-report.json'),JSON.stringify({count,checks,bottom,errors},null,2));console.log(`PASS: ${count} course-specific behavior and mobile scrolling assertions.`);
}finally{await browser.close()}
