import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve(process.argv[2] || new URL('../../../',import.meta.url).pathname);
const out=root+'/authoring/qa/scorm12-delivery/media-layout';
await fs.mkdir(out+'/screenshots',{recursive:true});
const c=JSON.parse(await fs.readFile(root+'/course.json'));
const browser=await chromium.launch({headless:true,args:['--mute-audio']});
const page=await browser.newPage();
const report={mediaSlides:c.modules.reduce((n,m)=>n+m.slides.filter(s=>s.figure).length,0),audioOutput:'Chromium muted; no audible playback',results:[],pageErrors:[],httpErrors:[]};
page.on('pageerror',e=>report.pageErrors.push(e.message));
page.on('response',r=>{if(r.status()>=400)report.httpErrors.push({status:r.status(),url:r.url()})});
for(const view of [{name:'desktop',width:1440,height:900},{name:'phone',width:390,height:844},{name:'small-phone',width:320,height:740}]){
 await page.setViewportSize(view);
 for(const theme of ['light','dark']){
  for(const m of c.modules)for(const s of m.slides.filter(s=>s.figure)){
   await page.goto(`file://${root}/module${m.id}.html?review=1&slide=${s.id}`);
   if(await page.locator('#ocpMotionIntroSkip').isVisible())await page.locator('#ocpMotionIntroSkip').click({force:true});
   await page.evaluate(t=>document.documentElement.setAttribute('data-theme',t),theme);
   await page.addStyleTag({content:'*,*::before,*::after{animation:none!important;transition:none!important}'});
   await page.evaluate(()=>document.fonts.ready);
   await page.waitForTimeout(40);
   const top=await page.locator('.slide.active').evaluate(e=>{
    const r=n=>{if(!n)return null;const b=n.getBoundingClientRect();return {left:b.left,right:b.right,top:b.top,bottom:b.bottom,width:b.width,height:b.height}};
    const wrap=e.querySelector('.figure-wrap'),frame=wrap?.querySelector('.figure-panel'),cap=wrap?.querySelector('.figure-caption'),main=e.querySelector('.slide-main-text'),aids=e.querySelector('.learner-aids'),firstPill=aids?.querySelector('.glossary-chip,.reference-pill');
    const capStyle=cap?getComputedStyle(cap):null;
    return{content:r(e.querySelector('.slide-content')),frame:r(frame),caption:r(cap),captionStyle:capStyle?{textAlign:capStyle.textAlign,fontSize:capStyle.fontSize,lineHeight:capStyle.lineHeight}:null,main:r(main),aids:r(aids),firstPill:r(firstPill),beforeAids:r(aids?.previousElementSibling),captionGap:cap?r(cap).top-r(frame).bottom:null,teachingGap:main?r(main).top-r(cap||frame).bottom:null,pillGap:firstPill?r(firstPill).top-r(aids.previousElementSibling).bottom:null,scrollHeight:e.scrollHeight,clientHeight:e.clientHeight,scrollWidth:e.scrollWidth,clientWidth:e.clientWidth,overflowY:getComputedStyle(e).overflowY,brokenImages:[...e.querySelectorAll('img')].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),overflowingPills:[...e.querySelectorAll('.glossary-chip,.reference-pill')].filter(p=>p.getBoundingClientRect().right>innerWidth+1||p.getBoundingClientRect().left<0).map(p=>p.textContent)};
   });
   const flags=[];const expectedTop=view.width<=768?96:84;
   if(Math.abs(top.content.top-expectedTop)>1)flags.push('top-alignment');
   if(!top.caption)flags.push('missing-caption');
   else{
    if(Math.abs(top.caption.left-top.frame.left)>1)flags.push('caption-left-edge');
    if(Math.abs(top.caption.width-top.frame.width)>1)flags.push('caption-width');
    if(top.captionStyle.textAlign!=='left')flags.push('caption-text-alignment');
    if(top.captionGap<15.9)flags.push('media-caption-gap');
   }
   if(top.teachingGap!==null&&top.teachingGap<15.9)flags.push('caption-teaching-gap');
   if(top.pillGap!==null&&top.pillGap<23.9)flags.push('text-pill-gap');
   if(top.scrollWidth>top.clientWidth+1||top.frame.left<0||top.frame.right>view.width+1||top.overflowingPills.length)flags.push('horizontal-overflow');
   if(top.brokenImages.length)flags.push('broken-images');
   if(top.scrollHeight>top.clientHeight+2&&!['auto','scroll'].includes(top.overflowY))flags.push('missing-scrolling');
   const key=`${view.name}-${theme}-m${m.id}-s${s.id}`;
   if(theme==='light'&&view.name!=='small-phone')await page.screenshot({path:`${out}/screenshots/${key}-top.png`});
   const bottom=await page.locator('.slide.active').evaluate(e=>{
    e.scrollTop=e.scrollHeight;
    const content=e.querySelector('.slide-content').getBoundingClientRect(),controls=document.querySelector('.controls').getBoundingClientRect();
    return{scrollTop:e.scrollTop,contentBottom:content.bottom,controlsTop:controls.top,clearance:controls.top-content.bottom};
   });
   if(bottom.clearance<15.9)flags.push('bottom-controls-clearance');
   if(theme==='light'&&view.name!=='small-phone'&&bottom.scrollTop>0)await page.screenshot({path:`${out}/screenshots/${key}-bottom.png`});
   report.results.push({view:view.name,viewport:{width:view.width,height:view.height},theme,module:m.id,slide:s.id,title:s.title,kind:s.figure.role==='original_video'?'recording':s.figure.media_type==='video'?'animation':'static',flags,...top,bottom});
  }
  console.log(view.name,theme,'complete;',report.results.filter(r=>r.flags.length).length,'flagged so far');
 }
}
report.flags=report.results.filter(r=>r.flags.length);
report.combinations=report.results.length;
await fs.writeFile(out+'/media-layout-results.json',JSON.stringify(report,null,2)+'\n');
console.log('Checked',report.combinations,'layouts;',report.flags.length,'flags;',report.pageErrors.length,'page errors;',report.httpErrors.length,'HTTP errors');
await browser.close();
if(report.flags.length||report.pageErrors.length||report.httpErrors.length)process.exitCode=1;
