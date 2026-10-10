import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { storyboards, createHtml } from './storyboards.mjs';

const [buildDir, selected = 'all', mode = 'encode'] = process.argv.slice(2);
if (!buildDir || !['preview','encode','inventory'].includes(mode)) throw new Error('Usage: node animations/render.mjs <built-course-with-approved-WAVs> [M1S4|M2S5|M4S4|all] [preview|encode|inventory]');
const source = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const output = path.join(source, 'figures');
const qa = process.env.ACADEMY_VIDEO_QA_DIR || path.join(os.tmpdir(), 'two-phase-video-review');
const playwright = await import(process.env.PLAYWRIGHT_MODULE || 'playwright');
const browser = await playwright.chromium.launch({headless:true, ...(process.env.PLAYWRIGHT_CHANNEL ? {channel:process.env.PLAYWRIGHT_CHANNEL} : {}), args:['--mute-audio']});
const page = await browser.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:1});
const capture = await page.context().newCDPSession(page);
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const manifest = { approval: 'User approved the suggested narration-synchronized M1S4, M2S5 and M4S4 videos on 2026-10-11.', fps:30, width:1920, height:1080, videos:[] };
await fs.mkdir(qa,{recursive:true});

// Refuse an unnoticed audio-duration change: narration edits need cue review.
function wavDuration(bytes) {
  if (bytes.toString('ascii',0,4) !== 'RIFF' || bytes.toString('ascii',8,12) !== 'WAVE') throw new Error('Expected RIFF WAV');
  let rate, data;
  for (let offset=12;offset+8<=bytes.length;) {
    const size=bytes.readUInt32LE(offset+4), name=bytes.toString('ascii',offset,offset+4);
    if (name==='fmt ') rate=bytes.readUInt32LE(offset+16);
    if (name==='data') data=size;
    offset+=8+size+(size%2);
  }
  if (!rate || data===undefined) throw new Error('WAV is missing format/data chunks');
  return data/rate;
}
try {
  for (const item of storyboards.filter((s)=>selected==='all'||selected.split(',').includes(s.slide))) {
    const wav=await fs.readFile(path.join(buildDir,item.audio));
    const duration=wavDuration(wav);
    if (Math.abs(duration-item.duration)>1/30) throw new Error(`${item.slide}: narration duration changed; review storyboard cues before encoding`);
    const html=path.join(qa,`${item.stem}.html`);
    await fs.writeFile(html,createHtml(item));
    await page.goto(pathToFileURL(html).href);
    await page.evaluate(()=>document.fonts.ready);
    const setTime=async(t)=>page.evaluate((seconds)=>window.setAcademyVideoTime(seconds),t);
    const sampled=[0,...item.cues.map(([t])=>Math.min(duration-.04,t+.15)),...Array.from({length:5},(_,i)=>(duration-.04)*i/4),duration-.05];
    const inventories=[];
    for (const t of [...new Set(sampled)].sort((a,b)=>a-b)) {
      await setTime(t);
      const labels=await page.locator('svg text').allTextContents();
      for (const label of labels) if (!inventories.some((entry)=>entry.text===label)) inventories.push({text:label,at_seconds:Number(t.toFixed(3))});
      const errors=await page.evaluate(()=>[...document.querySelectorAll('[data-text-box]')].flatMap((g)=>{
        const [x,y,w,h]=g.dataset.textBox.split(',').map(Number);
        return [...g.querySelectorAll('text')].filter((el)=>{const b=el.getBBox();return b.x<x+20||b.x+b.width>x+w-20||b.y<y+20||b.y+b.height>y+h-20;}).map((el)=>el.textContent);
      }));
      if(errors.length) throw new Error(`${item.slide} text leaves its padded shape: ${errors.join(', ')}`);
      await page.screenshot({path:path.join(qa,`${item.slide}-${t.toFixed(2)}.png`)});
    }
    if(mode==='preview') {console.log(`${item.slide}: preview frames and label containment passed`);continue;}
    await fs.mkdir(output,{recursive:true});
    const target=path.join(output,`${item.stem}.mp4`);
    const count=Math.round(duration*30);
    if(mode==='encode') {
    const encoder=spawn(process.env.FFMPEG_BIN||'ffmpeg',['-y','-f','image2pipe','-vcodec','png','-framerate','30','-i','pipe:0','-an','-vf','scale=out_color_matrix=bt709:out_range=tv:flags=bicubic+accurate_rnd','-c:v','libx264','-preset','slow','-tune','animation','-crf','8','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',target],{stdio:['pipe','ignore','pipe']});
    let diagnostics='';encoder.stderr.on('data',(chunk)=>{diagnostics+=chunk.toString();});
    const closed=once(encoder,'close');
    encoder.stdin.on('error',()=>{});
    for(let i=0;i<count;i++) {
      await setTime(i/30);
      const png=Buffer.from((await capture.send('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:false,clip:{x:0,y:0,width:1920,height:1080,scale:1}})).data,'base64');
      if(png.readUInt32BE(16)!==1920||png.readUInt32BE(20)!==1080)throw new Error('Unexpected native capture dimensions');
      if(!encoder.stdin.write(png))await Promise.race([once(encoder.stdin,'drain'),closed.then(([code])=>{throw new Error(`FFmpeg closed early (${code}): ${diagnostics.slice(-3000)}`);})]);
      if(i%300===0)console.log(`${item.slide}: ${i}/${count} frames`);
    }
    encoder.stdin.end();
    const [code]=await closed;if(code!==0)throw new Error(diagnostics.slice(-3000));
    await setTime(duration-2);
    const poster=path.join(output,`${item.stem}_poster.png`);
    await page.screenshot({path:poster});
    }
    manifest.videos.push({slide:item.slide,path:`figures/${item.stem}.mp4`,poster:`figures/${item.stem}_poster.png`,duration_seconds:count/30,narration_duration_seconds:duration,narration_sha256:sha(wav),script_sha256:sha(await fs.readFile(path.join(source,item.script))),poster_seconds:duration-2,cues:item.cues.map(([at_seconds,scene])=>({at_seconds,scene})),text_inventory:{sha256:sha(await fs.readFile(target)),entries:inventories}});
    console.log(`${item.slide}: encoded ${count} frames; ${(count/30).toFixed(3)} seconds`);
  }
  if(mode!=='preview')await fs.writeFile(path.join(qa,`video-manifest-${selected}.json`),JSON.stringify(manifest,null,2)+'\n');
} finally {await browser.close();}
