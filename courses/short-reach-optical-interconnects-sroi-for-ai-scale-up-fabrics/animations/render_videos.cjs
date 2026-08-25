const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { spawn } = require('child_process');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const QA_DIR = path.resolve(ROOT, '..', 'tmp', 'video-qa');
const FFMPEG = '/Applications/Logi Tune.app/Contents/Resources/ffmpeg/ffmpeg';
const FPS = 24;
const CLEARANCE = 12;

const animations = [
  { name: 'scale_up_bottleneck', duration: 22, poster: 0.57 },
  { name: 'optical_placement', duration: 22, poster: 0.72 },
  { name: 'retry_tax', duration: 24, poster: 0.72 },
  { name: 'optical_circuit_switching', duration: 22, poster: 0.72 },
  { name: 'slow_wide_wdm', duration: 20, poster: 0.64 },
];

const mode = process.argv.includes('--encode') ? 'encode' : 'qa';
const requested = process.argv.find(arg => arg.startsWith('--only='));
const selected = requested
  ? animations.filter(item => item.name === requested.slice('--only='.length))
  : animations;

if (!selected.length) {
  throw new Error('No animation matched --only.');
}

function waitForDrain(stream) {
  return new Promise(resolve => stream.once('drain', resolve));
}

function waitForExit(child) {
  return new Promise((resolve, reject) => {
    let stderr = '';
    child.stderr.on('data', chunk => { stderr += chunk.toString(); });
    child.on('error', reject);
    child.on('close', code => code === 0 ? resolve() : reject(new Error(`ffmpeg exited ${code}: ${stderr}`)));
  });
}

async function loadPage(browser, item) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  const input = path.join(__dirname, `${item.name}.html`);
  await page.goto(pathToFileURL(input).href, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  if (!(await page.evaluate(() => typeof window.setAnimationTime === 'function'))) {
    throw new Error(`${item.name} does not expose window.setAnimationTime(t).`);
  }
  return page;
}

async function containmentFlags(page, item, t) {
  await page.evaluate(value => window.setAnimationTime(value), t);
  return page.evaluate(({ clearance, animation, time }) => {
    const flags = [];
    const groups = [...document.querySelectorAll('[data-box]')];
    groups.forEach((group, groupIndex) => {
      const bound = group.querySelector('[data-bound]');
      if (!bound) return;
      const b = bound.getBoundingClientRect();
      [...group.querySelectorAll('text')].forEach((node, textIndex) => {
        const r = node.getBoundingClientRect();
        const gaps = {
          left: r.left - b.left,
          right: b.right - r.right,
          top: r.top - b.top,
          bottom: b.bottom - r.bottom,
        };
        const minGap = Math.min(gaps.left, gaps.right, gaps.top, gaps.bottom);
        if (minGap < clearance) {
          flags.push({ animation, time, groupIndex, textIndex, text: node.textContent.trim(), minGap: Number(minGap.toFixed(1)), gaps });
        }
      });
    });
    return flags;
  }, { clearance: CLEARANCE, animation: item.name, time: t });
}

async function renderQa(browser, item) {
  const page = await loadPage(browser, item);
  const times = [
    { label: 'start', t: 0.02 },
    { label: 'middle', t: item.poster },
    { label: 'end', t: 0.97 },
  ];
  const flags = [];
  for (const { label, t } of times) {
    flags.push(...await containmentFlags(page, item, t));
    await page.screenshot({ path: path.join(QA_DIR, `${item.name}-${label}.png`), type: 'png' });
  }
  await page.close();
  if (flags.length) {
    process.stderr.write(`${item.name}: text containment flags\n${JSON.stringify(flags, null, 2)}\n`);
  } else {
    process.stdout.write(`${item.name}: 12 px text containment passed at start, middle, and end.\n`);
  }
  return flags;
}

async function encode(browser, item) {
  const page = await loadPage(browser, item);
  const output = path.join(ROOT, 'figures', `${item.name}_motion.mp4`);
  const poster = path.join(ROOT, 'figures', `${item.name}_motion_poster.png`);
  await page.evaluate(value => window.setAnimationTime(value), item.poster);
  await page.screenshot({ path: poster, type: 'png' });

  const ffmpeg = spawn(FFMPEG, [
    '-hide_banner', '-loglevel', 'error',
    '-f', 'image2pipe', '-framerate', String(FPS), '-vcodec', 'png', '-i', '-',
    '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-y', output,
  ], { stdio: ['pipe', 'ignore', 'pipe'] });
  const exitPromise = waitForExit(ffmpeg);
  const totalFrames = Math.round(item.duration * FPS);
  let nextReport = 0;
  for (let frame = 0; frame < totalFrames; frame++) {
    const t = frame / (totalFrames - 1);
    await page.evaluate(value => window.setAnimationTime(value), t);
    const png = await page.screenshot({ type: 'png' });
    if (!ffmpeg.stdin.write(png)) await waitForDrain(ffmpeg.stdin);
    const percent = Math.floor((frame + 1) * 100 / totalFrames);
    if (percent >= nextReport) {
      process.stdout.write(`${item.name}: ${percent}%\n`);
      nextReport += 10;
    }
  }
  ffmpeg.stdin.end();
  await exitPromise;
  await page.close();
  process.stdout.write(`${item.name}: wrote ${path.basename(output)} and poster.\n`);
}

(async () => {
  fs.mkdirSync(QA_DIR, { recursive: true });
  const browser = await chromium.launch({ headless: true, args: ['--allow-file-access-from-files', '--mute-audio'] });
  try {
    if (mode === 'qa') {
      let flags = [];
      for (const item of selected) flags = flags.concat(await renderQa(browser, item));
      if (flags.length) process.exitCode = 2;
    } else {
      for (const item of selected) await encode(browser, item);
    }
  } finally {
    await browser.close();
  }
})().catch(error => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exit(1);
});
