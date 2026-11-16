import {chromium} from 'playwright';
import fs from 'node:fs/promises';import path from 'node:path';import {fileURLToPath,pathToFileURL} from 'node:url';import crypto from 'node:crypto';
const dir=path.dirname(fileURLToPath(import.meta.url));const stems=process.argv.slice(2);await fs.mkdir(path.join(dir,'qa'),{recursive:true});const browser=await chromium.launch({headless:true});
for(const stem of stems){
 const p=await browser.newPage({viewport:{width:1920,height:1080}});await p.goto(pathToFileURL(path.join(dir,stem+'.html')).href);await p.evaluate(()=>document.fonts.ready);
 const timeline=JSON.parse(await fs.readFile(path.join(dir,stem+'.timeline.json'),'utf8'));const duration=timeline.duration_ms/1000;
 const inventory=await p.evaluate(duration=>{const found=new Map();for(let t=0;t<=duration;t+=.1){window.setTeachingTime(t*1000);for(const text of document.querySelectorAll('text')){let opacity=1;for(let n=text;n;n=n.parentElement)opacity*=Number(getComputedStyle(n).opacity);if(opacity>.95&&!found.has(text.textContent)){const b=text.getBoundingClientRect();found.set(text.textContent,{text:text.textContent,first_readable_seconds:Math.round(t*10)/10,x:b.x,y:b.y,width:b.width,height:b.height});}}}return [...found.values()]},duration);
 const times=[0,duration*.25,duration*.5,duration*.75,duration-1/30];for(const [key,sec] of Object.entries(timeline.scene_seconds)){if(key.endsWith('duration'))continue;times.push(Math.max(0,sec-.1),Math.min(duration-1/30,sec+.7));}
 const unique=[...new Set(times.map(t=>Math.round(t*1000)/1000))].sort((a,b)=>a-b);
 for(const [i,t] of unique.entries()){await p.evaluate(t=>window.setTeachingTime(t*1000),t);await p.screenshot({path:path.join(dir,'qa',stem+'-source-'+i+'.png')});}
 await fs.writeFile(path.join(dir,'qa',stem+'-source-review.json'),JSON.stringify({duration_seconds:duration,review_frame_times_seconds:unique,visible_text:inventory},null,2));await p.close();
}
await browser.close();
