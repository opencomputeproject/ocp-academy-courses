import assert from 'node:assert/strict';
import { storyboards, createHtml } from './storyboards.mjs';

const { chromium } = await import(process.env.PLAYWRIGHT_MODULE || 'playwright');
const browser = await chromium.launch({ headless: true, ...(process.env.PLAYWRIGHT_CHANNEL ? { channel: process.env.PLAYWRIGHT_CHANNEL } : {}) });
try {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  for (const item of storyboards) {
    await page.goto('about:blank');
    await page.setContent(createHtml(item));
    const report = await page.evaluate(({ duration, slide, finalTime }) => {
      const errors = [];
      let dots = 0, shortDots = 0;
      const curves = {};
      for (let frame = 0; frame <= Math.round(duration * 30); frame++) {
        const t = frame / 30;
        window.setAcademyVideoTime(t);
        const svg = document.querySelector('#scene');
        const counts = new Map();
        for (const dot of svg.querySelectorAll('[data-motion-path]')) {
          const id = dot.dataset.motionPath;
          const path = svg.querySelector(`#${id}`);
          const key = [id, dot.getAttribute('stroke'), dot.dataset.motionStart || '0'].join(':');
          counts.set(key, (counts.get(key) || 0) + 1);
          const radius = Number(dot.getAttribute('r'));
          const outerRadius = radius + Number(dot.getAttribute('stroke-width')) / 2;
          const inset = outerRadius + 2;
          const length = path.getTotalLength();
          const start = Number(dot.dataset.motionStart || 0);
          const stop = dot.dataset.motionEnd ? Math.min(length, Number(dot.dataset.motionEnd)) : length;
          const distance = start + inset + Number(dot.dataset.motionProgress) * (stop - start - 2 * inset);
          const expected = path.getPointAtLength(distance);
          const center = new DOMPoint(Number(dot.getAttribute('cx')), Number(dot.getAttribute('cy')));
          if (Math.hypot(center.x - expected.x, center.y - expected.y) > 0.001 || !path.isPointInStroke(center)) errors.push(`${t}: ${id} leaves the shaft centerline`);
          if (distance - start < outerRadius + 1 || stop - distance < outerRadius + 1) errors.push(`${t}: ${id} covers an endpoint, pump, or arrowhead`);
          if (t >= finalTime) errors.push(`${t}: marker remains in the conclusion`);
          if (stop - start < 100) {
            shortDots++;
            if (radius > (slide === 'M1S4' ? 5 : 6) || 2 * outerRadius >= (stop - start) / 2) errors.push(`${t}: short connector marker is too large`);
          }
          let curve;
          if (id === 'nested-to-rejection' && center.y > 650 && center.y < 771.9) curve = 'rejection bend';
          if (id === 'controlled-return' && center.y > 760.1 && center.y < 789.9) curve = center.x > 1000 ? 'right liquid-return bend' : 'left liquid-return bend';
          if (id === 'purging-return' && center.y > 660.1 && center.y < 689.9) curve = center.x > 1000 ? 'right liquid-return bend' : 'left liquid-return bend';
          if (id === 'purging-port' && center.y > 720.1 && center.y < 749.9) curve = 'purge-route bend';
          if (curve) curves[curve] = (curves[curve] || 0) + 1;
          dots++;
        }
        for (const [key, count] of counts) {
          const expected = /^(controlled-return|purging-return|purging-port):/.test(key) ? 3 : 1;
          if (count !== expected) errors.push(`${t}: ${key} has ${count} simultaneous dots (expected ${expected})`);
        }
      }
      return { frames: Math.round(duration * 30) + 1, dots, shortDots, curves, errors };
    }, { duration: item.duration, slide: item.slide, finalTime: item.cues.at(-1)[0] });
    assert.deepEqual(report.errors, []);
    assert.ok(report.shortDots > 100);
    const expectedCurves = item.slide === 'M1S4' ? 1 : item.slide === 'M2S5' ? 2 : 3;
    assert.equal(Object.keys(report.curves).length, expectedCurves);
    for (const count of Object.values(report.curves)) assert.ok(count > 5);
    console.log(`${item.slide}: ${report.frames} frames, ${report.dots} exact-path positions; marker counts, sizes, and endpoint/pump clearance passed. Curves: ${JSON.stringify(report.curves)}`);
  }
} finally {
  await browser.close();
}
