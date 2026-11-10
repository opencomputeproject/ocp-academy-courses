import fs from 'node:fs/promises';
import path from 'node:path';
import { chromium, here, locales, scenes, editionRoot, readJSON, writeJSON } from './lib.mjs';

// Run explicitly to refresh the editable, reviewable label snapshot. Never runs during encoding.
const browser = await (await chromium()).launch({ headless: true, args: ['--mute-audio'] });
try {
  const page = await browser.newPage();
  const editions = {};
  for (const locale of locales) {
    const root = editionRoot(locale);
    const course = await readJSON(path.join(root, 'course.json'));
    const entries = {};
    for (const [id, scene] of Object.entries(scenes)) {
      const slide = course.modules[scene.module - 1].slides[scene.slide - 1];
      const texts = id === 'M4S8' ? [] : await page.evaluate(svg => {
        const doc = new DOMParser().parseFromString(svg, 'image/svg+xml');
        if (doc.querySelector('parsererror')) throw new Error('Invalid approved SVG');
        return [...doc.querySelectorAll('text')].map(el => el.textContent.trim());
      }, slide.figure.svg);
      entries[id] = { slide_id: slide.id, slug: slide.slug, audio: slide.audio.delivery_file || slide.audio.wav_file, alt: slide.figure.alt, caption: slide.figure.caption, source_refs: slide.source_refs, labels: texts.slice(1) };
    }
    const workflow = locale === 'en-US' ? {
      steps: [{ label: 'Use case', detail: 'business need' }, { label: 'Deployment', detail: 'location + topology' }, { label: 'Hazards', detail: 'credible risks' }, { label: 'Standards', detail: 'applicable stack' }, { label: 'Early review', detail: 'AHJ + insurer' }, { label: 'Evidence', detail: 'tests + plans' }, { label: 'Operations', detail: 'procedures' }, { label: 'OCP feedback', detail: 'lessons learned' }], loop: 'Continuous community learning',
    } : await readJSON(path.join(root, 'animations/locale_strings.json'));
    entries.M4S8.steps = workflow.steps;
    entries.M4S8.loop_label = workflow.loop;
    editions[locale] = entries;
  }
  await writeJSON(path.join(here, 'labels.json'), { schema_version: 1, provenance: 'Approved course SVG text and existing workflow locale_strings.json; decorative headings omitted. Refresh explicitly after editorial approval.', editions });
} finally { await browser.close(); }
