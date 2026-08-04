import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
import fs from 'node:fs/promises';

const [htmlPath, outputPath, posterPath, durationArg='13000', posterArg='9500'] = process.argv.slice(2);
if (!htmlPath || !outputPath || !posterPath) {
  throw new Error('usage: record_animation.mjs <html> <output.webm> <poster.png> [duration_ms] [poster_ms]');
}
const durationMs = Number(durationArg);
const posterMs = Number(posterArg);
await fs.mkdir(path.dirname(outputPath), { recursive: true });
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
  recordVideo: { dir: path.dirname(outputPath), size: { width: 1920, height: 1080 } }
});
const page = await context.newPage();
await page.goto(pathToFileURL(path.resolve(htmlPath)).href, { waitUntil: 'load' });
const video = page.video();
await page.waitForTimeout(durationMs);
await context.close();
await video.saveAs(outputPath);

const posterContext = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const posterPage = await posterContext.newPage();
await posterPage.goto(pathToFileURL(path.resolve(htmlPath)).href, { waitUntil: 'load' });
await posterPage.waitForTimeout(posterMs);
await posterPage.screenshot({ path: posterPath, type: 'png' });
await posterContext.close();
await browser.close();
