// Quiet, isolated regression checks for the maintained Slides player.
// Mock SCORM validates player logic, never actual LMS navigation or acceptance.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL, fileURLToPath} from 'node:url';
import {chromium} from 'playwright';

if (!process.argv[2]) throw new Error('Usage: node test_slide_resume_browser.mjs <built-package>');
const root = path.resolve(process.argv[2]);
const course = JSON.parse(await fs.readFile(path.join(root, 'course.json'), 'utf8'));
assert.equal(course.scorm?.compatibility_profile, undefined, 'Course uses the maintained player, not a compatibility profile');
assert.deepEqual(await fs.readFile(path.join(root, 'scorm_api.js')),
  await fs.readFile(path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../assets/scorm_api.js')),
  'Build uses the maintained SCORM wrapper');
const url = id => pathToFileURL(path.join(root, `module${id}.html`)).href;
const browser = await chromium.launch({headless: true, args: ['--mute-audio']});
let checks = 0;
const errors = [];
const check = (actual, expected, message) => { assert.deepEqual(actual, expected, message); checks++; };
async function contextFor(status = null, initialValues = {}) {
  const context = await browser.newContext({reducedMotion: 'reduce'});
  await context.route(/^https?:\/\//, route => route.abort());
  await context.addInitScript(({status, initialValues}) => {
    HTMLMediaElement.prototype.play = function() { return Promise.resolve(); };
    window.Audio = function() { return window.testAudio = document.createElement('audio'); };
    window.testCalls = [];
    if (status === null) return;
    const stateKey = 'test-lms:' + location.pathname;
    const values = JSON.parse(sessionStorage.getItem(stateKey) || 'null') || {
      'cmi.core.lesson_status': status, 'cmi.core.lesson_location': (location.pathname.match(/module\d+(?=\.html)/)?.[0] || 'module1') + ':slide3',
      'cmi.suspend_data': '{"modules":[1,2,3,4],"quizzes":{}}', ...initialValues};
    window.API = {
      LMSInitialize() { testCalls.push(['init']); return 'true'; },
      LMSGetValue(key) { testCalls.push(['get', key]); return values[key] || ''; },
      LMSSetValue(key, value) { testCalls.push(['set', key, value]); values[key] = value; sessionStorage.setItem(stateKey, JSON.stringify(values)); return 'true'; },
      LMSCommit() { testCalls.push(['commit']); return 'true'; },
      LMSFinish() { testCalls.push(['finish']); return 'true'; }
    };
  }, {status, initialValues});
  const page = await context.newPage();
  page.on('pageerror', e => errors.push(e.message));
  return {context, page};
}
try {
  // SCO status is authoritative, not stale bookmarks or another module's record.
  for (const status of ['incomplete', 'completed', 'passed']) {
    const {context, page} = await contextFor(status);
    for (const module of course.modules) {
      await page.goto(url(module.id));
      const expected = status === 'incomplete' ? '3' : String(module.slides.at(-1).id);
      check(await page.locator('.slide.active').getAttribute('data-slide'), expected,
        `M${module.id} ${status} resumes correctly without quiz detail`);
      check(await page.evaluate(() => testCalls.filter(c => c[0] === 'get' && c[1] === 'cmi.core.lesson_location')), [['get','cmi.core.lesson_location']],
        'Reads the current module bookmark once');
      if (status !== 'incomplete') check(await page.evaluate(() => testCalls.some(c => c[0] === 'set' && c[1] === 'cmi.core.lesson_status' && c[2] === 'incomplete')), false,
        'Completed/passed status is not downgraded');
      else {
        await page.locator('#nextBtn').click();
        await page.reload();
        check(await page.locator('.slide.active').getAttribute('data-slide'), '4', 'Unfinished module restores the updated slide after reload');
      }
    }
    await context.close();
  }

  const otherSession = await contextFor('completed', {
    'cmi.core.lesson_location': 'module1', 'cmi.suspend_data': '{"modules":[1],"quizzes":{}}'});
  await otherSession.page.goto(url(course.modules[1].id));
  check(await otherSession.page.locator('.slide.active').getAttribute('data-slide'), '1',
    'A completed previous-module session does not send the next module to its ending');
  await otherSession.context.close();
  const homeSession = await contextFor('completed', {'cmi.core.lesson_location':'', 'cmi.suspend_data':''});
  await homeSession.page.goto(url(course.modules[0].id));
  check(await homeSession.page.locator('.slide.active').getAttribute('data-slide'), '1',
    'A completed Home session does not make Module 1 appear completed');
  await homeSession.context.close();
  const ownSession = await contextFor('completed', {'cmi.core.lesson_location':`module${course.modules[0].id}`, 'cmi.suspend_data':''});
  await ownSession.page.goto(url(course.modules[0].id));
  check(await ownSession.page.locator('.slide.active').getAttribute('data-slide'), String(course.modules[0].slides.at(-1).id),
    'The completed module identity restores its ending even without suspend data');
  await ownSession.context.close();

  // Persist through the SCORM suspend-data path, including incorrect feedback.
  const lmsQuiz = await contextFor('incomplete');
  for (const module of course.modules) {
    const quiz = module.slides.find(s => s.type === 'knowledge_check');
    if (!quiz) continue;
    const reachQuiz = async () => {
      const current = Number(await lmsQuiz.page.locator('.slide.active').getAttribute('data-slide'));
      for (let n = current; n < quiz.id; n++) await lmsQuiz.page.locator('#nextBtn').click();
      await lmsQuiz.page.locator(`.slide.active[data-slide="${quiz.id}"]`).waitFor();
    };
    await lmsQuiz.page.goto(url(module.id));
    await reachQuiz();
    const firstCard = lmsQuiz.page.locator('.slide.active .quiz-card').first();
    await firstCard.locator('input:not([data-correct="true"])').first().check();
    await firstCard.locator('.quiz-submit').click();
    const feedback = await firstCard.locator('.quiz-feedback').innerText();
    const chosen = await firstCard.locator('input:checked').inputValue();
    await lmsQuiz.page.reload();
    await reachQuiz();
    check(await firstCard.locator('input:checked').inputValue(), chosen, 'LMS restores incorrect selection');
    check(await firstCard.locator('.quiz-feedback.incorrect').innerText(), feedback, 'LMS restores answer-specific incorrect feedback');
    await firstCard.locator('.quiz-retry').click();
    await lmsQuiz.page.reload();
    await reachQuiz();
    check(await firstCard.locator('input:checked').count(), 0, 'LMS retry persists across reload');
    check(await firstCard.locator('.quiz-feedback').innerText(), '', 'LMS retry clears old feedback');
    await lmsQuiz.page.evaluate(() => document.querySelectorAll('.slide.active .quiz-card').forEach(card => {
      card.querySelectorAll('input[data-correct="true"]').forEach(input => { input.checked = true; });
      card.querySelector('.quiz-submit').click();
    }));
    await lmsQuiz.page.locator('#nextBtn').click();
    await lmsQuiz.page.reload();
    check(await lmsQuiz.page.locator('.slide.active').getAttribute('data-slide'), String(module.slides.at(-1).id),
      'Completing the LMS quiz and module survives reload at the final slide');
  }
  await lmsQuiz.context.close();

  const {context, page} = await contextFor('completed');
  // A fresh editorial session ignores completed state and bypasses quiz gates.
  for (let i = 0; i < course.modules.length; i++) {
    const module = course.modules[i];
    await page.goto(`${url(module.id)}?review=1&slide=1`);
    check(await page.locator('.slide.active').getAttribute('data-slide'), '1', 'Review ignores LMS completion');
    check(await page.evaluate(() => testCalls), [], 'Review does not initialize or read/write LMS');
    if (i < course.modules.length - 1) {
      await page.goto(`${url(module.id)}?review=1&slide=${module.slides.at(-1).id}`);
      await page.locator('.slide.active .next-module-link').click();
      await page.waitForURL(`${url(course.modules[i + 1].id)}?review=1&slide=1`);
      check(await page.locator('.slide.active').getAttribute('data-slide'), '1', 'Next review module starts at slide 1');
    }
  }
  // Some authored courses omit a Home control; still exercise the delegated
  // review-link handler without requiring a course-content change.
  if (!await page.getByRole('link', {name: 'Course home', exact: true}).count()) {
    await page.evaluate(() => {
      const link = document.createElement('a'); link.href = 'index.html'; link.textContent = 'Course home';
      link.style.cssText = 'position:fixed;top:0;left:0;z-index:999999'; document.body.appendChild(link);
    });
  }
  await page.getByRole('link', {name: 'Course home', exact: true}).click();
  await page.waitForURL('**/index.html?review=1');
  check(await page.evaluate(() => testCalls), [], 'Review Home remains untracked');
  await context.close();

  const local = await contextFor();
  const first = course.modules[0];
  await local.page.goto(url(first.id));
  await local.page.evaluate(({slug, modules}) => {
    for (const module of modules) {
      localStorage.setItem(`ocp:${slug}:module${module.id}:quiz-state`, JSON.stringify({modules: [module.id], quizzes: {}}));
      localStorage.setItem(`ocp:${slug}:module${module.id}`, `module${module.id}:slide3`);
    }
  }, {slug: course.course_slug, modules: course.modules});
  let saved = await local.page.evaluate(() => ({...localStorage}));
  for (const module of course.modules) {
    await local.page.goto(`${url(module.id)}?review=1&slide=1`);
    check(await local.page.locator('.slide.active').getAttribute('data-slide'), '1', 'Review ignores local completion');
    const quiz = module.slides.find(s => s.type === 'knowledge_check');
    if (quiz) {
      await local.page.goto(`${url(module.id)}?review=1&slide=${quiz.id}`);
      await local.page.evaluate(() => {
        document.querySelectorAll('.slide.active .quiz-card').forEach(card => {
          card.querySelector('input').checked = true;
          card.querySelector('.quiz-submit').click();
          card.querySelector('.quiz-retry').click();
        });
      });
    }
    check(await local.page.evaluate(() => ({...localStorage})), saved, 'Editorial quiz and retry leave saved learner state intact');
    await local.page.goto(url(module.id));
    check(await local.page.locator('.slide.active').getAttribute('data-slide'), String(module.slides.at(-1).id),
      'Local completed module with missing quiz detail returns to ending');
    saved = await local.page.evaluate(() => ({...localStorage}));
  }
  await local.page.evaluate(() => localStorage.clear());
  await local.page.goto(url(first.id));
  const toggle = local.page.locator('#narrationModeBtn');
  const hint = local.page.locator('.hero-start-hint span');
  const originalHint = await hint.innerText();
  await toggle.click();
  check((await hint.innerText()).startsWith('Narration is off.'), true, 'Off hint appears');
  await local.page.reload();
  check(await toggle.getAttribute('aria-pressed'), 'false', 'Off preference survives reload');
  await toggle.click();
  check(await hint.innerText(), originalHint, 'Turning on restores authored hint after reload');
  await local.page.locator('#nextBtn').click();
  await local.page.locator('#transcriptBtn').click();
  check(await local.page.locator('#transcriptTitle').innerText(), first.slides[1].title, 'Transcript follows current slide');
  await local.page.keyboard.press('Escape');
  check(await local.page.locator('#transcriptPanel').isHidden(), true, 'Escape closes transcript');
  check(await local.page.evaluate(() => document.activeElement.id), 'transcriptBtn', 'Transcript returns focus to its control');
  await local.page.locator('#transcriptBtn').blur();
  await local.page.keyboard.press('Home');
  check(await local.page.locator('.slide.active').getAttribute('data-slide'), '1', 'Home key returns to first slide');
  await local.page.locator('#audioSpeedSlider').evaluate(el => { el.value = '1.3'; el.dispatchEvent(new Event('input')); });
  await local.page.reload();
  check(await local.page.evaluate(() => testAudio.playbackRate), 1.3, 'Playback-speed preference survives reload');
  await local.page.locator('#audioPlayBtn').click();
  await local.page.locator('#audioPlayBtn').click();
  check(await local.page.evaluate(() => testAudio.paused), true, 'Play/pause control can stop narration');

  // Exercise the maintained player with both video timing policies.
  const withVideo = course.modules.flatMap(m => m.slides.map(s => ({m, s})))
    .find(({s}) => s.figure?.media_type === 'video');
  assert.ok(withVideo, 'Fixture includes a video');
  await local.page.goto(`${url(withVideo.m.id)}?review=1&slide=${withVideo.s.id}`);
  const times = await local.page.evaluate(() => {
    const video = document.querySelector('.slide.active video.figure-video');
    const audio = testAudio;
    // This fixture deliberately exercises the legacy loop/finite policy.
    // Explicit synchronized video is covered by test_video_modes_browser.mjs.
    delete video.dataset.narrationSync;
    Object.defineProperty(audio, 'currentTime', {configurable: true, get: () => 22.5});
    Object.defineProperty(video, 'duration', {configurable: true, get: () => 8});
    let position = 0;
    Object.defineProperty(video, 'currentTime', {configurable: true, get: () => position, set: v => {position = v;}});
    video.loop = true; audio.dispatchEvent(new Event('seeking')); const loop = position;
    video.loop = false; audio.dispatchEvent(new Event('seeking'));
    return {loop, finite: position};
  });
  check(times.loop, 6.5, 'Looping video seeks to corresponding cycle');
  check(Math.abs(times.finite - (8 - 1 / 60)) < 0.001, true, 'Finite video holds final frame');
  await local.context.close();
  // Real learner-mode visits, without seeding bookmarks: save and reopen every
  // unfinished module independently, including closing/reopening the page.
  const partial = await contextFor();
  for (const module of course.modules) {
    await partial.page.goto(url(module.id));
    await partial.page.locator('#nextBtn').click();
    await partial.page.locator('#nextBtn').click();
    await partial.page.reload();
    check(await partial.page.locator('.slide.active').getAttribute('data-slide'), '3',
      `Local M${module.id} resumes at its real last-viewed slide`);
  }
  await partial.page.close();
  const reopened = await partial.context.newPage();
  reopened.on('pageerror', e => errors.push(e.message));
  for (const module of [...course.modules].reverse()) {
    await reopened.goto(url(module.id));
    check(await reopened.locator('.slide.active').getAttribute('data-slide'), '3',
      `M${module.id} bookmark survives page closure and visits to other modules`);
  }
  await partial.context.close();
  check(errors, [], 'No JavaScript errors');
  console.log(`PASS: ${checks} slide resume, control, review-isolation and video browser assertions.`);
} finally { await browser.close(); }
