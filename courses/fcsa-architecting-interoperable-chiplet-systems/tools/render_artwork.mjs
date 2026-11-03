import fs from 'node:fs/promises';import path from 'node:path';import{createRequire}from'node:module';
const sharp=createRequire(import.meta.url)(process.env.SHARP_MODULE||'sharp');
const root=process.cwd(),work=path.join(root,'audit/static-figures');await fs.mkdir(work,{recursive:true});
for(const f of (await fs.readdir(path.join(root,'figures'))).filter(x=>x.endsWith('.svg'))){await sharp(path.join(root,'figures',f),{density:72}).png().toFile(path.join(work,f.replace('.svg','.png')));}
const {spawnSync}=await import('node:child_process');
const result=spawnSync('python3',[path.join(root,'tools/create_poster.py')],{stdio:'inherit'});
if(result.error)throw result.error;if(result.status!==0)throw new Error('Poster render failed');
