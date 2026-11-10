// Run against a built Slides course. Silent, offline, no live LMS writes.
import assert from 'node:assert/strict';
import {chromium} from 'playwright';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const folder=process.argv[2];
assert.ok(folder,'Usage: node test_long_home_title_browser.mjs <built-course>');
const browser=await chromium.launch({headless:true,args:['--mute-audio']});
try{
 const page=await browser.newPage({reducedMotion:'reduce'});
 await page.route(/^https?:/,r=>r.abort());
 await page.goto(pathToFileURL(path.resolve(folder,'index.html')).href+'?review=1');
 await page.locator('#ocpMotionIntroSkip').click().catch(()=>{});
 await page.waitForTimeout(700);
 for(const width of [320,390,640,1440]){
  await page.setViewportSize({width,height:960});
  const result=await page.evaluate(()=>{const h=document.querySelector('.header h1').getBoundingClientRect();return{overflow:document.documentElement.scrollWidth>innerWidth,left:h.left,right:h.right,viewport:innerWidth}});
  assert.equal(result.overflow,false,`${width}px home has no horizontal overflow`);
  assert.ok(result.left>=0&&result.right<=result.viewport,`${width}px title stays in viewport`);
 }
 console.log('PASS: long home title fits 320, 390, 640 and 1440px viewports.');
}finally{await browser.close()}
