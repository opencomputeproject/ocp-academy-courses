const { chromium } = require('playwright');
const fs = require('fs');
const os = require('os');
const path = require('path');

const [htmlName, outputName, durationArg] = process.argv.slice(2);
if (!htmlName || !outputName || !durationArg) {
  throw new Error('Usage: node render_animation.js <html> <output.webm> <duration-ms>');
}

(async () => {
  const workDir = __dirname;
  const captureDir = fs.mkdtempSync(path.join(os.tmpdir(), 'academy-animation-'));
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    recordVideo: {
      dir: captureDir,
      size: { width: 1280, height: 720 }
    }
  });
  const page = await context.newPage();
  await page.goto(`file://${path.join(workDir, htmlName)}`);
  await page.waitForTimeout(Number(durationArg) + 700);
  const video = page.video();
  await context.close();
  const capturedPath = await video.path();
  fs.copyFileSync(capturedPath, path.join(workDir, outputName));
  await browser.close();
  fs.rmSync(captureDir, { recursive: true, force: true });
})();
