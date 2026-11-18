const fs = require('node:fs');
const path = require('node:path');
const sharp = require('sharp');
const dir = process.argv[2];
const timeline = JSON.parse(fs.readFileSync(path.join(dir,'timeline.json'),'utf8'));
(async () => {
  for (const [name] of timeline) {
    const source = path.join(dir, name+'.svg');
    await sharp(source).png({compressionLevel:2}).toFile(path.join(dir,name+'.png'));
  }
})().catch(err=>{console.error(err);process.exitCode=1;});
