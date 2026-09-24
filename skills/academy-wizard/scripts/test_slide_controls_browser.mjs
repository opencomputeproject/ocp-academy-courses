// Disposable browser regression checks; no live LMS, TTS or audible playback.
// Requires Python 3 and Playwright. Run from any directory with Node.js.
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {chromium} from 'playwright';

const scripts = path.dirname(fileURLToPath(import.meta.url));
const skill = path.dirname(scripts);
const tmp = await fs.mkdtemp(path.join(os.tmpdir(), 'academy-slide-controls-'));
const hint = 'La narración comienza automáticamente. Avanza con la flecha.';
const reference = 'https://example.org/spec#page=15';
const render = `import json,sys
sys.path.insert(0,sys.argv[1])
from render_module import render_module
print(render_module(json.load(sys.stdin),0))`;
let checks = 0;
const check = (actual, expected, message) => {
  assert.deepEqual(actual, expected, message); checks++;
};
let browser;
try {
  await fs.copyFile(path.join(skill, 'assets/scorm_api.js'), path.join(tmp, 'scorm_api.js'));
  await fs.writeFile(path.join(tmp, 'module2.html'), '<!doctype html><title>Destination</title>');
  for (const direct of [false, true]) {
    const course = {
      style: 'Slides', course_slug: 'controls-test', course_title: 'Controls test',
      motion_intro: {enabled: false}, ui_labels: {narration_hint: hint},
      scorm: {version: '1.2', organization: 'multi-sco', ...(direct ? {navigation: 'direct'} : {})},
      modules: [{id: 1, title: 'Read and Apply the Voltage Ride-Through Envelope', slides: [
        {id: 1, type: 'title', reference_links: [{label: 'Spec · Table 1 · p. 15', url: reference}]},
        {id: 2, type: 'up_next', next_module_number: 2, next_module_title: 'Destination'}
      ]}]
    };
    const html = execFileSync(process.env.PYTHON || 'python3', ['-c', render, scripts], {
      input: JSON.stringify(course), encoding: 'utf8'
    });
    await fs.writeFile(path.join(tmp, direct ? 'direct.html' : 'guarded.html'), html);
  }
  const videoCourse = {
    style: 'Slides', course_slug: 'video-seek-test', course_title: 'Video seek test',
    motion_intro: {enabled: false},
    modules: [{id: 1, title: 'Video timing', slides: [
      {id: 1, type: 'title'},
      {id: 2, type: 'content_two_column', title: 'Looping visual',
        figure: {path: 'loop.mp4', media_type: 'video', alt: 'Timing test', loop: true}}
    ]}]
  };
  await fs.writeFile(path.join(tmp, 'video.html'), execFileSync(process.env.PYTHON || 'python3',
    ['-c', render, scripts], {input: JSON.stringify(videoCourse), encoding: 'utf8'}));
  const mobileTitle = structuredClone(videoCourse);
  mobileTitle.modules[0].title = 'The Facility Compatibility Envelope';
  mobileTitle.modules[0].slides[0].subtitle = 'Coordinate what the facility must carry, clear, connect, and adapt.';
  await fs.writeFile(path.join(tmp, 'mobile-title.html'), execFileSync(process.env.PYTHON || 'python3',
    ['-c', render, scripts], {input: JSON.stringify(mobileTitle), encoding: 'utf8'}));
  browser = await chromium.launch({headless: true, args: ['--mute-audio']});
  const context = await browser.newContext({viewport: {width: 1440, height: 960}, reducedMotion: 'reduce'});
  await context.route(/^https?:/, route => route.abort());
  await context.addInitScript(() => {
    HTMLMediaElement.prototype.play = function() { return Promise.resolve(); };
    window.API = {
      LMSInitialize: () => 'true', LMSFinish: () => 'true', LMSCommit: () => 'true',
      LMSSetValue: () => 'true', LMSGetValue: () => ''
    };
  });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  const url = name => pathToFileURL(path.join(tmp, name + '.html')).href;
  for (const name of ['guarded', 'direct']) {
    await page.goto(url(name));
    await page.evaluate(() => localStorage.clear());
    await page.reload();
    const toggle = page.locator('#narrationModeBtn');
    const text = page.locator('.hero-start-hint span');
    check(await text.innerText(), hint, 'Authored localized hint is initially retained');
    for (let n = 0; n < 2; n++) {
      await toggle.click();
      check((await text.innerText()).startsWith('Narration is off.'), true, 'Disabling narration updates hint');
      await toggle.click();
      check(await text.innerText(), hint, 'Enabling restores the exact authored hint');
    }
    await toggle.click();
    await page.reload();
    check(await toggle.getAttribute('aria-pressed'), 'false', 'Saved off preference survives reload');
    await toggle.click();
    check(await text.innerText(), hint, 'Saved-off reload preserves original hint for re-enabling');
    await page.locator('#nextBtn').click();
    await toggle.click();
    await toggle.click();
    await page.locator('#prevBtn').click();
    check(await text.innerText(), hint, 'Toggling away from title keeps title hint synchronized');
    const pill = page.locator('.slide-hero .reference-pill');
    check(await pill.getAttribute('href'), reference, 'Title resource retains page-specific URL');
    check(await pill.getAttribute('target'), '_blank', 'Resource opens a separate tab');
    check(await page.locator('.slide-hero .term-pill').count(), 0, 'Title remains glossary-free');
    await page.setViewportSize({width: 320, height: 640});
    await pill.scrollIntoViewIfNeeded();
    const box = await pill.boundingBox();
    check(box.x >= 0 && box.x + box.width <= 320 && box.y >= 0 && box.y + box.height <= 640,
      true, 'Title resource remains reachable on a narrow screen');
    check(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, 'No horizontal overflow');
    await page.setViewportSize({width: 1440, height: 960});
    await page.locator('#nextBtn').click();
    await page.locator('.slide.active .next-module-link').click();
    if (name === 'direct') {
      await page.waitForURL('**/module2.html');
      check(page.url(), url('module2'), 'Explicit direct compatibility choice permits next-module navigation');
    } else {
      check(page.url(), url(name), 'Default LMS navigation guard remains intact');
      check(await page.locator('.lms-navigation-note').isVisible(), true, 'Guard retains syllabus instruction');
    }
    await page.goto(url(name) + '?review=1&slide=2');
    await page.locator('.slide.active .next-module-link').click();
    await page.waitForURL('**/module2.html?review=1&slide=1');
    check(page.url(), url('module2') + '?review=1&slide=1',
      'Next-module link retains quiet local review mode');
  }
  await page.setViewportSize({width:320,height:640});
  await page.goto(url('mobile-title') + '?review=1');
  const titleLayout = await page.evaluate(() => {
    const hero = document.querySelector('.hero-content');
    const box = hero.getBoundingClientRect();
    const badge = document.querySelector('.module-badge').getBoundingClientRect();
    const slide = document.querySelector('.slide.active');
    slide.scrollTop = slide.scrollHeight;
    return {inside: box.left >= 24 && box.right <= innerWidth - 24,
      belowBadge: box.top >= badge.bottom,
      scrollableEnd: hero.getBoundingClientRect().bottom <= document.querySelector('.controls').getBoundingClientRect().top};
  });
  check(titleLayout, {inside:true,belowBadge:true,scrollableEnd:true},
    'Long mobile title without resources fits, clears badge and scrolls above controls');
  await page.setViewportSize({width:1440,height:960});
  await page.addInitScript(() => {
    window.Audio = function() {
      const audio = document.createElement('audio');
      window.__testAudio = audio;
      return audio;
    };
  });
  await page.goto(url('video'));
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await page.locator('#nextBtn').click();
  await page.locator('.slide.active video.figure-video').waitFor();
  check(await page.locator('.slide.active video.figure-video').count(), 1,
    'Video test reaches its looping visual slide');
  check(await page.evaluate(() => Boolean(window.__testAudio)), true,
    'Video test captures the narration player');
  const videoTimes = await page.evaluate(() => {
    const audio = window.__testAudio;
    const video = document.querySelector('.slide.active video.figure-video');
    Object.defineProperty(audio, 'currentTime', {configurable: true, get: () => 22.5});
    Object.defineProperty(video, 'duration', {configurable: true, get: () => 8});
    let currentTime = 0;
    Object.defineProperty(video, 'currentTime', {
      configurable: true, get: () => currentTime, set: value => { currentTime = value; }
    });
    audio.dispatchEvent(new Event('seeking'));
    const looped = video.currentTime;
    video.loop = false;
    audio.dispatchEvent(new Event('seeking'));
    return {looped, finite: video.currentTime};
  });
  check(videoTimes.looped, 6.5, 'Seeking a short looping video wraps to the corresponding visual frame');
  check(Math.abs(videoTimes.finite - (8 - 1 / 60)) < 0.001, true,
    'Seeking a finite video stops at its final frame');
  check(errors, [], 'No JavaScript errors in navigation or video timing checks');
  console.log(`PASS: ${checks} slide-control browser assertions; no live LMS or audio playback.`);
} finally {
  if (browser) await browser.close();
  await fs.rm(tmp, {recursive: true, force: true});
}
