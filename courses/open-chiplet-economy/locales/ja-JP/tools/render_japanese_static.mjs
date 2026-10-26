import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const config=path.join(root,'_video_work/fontconfig');
await fs.mkdir(config,{recursive:true});
process.env.FONTCONFIG_FILE=path.join(config,'fonts.conf');
await fs.writeFile(process.env.FONTCONFIG_FILE,`<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd"><fontconfig><dir>${root}/fonts</dir><cachedir>${config}/cache</cachedir></fontconfig>`);
const sharp=createRequire(import.meta.url)(process.env.SHARP_MODULE||'sharp');
const course=JSON.parse(await fs.readFile(path.join(root,'course.json'),'utf8'));
let count=0;
for(const module of course.modules)for(const slide of module.slides){
 const f=slide.figure;
 if(!f?.localized_vector_source)continue;
 await sharp(await fs.readFile(path.join(root,f.localized_vector_source)),{density:96}).png().toFile(path.join(root,f.path));
 count++;
}
console.log(`Rendered ${count} Japanese figures with the bundled Noto Sans JP font.`);
