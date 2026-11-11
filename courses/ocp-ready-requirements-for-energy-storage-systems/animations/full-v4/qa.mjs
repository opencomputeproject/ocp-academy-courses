import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
import { chromium, here, repoRoot, locales, editionRoot, readJSON, writeJSON, run } from './lib.mjs';
import { withLock } from './locks.mjs';

export async function qa({ selectedLocales = locales, selectedScenes, screenshots = true } = {}) {
  const manifest = await readJSON(path.join(here, 'figure-patch-manifest.json'));
  const report = [];
  const browser = await (await chromium()).launch({ headless: true, args: ['--mute-audio'] });
  try {
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
    const errors = [];
    page.on('pageerror', error => errors.push(String(error)));
    for (const locale of selectedLocales) {
      for (const [id, item] of Object.entries(manifest.editions[locale].figures)) {
        if (selectedScenes && !selectedScenes.includes(id)) continue;
        const root = editionRoot(locale);
        await page.setViewportSize({ width: 1920, height: 1080 });
        await page.goto(pathToFileURL(path.join(root, item.source_html)).href);
        await page.evaluate(() => document.fonts.ready);
        assert.equal(errors.length, 0, errors.join('\n'));
        const duration = item.timing.duration_ms;
        await page.evaluate(t => window.setTeachingTime(t), duration);
        const info = await page.evaluate(() => window.animationQA());
        assert(info.timeline_end_ms <= duration - 1500, `${locale}/${id}: insufficient final hold`);
        for (const box of info.boxes) {
          const b = box.bbox, c = box.clearance - 1;
          assert(b.x >= box.x + c && b.y >= box.y + c && b.x + b.width <= box.x + box.width - c && b.y + b.height <= box.y + box.height - c, `${locale}/${id} 0.75em clearance: ${box.text} ${JSON.stringify(box)}`);
        }
        // Generate a fully materialized SVG, so maintained geometry QA does not miss JS-created nodes.
        const svg = await page.locator('svg').evaluate(el => el.outerHTML);
        const geometry = path.join(root, item.geometry_snapshot);
        await fs.writeFile(geometry, svg + '\n');
        run('python3', [path.join(repoRoot, 'skills/academy-wizard/scripts/check_svg_arrows.py'), geometry, '--fail-on-flags']);
        const dir = path.join(here, 'qa', locale, id);
        await fs.mkdir(dir, { recursive: true });
        const times = [...new Set([0, duration * .25, duration * .5, duration * .75, duration - 1000 / 30, ...info.transitions.flatMap(t => [Math.max(0, t - 34), Math.min(duration - 34, t + 34)])].map(Math.round))].sort((a, b) => a - b);
        for (const time of times) {
          await page.evaluate(t => window.setTeachingTime(t), time);
          if (screenshots) await page.screenshot({ path: path.join(dir, `${String(time).padStart(7, '0')}ms.png`) });
        }
        await page.evaluate(t => window.setTeachingTime(t), duration);
        const ending = await page.locator('svg').evaluate(el => el.outerHTML);
        await page.evaluate(t => window.setTeachingTime(t), duration + 10000);
        assert.equal(await page.locator('svg').evaluate(el => el.outerHTML), ending, 'Source must clamp, not wrap');
        await page.evaluate(t => window.setTeachingTime(t), duration - 1000);
        assert.equal(await page.locator('svg').evaluate(el => el.outerHTML), ending, 'Final second must be stable');
        if (screenshots) await page.screenshot({ path: path.join(root, item.figure.poster) });
        // Exercise non-monotonic seeks and a complete deterministic 30 fps pass without expensive captures.
        const continuity = await page.evaluate(({ duration }) => {
          let previous = [];
          let reversals = 0;
          for (let t = 0; t <= duration; t += 1000 / 30) {
            window.setTeachingTime(t);
            const values = [...document.querySelectorAll('[opacity]')].map(el => +el.getAttribute('opacity'));
            if (values.some((v, i) => v < (previous[i] || 0))) reversals++;
            previous = values;
          }
          window.setTeachingTime(0); window.setTeachingTime(duration / 2); window.setTeachingTime(0); window.setTeachingTime(duration);
          return reversals;
        }, { duration });
        assert.equal(continuity, 0, `${locale}/${id}: unexplained reveal reversal`);
        await page.setViewportSize({ width: 390, height: 220 });
        if (screenshots) await page.screenshot({ path: path.join(dir, 'mobile-final.png') });
        report.push({ locale, scene: id, source: item.source_html, timing_mode: item.timing.mode, clearance: 'pass', geometry: 'pass', final_second: 'stable', overrun: 'clamped', reveal_continuity: 'pass', sampled_frames: times.length, native_resolution: '1920x1080', mobile: '390x220', encoded_video_review: 'pending' });
        console.log(`${locale}/${id}: geometry, clearance, continuity, hold passed; ${times.length} frames`);
      }
    }
  } finally { await browser.close(); }
  const reportPath = path.join(here, 'qa', 'source-qa-report.json');
  await withLock('qa-report', async () => {
    let previous = [];
    try { previous = await readJSON(reportPath); } catch {}
    const merged = new Map(previous.map(row => [`${row.locale}/${row.scene}`, row]));
    report.forEach(row => merged.set(`${row.locale}/${row.scene}`, row));
    await writeJSON(reportPath, [...merged.values()]);
  }, 60000);
  return report;
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2), val = flag => args.includes(flag) ? args[args.indexOf(flag) + 1] : undefined;
  await qa({ selectedLocales: val('--locale') ? [val('--locale')] : locales, selectedScenes: val('--slide') ? [val('--slide')] : undefined, screenshots: !args.includes('--no-screenshots') });
}
