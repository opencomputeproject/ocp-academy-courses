// Measure Japanese phrase ink with the production SVG rasterizer and font.
import fs from 'node:fs/promises';import path from 'node:path';
import {fileURLToPath} from 'node:url';import {createRequire} from 'node:module';import crypto from 'node:crypto';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const config=path.join(root,'_video_work/synced-pilots/fontconfig');await fs.mkdir(config,{recursive:true});
process.env.FONTCONFIG_FILE=path.join(config,'fonts.conf');
await fs.writeFile(process.env.FONTCONFIG_FILE,`<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd"><fontconfig><dir>${root}/fonts</dir><cachedir>${config}/cache</cachedir></fontconfig>`);
const sharp=createRequire(import.meta.url)(process.env.SHARP_MODULE||'sharp');
const labels=JSON.parse(await fs.readFile(path.join(root,'video_source/labels.ja.json'),'utf8'));
const source=[['Initialization · errors','Initialization',48],['Initialization · errors','errors',48],['Accuracy: policies + evidence','policies + evidence',48],['Confidentiality: policies + evidence','policies + evidence',48],['Must be compatible','Must be compatible',62],['Framing · error protection','Framing',53],['Framing · error protection','error protection',53],['Flow control','Flow control',53],['Identity · version','Identity · version',50],['Query limits','Query limits',50],['Permitted outputs','Permitted outputs',50]];
const escape=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');const metrics={};
for(const [a,b,size] of source){
 const full=labels[a],phrase=labels[b],index=full.indexOf(phrase);if(index<0)throw Error('Underline phrase missing');
 const before=full.slice(0,index),after=full.slice(index+phrase.length);
 const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="200" viewBox="0 0 1920 200"><rect width="1920" height="200" fill="white"/><text x="960" y="100" text-anchor="middle" font-family="Noto Sans JP,sans-serif" font-size="${size}" font-weight="600" fill="white"><tspan x="960" dy="0">${escape(before)}<tspan fill="#5F6062">${escape(phrase)}</tspan>${escape(after)}</tspan></text></svg>`;
 const {data,info}=await sharp(Buffer.from(svg),{density:288}).removeAlpha().raw().toBuffer({resolveWithObject:true});let left=info.width,right=-1;
 for(let y=0;y<info.height;y++)for(let x=0;x<info.width;x++)if(data[(y*info.width+x)*info.channels]<200){left=Math.min(left,x);right=Math.max(right,x);}
 metrics[JSON.stringify([full,phrase,size,600])]=[left/4-960,(right+1)/4-960];
}
await fs.writeFile(path.join(root,'tools/synced_video/font_metrics.json'),JSON.stringify({method:'Visible Japanese glyph ink at 4x native resolution; Noto Sans JP/librsvg production stack',font_sha256:crypto.createHash('sha256').update(await fs.readFile(path.join(root,'fonts/NotoSansJP[wght].ttf'))).digest('hex'),bounds:metrics},null,2)+'\n');
console.log(`Measured ${source.length} Japanese underline cases.`);
