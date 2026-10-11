// Deterministically render the 14-second output-window animation and poster.
// Requires Sharp and ffmpeg; no narration generation or network calls.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
const require = createRequire(import.meta.url);
const sharp = require(process.env.SST_SHARP_MODULE || 'sharp');
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const figures = path.resolve(process.env.SST_OUTPUT_DIR || path.join(root, 'figures'));
const frames = fs.mkdtempSync(path.join(os.tmpdir(), 'ocp-sst-output-windows-'));
fs.mkdirSync(figures, {recursive:true});
const MASTER_DURATION=14, FPS=24, POSTER_TIME=11;
const base = fs.readFileSync(path.join(root,'figures/lvdc_output_envelope.svg'),'utf8');
const clamp = x => Math.min(1,Math.max(0,x));
function frame(t) {
  const fault=clamp((t-1)/4), overload=clamp((t-7)/4);
  const extra=`<g font-family="Arial,sans-serif">
    <rect x="345" y="135" width="260" height="280" rx="18" fill="none" stroke="#f4b13d" stroke-width="${t>=1&&t<=6?4:0}"/>
    <rect x="635" y="135" width="235" height="280" rx="18" fill="none" stroke="#4aa3df" stroke-width="${t>=7?4:0}"/>
    <text x="70" y="540" fill="#d9e2eb" font-size="19">Fault-support window · 150 ms</text>
    <text x="660" y="540" fill="#d9e2eb" font-size="19">Overload window · 5 s</text>
    <rect x="70" y="555" width="470" height="14" rx="7" fill="#40536b"/>
    <rect x="70" y="555" width="${470*fault}" height="14" rx="7" fill="#f4b13d"/>
    <rect x="660" y="555" width="470" height="14" rx="7" fill="#40536b"/>
    <rect x="660" y="555" width="${470*overload}" height="14" rx="7" fill="#4aa3df"/>
    <text x="70" y="598" fill="#d9e2eb" font-size="18">${fault>=1?'After 150 ms: SST may trip':'150% constant-current support'}</text>
    <text x="660" y="598" fill="#d9e2eb" font-size="18">120% overload at constant voltage</text>
    <text x="600" y="640" text-anchor="middle" fill="#9eaec2" font-size="15">Separate time scales · schematic, not a prescribed waveform · recommended settings</text>
  </g>`;
  return base.replace('</svg>',extra+'</svg>');
}
for(let n=0; n<MASTER_DURATION*FPS; n++) {
  const target=path.join(frames,`frame_${String(n).padStart(4,'0')}.png`);
  await sharp(Buffer.from(frame(n/FPS))).resize(1920,1080).flatten({background:'#121b31'}).png().toFile(target);
}
execFileSync(process.env.SST_FFMPEG_BIN || 'ffmpeg',[
  '-hide_banner','-loglevel','error','-framerate',String(FPS),
  '-i',path.join(frames,'frame_%04d.png'),'-frames:v',String(MASTER_DURATION*FPS),
  '-c:v','libx264','-preset','slow','-crf','12','-pix_fmt','yuv420p',
  '-movflags','+faststart','-an','-y',path.join(figures,'lvdc_output_windows.mp4')
]);
await sharp(Buffer.from(frame(POSTER_TIME))).resize(1920,1080).flatten({background:'#121b31'}).png().toFile(path.join(figures,'lvdc_output_windows_poster.png'));
console.log(JSON.stringify({duration:MASTER_DURATION,fps:FPS,frames:MASTER_DURATION*FPS,width:1920,height:1080,poster:POSTER_TIME,frame_directory:frames},null,2));
