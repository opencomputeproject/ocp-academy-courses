import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
import os from 'node:os';
import fs from 'node:fs/promises';
import { existsSync, readdirSync } from 'node:fs';
import { spawn, spawnSync } from 'node:child_process';
import { once } from 'node:events';

const [htmlPath, outputPath, posterPath, durationArg = '', posterArg = '', fpsArg = '30'] = process.argv.slice(2);
if (!htmlPath || !outputPath || !posterPath) {
  throw new Error('usage: record_animation.mjs <html> <output.mp4|output.webm> <poster.png> [duration_ms] [poster_ms] [fps]');
}

function supportsEncoder(candidate, encoderName) {
  const result = spawnSync(candidate, ['-hide_banner', '-encoders'], { encoding: 'utf8' });
  return result.status === 0 && `${result.stdout}\n${result.stderr}`.includes(encoderName);
}

function findFfmpeg(encoderName) {
  const candidates = [];
  if (process.env.FFMPEG_BIN) candidates.push(process.env.FFMPEG_BIN);
  candidates.push(
    'ffmpeg',
    '/Applications/Logi Tune.app/Contents/Resources/ffmpeg/ffmpeg',
  );
  const roots = [
    path.join(os.homedir(), 'Library', 'Caches', 'ms-playwright'),
    path.join(os.homedir(), '.cache', 'ms-playwright'),
  ];
  for (const root of roots) {
    if (!existsSync(root)) continue;
    const folders = readdirSync(root).filter((name) => name.startsWith('ffmpeg-')).sort().reverse();
    for (const folder of folders) {
      for (const binary of ['ffmpeg-mac', 'ffmpeg-linux', 'ffmpeg']) {
        const candidate = path.join(root, folder, binary);
        if (existsSync(candidate)) candidates.push(candidate);
      }
    }
  }
  for (const candidate of candidates) {
    if (supportsEncoder(candidate, encoderName)) return candidate;
  }
  throw new Error(`no ffmpeg build with ${encoderName} is available; set FFMPEG_BIN to a full ffmpeg build`);
}

async function setAnimationTime(page, milliseconds) {
  await page.evaluate((time) => {
    for (const animation of document.getAnimations()) {
      animation.pause();
      animation.currentTime = time;
    }
  }, milliseconds);
}

const fps = Number(fpsArg);
if (!Number.isFinite(fps) || fps <= 0) throw new Error(`invalid fps: ${fpsArg}`);
const renderScale = Number(process.env.ACADEMY_ANIMATION_SCALE || 1);
if (!Number.isFinite(renderScale) || renderScale < 1 || renderScale > 3) {
  throw new Error(`invalid ACADEMY_ANIMATION_SCALE: ${process.env.ACADEMY_ANIMATION_SCALE}`);
}
await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.mkdir(path.dirname(posterPath), { recursive: true });

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: renderScale });
await page.goto(pathToFileURL(path.resolve(htmlPath)).href, { waitUntil: 'load' });
await page.evaluate(() => Promise.race([
  document.fonts?.ready || Promise.resolve(),
  new Promise((resolve) => setTimeout(resolve, 5000)),
]));

const declared = await page.evaluate(() => ({
  durationMs: Number(document.body.dataset.durationMs || 0),
  posterMs: Number(document.body.dataset.posterMs || 0),
  infiniteAnimations: document.getAnimations().filter((animation) => !Number.isFinite(Number(animation.effect.getTiming().iterations))).length,
  animationEndMs: Math.max(0, ...document.getAnimations().map((animation) => Number(animation.effect.getComputedTiming().endTime || 0))),
}));
if (declared.infiniteAnimations > 0) {
  throw new Error(`source contains ${declared.infiniteAnimations} infinite animation(s); teaching videos must use a finite one-pass master timeline`);
}
const durationMs = Number(durationArg || declared.durationMs || declared.animationEndMs);
const posterMs = Number(posterArg || declared.posterMs || Math.round(durationMs * 0.75));
if (!Number.isFinite(durationMs) || durationMs <= 0) throw new Error('animation duration is missing or invalid');

await setAnimationTime(page, 0);
const extension = path.extname(outputPath).toLowerCase();
const isMp4 = extension === '.mp4' || extension === '.m4v';
const isWebm = extension === '.webm';
if (!isMp4 && !isWebm) throw new Error(`unsupported video extension: ${extension}`);
const encoderName = isMp4 ? 'libx264' : 'libvpx-vp9';
const ffmpeg = findFfmpeg(encoderName);
const codecArgs = isMp4
  ? [
      '-c:v', 'libx264',
      '-preset', 'slow',
      '-tune', 'animation',
      '-crf', '8',
      '-pix_fmt', 'yuv420p',
      '-color_primaries', 'bt709',
      '-color_trc', 'bt709',
      '-colorspace', 'bt709',
      '-movflags', '+faststart',
    ]
  : [
      '-c:v', 'libvpx-vp9',
      '-b:v', '0',
      '-crf', '12',
      '-deadline', 'good',
      '-cpu-used', '2',
      '-row-mt', '1',
      '-pix_fmt', 'yuv420p',
    ];
const encoder = spawn(ffmpeg, [
  '-y',
  '-f', 'image2pipe',
  '-vcodec', 'png',
  '-framerate', String(fps),
  '-i', 'pipe:0',
  '-an',
  ...codecArgs,
  outputPath,
], { stdio: ['pipe', 'ignore', 'pipe'] });

let encoderErrors = '';
encoder.stderr.on('data', (chunk) => { encoderErrors += chunk.toString(); });
const encoderClosed = once(encoder, 'close');
const frameCount = Math.round((durationMs / 1000) * fps);
for (let frame = 0; frame < frameCount; frame += 1) {
  const time = Math.min(durationMs - (1000 / fps), frame * (1000 / fps));
  await setAnimationTime(page, time);
  const png = await page.screenshot({ type: 'png' });
  if (!encoder.stdin.write(png)) await once(encoder.stdin, 'drain');
}
encoder.stdin.end();
const [exitCode] = await encoderClosed;
if (exitCode !== 0) throw new Error(`ffmpeg exited ${exitCode}: ${encoderErrors.slice(-3000)}`);

const safePosterMs = Math.max(0, Math.min(durationMs - (1000 / fps), posterMs));
await setAnimationTime(page, safePosterMs);
await page.screenshot({ path: posterPath, type: 'png' });
await browser.close();

console.log(`encoded ${path.basename(outputPath)}: ${frameCount} frames, ${(frameCount / fps).toFixed(3)}s at ${fps} fps, ${1920 * renderScale}x${1080 * renderScale} ${encoderName}`);
console.log(`poster ${path.basename(posterPath)}: ${(safePosterMs / 1000).toFixed(3)}s`);
