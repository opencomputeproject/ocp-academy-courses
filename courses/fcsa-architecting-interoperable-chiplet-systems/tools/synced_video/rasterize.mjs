// Rasterize deterministic vectors with the packaged Open Sans font. No browser.
import fs from 'node:fs/promises';
import {createReadStream} from 'node:fs';
import {createInterface} from 'node:readline';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const work=path.join(root,'_video_work/synced-pilots');
const fontDir=path.join(work,'fontconfig');
await fs.mkdir(fontDir,{recursive:true});
process.env.FONTCONFIG_FILE=path.join(fontDir,'fonts.conf');
await fs.writeFile(process.env.FONTCONFIG_FILE,`<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd"><fontconfig><dir>${root}/fonts</dir><cachedir>${fontDir}/cache</cachedir></fontconfig>`);
const sharp=createRequire(import.meta.url)(process.env.SHARP_MODULE||'sharp');
const [mode,name]=process.argv.slice(2);
if(mode==='samples'){
  const dir=path.join(root,'audit/synced-video-production/native-svgs',name);
  const out=path.join(work,'samples',name);await fs.mkdir(out,{recursive:true});
  for(const f of (await fs.readdir(dir)).filter(f=>f.endsWith('.svg'))){
    await sharp(await fs.readFile(path.join(dir,f)),{density:96}).png().toFile(path.join(out,f.replace('.svg','.png')));
  }
  console.log(`${name}: native PNG samples ready`);
}else if(mode==='encode'){
  const ff=spawn(process.env.FFMPEG_BIN||'ffmpeg',[
    '-y','-v','warning','-f','image2pipe','-framerate','30','-vcodec','png','-i','pipe:0',
    '-an','-c:v','libx264','-crf','6','-preset','slow','-pix_fmt','yuv420p',
    '-vf','scale=in_range=pc:out_color_matrix=bt709:out_range=pc,format=yuv420p','-color_range','pc','-colorspace','bt709',
    '-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',path.join(work,`${name}.mp4`)
  ],{stdio:['pipe','ignore','pipe']});
  let error='';ff.stderr.on('data',b=>error+=b);
  const done=once(ff,'exit');
  let count=0;
  for await (const l of createInterface({input:createReadStream(path.join(work,`${name}-frames.jsonl`)),crlfDelay:Infinity})){
    const {svg}=JSON.parse(l);const buffer=await sharp(Buffer.from(svg),{density:96}).png().toBuffer();
    if(!ff.stdin.write(buffer))await once(ff.stdin,'drain');
    if(++count%300===0)console.log(`${name}: ${count} frames`);
  }
  ff.stdin.end();const [code]=await done;if(code!==0)throw new Error(error);
  console.log(`${name}: encoded ${count} frames; ${error.trim()||'no encoder warnings'}`);
}else throw new Error('Use samples|encode and m1|m4|m5|m9');
