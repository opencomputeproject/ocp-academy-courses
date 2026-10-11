const path = require('path');
const sharp = require('sharp');

(async () => {
  const folder = __dirname;
  const logo = await sharp(path.join(folder, 'academy-logo.svg'))
    .resize({ width: 148, height: 73, fit: 'contain' })
    .png().toBuffer();
  await sharp(path.join(folder, 'thumbnail.svg'))
    .composite([{ input: logo, left: 41, top: 19 }])
    .png()
    .toFile(path.join(folder, '..', 'thumbnail.png'));
})();
