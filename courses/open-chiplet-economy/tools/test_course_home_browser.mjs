// Actual-page tracked Home, review isolation and first-module navigation checks.
import assert from 'node:assert/strict';import fs from 'node:fs/promises';import path from 'node:path';import {pathToFileURL} from 'node:url';import {chromium} from 'playwright';
const root=path.resolve(process.argv[2]),out=path.resolve(process.argv[3]);await fs.mkdir(out,{recursive:true});const course=JSON.parse(await fs.readFile(path.join(root,'course.json'),'utf8'));assert.equal(course.scorm.include_home_sco,true);
const browser=await chromium.launch({headless:true,executablePath:process.env.ACADEMY_CHROMIUM_BIN||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--mute-audio']});const checks=[],errors=[];const check=(a,b,n)=>{assert.deepEqual(a,b,n);checks.push(n)};
const file=name=>pathToFileURL(path.join(root,name)).href;
async function make(viewport,lms,preset=null){
 const context=await browser.newContext({viewport,reducedMotion:'reduce'});await context.route(/^https?:/,r=>r.abort());await context.addInitScript(({lms,preset})=>{
  HTMLMediaElement.prototype.play=function(){return Promise.resolve()};window.testCalls=[];if(!lms)return;
  window.testValues=preset||{'cmi.core.lesson_status':'not attempted','cmi.core.lesson_location':'','cmi.suspend_data':''};
  window.API={LMSInitialize(){testCalls.push(['init']);return'true'},LMSGetValue(k){testCalls.push(['get',k]);return testValues[k]||''},LMSSetValue(k,v){testCalls.push(['set',k,v]);testValues[k]=v;return'true'},LMSCommit(){testCalls.push(['commit']);return'true'},LMSFinish(){testCalls.push(['finish']);return'true'}};
 },{lms,preset});const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));return {context,page};
}
async function ready(page){await page.evaluate(()=>document.querySelector('#ocpMotionIntroSkip')?.click());await page.locator('#ocpMotionIntro').waitFor({state:'detached'});await page.evaluate(()=>document.fonts.ready);}
let starts=0,homeCompletions=0,homeIsolation=0;
try{
 for(const [device,viewport] of [['desktop',{width:1440,height:960}],['mobile',{width:390,height:844}]]){
  for(const lms of [false,true])for(const review of [false,true]){
   const {context,page}=await make(viewport,lms);await page.goto(file('index.html')+(review?'?review=1':''));await ready(page);
   check(await page.locator('article.module-card').count(),course.modules.length,'Home lists every teaching module');check(await page.locator('a.module-card,.module-card[tabindex],.module-card.completed').count(),0,'Informational tiles retain their policy');
   if(lms&&!review){
    check(await page.evaluate(()=>testCalls.filter(c=>c[0]==='init').length),1,'Home initializes its SCO once');
    check(await page.evaluate(()=>testValues['cmi.core.lesson_status']),'completed','Home completes on launch');
    check(await page.evaluate(()=>testCalls.filter(c=>c[0]==='set'&&c[1]==='cmi.core.lesson_status').map(c=>c[2])),['completed'],'Home only completes its own activity');
    check(await page.evaluate(()=>testCalls.some(c=>c[0]==='get'&&['cmi.suspend_data','cmi.core.lesson_location'].includes(c[1]))),false,'Home does not read module progress');homeCompletions++;
   }else check(await page.evaluate(()=>testCalls),[],'Local/review does not access an LMS');
   check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,'Home has no horizontal overflow');
   const start=page.locator('.index-start-link');check(await start.isVisible(),true,'Start button visible');await start.scrollIntoViewIfNeeded();await page.mouse.move(0,0);await page.waitForTimeout(150);check(await start.evaluate(e=>getComputedStyle(e).backgroundColor),'rgb(141, 198, 63)','Start keeps canonical green');
   if(lms&&!review)await page.screenshot({path:path.join(out,`${device}-tracked-home.png`),fullPage:true});
   await start.click();await page.waitForURL(file(`module${course.modules[0].id}.html`)+(review?'?review=1&slide=1':''));check(await page.locator('.slide.active').getAttribute('data-slide'),'1','Green Start opens teaching Module 1');starts++;
   if(review)check(await page.evaluate(()=>testCalls),[],'Review remains isolated after the click');else if(lms)check(await page.evaluate(()=>testValues['cmi.core.lesson_status']),'incomplete','A separately launched fresh module starts incomplete');
   await context.close();
  }
  const {context,page}=await make(viewport,true,{'cmi.core.lesson_status':'completed','cmi.core.lesson_location':'','cmi.suspend_data':''});await page.goto(file(`module${course.modules[0].id}.html`));await ready(page);check(await page.locator('.slide.active').getAttribute('data-slide'),'1','Completed Home context never skips teaching Module 1');homeIsolation++;await context.close();
 }
 check(errors,[],'No browser errors');const result={course:course.course_title,assertions:checks.length,real_home_start_clicks:starts,home_completion_cases:homeCompletions,home_status_isolation_cases:homeIsolation,errors,lms_scope:'Isolated SCORM API simulation; no live LMS upload'};await fs.writeFile(path.join(out,'home-results.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
}finally{await browser.close()}
