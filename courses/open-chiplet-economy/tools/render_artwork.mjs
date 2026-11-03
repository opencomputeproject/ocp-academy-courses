import {chromium} from 'playwright';import fs from 'node:fs/promises';import path from 'node:path';import {pathToFileURL} from 'node:url';
const root=path.resolve(import.meta.dirname,'..');const browser=await chromium.launch({headless:true,executablePath:process.env.ACADEMY_CHROMIUM_BIN});const p=await browser.newPage({viewport:{width:1200,height:600}});const out=path.join(root,'audit/static-figures');await fs.mkdir(out,{recursive:true});
for(const name of (await fs.readdir(path.join(root,'figures'))).filter(x=>x.endsWith('.svg'))){await p.goto(pathToFileURL(path.join(root,'figures',name)).href);await p.screenshot({path:path.join(out,name+'.png')});}
await browser.close();
const {spawnSync}=await import('node:child_process');
const result=spawnSync('python3',[path.join(root,'tools/create_poster.py')],{stdio:'inherit'});
if(result.error)throw result.error;if(result.status!==0)throw new Error('Poster render failed');
console.log('Rendered diagram review images and shared Academy poster.');
