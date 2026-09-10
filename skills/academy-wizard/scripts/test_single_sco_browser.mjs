// Run with a fully built Open DC package. No real LMS or audio playback.
import assert from 'node:assert/strict';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
const require = createRequire(import.meta.url);
const {chromium} = require('playwright');
const root = path.resolve(process.argv[2]);
const course = JSON.parse(fs.readFileSync(path.join(root, 'course.json'), 'utf8'));
const checks = [];
const check = (name, actual, expected) => { assert.deepEqual(actual, expected, name); checks.push(name); };
const harness = `<!doctype html><style>html,body,iframe{margin:0;width:100%;height:100%;border:0}</style>
<script>
window.data={'cmi.core.lesson_status':'not attempted','cmi.suspend_data':''};
window.calls=[];window.active=false;window.rejectSave=false;window.rejectCommit=false;
window.API={
 LMSInitialize:()=>{calls.push(['init']);if(active)throw Error('Duplicate initialize');active=true;return 'true';},
 LMSFinish:()=>{calls.push(['finish']);if(!active)throw Error('Duplicate finish');active=false;return 'true';},
 LMSCommit:()=>{if(!active)throw Error('Commit outside session');return rejectCommit?'false':'true';},
 LMSGetValue:k=>{if(!active)throw Error('Read outside session');return data[k]||'';},
 LMSSetValue:(k,v)=>{if(!active)throw Error('Write outside session');calls.push(['set',k,v]);
  if(rejectSave || k==='cmi.suspend_data' && v.length>4096)return 'false';data[k]=v;
  const match=/^cmi\\.interactions\\.(\\d+)\\.id$/.exec(k);
  if(match)data['cmi.interactions._count']=String(Math.max(Number(data['cmi.interactions._count']||0),Number(match[1])+1));
  return 'true';}
};
</script><iframe id="lms" src="/package/launch.html" allow="autoplay; fullscreen" allowfullscreen></iframe>`;
const server = http.createServer((req,res)=>{
  const url = new URL(req.url, 'http://local');
  if (url.pathname === '/harness') { res.setHeader('Content-Type','text/html');res.end(harness);return; }
  const file = path.resolve(root, '.' + decodeURIComponent(url.pathname.replace(/^\/package/,'')));
  if (!file.startsWith(root + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {res.statusCode=404;res.end();return;}
  const types={'.html':'text/html','.js':'text/javascript','.svg':'image/svg+xml','.wav':'audio/wav','.mp4':'video/mp4','.png':'image/png'};
  res.setHeader('Content-Type',types[path.extname(file)]||'application/octet-stream');
  fs.createReadStream(file).pipe(res);
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const base = `http://127.0.0.1:${server.address().port}`;
const browser=await chromium.launch({channel:'chrome',headless:true,args:['--mute-audio']});
try {
  const context = await browser.newContext({viewport:{width:1440,height:900}});
  await context.addInitScript(()=>{
    HTMLMediaElement.prototype.play=function(){this.muted=true;return Promise.resolve();};
    try{localStorage.setItem('ocp-narration-enabled','false');}catch(_){}
  });
  const page=await context.newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  const data=()=>page.evaluate(()=>window.data);
  const state=async()=>JSON.parse((await data())['cmi.suspend_data']);
  const status=async()=> (await data())['cmi.core.lesson_status'];
  async function current(file) {
    await page.waitForFunction(file=>{
      const host=document.querySelector('#lms')?.contentWindow || window;
      const frame=host.document.querySelector('#courseFrame');
      return frame?.contentWindow.location.pathname.endsWith('/'+file) && frame.contentDocument.readyState==='complete';
    },file);
    const frame=page.frames().find(f=>new URL(f.url()).pathname.endsWith('/'+file));
    // Skip only the decorative intro delay; exercise real course controls.
    await frame.evaluate(()=>{document.body.classList.add('motion-intro-done');document.querySelector('.ocp-motion-intro')?.remove();});
    return frame;
  }
  const slide=frame=>frame.locator('.slide.active').getAttribute('data-slide');
  await page.goto(base+'/harness');
  let frame=await current('index.html');
  check('Home does not complete course',await status(),'incomplete');
  for(const module of course.modules) {
    await frame.locator(`[data-module="${module.id}"]`).click();
    frame=await current(`module${module.id}.html`);
    check(`Home opens module ${module.id}`,await slide(frame),'1');
    await frame.locator('a[href="index.html"]').first().click();
    frame=await current('index.html');
    check(`Return from module ${module.id} preserves incomplete`,await status(),'incomplete');
  }
  // Revisit uses its own bookmark, not the last other module's position.
  await frame.locator('[data-module="2"]').click();frame=await current('module2.html');
  await frame.locator('#nextBtn').click();await frame.locator('#nextBtn').click();
  await frame.locator('a[href="index.html"]').first().click();frame=await current('index.html');
  await frame.locator('[data-module="2"]').click();frame=await current('module2.html');
  check('Same-session module bookmark',await slide(frame),'3');
  await page.locator('#lms').evaluate(el=>new Promise(resolve=>{
    el.addEventListener('load',resolve,{once:true});el.contentWindow.location.reload();
  }));
  frame=await current('module2.html');
  check('Relaunch restores last module and slide',await slide(frame),'3');
  await frame.locator('a[href="index.html"]').first().click();frame=await current('index.html');
  await frame.locator('[data-module="1"]').click();
  for(const module of course.modules) {
    frame=await current(`module${module.id}.html`);
    await frame.locator('.slide.active h1,.slide.active h2').first().click();await page.keyboard.press('End');
    const quiz=module.slides.find(s=>s.type==='knowledge_check');
    check(`Module ${module.id} cannot skip unanswered quiz`,await slide(frame),String(quiz.id));
    check(`Module ${module.id} quiz not yet completion`,await status(),'incomplete');
    for(const card of await frame.locator('.slide.active .quiz-card').all()) {
      for(const input of await card.locator('input[data-correct="true"]').all()) await input.check();
      await card.locator('.quiz-submit').click();
    }
    await frame.locator('#nextBtn').click();
    check(`Module ${module.id} reaches end`,await slide(frame),String(module.slides.length));
    check(`Module ${module.id} saved internally`,(await state()).modules.includes(module.id),true);
    check(`Completion after module ${module.id}`,await status(),module.id===4?'completed':'incomplete');
    if(module.id<4) {
      await frame.locator(`a[href="module${module.id+1}.html"]`).click();
      const next=await current(`module${module.id+1}.html`);
      check(`Next-module ${module.id} button navigates`,await slide(next),module.id===1?'3':'1');
    }
  }
  await frame.locator('a[href="index.html"]').first().click();frame=await current('index.html');
  check('All four home cards show completion',await frame.locator('.module-card.completed').count(),4);
  check('Home completion labels are readable',await frame.locator('.status-completed').allTextContents(),Array(4).fill('Completed'));
  const completeWrites=await page.evaluate(()=>calls.filter(x=>x[1]==='cmi.core.lesson_status' && x[2]==='completed').length);
  check('Overall completion is written once',completeWrites,1);
  check('State remains under SCORM 1.2 limit',(await data())['cmi.suspend_data'].length<4096,true);
  check('All eight quiz responses are retained',Object.keys((await state()).quizzes).length,8);
  check('All eight LMS interactions are recorded',(await data())['cmi.interactions._count'],'8');
  const initCount=await page.evaluate(()=>calls.filter(x=>x[0]==='init').length);
  check('Internal navigation does not reinitialize LMS',initCount,2); // launch + explicit reload
  check('Module changes do not finish LMS',await page.evaluate(()=>calls.filter(x=>x[0]==='finish').length),1);
  await page.evaluate(()=>window.rejectCommit=true);
  await frame.locator('[data-module="1"]').click();frame=await current('module1.html');
  const host=page.frames().find(f=>f.url().endsWith('/launch.html'));
  check('Commit failure is visible',await host.locator('#saveWarning').isVisible(),true);
  await page.evaluate(()=>window.rejectCommit=false);
  await frame.locator('a[href="index.html"]').first().click();frame=await current('index.html');
  check('Recovery clears save warning',await host.locator('#saveWarning').isVisible(),false);
  await page.locator('#lms').evaluate(el=>el.src='about:blank');
  await page.waitForFunction(()=>!window.active);
  check('Exit finishes exactly once',await page.evaluate(()=>calls.filter(x=>x[0]==='finish').length),2);
  check('Exit requests suspend',(await data())['cmi.core.exit'],'suspend');
  check('No runtime errors',errors,[]);
  // A completed relaunch must not reset completion or saved quiz attempts.
  await page.locator('#lms').evaluate(el=>new Promise(resolve=>{
    el.addEventListener('load',resolve,{once:true});el.src='/package/launch.html';
  }));frame=await current('index.html');
  check('Completed relaunch retains completion',await status(),'completed');
  await frame.locator('[data-module="4"]').click();frame=await current('module4.html');
  check('Completed module resumes at final slide',await slide(frame),'9');
  check('Quiz attempts survive relaunch',await frame.locator('.quiz-card[data-attempted="true"]').count(),2);
  // Review mode must never call the real API, even when nested beneath it.
  await page.locator('#lms').evaluate(el=>el.src='/package/launch.html?review=1');
  frame=await current('index.html');
  const callsBefore=await page.evaluate(()=>calls.length);
  await frame.locator('[data-module="1"]').click();frame=await current('module1.html');
  await frame.locator('.slide.active h1,.slide.active h2').first().click();await page.keyboard.press('End');
  check('Review can inspect final slide',await slide(frame),'9');
  check('Review does not initialize or write LMS',await page.evaluate(()=>calls.length),callsBefore);
  // Test a small viewport inside the persistent host, including keyboard navigation.
  await page.setViewportSize({width:320,height:740});
  check('Phone frame fits viewport',await frame.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  await page.keyboard.press('Home');check('Home key remains functional',await slide(frame),'1');
  if(process.argv[3]) {
    fs.mkdirSync(process.argv[3],{recursive:true});
    await frame.waitForFunction(()=>Number(getComputedStyle(document.querySelector('.slide.active')).opacity)>0.99);
    await page.screenshot({path:path.join(process.argv[3],'phone.png'),animations:'disabled'});
  }
  await page.setViewportSize({width:1440,height:900});
  await frame.locator('a[href="index.html"]').first().click();frame=await current('index.html');
  if(process.argv[3]) {
    await frame.waitForFunction(()=>Number(getComputedStyle(document.querySelector('.index-shell')).opacity)>0.99);
    await page.screenshot({path:path.join(process.argv[3],'home.png'),animations:'disabled'});
  }
  // An initialization failure must not borrow browser-local progress as LMS data.
  await page.evaluate(()=>{window.API.LMSInitialize=()=>{calls.push(['init-rejected']);return 'false';};});
  await page.locator('#lms').evaluate(el=>new Promise(resolve=>{
    el.addEventListener('load',resolve,{once:true});el.src='/package/launch.html';
  }));frame=await current('index.html');
  const failedHost=page.frames().find(f=>f.url().endsWith('/launch.html'));
  check('Initialization failure is visible',await failedHost.locator('#saveWarning').isVisible(),true);
  check('Initialization failure does not falsely complete cards',await frame.locator('.module-card.completed').count(),0);
  // Standalone HTTP review uses a separate browser-local session, not LMS tracking.
  const local=await context.newPage();
  await local.goto(base+'/package/launch.html');
  await local.waitForFunction(()=>document.querySelector('#courseFrame')?.contentWindow.location.pathname.endsWith('/index.html'));
  let localFrame=local.frames().find(f=>f.url().endsWith('/index.html'));
  await localFrame.evaluate(()=>{document.body.classList.add('motion-intro-done');document.querySelector('.ocp-motion-intro')?.remove();});
  await localFrame.locator('[data-module="3"]').click();
  await local.waitForFunction(()=>document.querySelector('#courseFrame')?.contentWindow.location.pathname.endsWith('/module3.html'));
  localFrame=local.frames().find(f=>f.url().endsWith('/module3.html'));
  await localFrame.waitForLoadState();
  await localFrame.evaluate(()=>{document.body.classList.add('motion-intro-done');document.querySelector('.ocp-motion-intro')?.remove();});
  await localFrame.locator('#nextBtn').click();
  await local.reload();
  await local.waitForFunction(()=>document.querySelector('#courseFrame')?.contentWindow.location.pathname.endsWith('/module3.html'));
  localFrame=local.frames().find(f=>f.url().endsWith('/module3.html'));
  await localFrame.waitForLoadState();
  check('Standalone HTTP session restores its own bookmark',await slide(localFrame),'2');
  check('No final runtime errors',errors,[]);
  const result={checks:checks.length,passed:checks,stateCharacters:(await data())['cmi.suspend_data'].length,muted:true,actualDocebo:false};
  if(process.argv[3])fs.writeFileSync(path.join(process.argv[3],'browser_results.json'),JSON.stringify(result,null,2));
  console.log(JSON.stringify(result,null,2));
} finally {await browser.close();server.closeAllConnections();await new Promise(resolve=>server.close(resolve));}
