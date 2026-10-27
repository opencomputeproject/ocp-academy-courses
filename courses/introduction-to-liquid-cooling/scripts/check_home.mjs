import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {chromium} from 'playwright';

const root=path.resolve(process.argv[2]);
const dest=path.resolve(process.argv[3]);
await fs.mkdir(dest,{recursive:true});
const file=name=>pathToFileURL(path.join(root,name)).href;
const browser=await chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH,args:['--mute-audio']});
const checks=[],cases=[],errors=[];
const check=(actual,expected,label)=>{assert.deepEqual(actual,expected,label);checks.push(label)};
try {
 for(const [device,viewport] of [['desktop',{width:1440,height:960}],['phone',{width:390,height:844}]]) {
  for(const mode of [{name:'local',lms:false,review:false},{name:'local-review',lms:false,review:true},{name:'LMS-simulation',lms:true,review:false},{name:'LMS-review',lms:true,review:true}]) {
   const context=await browser.newContext({viewport,reducedMotion:'reduce'});
   await context.route(/^https?:/,r=>r.abort());
   await context.addInitScript(({lms})=>{
    HTMLMediaElement.prototype.play=function(){return Promise.resolve()};
    window.qaCalls=[];
    const valueKey=name=>'qa:state:'+name;
    window.qaState=name=>JSON.parse(sessionStorage.getItem(valueKey(name))||'{}');
    const name=location.pathname.split('/').at(-1);
    if(!sessionStorage.getItem('qa:seeded')) {
     sessionStorage.setItem(valueKey('module2.html'),JSON.stringify({'cmi.core.lesson_status':'completed','cmi.core.lesson_location':'13'}));
     sessionStorage.setItem(valueKey('module4.html'),JSON.stringify({'cmi.core.lesson_status':'incomplete','cmi.core.lesson_location':'4'}));
     sessionStorage.setItem('qa:seeded','1');
    }
    if(!lms)return;
    const log=(...args)=>{qaCalls.push(args);sessionStorage.setItem('qa:calls:'+name,JSON.stringify(qaCalls))};
    const values=qaState(name);
    window.API={
     LMSInitialize(){log('init');return 'true'},
     LMSGetValue(k){log('get',k);return values[k]||''},
     LMSSetValue(k,v){log('set',k,v);values[k]=v;sessionStorage.setItem(valueKey(name),JSON.stringify(values));return 'true'},
     LMSCommit(){log('commit');return 'true'},
     LMSFinish(){log('finish');return 'true'},
    };
   },{lms:mode.lms});
   const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
   await page.goto(file('index.html')+(mode.review?'?review=1':''));
   const skip=page.locator('#ocpMotionIntroSkip');if(await skip.isVisible())await skip.click();
   await page.waitForFunction(()=>!document.getElementById('ocpMotionIntro'));
   await page.evaluate(()=>document.fonts.ready);
   check(await page.locator('article.module-card').count(),4,'Four informational module tiles');
   check(await page.locator('a.module-card').count(),0,'No unintended module tile links');
   check(await page.locator('.module-card .status').count(),0,'No inferred cross-SCO status labels');
   check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,'Home fits viewport');
   const start=page.locator('.index-start-link');check(await start.isVisible(),true,'Start action visible');
   check(await start.getAttribute('href'),'module1.html','Start targets module one');
   if(mode.lms&&!mode.review) {
    check(await page.evaluate(()=>qaCalls.filter(c=>c[0]==='init').length),1,'Home initializes once');
    check(await page.evaluate(()=>qaState('index.html')['cmi.core.lesson_status']),'completed','Home completes on launch');
    check(await page.evaluate(()=>qaCalls.filter(c=>c[0]==='set').map(c=>c[1])),['cmi.core.lesson_status'],'Home writes only its completion');
   } else check(await page.evaluate(()=>qaCalls),[],'Local/review home makes no LMS calls');
   check(await page.evaluate(()=>qaState('module2.html')),{'cmi.core.lesson_status':'completed','cmi.core.lesson_location':'13'},'Home preserves completed module state');
   check(await page.evaluate(()=>qaState('module4.html')),{'cmi.core.lesson_status':'incomplete','cmi.core.lesson_location':'4'},'Home preserves unfinished module bookmark');
   if(mode.name==='LMS-simulation')await page.screenshot({path:path.join(dest,device+'-home.png'),fullPage:true});
   await start.scrollIntoViewIfNeeded();await start.click();
   await page.waitForURL(file('module1.html')+(mode.review?'?review=1&slide=1':''));
   check(await page.locator('.slide.active').getAttribute('data-slide'),'1','Start click opens first teaching slide');
   if(mode.lms&&!mode.review) {
    const calls=await page.evaluate(()=>JSON.parse(sessionStorage.getItem('qa:calls:index.html')));
    check(calls.at(-1),['finish'],'Home finishes its session on exit');
    check(await page.evaluate(()=>qaState('module1.html')['cmi.core.lesson_status']),'incomplete','Module starts with its own incomplete status');
   } else check(await page.evaluate(()=>qaCalls),[],'Review/local navigation remains isolated');
   cases.push({device,mode:mode.name,result:'pass'});await context.close();
  }
 }
 check(errors,[],'No JavaScript errors');
 await fs.writeFile(path.join(dest,'home-browser-results.json'),JSON.stringify({assertions:checks.length,cases,errors,transport:'file://; no localhost server',scope:'SCORM API simulation; actual target LMS not tested'},null,2));
 console.log(`PASS: ${checks.length} home lifecycle, navigation and layout assertions across ${cases.length} cases.`);
} finally {await browser.close()}
