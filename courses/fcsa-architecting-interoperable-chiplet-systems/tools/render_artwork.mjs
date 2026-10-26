import fs from 'node:fs/promises';import path from 'node:path';import{createRequire}from'node:module';
const sharp=createRequire(import.meta.url)(process.env.SHARP_MODULE||'sharp');
const root=process.cwd(),work=path.join(root,'audit/static-figures');await fs.mkdir(work,{recursive:true});
for(const f of (await fs.readdir(path.join(root,'figures'))).filter(x=>x.endsWith('.svg'))){await sharp(path.join(root,'figures',f),{density:72}).png().toFile(path.join(work,f.replace('.svg','.png')));}
await sharp(path.join(root,'thumbnail.svg')).png().toFile(path.join(root,'thumbnail.png'));
