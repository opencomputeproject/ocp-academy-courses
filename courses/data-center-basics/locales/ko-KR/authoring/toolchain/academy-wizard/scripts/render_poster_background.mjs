#!/usr/bin/env node
// Rebuild the fixed catalog shell after intentional edits to background.svg.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const {Resvg}=createRequire(import.meta.url)('@resvg/resvg-js');
const folder=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../templates/poster');
const svg=await fs.readFile(path.join(folder,'background.svg'),'utf8');
await fs.writeFile(path.join(folder,'background.png'),new Resvg(svg).render().asPng());
console.log('Rendered shared 800×400 poster background. Rebuild the catalog next.');
