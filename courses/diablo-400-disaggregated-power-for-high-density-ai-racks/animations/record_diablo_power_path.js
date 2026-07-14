const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const workDir = __dirname;
const htmlPath = path.join(workDir, 'diablo_power_path_animation.html');
const outputDir = path.resolve(workDir, '..', 'figures');
const videoPath = path.join(outputDir, 'ride_through_output_model.webm');
const posterPath = path.join(outputDir, 'ride_through_output_model_poster.png');
const rawVideoPath = path.join(workDir, 'ride_through_output_model_raw.webm');

function playwrightFfmpegPath() {
  const cacheRoot = path.join(os.homedir(), 'Library', 'Caches', 'ms-playwright');
  const ffmpegDir = fs.readdirSync(cacheRoot).find((name) => name.startsWith('ffmpeg-'));
  if (!ffmpegDir) throw new Error('Playwright ffmpeg runtime was not found.');
  return path.join(cacheRoot, ffmpegDir, 'ffmpeg-mac');
}

(async () => {
  fs.mkdirSync(outputDir, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'load' });

  const bytes = await page.evaluate(() => window.captureAnimation());
  fs.writeFileSync(rawVideoPath, Buffer.from(bytes));
  execFileSync(playwrightFfmpegPath(), ['-y', '-i', rawVideoPath, '-c:v', 'copy', videoPath], { stdio: 'ignore' });
  fs.rmSync(rawVideoPath);
  await page.reload({ waitUntil: 'load' });
  await page.evaluate(() => {
    if (window.__previewFrame) cancelAnimationFrame(window.__previewFrame);
    window.renderFrame(6800);
  });
  await page.waitForTimeout(150);
  await page.locator('#scene').screenshot({ path: posterPath });
  await browser.close();

  const stat = fs.statSync(videoPath);
  console.log(JSON.stringify({ videoPath, posterPath, bytes: stat.size }));
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
