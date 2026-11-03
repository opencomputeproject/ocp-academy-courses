// Run from any directory with Playwright installed. No server or remote assets.
// Usage: node poster/render.mjs [thumbnail.png] [preview-output-folder]
import {chromium} from 'playwright';
import path from 'node:path';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {fileURLToPath,pathToFileURL} from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const course=path.resolve(here,'..');
const output=path.resolve(process.argv[2]||path.join(course,'thumbnail.png'));
const qa=path.resolve(process.argv[3]||path.join(here,'../../../build/poster-qa/open-rack'));
await fs.mkdir(path.dirname(output),{recursive:true});
await fs.mkdir(qa,{recursive:true});
const browser=await chromium.launch({headless:true});
const errors=[],bounds=[];
try{
  for(const [scale,target] of [[1,output],[.5,path.join(qa,'preview-400x200.png')],[.3,path.join(qa,'preview-240x120.png')]]){
    const page=await browser.newPage({viewport:{width:800,height:400},deviceScaleFactor:scale});
    await page.route(/^https?:/,route=>route.abort());
    page.on('pageerror',e=>errors.push(e.message));
    await page.goto(pathToFileURL(path.join(here,'poster.html')).href);
    await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()));});
    assert.ok(await page.evaluate(()=>document.fonts.check('700 22px Lato')),'Bundled Lato loaded');
    if(scale===1){
      const measured=await page.locator('[data-poster-text],.logo').evaluateAll(nodes=>nodes.map(n=>{const r=n.getBoundingClientRect();return {text:n.textContent.trim()||n.alt,left:r.left,right:r.right,top:r.top,bottom:r.bottom};}));
      for(const b of measured)assert.ok(b.left>=0&&b.right<=485&&b.top>=0&&b.bottom<=380,'Text/logo stays in its reserved field: '+b.text);
      bounds.push(...measured);
      assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth===800&&document.documentElement.scrollHeight===400),'Exact artboard');
    }
    await page.screenshot({path:target,clip:{x:0,y:0,width:800,height:400}});
    await page.close();
  }
  assert.deepEqual(errors,[]);
  const png=await fs.readFile(output);
  assert.equal(png.readUInt32BE(16),800);assert.equal(png.readUInt32BE(20),400);
  await fs.writeFile(path.join(qa,'poster-qa.json'),JSON.stringify({width:800,height:400,localAssetsOnly:true,bounds,errors},null,2)+'\n');
  console.log('PASS: 800×400 poster, 400×200/240×120 previews, bundled fonts and authoritative brand assets, no clipping or network dependencies.');
}finally{await browser.close();}
