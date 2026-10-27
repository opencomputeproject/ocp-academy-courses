import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
const root=path.resolve(import.meta.dirname,'..');
const recorder=path.join(root,'tools/academy_wizard/scripts/record_css_animation.mjs');
const course=JSON.parse(await fs.readFile(path.join(root,'course.json'),'utf8'));
const synced=new Set(course.modules.flatMap(m=>m.slides).filter(s=>s.figure?.sync_to_narration===true).map(s=>path.basename(s.figure.path,'.mp4')+'.html'));
const sources=(await fs.readdir(path.join(root,'animation_sources'))).filter(x=>x.endsWith('.html')&&!synced.has(x));
const browser=await chromium.launch({headless:true,args:["--mute-audio"],executablePath:process.env.ACADEMY_CHROMIUM_BIN});
const page=await browser.newPage({viewport:{width:1920,height:1080}});
const checks=[];
for(const name of sources){
 const file=path.join(root,'animation_sources',name);
 await page.goto(pathToFileURL(file).href);
 await page.evaluate(()=>document.fonts.ready);
 const check=await page.evaluate(()=>{
  const errors=[];
  for(const t of document.querySelectorAll('svg text')){
   const b=t.getBBox(); const fs=parseFloat(getComputedStyle(t).fontSize);
   if(b.x<12||b.y<12||b.x+b.width>1188||b.y+b.height>588)errors.push({text:t.textContent,bounds:{x:b.x,y:b.y,w:b.width,h:b.height}});
   const group=t.closest('g.stage');const box=group?.querySelector('rect');
   if(box){const r=box.getBBox();if(b.x<r.x+fs*.75||b.x+b.width>r.x+r.width-fs*.75||b.y<r.y+fs*.75||b.y+b.height>r.y+r.height-fs*.75)errors.push({text:t.textContent,reason:'insufficient interior clearance'});}
  }
  return errors;
 });
 checks.push({name,errors:check});
}
await browser.close();
await fs.writeFile(path.join(root,'audit/animation-text-fit.json'),JSON.stringify(checks,null,2));
if(checks.some(x=>x.errors.length))throw new Error('Text-fit review failed; inspect audit/animation-text-fit.json');
for(const name of sources){
 const stem=path.basename(name,'.html'); const out=path.join(root,'figures',stem+'.mp4');
 if(!process.env.ACADEMY_REENCODE){try{await fs.access(out);console.log('Exists:',stem);continue;}catch{}}
 await new Promise((resolve,reject)=>{const p=spawn(process.execPath,[recorder,path.join(root,'animation_sources',name),out,path.join(root,'figures',stem+'.png'),'8000','6500','30'],{env:process.env,stdio:'inherit'});p.on('exit',c=>c===0?resolve():reject(Error('Recorder exit '+c)));});
}
