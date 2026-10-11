const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const sourceDir = path.resolve(process.argv[2] || '.');
const htmlPath = path.join(sourceDir, 'animation.html');
const framesDir = path.resolve(process.argv[3] || path.join('/tmp', `${path.basename(sourceDir)}_frames`));
const fps = Number(process.env.ANIMATION_FPS || 24);
const duration = Number(process.env.ANIMATION_DURATION || 16);
const frameCount = Math.round(fps * duration);

if (!fs.existsSync(htmlPath)) {
  throw new Error(`Animation source not found: ${htmlPath}`);
}

fs.rmSync(framesDir, { recursive: true, force: true });
fs.mkdirSync(framesDir, { recursive: true });

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: 1280, height: 720 },
    deviceScaleFactor: 1,
  });
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);

  for (let frame = 0; frame < frameCount; frame += 1) {
    const time = frame / fps;
    await page.evaluate((value) => window.renderAt(value), time);
    await page.screenshot({
      path: path.join(framesDir, `frame_${String(frame).padStart(4, '0')}.png`),
      type: 'png',
      animations: 'disabled',
    });
  }

  await browser.close();
  process.stdout.write(`${frameCount} frames rendered to ${framesDir}\n`);
})().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exit(1);
});
