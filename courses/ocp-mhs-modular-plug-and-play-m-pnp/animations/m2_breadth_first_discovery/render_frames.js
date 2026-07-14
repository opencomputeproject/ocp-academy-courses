const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const sourceDir = __dirname;
const htmlPath = path.join(sourceDir, 'animation.html');
const framesDir = process.argv[2] || path.join('/tmp', 'm2_breadth_first_discovery_frames');
const fps = Number(process.env.ANIMATION_FPS || 24);
const duration = Number(process.env.ANIMATION_DURATION || 16);
const frameCount = Math.round(fps * duration);

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
    const t = frame / fps;
    await page.evaluate((time) => window.renderAt(time), t);
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
