// Encode exactly one declared SVG timeline from lossless browser frames.
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
import fs from 'node:fs/promises';
import { spawn } from 'node:child_process';
import { once } from 'node:events';

const [sourceArg='animation.html',videoArg='../../figures/commissioning_sequence.mp4',posterArg='../../figures/commissioning_sequence_poster.png'] = process.argv.slice(2);
const source=path.resolve(sourceArg),video=path.resolve(videoArg),poster=path.resolve(posterArg);
const ffmpeg=process.env.FFMPEG_BIN||'ffmpeg';
const fps=30;
await fs.mkdir(path.dirname(video),{recursive:true});
await fs.mkdir(path.dirname(poster),{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true,args:['--mute-audio']});
try {
  const page=await browser.newPage({viewport:{width:1920,height:1080}});
  await page.goto(pathToFileURL(source).href);
  await page.evaluate(()=>document.fonts.ready);
  const meta=await page.evaluate(()=>({duration:Number(document.body.dataset.durationMs)/1000,poster:Number(document.body.dataset.posterMs)/1000}));
  if(!meta.duration||await page.evaluate(()=>typeof window.renderAt)!=='function')throw new Error('Missing source timeline');
  const frames=Math.round(meta.duration*fps);
  const encoder=spawn(ffmpeg,['-y','-f','image2pipe','-vcodec','png','-framerate',String(fps),'-i','pipe:0','-an','-vf','scale=out_color_matrix=bt709:out_range=tv','-c:v','libx264','-preset','slow','-tune','animation','-crf','8','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',video],{stdio:['pipe','ignore','pipe']});
  let errors='';encoder.stderr.on('data',data=>errors+=data);
  const closed=once(encoder,'close');
  for(let frame=0;frame<frames;frame++){
    await page.evaluate(t=>window.renderAt(t),frame/fps);
    const png=await page.screenshot({type:'png'});
    if(!encoder.stdin.write(png))await once(encoder.stdin,'drain');
    if(frame%90===0)console.log('Rendered '+frame+'/'+frames+' lossless frames');
  }
  encoder.stdin.end();
  const [code]=await closed;if(code!==0)throw new Error(errors.slice(-3000));
  await page.evaluate(t=>window.renderAt(t),Math.min(meta.poster,meta.duration-1/fps));
  await page.screenshot({path:poster,type:'png'});
  console.log('Encoded '+frames+' frames: '+meta.duration+' seconds, 1920x1080, H.264, no audio.');
} finally {await browser.close();}
