// Isolated, silent browser QA. Never changes the user's browser or live LMS.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {chromium} from 'playwright';

if (!process.argv[2]) throw new Error('Usage: node test_syllabus_home_browser.mjs <built-open-dc-package> [qa-folder]');
const pkg = path.resolve(process.argv[2]);
const qa = path.resolve(process.argv[3] || path.join(pkg, '..', 'syllabus-home-qa'));
await fs.mkdir(qa, {recursive: true});
const checks = [], errors = [];
const home = pathToFileURL(path.join(pkg, 'index.html')).href;
const check = (name, actual, expected) => {
  assert.deepEqual(actual, expected, name); checks.push(name); console.log('PASS: ' + name);
};
const browser = await chromium.launch({channel: 'chrome', headless: true, args: ['--mute-audio']});
try {
  const context = await browser.newContext({viewport: {width: 1440, height: 1000}, reducedMotion: 'reduce'});
  // Prevent all live network calls and any media playback in this disposable context.
  await context.route(/^https?:/, route => route.abort());
  await context.addInitScript(() => {
    HTMLMediaElement.prototype.play = function() { return Promise.resolve(); };
    window.testCalls = [];
    window.API = {
      LMSInitialize() { testCalls.push(['init']); return 'true'; },
      LMSSetValue(k,v) { testCalls.push(['set', k, v]); return 'true'; },
      LMSGetValue(k) {
        testCalls.push(['get', k]);
        if (k === 'cmi.core.lesson_status') return 'incomplete';
        if (k === 'cmi.core.lesson_location') return (location.pathname.match(/module\d+(?=\.html)/)?.[0] || 'module1') + ':slide3';
        return '{"modules":[1,2,3,4]}';
      },
      LMSCommit() { testCalls.push(['commit']); return 'true'; },
      LMSFinish() { testCalls.push(['finish']); return 'true'; }
    };
  });
  const page = await context.newPage();
  page.on('pageerror', error => errors.push(error.message));
  async function ready(url) {
    await page.goto(url);
    await page.waitForFunction(() => document.body.classList.contains('motion-intro-done'));
    await page.locator('#ocpMotionIntro').waitFor({state:'detached'});
    if (await page.locator('.index-shell').count())
      await page.waitForFunction(() => Number(getComputedStyle(document.querySelector('.index-shell')).opacity) > .99);
  }
  const styles = async (selector, names) => page.locator(selector).first().evaluate((e, names) => {
    const s = getComputedStyle(e); return Object.fromEntries(names.map(k => [k, s[k]]));
  }, names);
  const buttonProps = ['width','height','minWidth','borderRadius','backgroundColor','color','animationName'];
  await ready(home + '?review=1');
  check('Four informational tiles', await page.locator('article.module-card').count(), 4);
  check('No tile anchors, tabindex or status elements', await page.locator('a.module-card,.module-card[tabindex],.module-card .status,.module-card.completed').count(), 0);
  check('Exact Syllabus instruction', await page.locator('#lmsNavNote').innerText(), 'Navigate modules in any order using the Syllabus in the left sidebar.');
  check('Syllabus instruction matches normal tile body size', await styles('#lmsNavNote', ['fontSize']), await styles('.module-info p', ['fontSize']));
  check('Exact start label', await page.locator('.index-start-label').innerText(), 'Start with MODULE 1');
  check('Start label uses OCP indigo', await styles('.index-start-label', ['color']), {color: 'rgb(52, 56, 149)'});
  const card = page.locator('.module-card').first();
  await card.hover();
  check('Informational hover does not lift or show pointer', await styles('.module-card', ['transform','cursor']), {transform:'none',cursor:'auto'});
  await card.click();
  check('Tile click does not navigate', page.url(), home + '?review=1');
  check('Review mode makes no LMS calls', await page.evaluate(() => testCalls), []);
  const start = await page.locator('.index-start-link').boundingBox();
  const label = await page.locator('.index-start-label').boundingBox();
  const note = await page.locator('#lmsNavNote').boundingBox();
  check('Label is left of circular button, action below note', label.x + label.width < start.x && start.y >= note.y + note.height, true);
  await page.locator('.index-start-link').focus();
  check('Keyboard focus is visible', (await styles('.index-start-link', ['outlineStyle'])).outlineStyle, 'solid');
  await page.locator('.index-start-link').blur();
  // Capture the resting color, not an intermediate focus-transition frame.
  await page.waitForFunction(() => document.querySelector('.index-start-link').getAnimations().length === 0);
  const startStyle = await styles('.index-start-link', buttonProps);
  const startPaths = await page.locator('.index-start-link path').evaluateAll(nodes => nodes.map(n => n.getAttribute('d')));
  for (const [width, height] of [[1440,1000],[1024,900],[640,960],[390,844],[320,900]]) {
    await page.setViewportSize({width,height});
    check(`${width}px has no horizontal overflow`, await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
    const boxes = await page.locator('.module-card').evaluateAll(nodes => nodes.map(n => ({x:n.getBoundingClientRect().x,y:n.getBoundingClientRect().y})));
    check(`${width}px column layout`, boxes[0].y === boxes[1].y, width > 600);
    await page.screenshot({path:path.join(qa, `home-${width}.png`),fullPage:true});
  }
  await page.setViewportSize({width:1440,height:1000});
  await page.locator('.index-start-link').click();
  await page.waitForURL('**/module1.html?review=1&slide=1');
  check('Start opens Module 1 slide 1', await page.locator('.slide.active').getAttribute('data-slide'), '1');
  check('Start preserves narration-off review', await page.locator('#narrationModeBtn').getAttribute('aria-pressed'), 'false');
  check('Start review does not initialize LMS', await page.evaluate(() => testCalls), []);
  check('Start control matches original module control', await styles('.next-module-link', buttonProps), startStyle);
  check('Double-chevron SVG is identical', await page.locator('.next-module-link path').evaluateAll(nodes => nodes.map(n=>n.getAttribute('d'))), startPaths);
  await ready(home);
  check('Real launch completes Home only', await page.evaluate(() => testCalls.filter(x=>x[0]==='set')), [['set','cmi.core.lesson_status','completed']]);
  check('Home never reads suspend data or module progress', await page.evaluate(() => testCalls.filter(x=>x[0]==='get')), []);
  check('Completed LMS data cannot color tiles', await page.locator('.module-card.completed,.module-card .status').count(), 0);
  for (let m = 1; m <= 4; m++) {
    await ready(pathToFileURL(path.join(pkg, `module${m}.html`)).href);
    check(`M${m} resumes at saved slide 3`, await page.locator('.slide.active').getAttribute('data-slide'), '3');
    check(`M${m} reads its slide bookmark once`, await page.evaluate(() => testCalls.filter(c => c[0] === 'get' && c[1] === 'cmi.core.lesson_location')), [['get', 'cmi.core.lesson_location']]);
    await page.keyboard.press('ArrowRight');
    await page.keyboard.press('ArrowRight');
    check(`M${m} saves each visited slide`, await page.evaluate(() => testCalls.filter(c => c[0] === 'set' && c[1] === 'cmi.core.lesson_location')), [3,4,5].map(s => ['set', 'cmi.core.lesson_location', `module${m}:slide${s}`]));
    check(`M${m} keeps course-home link`, await page.getByRole('link', {name:'Course home', exact:true}).getAttribute('href'), 'index.html');
  }
  check('No JavaScript errors', errors, []);
  await fs.writeFile(path.join(qa,'browser-results.json'), JSON.stringify({passed:checks.length,checks,silent:true,liveLMSAcceptance:false},null,2)+'\n');
  await context.close();
} finally { await browser.close(); }
