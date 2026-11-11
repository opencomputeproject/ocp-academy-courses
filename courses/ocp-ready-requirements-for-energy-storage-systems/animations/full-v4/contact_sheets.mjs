import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { here, chromium, locales, editionRoot, readJSON } from './lib.mjs';
const manifest = await readJSON(path.join(here, 'figure-patch-manifest.json'));
const browser = await (await chromium()).launch({ headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  for (const locale of locales) {
    const figures = Object.values(manifest.editions[locale].figures);
    const images = [];
    for (const item of figures) {
      const png = await fs.readFile(path.join(editionRoot(locale), item.figure.poster));
      images.push(`<img width="960" height="540" src="data:image/png;base64,${png.toString('base64')}">`);
    }
    await page.setContent(`<html><body style="margin:0;display:grid;grid-template-columns:960px 960px;background:white">${images.join('')}</body></html>`);
    await page.screenshot({ path: path.join(here, 'qa', locale, 'four-scene-contact-sheet.png') });
  }
} finally { await browser.close(); }
