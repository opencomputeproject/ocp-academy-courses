#!/usr/bin/env node
/** Reproducible catalog posters. Requires Playwright (see references/lms_poster_style.md). */
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const { Resvg } = require('@resvg/resvg-js');
const skill = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
for(let i=0;i<args.length;i++){
  if(['--check','--help'].includes(args[i]))continue;
  assert.ok(['--repo-root','--course','--qa-dir'].includes(args[i]),`Unknown option: ${args[i]}; use --help`);
  assert.ok(args[i+1]&&!args[i+1].startsWith('--'),`Missing value for ${args[i]}`);i++;
}
const check = args.includes('--check');
const value = flag => {const i=args.indexOf(flag);return i<0?null:args[i+1];};
if(args.includes('--help')){
  console.log('node render_lms_posters.mjs --repo-root <repo> [--course <course-folder>] [--check] [--qa-dir <folder>]\nWithout --course, discovers canonical courses/**/thumbnail.png (excluding locales) and requires poster.json. --check renders and compares without writing source assets.');
  process.exit(0);
}
const root = path.resolve(value('--repo-root') || process.cwd());
const qa = path.resolve(value('--qa-dir') || path.join(root, 'build/poster-qa'));
const template = await fs.readFile(path.join(skill,'templates/poster/poster.html'),'utf8');
const escape = s => String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const uri = async file => {
  const ext=path.extname(file).toLowerCase();
  const mime={'.svg':'image/svg+xml','.png':'image/png','.woff':'font/woff','.woff2':'font/woff2'}[ext];
  assert.ok(mime,`Unsupported poster asset: ${file}`);
  return `data:${mime};base64,${(await fs.readFile(file)).toString('base64')}`;
};
async function discover(dir){
  const result=[];
  for(const entry of await fs.readdir(dir,{withFileTypes:true})){
    if(entry.isDirectory()&&entry.name!=='locales') result.push(...await discover(path.join(dir,entry.name)));
    else if(entry.name==='thumbnail.png'||entry.name==='poster.json') result.push(dir);
  }
  return [...new Set(result)].sort();
}
const dirs=value('--course')?[path.resolve(root,value('--course'))]:await discover(path.join(root,'courses'));
assert.ok(dirs.length,'No posters found');
for(const dir of dirs)assert.ok(!dir.split(path.sep).includes('locales'),'Use the canonical English poster; translations do not have separate posters');
await fs.mkdir(qa,{recursive:true});
const logo = await uri(path.join(skill,'assets/ocp_academy_white.svg'));
const lato = await uri(path.join(skill,'assets/fonts/lato2-bold.woff'));
const backgroundSource=await fs.readFile(path.join(skill,'templates/poster/background.svg'),'utf8');
const backgroundPng=await fs.readFile(path.join(skill,'templates/poster/background.png'));
assert.ok(new Resvg(backgroundSource).render().asPng().equals(backgroundPng),'Shared background is stale; run render_poster_background.mjs');
const background=await uri(path.join(skill,'templates/poster/background.png'));
const browser = await chromium.launch({headless:true,args:['--disable-gpu','--force-color-profile=srgb']});
const reports=[];
try{
  for(const dir of dirs){
    const rel=path.relative(root,dir).split(path.sep).join('/');
    const data=JSON.parse(await fs.readFile(path.join(dir,'poster.json'),'utf8'));
    for(const key of Object.keys(data))assert.ok(['schema_version','language','badge','title_lines','support_lines','mark','mark_alt'].includes(key),`${rel}: unknown poster field ${key}; layout is shared`);
    assert.ok(/^en(?:-|$)/i.test(data.language),`${rel}: catalog posters must be in English; reuse one poster for every translation`);
    assert.equal(data.schema_version,1,`${rel}: schema_version must be 1`);
    for(const key of ['badge','mark','mark_alt','language'])assert.ok(typeof data[key]==='string'&&data[key].trim(),`${rel}: ${key} required`);
    for(const key of ['title_lines','support_lines'])assert.ok(Array.isArray(data[key])&&data[key].length&&data[key].every(x=>typeof x==='string'&&x.trim()),`${rel}: ${key} required`);
    assert.ok(data.support_lines.length<=2,`${rel}: at most two support lines`);
    const text=[data.badge,...data.title_lines,...data.support_lines].join('');
    assert.ok(!/[\u3000-\u9fff\uac00-\ud7af]/u.test(text),`${rel}: catalog poster copy must be in English`);
    const replacements={LANG:escape(data.language),TITLE:escape(data.title_lines.join(' ')),LATO:lato,LOGO:logo,BACKGROUND:background,BADGE:escape(data.badge),TITLE_LINES:data.title_lines.map(x=>`<span class="title-line">${escape(x).replaceAll('™','<sup>TM</sup>')}</span>`).join(''),SUPPORT:data.support_lines.map(x=>`<span>${escape(x)}</span>`).join(''),MARK:await uri(path.resolve(dir,data.mark)),MARK_ALT:escape(data.mark_alt)};
    const html=template.replace(/\{\{([A-Z_]+)\}\}/g,(_,key)=>{assert.ok(key in replacements,key);return replacements[key];});
    const page=await browser.newPage({viewport:{width:800,height:400},deviceScaleFactor:1});
    const errors=[];page.on('pageerror',e=>errors.push(e.message));
    await page.route(/^https?:/,r=>{errors.push(`Unexpected network request: ${r.request().url()}`);return r.abort();});
    await page.setContent(html,{waitUntil:'load'});
    await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()));});
    const layout=await page.evaluate(({titleLines})=>{
      const title=document.querySelector('.title');
      const canvas=document.createElement('canvas').getContext('2d');
      // Prefer editorial line breaks. If they do not fit, wrap at word boundaries
      // before stepping down the shared size ladder; never distort or crop text.
      function wrap(words,size){
        canvas.font=`700 ${size}px AcademyLato`;
        const measure=s=>canvas.measureText(s.replaceAll('™','')).width+(s.includes('™')?size*.55:0);
        const maxLines=Math.floor(144/(size*1.1));
        const memo=new Map();
        function solve(start,left){
          if(start===words.length)return {cost:0,lines:[]};
          if(!left)return null;
          const key=start+':'+left;if(memo.has(key))return memo.get(key);
          let best=null;
          for(let end=start+1;end<=words.length;end++){
            const line=words.slice(start,end).join(' '),width=measure(line);
            if(width>458)break;
            const rest=solve(end,left-1);if(!rest)continue;
            const cost=(458-width)**2+rest.cost;
            if(!best||cost<best.cost)best={cost,lines:[line,...rest.lines]};
          }
          memo.set(key,best);return best;
        }
        if(titleLines.length<=maxLines&&titleLines.every(x=>measure(x)<=458))return titleLines;
        return solve(0,maxLines)?.lines;
      }
      let size,lines;
      for(size of [40,36,32]){lines=wrap(titleLines.join(' ').toUpperCase().split(/\s+/),size);if(lines)break;}
      if(!lines)throw new Error('Title exceeds all maintained sizes; edit poster copy explicitly');
      title.style.fontSize=size+'px';title.replaceChildren();
      for(const line of lines){const span=document.createElement('span');span.className='title-line';
        const parts=line.split('™');span.append(document.createTextNode(parts[0]));
        for(const part of parts.slice(1)){const sup=document.createElement('sup');sup.textContent='TM';span.append(sup,document.createTextNode(part));}
        title.append(span);
      }
      const rect=n=>{const r=n.getBoundingClientRect();return {left:r.left,top:r.top,width:r.width,height:r.height,right:r.right,bottom:r.bottom};};
      const textBounds=[...document.querySelectorAll('.title-line,.support span,.badge')].map(n=>{const range=document.createRange();range.selectNodeContents(n);const r=range.getBoundingClientRect();return {text:n.textContent,left:r.left,right:r.right,top:r.top,bottom:r.bottom,role:n.className||'support'};});
      return {titleSize:size,titleLines:lines,textBounds,logo:rect(document.querySelector('.logo')),badge:rect(document.querySelector('.badge')),emblem:rect(document.querySelector('.emblem')),mark:rect(document.querySelector('.mark')),latoLoaded:document.fonts.check('700 40px AcademyLato'),fonts:[...document.fonts].map(f=>({family:f.family,status:f.status})),canvas:{width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight}};
    },{titleLines:data.title_lines});
    assert.ok(layout.latoLoaded&&layout.fonts.every(f=>f.status==='loaded'),`${rel}: fonts failed`);
    assert.deepEqual(layout.canvas,{width:800,height:400});
    assert.deepEqual([layout.logo.left,layout.logo.top,layout.logo.width],[42,26,145]);
    assert.deepEqual([layout.badge.left,layout.badge.top,layout.badge.height],[42,118,28]);
    assert.deepEqual([layout.emblem.left,layout.emblem.top,layout.emblem.width,layout.emblem.height],[528,78,244,244]);
    assert.deepEqual([layout.mark.width,layout.mark.height],[176,176]);
    for(const b of layout.textBounds){
      assert.ok(b.left>=41.5&&b.right<=500.5,`${rel}: text exceeds field: ${b.text}`);
      const [top,bottom]=b.role==='title-line'?[160,307]:b.role==='badge'?[119,145]:[334,386];
      assert.ok(b.top>=top&&b.bottom<=bottom,`${rel}: vertical overflow: ${b.text} (${b.top},${b.bottom})`);
    }
    assert.deepEqual(errors,[],`${rel}: browser errors`);
    // Title fitting changes layout after font readiness. Wait for completed paints
    // and require consecutive identical captures before accepting the raster.
    await page.evaluate(async()=>{await document.fonts.ready;await new Promise(requestAnimationFrame);await new Promise(requestAnimationFrame);});
    const capture=()=>page.screenshot({type:'png',animations:'disabled',clip:{x:0,y:0,width:800,height:400}});
    let png=await capture(),stable=false;
    for(let attempt=0;attempt<3;attempt++){
      const next=await capture();stable=png.equals(next);png=next;if(stable)break;
    }
    assert.ok(stable,`${rel}: poster paint did not stabilize`);
    assert.equal(png.readUInt32BE(16),800);assert.equal(png.readUInt32BE(20),400);
    const target=path.join(dir,'thumbnail.png');
    let rasterComparison={exact:true,changedPixels:0,maxChannelDelta:0};
    if(check){
      const accepted=await fs.readFile(target);
      if(!png.equals(accepted)){
        // Allow only isolated native text-antialias rounding: <=16 of 320,000
        // pixels, each <=16/255 per channel. Structural/text changes still fail.
        rasterComparison=await page.evaluate(async({accepted,rendered})=>{
          async function pixels(data){const im=new Image();im.src='data:image/png;base64,'+data;await im.decode();
            if(im.width!==800||im.height!==400)throw new Error('Accepted poster dimensions changed');
            const c=document.createElement('canvas');c.width=800;c.height=400;const ctx=c.getContext('2d');ctx.drawImage(im,0,0);return ctx.getImageData(0,0,800,400).data;}
          const a=await pixels(accepted),b=await pixels(rendered);let changedPixels=0,maxChannelDelta=0;
          for(let i=0;i<a.length;i+=4){let changed=false;for(let j=0;j<4;j++){const d=Math.abs(a[i+j]-b[i+j]);maxChannelDelta=Math.max(maxChannelDelta,d);changed ||= d!==0;}if(changed)changedPixels++;}
          return {exact:changedPixels===0,changedPixels,maxChannelDelta};
        },{accepted:accepted.toString('base64'),rendered:png.toString('base64')});
        if(rasterComparison.changedPixels>16||rasterComparison.maxChannelDelta>16){
          await fs.writeFile(path.join(qa,rel.replaceAll('/','__')+'-drift.png'),png);
          throw new Error(`${rel}: thumbnail differs from renderer; inspect the drift PNG (${JSON.stringify(rasterComparison)})`);
        }
      }
    }
    else await fs.writeFile(target,png);
    const slug=rel.replaceAll('/','__');
    await fs.writeFile(path.join(qa,slug+'.html'),await page.content());
    await fs.writeFile(path.join(qa,slug+'.png'),png);
    // Rasterize the actual PNG in a browser at both catalog-card sizes.
    await page.setContent(`<style>html,body{margin:0}img{display:block}</style><img src="data:image/png;base64,${png.toString('base64')}" width="400" height="200">`);
    await page.locator('img').evaluate(i=>i.decode());
    await page.screenshot({path:path.join(qa,slug+'-400.png'),clip:{x:0,y:0,width:400,height:200}});
    await page.locator('img').evaluate(i=>{i.width=240;i.height=120;});
    await page.screenshot({path:path.join(qa,slug+'-240.png'),clip:{x:0,y:0,width:240,height:120}});
    reports.push({course:rel,rasterComparison,...layout});
    console.log(`${check?'CHECK':'BUILD'} ${rel} (${layout.titleSize}px)`);
    await page.close();
  }
}finally{await browser.close();}
await fs.writeFile(path.join(qa,'report.json'),JSON.stringify({browser:browser.version(),posters:reports},null,2)+'\n');
const cards=reports.map(r=>{const slug=r.course.replaceAll('/','__');return `<figure><a href="${slug}.html"><img src="${slug}.png" width="400" height="200"></a><figcaption>${escape(r.course)} · ${r.titleSize}px</figcaption></figure>`;}).join('\n');
await fs.writeFile(path.join(qa,'index.html'),`<!doctype html><meta charset="utf-8"><title>OCP Academy posters</title><style>body{background:#e9edf2;font:14px sans-serif;margin:24px}main{display:grid;grid-template-columns:repeat(auto-fit,400px);gap:24px}figure{margin:0}figcaption{max-width:400px;overflow-wrap:anywhere;margin-top:8px}img{display:block}</style><h1>OCP Academy catalog posters</h1><p>${reports.length} posters · fixed layout · click for full size</p><main>${cards}</main>`);
console.log(`PASS: ${reports.length} posters; full-size and reduced previews in ${qa}`);
