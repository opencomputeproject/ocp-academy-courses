const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '..');
const outputDir = path.resolve(root, '..', 'tmp', 'course-slide-qa');
const course = JSON.parse(fs.readFileSync(path.join(root, 'course.json'), 'utf8'));
const targets = [
  { module: 1, slide: 3, media: 'video' },
  { module: 2, slide: 3, media: 'image' },
  { module: 2, slide: 6, media: 'video' },
  { module: 3, slide: 5, media: 'video' },
  { module: 4, slide: 6, media: 'video' },
  { module: 4, slide: 8, media: 'video' },
];

(async () => {
  fs.mkdirSync(outputDir, { recursive: true });
  const browser = await chromium.launch({ headless: true, args: ['--mute-audio', '--allow-file-access-from-files'] });
  const results = [];
  const ungatedResults = [];
  try {
    for (const target of targets) {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.goto(pathToFileURL(path.join(root, `module${target.module}.html`)).href, { waitUntil: 'load' });
      const skipIntro = page.locator('#ocpMotionIntroSkip');
      if (await skipIntro.count()) {
        await skipIntro.click();
        await page.waitForTimeout(800);
      }
      for (let step = 1; step < target.slide; step++) {
        await page.keyboard.press('ArrowRight');
        await page.waitForTimeout(40);
      }
      await page.waitForTimeout(900);
      const inspection = await page.evaluate(({ slide, media }) => {
        const active = document.querySelector(`.slide[data-slide="${slide}"]`);
        const node = active.querySelector(media === 'video' ? 'video.figure-video' : '.figure-panel img');
        const rect = node.getBoundingClientRect();
        const panel = node.closest('.figure-panel').getBoundingClientRect();
        const base = {
          slideTitle: active.querySelector('h1,h2')?.textContent?.trim(),
          media,
          viewport: { width: innerWidth, height: innerHeight },
          rect: { left: rect.left, right: rect.right, top: rect.top, bottom: rect.bottom, width: rect.width, height: rect.height },
          panel: { left: panel.left, right: panel.right, top: panel.top, bottom: panel.bottom },
          horizontalOverflow: rect.left < -0.5 || rect.right > innerWidth + 0.5,
          panelOverflow: rect.left < panel.left - 1 || rect.right > panel.right + 1,
        };
        if (media === 'video') {
          Object.assign(base, {
            muted: node.muted,
            loop: node.loop,
            autoplay: node.autoplay,
            paused: node.paused,
            currentTime: node.currentTime,
            videoWidth: node.videoWidth,
            videoHeight: node.videoHeight,
          });
        } else {
          Object.assign(base, { naturalWidth: node.naturalWidth, naturalHeight: node.naturalHeight, complete: node.complete });
        }
        return base;
      }, target);
      inspection.module = target.module;
      inspection.slide = target.slide;
      inspection.errors = errors;
      results.push(inspection);
      await page.screenshot({ path: path.join(outputDir, `module${target.module}-slide${target.slide}.png`), type: 'png' });
      await page.close();
    }
    for (const module of course.modules) {
      const quiz = module.slides.find(slide => slide.type === 'knowledge_check');
      if (!quiz) continue;
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
      await page.goto(pathToFileURL(path.join(root, `module${module.id}.html`)).href, { waitUntil: 'load' });
      const skipIntro = page.locator('#ocpMotionIntroSkip');
      if (await skipIntro.count()) {
        await skipIntro.click();
        await page.waitForTimeout(800);
      }
      for (let step = 1; step <= quiz.id; step++) {
        await page.keyboard.press('ArrowRight');
        await page.waitForTimeout(40);
      }
      const activeSlide = await page.locator('.slide.active').getAttribute('data-slide');
      ungatedResults.push({ module: module.id, quizSlide: quiz.id, activeSlide: Number(activeSlide), passed: Number(activeSlide) === quiz.id + 1 });
      await page.close();
    }
  } finally {
    await browser.close();
  }
  process.stdout.write(`${JSON.stringify({ mediaResults: results, ungatedResults }, null, 2)}\n`);
  const failed = results.some(item => item.horizontalOverflow || item.panelOverflow || item.errors.length || (item.media === 'video' && (!item.muted || !item.loop || !item.autoplay || item.videoWidth !== 1280 || item.videoHeight !== 720)) || (item.media === 'image' && (!item.complete || !item.naturalWidth))) || ungatedResults.some(item => !item.passed);
  if (failed) process.exitCode = 2;
})().catch(error => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exit(1);
});
