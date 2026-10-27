// Verify actual generated course pages, muted, with and without a SCORM API.
// Usage: node tools/test_green_navigation.mjs <built-course> <audit-directory>
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {chromium} from 'playwright';
const root=path.resolve(process.argv[2]),out=path.resolve(process.argv[3]);
await fs.mkdir(out,{recursive:true});
const course=JSON.parse(await fs.readFile(path.join(root,'course.json'),'utf8'));
const browser=await chromium.launch({headless:true,executablePath:process.env.ACADEMY_CHROMIUM_BIN||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--mute-audio']});
const results=[],errors=[],checks=[];
const check=(actual,expected,label)=>{assert.deepEqual(actual,expected,label);checks.push(label)};
const url=(id,review=false,last=false)=>pathToFileURL(path.join(root,id?`module${id}.html`:'index.html')).href+(review?`?review=1${id?'&slide='+(last?course.modules.find(m=>m.id===id).slides.at(-1).id:1):''}`:'');
async function contextFor(viewport,lms){
 const context=await browser.newContext({viewport,reducedMotion:'reduce'});
 await context.route(/^https?:/,r=>r.abort());
 await context.addInitScript(({lms})=>{
  HTMLMediaElement.prototype.play=function(){return Promise.resolve()};
  window.testCalls=[];
  if(!lms)return;
  const key='navigation-test:'+location.pathname;
  window.testValues=JSON.parse(sessionStorage.getItem(key)||'null')||{'cmi.core.lesson_status':'not attempted','cmi.core.lesson_location':'','cmi.suspend_data':''};
  window.API={LMSInitialize(){testCalls.push(['init']);return'true'},LMSGetValue(k){testCalls.push(['get',k]);return testValues[k]||''},LMSSetValue(k,v){testCalls.push(['set',k,v]);testValues[k]=v;sessionStorage.setItem(key,JSON.stringify(testValues));return'true'},LMSCommit(){testCalls.push(['commit']);return'true'},LMSFinish(){testCalls.push(['finish']);return'true'}};
 },{lms});
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 return {context,page};
}
async function ready(page){
 await page.evaluate(()=>document.querySelector('#ocpMotionIntroSkip')?.click());
 await page.locator('#ocpMotionIntro').waitFor({state:'detached'});
 await page.evaluate(()=>document.fonts.ready);
}
async function advanceToEnd(page,module){
 for(const slide of module.slides){
  check(await page.locator('.slide.active').getAttribute('data-slide'),String(slide.id),'Authored slide order preserved');
  if(slide.type==='knowledge_check'){
   await page.locator('#nextBtn').click();
   check(await page.locator('.slide.active').getAttribute('data-slide'),String(slide.id),'Unattempted quiz blocks slide advancement');
   for(const card of await page.locator('.slide.active .quiz-card').all()){
    for(const label of await card.locator('label:has(input[data-correct="true"])').all())await label.click();
    await card.locator('.quiz-submit').click();
    check(await card.locator('.quiz-feedback.correct').count(),1,'Correct answer feedback and quiz submission preserved');
   }
  }
  if(slide!==module.slides.at(-1))await page.locator('#nextBtn').click();
 }
}
try{
 for(const [device,viewport] of [['desktop',{width:1440,height:960}],['mobile',{width:390,height:844}]]){
  let baseline;
  for(const mode of [{name:'local',lms:false,review:false},{name:'review',lms:false,review:true},{name:'LMS',lms:true,review:false},{name:'LMS-review',lms:true,review:true}]){
   const signatures=[];
   for(let i=0;i<course.modules.length-1;i++){
    const module=course.modules[i],next=course.modules[i+1],{context,page}=await contextFor(viewport,mode.lms);
    await page.goto(url(module.id,mode.review,true));await ready(page);
    if(!mode.review)await advanceToEnd(page,module);
    const link=page.locator('.slide.active .next-module-link');
    check(await link.count(),1,'One authored next-module button');
    check(await link.isVisible(),true,'Next-module button remains visible');
    await link.scrollIntoViewIfNeeded();await page.mouse.move(0,0);await page.waitForTimeout(180);
    const signature=await link.evaluate(el=>({destination:new URL(el.href).pathname.split('/').at(-1),label:el.getAttribute('aria-label'),color:getComputedStyle(el).backgroundColor,width:el.getBoundingClientRect().width,height:el.getBoundingClientRect().height,paths:[...el.querySelectorAll('path')].map(p=>p.getAttribute('d'))}));
    check(signature.destination,`module${next.id}.html`,'Correct next-module destination');
    check(signature.color,'rgb(141, 198, 63)','Canonical green control');check(signature.width,46,'Canonical control width');check(signature.height,46,'Canonical control height');
    const box=await link.boundingBox();check(box.x>=0&&box.x+box.width<=viewport.width+1&&box.y>=0&&box.y+box.height<=viewport.height+1,true,'Control is reachable inside the viewport');
    check(await page.locator('.lms-navigation-note:not([hidden])').count(),0,'No navigation-blocking popup');
    if(mode.lms){if(mode.review)check(await page.evaluate(()=>testCalls),[],'Review makes no LMS calls');else check(await page.evaluate(()=>testValues['cmi.core.lesson_status']),'completed','Current SCO completes after its own quiz gates');}
    if(i===0)await page.screenshot({path:path.join(out,`${device}-${mode.name}-m${module.id}-ending.png`)});
    const savedBefore=await page.evaluate(()=>({values:window.testValues,session:[...Array(sessionStorage.length)].map((_,i)=>[sessionStorage.key(i),sessionStorage.getItem(sessionStorage.key(i))])}));
    await link.click();await page.waitForURL(url(next.id,mode.review));
    check(await page.locator('.slide.active').getAttribute('data-slide'),'1','A real click advances to slide 1 of the next module');
    if(mode.review){check(new URL(page.url()).searchParams.get('review'),'1','Review mode survives the next-module link');if(mode.lms)check(await page.evaluate(()=>testCalls),[],'Review stays isolated after navigation');}
    if(!mode.review){
     await page.goto(url(module.id));await ready(page);
     const returnedSlide=await page.locator('.slide.active').getAttribute('data-slide');
     if(returnedSlide!==String(module.slides.at(-1).id))await fs.writeFile(path.join(out,'roundtrip-failure.json'),JSON.stringify({module:module.id,mode:mode.name,device,savedBefore,returned:await page.evaluate(()=>({url:location.href,values:window.testValues,calls:window.testCalls,session:[...Array(sessionStorage.length)].map((_,i)=>[sessionStorage.key(i),sessionStorage.getItem(sessionStorage.key(i))])}))},null,2));
     check(returnedSlide,String(module.slides.at(-1).id),`${mode.name} M${module.id}: completed module and bookmark survive a next-module round trip`);
     if(mode.lms)check(await page.evaluate(()=>testValues['cmi.core.lesson_status']),'completed','Reopening a completed SCO does not downgrade it');
    }
    signatures.push(signature);results.push({device,mode:mode.name,module:module.id,next:next.id,signature,click:'pass'});
    await context.close();
   }
   if(!baseline)baseline=signatures;else check(signatures,baseline,'LMS/review controls match standalone destinations, labels, colors and chevrons');
   const {context,page}=await contextFor(viewport,mode.lms);
   await page.goto(url(0,mode.review));await ready(page);
   check(await page.locator('a.module-card').count(),0,'Home tiles retain their informational policy');
   const start=page.locator('.index-start-link');check(await start.isVisible(),true,'Home start action stays visible');
   if(mode.lms&&(mode.review||course.scorm?.include_home_sco===false))check(await page.evaluate(()=>testCalls),[],'Untracked Home/review makes no LMS calls');
   await start.scrollIntoViewIfNeeded();await start.click();await page.waitForURL(url(course.modules[0].id,mode.review));
   check(await page.locator('.slide.active').getAttribute('data-slide'),'1','Home start continues to open Module 1');
   await context.close();
   console.log(`PASS: ${device} ${mode.name}: ${course.modules.length-1} real next-module clicks and Home start`);
  }
 }
 check(errors,[],'No browser JavaScript errors');
 const report={course:course.course_title,language:course.language,assertions:checks.length,next_module_clicks:results.length,results,errors,transport:'file://',lms_scope:'SCORM 1.2 API simulation on actual generated pages; no live LMS upload or tracking acceptance claimed'};
 await fs.writeFile(path.join(out,'navigation-results.json'),JSON.stringify(report,null,2)+'\n');
 console.log(`PASS: ${checks.length} assertions; ${results.length} next-module clicks`);
}finally{await browser.close()}
