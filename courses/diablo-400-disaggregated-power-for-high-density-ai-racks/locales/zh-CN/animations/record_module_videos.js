const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const workDir = __dirname;
const outputDir = path.resolve(workDir, '..', 'figures');
const specs = [
  {
    html: 'module1_current_loss.html',
    video: 'current_copper_loss.webm',
    poster: 'current_copper_loss_poster.png'
  },
  {
    html: 'module3_interface_path.html',
    video: 'serviceable_interface_path.webm',
    poster: 'serviceable_interface_path_poster.png'
  },
  {
    html: 'module4_coordinated_lvdc.html',
    video: 'coordinated_lvdc_response.webm',
    poster: 'coordinated_lvdc_response_poster.png'
  }
];

function playwrightFfmpegPath() {
  const cacheRoot = path.join(os.homedir(), 'Library', 'Caches', 'ms-playwright');
  const ffmpegDir = fs.readdirSync(cacheRoot).find((name) => name.startsWith('ffmpeg-'));
  if (!ffmpegDir) throw new Error('Playwright ffmpeg runtime was not found.');
  return path.join(cacheRoot, ffmpegDir, 'ffmpeg-mac');
}

async function recordOne(browser, spec) {
  const htmlPath = path.join(workDir, spec.html);
  const videoPath = path.join(outputDir, spec.video);
  const posterPath = path.join(outputDir, spec.poster);
  const rawPath = path.join(workDir, `${path.parse(spec.video).name}_raw.webm`);
  if (process.env.POSTERS_ONLY !== '1') {
    const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
    await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'load' });
    const bytes = await page.evaluate(() => window.captureAnimation());
    fs.writeFileSync(rawPath, Buffer.from(bytes));
    execFileSync(playwrightFfmpegPath(), ['-y', '-i', rawPath, '-c:v', 'copy', videoPath], { stdio: 'ignore' });
    fs.rmSync(rawPath);
    await page.close();
  }

  const posterPage = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  await posterPage.goto(pathToFileURL(htmlPath).href + '?poster=1', { waitUntil: 'load' });
  await posterPage.evaluate(() => {
    if (window.__previewFrame) cancelAnimationFrame(window.__previewFrame);
    window.renderFrame(window.__posterTimeMs);
  });
  await posterPage.waitForTimeout(150);
  await posterPage.locator('#scene').screenshot({ path: posterPath });
  await posterPage.close();
  return { videoPath, posterPath, bytes: fs.statSync(videoPath).size };
}

(async () => {
  fs.mkdirSync(outputDir, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const selectedSpecs = process.env.VIDEO_FILTER
    ? specs.filter((spec) => spec.video.includes(process.env.VIDEO_FILTER))
    : specs;
  const results = [];
  for (const spec of selectedSpecs) results.push(await recordOne(browser, spec));
  await browser.close();
  console.log(JSON.stringify(results));
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
