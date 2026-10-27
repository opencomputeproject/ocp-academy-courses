import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import assert from 'node:assert/strict';
const root=path.resolve(process.argv[2]||new URL('../../../',import.meta.url).pathname);
const out=root+'/authoring/qa/green-navigation-refresh';await fs.mkdir(out+'/screenshots',{recursive:true});
const course=JSON.parse(await fs.readFile(root+'/course.json'));
const completed=JSON.parse(await fs.readFile(root+'/authoring/qa/scorm12-delivery/scorm-results.json')).modules;
const report={checks:[],cases:[],errors:[],audio:'Playback suppressed and Chromium muted',lms:'Persistent parent SCORM 1.2 API in an isolated local fixture; no live LMS upload',tracking_scope:'Cross-page button parity is verified separately from independent LMS-launched SCO tracking.'};
const browser=await chromium.launch({headless:true,args:['--mute-audio']});
const types={'.html':'text/html','.js':'text/javascript','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.ttf':'font/ttf','.woff':'font/woff','.wav':'audio/wav','.mp4':'video/mp4'};
try{
 for(const viewport of [{name:'desktop',width:1440,height:900},{name:'phone',width:390,height:844}])
 for(const theme of ['light','dark'])
 for(const m of course.modules.slice(0,-1))
 for(const mode of ['local','review','lms','lms-review']){
  const lms=mode.startsWith('lms'),review=mode.includes('review');
  const seed=completed.find(r=>r.module===m.id).state;
  const context=await browser.newContext({viewport:{width:viewport.width,height:viewport.height},reducedMotion:'reduce'});
  await context.addInitScript(({seed,id,slug,theme,lms})=>{
   HTMLMediaElement.prototype.play=function(){this.muted=true;return Promise.resolve()};
   if(lms&&location.pathname==='/_lms_shell.html'){
    window.mockState={...seed};window.mockCalls=[];
    window.API={
     LMSInitialize(){mockCalls.push(['init']);return'true'},
     LMSGetValue(k){mockCalls.push(['get',k]);return mockState[k]||''},
     LMSSetValue(k,v){mockCalls.push(['set',k,String(v)]);mockState[k]=String(v);return'true'},
     LMSCommit(){mockCalls.push(['commit']);return'true'},
     LMSFinish(){mockCalls.push(['finish']);return'true'},
     LMSGetLastError(){return'0'},LMSGetErrorString(){return''},LMSGetDiagnostic(){return''}
    };
   }
   if(!lms&&location.pathname.endsWith(`/module${id}.html`)){
    localStorage.setItem(`ocp:${slug}:module${id}`,seed['cmi.core.lesson_location']);
    localStorage.setItem(`ocp:${slug}:module${id}:quiz-state`,seed['cmi.suspend_data']);
   }
  },{seed,id:m.id,slug:course.course_slug,theme,lms});
  await context.route(/^https?:/,async route=>{
   const url=new URL(route.request().url());
   if(url.origin!=='https://dc-basics.test')return route.abort();
   if(url.pathname==='/_lms_shell.html')return route.fulfill({contentType:'text/html',body:`<!doctype html><html><head><title>Isolated LMS API fixture</title><style>html,body{margin:0;height:100%;overflow:hidden}iframe{border:0;width:100%;height:100%}</style></head><body><iframe name="course" title="Course content" src="module${m.id}.html${review?'?review=1&slide='+m.slides.length:''}"></iframe></body></html>`});
   const file=path.resolve(root,'.'+decodeURIComponent(url.pathname));
   if(!file.startsWith(root+path.sep))return route.abort();
   try{return await route.fulfill({contentType:types[path.extname(file)]||'application/octet-stream',body:await fs.readFile(file)})}catch{return route.fulfill({status:404,body:'Not found'})}
  });
  const page=await context.newPage();page.on('pageerror',e=>report.errors.push(`${mode} M${m.id}: ${e.message}`));
  await page.goto(lms?'https://dc-basics.test/_lms_shell.html':pathToFileURL(root+`/module${m.id}.html`).href+(review?'?review=1&slide='+m.slides.length:''));
  let frame=lms?page.frame({name:'course'}):page;
  await frame.waitForSelector('.slide.active');
  if(await frame.locator('#ocpMotionIntroSkip').isVisible())await frame.locator('#ocpMotionIntroSkip').click({force:true});
  await frame.addStyleTag({content:'*,*::before,*::after{animation:none!important;transition:none!important}'});
  await frame.evaluate(async theme=>{document.documentElement.setAttribute('data-theme',theme);await document.fonts.ready},theme);
  assert.equal(await frame.locator('.slide.active').getAttribute('data-slide'),String(m.slides.length));
  assert.equal(await frame.locator('.lms-next-instruction').count(),0);
  const link=frame.locator('.slide.active .next-module-link');assert.equal(await link.count(),1);assert.equal(await link.isVisible(),true);await link.scrollIntoViewIfNeeded();
  const properties=await link.evaluate(e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return{href:e.getAttribute('href'),width:r.width,height:r.height,background:s.backgroundColor,color:s.color,borderRadius:s.borderRadius,display:s.display,pointerEvents:s.pointerEvents,ariaLabel:e.getAttribute('aria-label'),paths:[...e.querySelectorAll('path')].map(p=>p.getAttribute('d'))}});
  assert.equal(properties.href,`module${m.id+1}.html`);assert.equal(properties.background,'rgb(141, 198, 63)');assert.equal(properties.pointerEvents,'auto');assert.equal(Math.round(properties.width),46);assert.equal(Math.round(properties.height),46);
  const same=report.cases.find(x=>x.module===m.id&&x.viewport===viewport.name&&x.theme===theme);if(same)assert.deepEqual(properties,same.properties,'Button appearance and destination match without/with LMS API');
  if(theme==='light'&&((viewport.name==='desktop'&&m.id===1)||(viewport.name==='phone'&&m.id===2&&lms))){await page.screenshot({path:out+`/screenshots/${viewport.name}-${mode}-m${m.id}-ending.png`});}
  if(lms&&review)assert.deepEqual(await page.evaluate(()=>mockCalls),[]);
  await link.click();
  if(lms){await page.waitForFunction(n=>document.querySelector('iframe').contentWindow.location.pathname===`/module${n}.html`,m.id+1);frame=page.frame({name:'course'})}
  else await page.waitForURL(u=>u.pathname.endsWith(`/module${m.id+1}.html`));
  await frame.waitForSelector('.slide.active');
  assert.equal(await frame.locator('.slide.active').getAttribute('data-slide'),'1');
  const target=new URL(frame.url());assert.equal(target.searchParams.get('review'),review?'1':null);if(review)assert.equal(target.searchParams.get('slide'),'1');
  const api=lms?await page.evaluate(()=>({calls:mockCalls,status:mockState['cmi.core.lesson_status'],suspend:mockState['cmi.suspend_data']})):null;
  if(lms&&!review){assert.equal(api.calls.filter(x=>x[0]==='init').length,2);assert.equal(api.calls.filter(x=>x[0]==='finish').length,1);assert.equal(api.status,'completed');assert.deepEqual(JSON.parse(api.suspend).modules,[m.id]);assert.equal(api.calls.some(x=>x[1]?.startsWith('adl.')),false)}
  if(lms&&review)assert.deepEqual(api.calls,[]);
  report.cases.push({module:m.id,viewport:viewport.name,theme,mode,properties,destination:`module${m.id+1}.html`,destination_slide:1,review_preserved:review?true:null,passed:true});
  await context.close();
 }
 report.checks.push('48 desktop/phone, light/dark button states have identical green appearance and correct targets across local, review, LMS and LMS-review modes.','All 48 real button clicks reach the next module at slide 1.','Review mode propagates through next-module links and makes no LMS API calls.','Persistent parent API does not hide or cancel next-module clicks; outgoing session finishes and target page initializes.','Incoming pages do not inherit the outgoing module completion as their own; no SCORM 2004 navigation requests are introduced.','SCORM structure and independently launched SCO tracking are audited separately.');
}catch(e){report.errors.push(e.stack);console.error(e.stack)}
report.passed=report.cases.length===48&&report.errors.length===0;
await fs.writeFile(out+'/navigation-parity-results.json',JSON.stringify(report,null,2)+'\n');await browser.close();console.log('Navigation parity:',report.cases.length,'cases;',report.errors.length,'errors');if(!report.passed)process.exitCode=1;
