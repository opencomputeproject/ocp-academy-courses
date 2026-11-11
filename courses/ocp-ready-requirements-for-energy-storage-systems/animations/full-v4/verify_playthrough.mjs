import path from 'node:path';
import { pathToFileURL } from 'node:url';
import assert from 'node:assert/strict';
import { here, editionRoot, readJSON, writeJSON, option, chromium, sha256 } from './lib.mjs';

const locale = option('--locale') || 'en-US';
const manifest = await readJSON(path.join(here, 'figure-patch-manifest.json'));
const items = Object.entries(manifest.editions[locale].figures).filter(([id, item]) => item.encoded && (!option('--slide') || option('--slide') === id));
assert(items.length, 'No matching encoded videos');
for (const [, item] of items) assert.equal(await sha256(path.join(editionRoot(locale), item.figure.path)), item.encoded.sha256, 'Video changed before playback check');
const browser = await (await chromium()).launch({ headless: true, args: ['--mute-audio'] });
try {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto(pathToFileURL(path.join(editionRoot(locale), items[0][1].source_html)).href);
  const results = await page.evaluate(async inputs => {
    document.body.replaceChildren();
    return Promise.all(inputs.map(async ({ id, url, expected, digest, independentLoop }) => {
      const video = document.createElement('video');
      video.muted = true; video.loop = false; video.playbackRate = 1; video.preload = 'auto';
      video.style.cssText = 'width:480px;height:270px;background:white';
      document.body.appendChild(video); video.src = url;
      await new Promise((resolve, reject) => { video.onloadeddata = resolve; video.onerror = () => reject(new Error(`Cannot load ${id}`)); });
      let last = 0, reversals = 0, samples = 0;
      const poll = setInterval(() => { if (video.currentTime < last - 0.001) reversals++; last = video.currentTime; samples++; }, 100);
      await video.play();
      await new Promise((resolve, reject) => {
        const timeout = setTimeout(() => reject(new Error(`${id} did not finish in real time`)), (expected + 30) * 1000);
        video.onended = () => { clearTimeout(timeout); resolve(); };
      });
      clearInterval(poll);
      const ending = video.currentTime;
      await new Promise(resolve => setTimeout(resolve, 1200));
      const result = { id, video_sha256: digest, duration: video.duration, ended: video.ended, paused: video.paused, muted: video.muted, rate: video.playbackRate, samples, reversals, final_time: video.currentTime, final_hold_stable: video.currentTime === ending, expected };
      if (independentLoop) {
        video.loop = true; video.currentTime = expected - .5;
        await video.play();
        await new Promise(resolve => setTimeout(resolve, 1500));
        result.independent_loop_boundary = video.loop && !video.paused && video.currentTime > 0 && video.currentTime < 3;
        video.pause();
      }
      return result;
    }));
  }, items.map(([id, item]) => ({ id, url: pathToFileURL(path.join(editionRoot(locale), item.figure.path)).href, expected: item.encoded.duration, digest: item.encoded.sha256, independentLoop: item.figure.loop })));
  for (const result of results) {
    assert(result.ended && result.paused && result.muted && result.final_hold_stable && result.reversals === 0, JSON.stringify(result));
    assert(Math.abs(result.duration - result.expected) < .034);
    if (result.id === 'M4S8') assert(result.independent_loop_boundary, 'Independent loop did not cross its boundary');
  }
  await writeJSON(path.join(here, 'qa', locale, 'muted-playthrough.json'), { results, scope: 'Real-time standalone media decoding at 1x, one complete finite pass, plus 1.2-second ending hold; retained loops also cross a loop boundary. This does not establish integrated player or LMS behavior.', human_audio_review: 'pending' });
  console.log(`${locale}: ${results.length} complete muted 1x playthroughs passed`);
} finally { await browser.close(); }
