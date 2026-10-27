// Measure visible phrase ink with the exact SVG rasterizer/font used for media.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import crypto from 'node:crypto';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
process.env.FONTCONFIG_FILE=path.join(root,'_video_work/synced-pilots/fontconfig/fonts.conf');
const sharp=createRequire(import.meta.url)(process.env.SHARP_MODULE||'sharp');
const targets=[['Initialization · errors','Initialization'],['Initialization · errors','errors'],['Accuracy: policies + evidence','policies + evidence'],['Confidentiality: policies + evidence','policies + evidence']];
const escape=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const metrics={};
for(const [full,phrase] of targets){
 const before=full.slice(0,full.indexOf(phrase)),after=full.slice(full.indexOf(phrase)+phrase.length);
 const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="200" viewBox="0 0 1920 200"><rect width="1920" height="200" fill="white"/><text x="960" y="100" text-anchor="middle" font-family="Open Sans,sans-serif" font-size="48" font-weight="600" fill="white"><tspan x="960" dy="0">${escape(before)}<tspan fill="#5F6062">${escape(phrase)}</tspan>${escape(after)}</tspan></text></svg>`;
 const {data,info}=await sharp(Buffer.from(svg),{density:288}).removeAlpha().raw().toBuffer({resolveWithObject:true});
 let left=info.width,right=-1;
 for(let y=0;y<info.height;y++)for(let x=0;x<info.width;x++)if(data[(y*info.width+x)*info.channels]<200){left=Math.min(left,x);right=Math.max(right,x);}
 const key=JSON.stringify([full,phrase,48,600]);metrics[key]=[left/4-960,(right+1)/4-960];
 console.log(phrase,metrics[key].map(x=>x+960));
}
await fs.writeFile(path.join(root,'tools/synced_video/font_metrics.json'),JSON.stringify({method:'Visible SVG glyph ink at4x native resolution, exact Open Sans/librsvg production stack',font_sha256:crypto.createHash('sha256').update(await fs.readFile(path.join(root,'fonts/OpenSans[wdth,wght].ttf'))).digest('hex'),bounds:metrics},null,2)+'\n');
