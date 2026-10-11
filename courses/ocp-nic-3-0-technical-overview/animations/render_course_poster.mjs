import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';

const root=path.resolve(import.meta.dirname,'..');
const source=await fs.readFile(path.join(root,'animations/course_poster.svg'),'utf8');
const skill=process.env.ACADEMY_WIZARD_SKILL_DIR||path.resolve(root,'../../skills/academy-wizard');
const logo=await fs.readFile(path.join(skill,'assets/ocp_academy_white.svg'));
const svg=source.replace('ACADEMY_LOGO_DATA_URI',`data:image/svg+xml;base64,${logo.toString('base64')}`);
const out=path.join(root,'thumbnail.png');
await sharp(Buffer.from(svg)).png().toFile(out);
const metadata=await sharp(out).metadata();
if(metadata.width!==800||metadata.height!==400||metadata.format!=='png') throw new Error('Poster must be an 800 x 400 PNG');
const review=path.join(root,'animation-qa');
await fs.mkdir(review,{recursive:true});
await sharp(out).resize(400,200).png().toFile(path.join(review,'poster_400.png'));
await sharp(out).resize(240,120).png().toFile(path.join(review,'poster_240.png'));
console.log(`Rendered ${out} and two LMS-card previews.`);
