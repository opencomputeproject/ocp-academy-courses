import assert from 'node:assert/strict';import fs from 'node:fs/promises';import path from 'node:path';import {pathToFileURL} from 'node:url';
import {chromium} from 'playwright';
const root=path.resolve(process.argv[2]),out=path.resolve(process.argv[3]);await fs.mkdir(out,{recursive:true});
const course=JSON.parse(await fs.readFile(path.join(root,'course.json'),'utf8'));
const browser=await chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH,args:['--mute-audio']});
const results=[],errors=[],checks=[];const check=(a,b,label)=>{assert.deepEqual(a,b,label);checks.push(label)};
const file=name=>pathToFileURL(path.join(root,name)).href;
async function ready(page){
 await page.waitForFunction(()=>!document.getElementById('ocpMotionIntro'));await page.evaluate(()=>document.fonts.ready);await page.waitForTimeout(450);
}
async function advanceToEnd(page,m){
 for(const s of m.slides){
  check(await page.locator('.slide.active').getAttribute('data-slide'),String(s.id),'Authored slide order retained');
  if(s.type==='knowledge_check'){
   await page.locator('#nextBtn').click();check(await page.locator('.slide.active').getAttribute('data-slide'),String(s.id),'Quiz gate blocks before attempts');
   for(const card of await page.locator('.slide.active .quiz-card').all()){
    for(const a of await card.locator('input[data-correct="true"]').all())await a.check();await card.locator('.quiz-submit').click();
   }
  }
  if(s!==m.slides.at(-1))await page.locator('#nextBtn').click();
 }
}
try{
 for(const [device,viewport] of [['desktop',{width:1440,height:960}],['mobile',{width:390,height:844}]]){
  let baseline;
  for(const mode of [{name:'local',lms:false,review:false},{name:'review',lms:false,review:true},{name:'LMS',lms:true,review:false},{name:'LMS-review',lms:true,review:true}]){
   const signatures=[];
   for(let i=0;i<course.modules.length-1;i++){
    const m=course.modules[i],next=course.modules[i+1],context=await browser.newContext({viewport,reducedMotion:'reduce'});
    await context.route(/^https?:/,r=>r.abort());
    await context.addInitScript(({lms})=>{
     HTMLMediaElement.prototype.play=function(){return Promise.resolve()};window.testCalls=[];
     if(!lms)return;
     window.testValues={'cmi.core.lesson_status':'not attempted','cmi.core.lesson_location':'','cmi.suspend_data':''};
     window.API={LMSInitialize(){testCalls.push(['init']);return'true'},LMSGetValue(k){testCalls.push(['get',k]);return testValues[k]||''},LMSSetValue(k,v){testCalls.push(['set',k,v]);testValues[k]=v;return'true'},LMSCommit(){testCalls.push(['commit']);return'true'},LMSFinish(){testCalls.push(['finish']);return'true'}};
    },{lms:mode.lms});
    const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
    await page.goto(file(`module${m.id}.html`)+(mode.review?`?review=1&slide=${m.slides.at(-1).id}`:''));await ready(page);
    if(!mode.review)await advanceToEnd(page,m);
    const link=page.locator('.slide.active .next-module-link');check(await link.count(),1,'One authored next-module link remains');check(await link.isVisible(),true,'Button remains visible');await link.scrollIntoViewIfNeeded();await page.waitForTimeout(250);
    const sig=await link.evaluate(el=>({href:new URL(el.href).pathname.split('/').at(-1),label:el.getAttribute('aria-label'),color:getComputedStyle(el).backgroundColor,width:el.getBoundingClientRect().width,height:el.getBoundingClientRect().height,paths:[...el.querySelectorAll('path')].map(x=>x.getAttribute('d'))}));
    check(sig.href,`module${next.id}.html`,'Correct next-module destination');check(sig.color,'rgb(141, 198, 63)','Green treatment retained');check(sig.width,46,'Canonical circular control width');check(sig.height,46,'Canonical circular control height');
    const box=await link.boundingBox();check(box.x>=0&&box.x+box.width<=viewport.width+1&&box.y>=0&&box.y+box.height<=viewport.height+1,true,'Button lies inside viewport');
    if(mode.lms){if(mode.review)check(await page.evaluate(()=>testCalls),[],'Review never initializes or writes LMS');else check(await page.evaluate(()=>testValues['cmi.core.lesson_status']),'completed','Launched module completes after its own quiz gate');}
    if(i===0||i===4)await page.screenshot({path:path.join(out,`${device}-${mode.name}-m${m.id}-ending.png`)});
    await link.click();await page.waitForURL(file(`module${next.id}.html`)+(mode.review?'?review=1&slide=1':''));
    check(await page.locator('.slide.active').getAttribute('data-slide'),'1','Real click opens the next module');
    if(mode.review&&mode.lms)check(await page.evaluate(()=>testCalls),[],'Review remains isolated after navigation');
    signatures.push(sig);results.push({device,mode:mode.name,module:m.id,next:next.id,signature:sig,click:'pass'});await context.close();
   }
   if(!baseline)baseline=signatures;else check(signatures,baseline,'Button geometry, label, chevrons and destination match local playback');
   const context=await browser.newContext({viewport,reducedMotion:'reduce'});await context.route(/^https?:/,r=>r.abort());
   await context.addInitScript(()=>{HTMLMediaElement.prototype.play=function(){return Promise.resolve()}});
   const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));await page.goto(file('index.html')+(mode.review?'?review=1':''));await ready(page);
   check(await page.locator('a.module-card').count(),0,'Course-home tiles remain informational');const start=page.locator('.index-start-link');check(await start.isVisible(),true,'Local index retains its first-module start control');await start.scrollIntoViewIfNeeded();
   if(mode.name==='local')await page.screenshot({path:path.join(out,`${device}-local-index.png`),fullPage:true});
   await start.click();await page.waitForURL(file('module1.html')+(mode.review?'?review=1&slide=1':''));check(await page.locator('.slide.active').getAttribute('data-slide'),'1','Local index starts module one');await context.close();
   console.log(`PASS: ${device} ${mode.name}, all next-module clicks and file-based index start`);
  }
 }
 check(errors,[],'No JavaScript errors');await fs.writeFile(path.join(out,'navigation-results.json'),JSON.stringify({assertions:checks.length,next_module_clicks:results.length,results,errors,transport:'file://, no HTTP server',lms_scope:'SCORM 1.2 API simulation on actual generated pages; target-LMS navigation/tracking acceptance not claimed'},null,2));console.log(`PASS: ${checks.length} assertions and ${results.length} next-module clicks`);
}finally{await browser.close()}
