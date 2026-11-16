import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
await fs.mkdir(path.join(dir,'qa'),{recursive:true});const browser=await chromium.launch({headless:true});const page=await browser.newPage({viewport:{width:1920,height:1080}});
for(const stem of process.argv.slice(2)){
 await page.goto(pathToFileURL(path.join(dir,stem+'.html')).href);await page.evaluate(()=>document.fonts.ready);
 const report=[];
 for(const f of [0,.25,.5,.75,.99]){
 await page.evaluate(f=>window.setTeachingTime(f*Number(document.body.dataset.durationMs)),f);
 await page.screenshot({path:path.join(dir,'qa',stem+'-'+f+'.png')});
 report.push(await page.evaluate(f=>({fraction:f,text:[...document.querySelectorAll('text')].map(x=>{let r=x.getBoundingClientRect();return {text:x.textContent,x:r.x,y:r.y,width:r.width,height:r.height}})}),f));
 }
 await fs.writeFile(path.join(dir,'qa',stem+'-bounds.json'),JSON.stringify(report,null,2));
}
await browser.close();
