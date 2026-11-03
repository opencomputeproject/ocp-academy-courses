import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import assert from 'node:assert/strict';
const root=path.resolve(process.argv[2]||new URL('../../../',import.meta.url).pathname),out=root+'/authoring/qa/matty-author-credit-2026-11-03';await fs.mkdir(out+'/screenshots',{recursive:true});
const browser=await chromium.launch({headless:true,args:['--mute-audio']});const report={states:[],errors:[],audio:'Chromium muted; editorial review only'};
try{
 for(const viewport of [{name:'desktop',width:1440,height:900},{name:'tablet',width:1024,height:768},{name:'phone',width:390,height:844},{name:'small-phone',width:320,height:740}])for(const theme of ['light','dark']){
  const context=await browser.newContext({viewport,reducedMotion:'reduce'});const p=await context.newPage();p.on('pageerror',e=>report.errors.push(e.message));await p.route(/^https?:/,r=>r.abort());
  await p.goto(pathToFileURL(root+'/module1.html').href+'?review=1&slide=2');if(await p.locator('#ocpMotionIntroSkip').isVisible())await p.locator('#ocpMotionIntroSkip').click({force:true});
  await p.addStyleTag({content:'*,*::before,*::after{animation:none!important;transition:none!important}'});await p.evaluate(async theme=>{document.documentElement.setAttribute('data-theme',theme);await document.fonts.ready},theme);
  const portrait=p.locator('.slide.active img[src="figures/matty-bakkeren.jpg"]');assert.equal(await portrait.count(),1);const card=portrait.locator('..');await card.scrollIntoViewIfNeeded();
  const state=await card.evaluate(e=>{const img=e.querySelector('img'),text=e.querySelector('div'),s=getComputedStyle(img),r=e.getBoundingClientRect(),ir=img.getBoundingClientRect(),tr=text.getBoundingClientRect(),controls=document.querySelector('.controls').getBoundingClientRect(),slide=e.closest('.slide');return{text:e.innerText,card:{left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width},portrait:{width:ir.width,height:ir.height,radius:s.borderRadius,borderWidth:s.borderTopWidth,borderColor:s.borderTopColor,fit:s.objectFit,naturalWidth:img.naturalWidth,naturalHeight:img.naturalHeight},overflowX:slide.scrollWidth>slide.clientWidth+1,textFits:tr.right<=r.right-12&&tr.bottom<=r.bottom-8,controlTop:controls.top,unobscured:document.elementFromPoint(ir.x+ir.width/2,ir.y+ir.height/2)===img,slideScroll:slide.scrollTop}});
  assert.match(state.text,/Matty Bakkeren/);assert.match(state.text,/Founder, Momenthesis/);assert.equal(state.portrait.naturalWidth,721);assert.equal(state.portrait.naturalHeight,720);assert.equal(state.portrait.width,78);assert.equal(state.portrait.height,78);assert.equal(state.portrait.radius,'50%');assert.equal(state.portrait.borderWidth,'3px');assert.equal(state.portrait.borderColor,'rgb(141, 198, 63)');assert.equal(state.portrait.fit,'cover');assert.equal(state.overflowX,false);assert.equal(state.textFits,true);assert.equal(state.unobscured,true);assert.ok(state.card.left>=0&&state.card.right<=viewport.width);assert.ok(state.card.bottom<=state.controlTop-16);assert.equal(await p.locator('.slide.active').getAttribute('data-slide'),'2');
  await p.screenshot({path:out+`/screenshots/m1s2-${viewport.name}-${theme}.png`});report.states.push({viewport:viewport.name,theme,...state});await context.close();
 }
}catch(e){report.errors.push(e.stack);console.error(e.stack)}
await browser.close();report.passed=report.states.length===8&&report.errors.length===0;await fs.writeFile(out+'/browser-results.json',JSON.stringify(report,null,2)+'\n');console.log('Matty credit:',report.states.length,'states;',report.errors.length,'errors');if(!report.passed)process.exitCode=1;
