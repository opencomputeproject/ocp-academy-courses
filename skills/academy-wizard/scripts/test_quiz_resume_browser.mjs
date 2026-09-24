// Isolated browser check for a built Slides package; no live LMS or audible playback.
// Usage: node test_quiz_resume_browser.mjs <built-package-folder>
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {chromium} from 'playwright';

if (!process.argv[2]) throw new Error('Usage: node test_quiz_resume_browser.mjs <built-package-folder>');
const root = path.resolve(process.argv[2]);
const course = JSON.parse(await fs.readFile(path.join(root, 'course.json'), 'utf8'));
assert.equal(course.scorm?.compatibility_profile, undefined, 'This check exercises the maintained Slides player');
const url = moduleId => pathToFileURL(path.join(root, `module${moduleId}.html`)).href;
const browser = await chromium.launch({headless: true, args: ['--mute-audio']});
let checks = 0;
const errors = [];
try {
  const context = await browser.newContext({reducedMotion: 'reduce'});
  await context.route(/^https?:\/\//, route => route.abort());
  await context.addInitScript(() => {
    HTMLMediaElement.prototype.play = function() { return Promise.resolve(); };
  });
  const page = await context.newPage();
  page.on('pageerror', error => errors.push(error.message));

  for (const module of course.modules) {
    const quiz = module.slides.find(slide => slide.type === 'knowledge_check');
    if (!quiz) continue;
    const last = module.slides.at(-1);
    const bookmarkKey = `ocp:${course.course_slug}:module${module.id}`;
    const quizKey = `${bookmarkKey}:quiz-state`;
    await page.goto(url(module.id));
    await page.evaluate(() => localStorage.clear());
    await page.evaluate(({key, value}) => localStorage.setItem(key, value),
      {key: bookmarkKey, value: `module${module.id}:slide${quiz.id}`});
    await page.reload();
    await page.locator(`.slide.active[data-slide="${quiz.id}"]`).waitFor();
    const questionCount = await page.locator('.slide.active .quiz-card').count();
    assert.ok(questionCount > 0, `Module ${module.id} has quiz questions`);
    await page.evaluate(() => {
      document.querySelectorAll('.slide.active .quiz-card').forEach(card => {
        card.querySelectorAll('input[data-correct="true"]').forEach(input => { input.checked = true; });
        card.querySelector('.quiz-submit').click();
      });
    });
    const saved = await page.evaluate(key => JSON.parse(localStorage.getItem(key)), quizKey);
    assert.equal(Object.keys(saved.quizzes).length, questionCount,
      `Module ${module.id} saves every attempt`); checks++;
    await page.locator('#nextBtn').click();
    await page.locator(`.slide.active[data-slide="${last.id}"]`).waitFor();
    await page.reload();
    await page.locator(`.slide.active[data-slide="${last.id}"]`).waitFor();
    assert.equal(await page.locator('.quiz-card[data-attempted="true"]').count(), questionCount,
      `Module ${module.id} restores every attempt`); checks++;
    assert.ok(await page.locator('.quiz-card input:checked').count() > 0,
      `Module ${module.id} restores selected answers`); checks++;
    assert.equal(await page.locator('.quiz-card .quiz-feedback.correct').count(), questionCount,
      `Module ${module.id} restores correct feedback`); checks++;
    await page.locator('#prevBtn').click();
    await page.locator(`.slide.active[data-slide="${quiz.id}"]`).waitFor();
    const firstQuestion = await page.locator('.slide.active .quiz-card').first().getAttribute('data-question-id');
    await page.locator('.slide.active .quiz-card').first().locator('.quiz-retry').click();
    const retried = await page.evaluate(key => JSON.parse(localStorage.getItem(key)), quizKey);
    assert.equal(retried.quizzes[firstQuestion], undefined,
      `Module ${module.id} clears the retried question`); checks++;
    assert.equal(Object.keys(retried.quizzes).length, questionCount - 1,
      `Module ${module.id} retains other questions`); checks++;
    await page.reload();
    assert.equal(await page.locator('.slide.active').getAttribute('data-slide'), String(last.id),
      `Completed module ${module.id} returns to its final slide after retry`); checks++;
    assert.equal(await page.locator(`[data-question-id="${firstQuestion}"] input:checked`).count(), 0,
      `Module ${module.id} does not resurrect retried answers`); checks++;
  }

  if (course.modules.length > 1) {
    const first = course.modules[0];
    const second = course.modules[1];
    const finalSlide = first.slides.at(-1).id;
    await page.goto(`${url(first.id)}?review=1&slide=${finalSlide}`);
    await page.locator('.slide.active .next-module-link').click();
    await page.waitForURL(`${url(second.id)}?review=1&slide=1`);
    assert.equal(await page.locator('.slide.active').getAttribute('data-slide'), '1',
      'Review navigation opens the next module at slide 1'); checks++;
  }
  assert.deepEqual(errors, [], 'No browser JavaScript errors'); checks++;
  console.log(`PASS: ${checks} quiz-resume and review-navigation browser assertions.`);
} finally {
  await browser.close();
}
