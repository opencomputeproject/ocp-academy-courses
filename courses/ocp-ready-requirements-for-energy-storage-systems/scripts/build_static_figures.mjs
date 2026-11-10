#!/usr/bin/env node
// Generates only editable static SVGs and unreviewed QA candidates. Never edits course.json.
// node scripts/build_static_figures.mjs [--output /tmp/ess-static-review] [--locale es-419] [--figure m3_evidence_chain]
// PLAYWRIGHT_MODULE may point to a locally installed playwright package.
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import os from 'node:os';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { INLINE_CORRECTIONS, LABELS, LOCALES } from './static_labels.mjs';

const require = createRequire(import.meta.url);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const playwrightModules = process.env.PLAYWRIGHT_MODULE ? [process.env.PLAYWRIGHT_MODULE] : [
  'playwright',
  path.resolve(root, '..', '..', 'skills', 'academy-wizard', 'node_modules', 'playwright'),
  path.join(process.env.CODEX_HOME || path.join(os.homedir(), '.codex'), 'skills', 'academy-wizard', 'node_modules', 'playwright'),
];
let playwright;
for (const module of playwrightModules) {
  try { playwright = require(module); break; } catch (error) { if (error.code !== 'MODULE_NOT_FOUND') throw error; }
}
if (!playwright) throw new Error('Install Playwright locally or set PLAYWRIGHT_MODULE to an installed package path.');
const { chromium } = playwright;
const output = process.argv.includes('--output') ? process.argv[process.argv.indexOf('--output') + 1] : '/tmp/ess-static-review';
const requestedLocale = process.argv.includes('--locale') ? process.argv[process.argv.indexOf('--locale') + 1] : null;
const requestedFigure = process.argv.includes('--figure') ? process.argv[process.argv.indexOf('--figure') + 1] : null;
const correctionsOnly = process.argv.includes('--corrections-only');
const languageFixes = JSON.parse(await fs.readFile(path.join(root, 'scripts', 'static_language_fixes.json'), 'utf8')).corrections;
if (requestedLocale && !LOCALES.includes(requestedLocale)) throw new Error(`Unknown locale: ${requestedLocale}`);
const selectedLocales = LOCALES.filter(locale => (!requestedLocale || locale === requestedLocale) && (!correctionsOnly || languageFixes.some(fix => fix.locale === locale)));
const inlineSourcePath = path.join(root, 'scripts', 'static_inline_text.json');
let inlineSource;
try { inlineSource = JSON.parse(await fs.readFile(inlineSourcePath, 'utf8')); }
catch (error) { if (error.code !== 'ENOENT') throw error; inlineSource = {}; }
await fs.mkdir(output, { recursive: true });
const candidates = requestedLocale || requestedFigure || correctionsOnly ? JSON.parse(await fs.readFile(path.join(output, 'candidates.json'), 'utf8')).assets : [];
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1800, height: 1200 }, deviceScaleFactor: 1 });
try {
  for (const locale of selectedLocales) {
    const dir = locale === 'en-US' ? root : path.join(root, 'locales', locale);
    const course = JSON.parse(await fs.readFile(path.join(dir, 'course.json'), 'utf8'));
    const labels = Object.fromEntries(Object.entries(LABELS).map(([k, v]) => [k, v[LOCALES.indexOf(locale)]]));
    if (!inlineSource[locale]) {
      inlineSource[locale] = await page.evaluate(course => {
        const out = {};
        for (const [m, s] of [[1, 5], [2, 5], [3, 3], [3, 7], [4, 3]]) {
          const figure = course.modules.find(x => x.id === m).slides.find(x => x.id === s).figure;
          if (!figure.svg) throw new Error(`Missing original inline SVG M${m}S${s}; restore the source-text snapshot before building.`);
          const dom = new DOMParser().parseFromString(figure.svg, 'image/svg+xml');
          out[`M${m}S${s}`] = [...dom.querySelectorAll('text')].map(t => {
            const spans = [...t.querySelectorAll('tspan')];
            return spans.length ? spans.map(x => x.textContent.trim()).join(' ') : t.textContent.trim();
          });
        }
        return out;
      }, course);
    }
    const fixes = languageFixes.filter(fix => fix.locale === locale);
    const figures = (await page.evaluate(generateFigures, { locale, course, labels, inlineText: inlineSource[locale], corrections: INLINE_CORRECTIONS[locale] || {}, languageFixes: fixes })).filter(figure => (!requestedFigure || figure.name === requestedFigure) && (!correctionsOnly || fixes.some(fix => fix.asset === `${figure.name}.svg`)));
    if (!figures.length) throw new Error(`Unknown static figure: ${requestedFigure}`);
    await fs.mkdir(path.join(output, locale), { recursive: true });
    for (const figure of figures) {
      const relative = `figures/${figure.name}.svg`;
      const file = path.join(dir, relative);
      await fs.writeFile(file, figure.svg);
      await page.setContent(figure.svg);
      await page.evaluate(() => document.fonts.ready);
      const checks = await page.evaluate(() => {
        const svg = document.querySelector('svg');
        const bounds = svg.viewBox.baseVal;
        const errors = [];
        for (const t of svg.querySelectorAll('text[data-container]')) {
          const [x, y, w, h] = t.dataset.container.split(' ').map(Number);
          const b = t.getBBox(), s = Number(t.getAttribute('font-size'));
          const gaps = [b.x - x, b.y - y, x + w - b.x - b.width, y + h - b.y - b.height];
          if (gaps.some(v => v < .75 * s - .3)) errors.push({ text: t.dataset.phrase, gaps, required: .75 * s });
          if (b.x < 0 || b.y < 0 || b.x + b.width > bounds.width || b.y + b.height > bounds.height) errors.push({ outside_artboard: t.dataset.phrase });
        }
        return { errors, phrases: [...new Set([...svg.querySelectorAll('text[data-phrase]')].map(t => t.dataset.phrase))] };
      });
      if (checks.errors.length) throw new Error(`${locale}/${figure.name}: ${JSON.stringify(checks.errors)}`);
      const native = path.join(output, locale, `${figure.name}.png`);
      await page.setViewportSize({ width: figure.width, height: figure.height });
      await page.locator('svg').screenshot({ path: native });
      for (const width of [1000, 390]) {
        await page.setViewportSize({ width, height: 900 });
        await page.addStyleTag({ content: `html,body{margin:0;background:#fff}svg{display:block;width:${width}px;height:auto}` });
        await page.locator('svg').screenshot({ path: path.join(output, locale, `${figure.name}-${width}.png`) });
      }
      const candidate = { locale, module: figure.module, slide: figure.slide, figure: { path: relative },
        absolute_path: file, previous_path: figure.previous, review_status: 'unreviewed',
        candidate_text_inventory: { sha256: crypto.createHash('sha256').update(figure.svg).digest('hex'), entries: checks.phrases.map(text => ({ text })) },
        review_images: { native, desktop: path.join(output, locale, `${figure.name}-1000.png`), mobile: path.join(output, locale, `${figure.name}-390.png`) },
        geometry_checks: { text_clearance_em: .75, violations: 0, width: figure.width, height: figure.height },
        provenance: figure.provenance, source_text_repairs: figure.repairs };
      const previous = candidates.findIndex(x => x.locale === locale && x.module === figure.module && x.slide === figure.slide);
      if (previous < 0) candidates.push(candidate); else candidates[previous] = candidate;
    }
    console.log(`${locale}: ${figures.length} static SVGs; rendered text containment passed`);
  }
  for (const locale of selectedLocales) {
    const tiles = [];
    for (const item of candidates.filter(x => x.locale === locale)) {
      const data = (await fs.readFile(item.review_images.mobile)).toString('base64');
      tiles.push(`<section><p>M${item.module}S${item.slide} ${path.basename(item.figure.path)}</p><img src="data:image/png;base64,${data}"/></section>`);
    }
    await page.setViewportSize({ width: 836, height: 1000 });
    await page.setContent(`<style>body{margin:0;background:#eee;font:13px Arial}main{width:812px;padding:12px;display:grid;grid-template-columns:390px 390px;gap:16px}section{background:white}p{margin:8px;font-weight:bold}img{display:block;width:390px}</style><main>${tiles.join('')}</main>`);
    await page.locator('img').evaluateAll(imgs => Promise.all(imgs.map(img => img.decode())));
    await page.locator('main').screenshot({ path: path.join(output, `${locale}-mobile-sheet.png`) });
  }
  await fs.writeFile(path.join(output, 'candidates.json'), JSON.stringify({ schema_version: 1, course_root: root, assets: candidates }, null, 2) + '\n');
  await fs.writeFile(inlineSourcePath, JSON.stringify(inlineSource, null, 2) + '\n');
} finally { await browser.close(); }

function generateFigures({ locale, course, labels: L, inlineText, corrections, languageFixes }) {
  const NS = 'http://www.w3.org/2000/svg';
  const FONT = 'Open Sans, Arial, sans-serif';
  const C = { ink: '#343895', green: '#8DC63F', text: '#3F4246', pale: '#F4F8F1', gray: '#72777B', line: '#B9C1C4', gold: '#BD9200' };
  const ctx = document.createElement('canvas').getContext('2d');
  const esc = s => String(s).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
  const slide = (m, s) => course.modules.find(x => x.id === m).slides.find(x => x.id === s);
  const repairs = {};
  let currentFigure;
  const polish = original => {
    const key = `M${currentFigure.module}S${currentFigure.slide}`;
    const seen = new Set();
    let phrase = original;
    while (true) {
      const fix = languageFixes.find(fix => fix.asset === `${currentFigure.name}.svg` && fix.old === phrase);
      if (!fix) return phrase;
      if (seen.has(phrase)) throw new Error(`Cyclic language correction: ${phrase}`);
      seen.add(phrase);
      const entries = repairs[key] ||= [];
      if (!entries.some(entry => entry.original === phrase && entry.repaired === fix.new)) entries.push({ original: phrase, repaired: fix.new, method: 'user-approved static-label language audit', review: fix.review || 'Dewey seven-language static audit', source: 'scripts/static_language_fixes.json' });
      phrase = fix.new;
    }
  };
  const inline = (m, s) => inlineText[`M${m}S${s}`].map((original, index) => {
    const corrected = corrections[`M${m}S${s}`]?.[index];
    if (corrected) {
      (repairs[`M${m}S${s}`] ||= []).push({ original, repaired: corrected, method: 'explicit user-approved static-label semantic correction' });
      return corrected;
    }
    const sameSlidePhrases = {
      'ko-KR': { 3: ['지역 발전', 0], 9: ['고립 모드', 1, 'bold_lead'] },
      'ja-JP': { 3: ['ローカル発電', 0] },
      'zh-CN': { 1: ['电网', 1], 3: ['本地发电', 0], 9: ['孤岛模式', 1, 'bold_lead'] },
      'zh-TW': { 1: ['電網', 1], 3: ['本地發電', 0], 9: ['孤島模式', 1, 'bold_lead'] },
      'vi-VN': { 3: ['phát điện cục bộ', 0] },
      'pt-BR': { 1: ['rede', 1] },
      'es-419': { 1: ['red', 1] },
    };
    const replacement = m === 2 && s === 5 ? sameSlidePhrases[locale]?.[index] : null;
    if (replacement) {
      const [repaired, bullet, field = 'text'] = replacement, source = `M${m}S${s}.bullets[${bullet}].${field}`;
      const evidence = inlineText._learner_phrase_evidence?.[source] || slide(m, s).bullets[bullet][field];
      if (!evidence.includes(repaired)) throw new Error(`Learner phrase is no longer supported: ${repaired}`);
      (repairs[`M${m}S${s}`] ||= []).push({ original, repaired, method: 'exact existing same-slide learner phrase', source: `M${m}S${s}.bullets[${bullet}].${field}`, evidence });
      return repaired;
    }
    if (/[\u0080-\u009f]/.test(original) && [...original].every(c => c.codePointAt(0) <= 255)) {
      try {
        const repaired = new TextDecoder('utf-8', { fatal: true }).decode(Uint8Array.from([...original].map(c => c.codePointAt(0))));
        (repairs[`M${m}S${s}`] ||= []).push({ original, repaired, method: 'reversible Latin-1 bytes decoded as UTF-8' });
        return repaired;
      } catch { /* Not a reversible encoding defect: retain the original for review. */ }
    }
    return original;
  });
  const widthOf = (s, size = 20, bold = false) => { ctx.font = `${bold ? 700 : 400} ${size}px ${FONT}`; return ctx.measureText(s).width; };
  const wrap = (s, width, size, bold = false) => {
    s = polish(s);
    const pieces = [...new Intl.Segmenter(locale, { granularity: 'word' }).segment(s)].map(x => x.segment).reduce((out, piece) => {
      if ((/^[,.;:!?%）)\]}、。\-/]/u.test(piece) || /[（(±≤<>\-/]$/u.test(out.at(-1) || '')) && out.length) out[out.length - 1] += piece;
      else out.push(piece);
      return out;
    }, []);
    const lines = []; let line = '';
    for (let piece of pieces) {
      if (widthOf(line + piece, size, bold) > width && line.trim()) { lines.push(line.trimEnd()); line = ''; piece = piece.trimStart(); }
      if (widthOf(piece, size, bold) > width) {
        for (const ch of [...piece]) {
          if (widthOf(line + ch, size, bold) > width) { lines.push(line); line = ''; }
          line += ch;
        }
      } else line += piece;
    }
    if (line.trim()) lines.push(line.trimEnd());
    return lines.length ? lines : [''];
  };
  const textHeight = (s, w, size = 20, bold = false) => Math.ceil(wrap(s, w - 2 * size, size, bold).length * size * 1.38 + 2 * size);
  const figures = [];
  let parts = [];
  const start = (name, module, slide) => { parts = []; currentFigure = { name, module, slide }; };
  const rect = (x, y, w, h, fill = '#FFFFFF', stroke = C.line, radius = 4, extra = '') => {
    parts.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${radius}" fill="${fill}" stroke="${stroke}" stroke-width="2" ${extra}/>`);
  };
  const line = (x1, y1, x2, y2, color = C.ink, sw = 3) => parts.push(`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${sw}"/>`);
  const text = (s, x, y, w, h, size = 20, bold = false, color = C.text, align = 'middle') => {
    s = polish(s);
    const lines = wrap(s, w - 2 * size, size, bold), lh = size * 1.38;
    const required = (lines.length - 1) * lh + 2.9 * size;
    if (required > h + 1) throw new Error(`Text area too short (${required}>${h}): ${s}`);
    const tx = align === 'start' ? x + size : x + w / 2;
    const ty = y + h / 2 - (lines.length - 1) * lh / 2 + size * .33;
    parts.push(`<text data-phrase="${esc(s)}" data-container="${x} ${y} ${w} ${h}" x="${tx}" y="${ty}" font-size="${size}" font-weight="${bold ? 700 : 400}" fill="${color}" text-anchor="${align}">${lines.map((l, i) => `<tspan x="${tx}" y="${(ty + i * lh).toFixed(2)}">${esc(l)}</tspan>`).join('')}</text>`);
  };
  const arrow = (points, color = C.ink, size = 12) => {
    const [tx, ty] = points.at(-1), [px, py] = points.at(-2);
    const mag = Math.hypot(tx - px, ty - py), ux = (tx - px) / mag, uy = (ty - py) / mag;
    const bx = tx - ux * size, by = ty - uy * size, half = size * .42;
    const shaft = [...points.slice(0, -1), [bx, by]];
    parts.push(`<path d="${shaft.map(([x, y], i) => `${i ? 'L' : 'M'}${x} ${y}`).join(' ')}" fill="none" stroke="${color}" stroke-width="3"/>`);
    parts.push(`<polygon class="arrowhead" points="${bx - uy * half},${by + ux * half} ${bx + uy * half},${by - ux * half} ${tx},${ty}" fill="${color}"/>`);
  };
  const dim = (x1, y1, x2, y2, color = C.gray) => {
    const mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
    arrow([[mx, my], [x1, y1]], color, 9); arrow([[mx, my], [x2, y2]], color, 9);
  };
  const panelHeight = (w, items, size = 20) => items.reduce((h, a, i) => h + textHeight(a, w, i === 0 ? size + 2 : size, i === 0), 0);
  const panel = (x, y, w, items, { h = panelHeight(w, items), size = 20, fill = C.pale, stroke = C.green, icon = false } = {}) => {
    rect(x, y, w, h, fill, stroke);
    let cy = y;
    items.forEach((a, i) => {
      const s = i === 0 ? size + 2 : size;
      const th = textHeight(a, w, s, i === 0);
      text(a, x, cy, w, th, s, i === 0, i === 0 ? C.ink : C.text);
      cy += th;
    });
    if (icon) cabinet(x + w / 2 - 28, y + h - 95, 56, 72);
    return h;
  };
  const cabinet = (x, y, w, h) => {
    rect(x, y, w, h, '#FFFFFF', C.ink, 2);
    for (let i = 0; i < 4; i++) { rect(x + 8, y + 8 + i * (h - 12) / 4, w - 16, (h - 28) / 4, i === 0 ? '#EAF4E1' : '#EDF0F2', C.line, 1); }
  };
  const finish = (name, m, s, w, h, previous = `figures/${name}.png`, provenance = 'Faithful code-native reconstruction of the existing PNG; localized source labels in scripts/static_labels.mjs; technical content preserved.') => {
    const svg = `<svg xmlns="${NS}" xml:lang="${locale}" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(slide(m, s).figure.alt)}" font-family="${FONT}">\n<rect width="${w}" height="${h}" fill="#FFFFFF"/>\n${parts.join('\n')}\n</svg>\n`;
    figures.push({ name, module: m, slide: s, width: w, height: h, previous, svg, provenance, repairs: repairs[`M${m}S${s}`] || [] });
  };
  const inlineFinish = (name, m, s, w, h) => finish(name, m, s, w, h, `figures/${name}.svg`, 'Uses existing localized figure.svg text and documented same-slide learner-phrase corrections; redundant media heading removed; layout and connectors rebuilt. Raw inline strings preserved in scripts/static_inline_text.json.');

  // The five source-inline figures: retain their localized text, not a back-translation.
  {
    start('m1_response_continuum', 1, 5); const t = inline(1, 5), w = 1240, slot = 240;
    const sizes = [0, 1, 2, 3, 4].map(i => {
      const words = [...new Intl.Segmenter(locale, { granularity: 'word' }).segment(t[1 + i * 2])].filter(x => x.isWordLike).map(x => x.segment);
      let size = 20;
      while (size > 18 && words.some(word => widthOf(word, size, true) > slot - 2 * size)) size -= 1;
      return size;
    });
    const labelH = Math.max(...[0, 1, 2, 3, 4].map(i => textHeight(t[1 + i * 2], slot, sizes[i], true)));
    const timeH = 66, y = 44;
    line(140, y, 1100, y, C.ink, 4);
    for (let i = 0; i < 5; i++) {
      const x = 20 + i * slot;
      parts.push(`<circle cx="${x + slot / 2}" cy="${y}" r="14" fill="${C.green}" stroke="${C.ink}" stroke-width="3"/>`);
      text(t[1 + i * 2], x, 70, slot, labelH, sizes[i], true, C.ink);
      text(t[2 + i * 2], x, 70 + labelH, slot, timeH, 19);
    }
    const h = 70 + labelH + timeH + 90;
    text(t[11], 20, h - 80, 520, 66, 20, false, C.gray, 'start');
    text(t[12], 700, h - 80, 520, 66, 20, false, C.gray);
    inlineFinish('m1_response_continuum', 1, 5, w, h);
  }
  {
    start('m2_microgrid', 2, 5); const t = inline(2, 5), w = 1240;
    const genH = panelHeight(320, [t[3], t[4]]), essH = panelHeight(320, [t[5], t[6]]);
    const mid = genH + 94, essY = genH + 188, bottom = essY + essH + 24;
    parts.push(`<path d="M320 12 H1220 V${bottom} H320 Z" fill="none" stroke="${C.gray}" stroke-width="2" stroke-dasharray="8 7"/>`);
    const gridH = panelHeight(240, [t[1], t[2]]), dcH = panelHeight(280, [t[7], t[8]]);
    panel(20, mid - gridH / 2, 240, [t[1], t[2]], { h: gridH });
    panel(370, 36, 320, [t[3], t[4]], { h: genH });
    panel(370, essY, 320, [t[5], t[6]], { h: essH });
    panel(900, mid - dcH / 2, 280, [t[7], t[8]], { h: dcH, stroke: C.ink });
    line(800, 36 + genH / 2, 800, essY + essH / 2, C.ink, 4);
    arrow([[260, mid], [800, mid]]);
    arrow([[690, 36 + genH / 2], [800, 36 + genH / 2]]);
    arrow([[690, essY + essH / 2], [800, essY + essH / 2]]);
    arrow([[800, mid], [900, mid]]);
    arrow([[530, 36 + genH], [530, essY]]);
    const noteH = textHeight(t[9], 880, 20);
    text(t[9], 320, bottom + 4, 880, noteH, 20, false, C.gray);
    inlineFinish('m2_microgrid', 2, 5, w, bottom + noteH + 24);
  }
  {
    start('m3_voltage', 3, 3); const t = inline(3, 3), w = 1240;
    const bottomH = Math.max(textHeight(t[2], 450, 20), textHeight(t[4], 710, 20));
    text(t[1], 20, 12, 450, 80, 24, true, C.ink);
    text(t[3], 510, 12, 710, 80, 24, true, C.ink);
    line(110, 122, 1130, 122, C.line, 4);
    rect(690, 102, 350, 40, C.pale, C.green, 4);
    line(245, 92, 245, 154, C.ink, 4);
    line(690, 92, 690, 154, C.green, 4); line(1040, 92, 1040, 154, C.green, 4);
    text(t[2], 20, 170, 450, bottomH, 20);
    text(t[4], 510, 170, 710, bottomH, 20);
    inlineFinish('m3_voltage', 3, 3, w, 190 + bottomH);
  }
  {
    start('m3_evidence_chain', 3, 7); const t = inline(3, 7), items = [[t[1], t[2]], [t[3], t[4]], [t[5], t[6]], [t[7], t[8]]];
    const pw = 280, gap = 52, h = Math.max(...items.map(a => panelHeight(pw, a))) + 24;
    items.forEach((a, i) => {
      const x = 20 + i * (pw + gap); panel(x, 20, pw, a, { h });
      if (i < 3) arrow([[x + pw, 20 + h / 2], [x + pw + gap, 20 + h / 2]]);
    });
    inlineFinish('m3_evidence_chain', 3, 7, 1316, h + 40);
  }
  {
    start('m4_compliance_layers', 4, 3); const t = inline(4, 3); let y = 20;
    t.slice(1).forEach((s, i) => {
      const w = 1120 - i * 80, x = (1200 - w) / 2, h = textHeight(s, w, 22, true);
      rect(x, y, w, h, i % 2 ? '#FFFFFF' : C.pale, i < 3 ? C.green : C.ink);
      text(s, x, y, w, h, 22, true, C.ink); y += h + 10;
    });
    inlineFinish('m4_compliance_layers', 4, 3, 1200, y + 10);
  }

  {
    start('summit_deployment_architecture', 2, 3); const pw = 272, gap = 44;
    const columns = [[L.grid], [L.facility, L.centralized, L.facilityInterface], [L.row, L.sidecar, L.sharedRacks, L.busway], [L.rack, 'BBU', L.openRack, L.localBackup, L.closestIT], [L.it, L.servers]];
    const ph = Math.max(...columns.map(a => panelHeight(pw, a))) + 110;
    columns.forEach((a, i) => {
      const x = 20 + i * (pw + gap); panel(x, 20, pw, a, { h: ph, icon: true, stroke: i === 3 ? C.gold : C.green });
      if (i < 4) arrow([[x + pw, ph - 32], [x + pw + gap, ph - 32]], C.green, 13);
    });
    let y = ph + 44;
    text(L.batteryTech, 20, y, 1536, 80, 24, true, C.ink, 'start'); y += 88;
    const tech = [L.lithium, L.nickel, L.lead, L.sodium, L.supercaps];
    const th = Math.max(...tech.map(s => textHeight(s, pw, 22, true)));
    tech.forEach((s, i) => {
      const x = 20 + i * (pw + gap); rect(x, y, pw, 86 + th, '#FFFFFF', C.line);
      rect(x + pw / 2 - 30, y + 20, 60, 48, C.pale, C.ink, 3);
      line(x + pw / 2 - 12, y + 16, x + pw / 2 - 12, y + 20, C.ink, 5); line(x + pw / 2 + 12, y + 16, x + pw / 2 + 12, y + 20, C.ink, 5);
      text(s, x, y + 86, pw, th, 22, true, C.ink);
    });
    finish('summit_deployment_architecture', 2, 3, 1576, y + 106 + th);
  }
  {
    start('summit_hazard_taxonomy', 3, 4); const top = [[L.electrical, L.highDC, L.energized], [L.thermal, L.runaway, L.propagation], [L.gas, L.offgas, L.flammable], [L.chemical, L.electrolyte, L.toxic]];
    const w = 384, h = Math.max(...top.map(a => panelHeight(w, a)));
    top.forEach((a, i) => panel(20 + i * 400, 20, w, a, { h, stroke: i === 2 ? C.gold : C.green }));
    let y = h + 42; text(L.systemIssues, 20, y, 1584, 80, 24, true, C.ink, 'start'); y += 96;
    const bottom = [[L.integration, L.layers, L.infrastructure], [L.compliance, L.overlap, L.alignment], [L.installation, L.locationConstraint, L.ventilationConstraint]];
    const bw = 517, bh = Math.max(...bottom.map(a => panelHeight(bw, a)));
    bottom.forEach((a, i) => panel(20 + i * 533, y, bw, a, { h: bh, stroke: i === 2 ? C.gold : C.green }));
    finish('summit_hazard_taxonomy', 3, 4, 1624, y + bh + 20);
  }
  {
    start('summit_standards_framework', 4, 6); const top = [[L.installSafety, L.nfpa855, L.nfpa70], [L.testing, L.ul9540, L.ul9540a], [L.international, L.iec]];
    const w = 500, h = Math.max(...top.map(a => panelHeight(w, a)));
    top.forEach((a, i) => panel(20 + i * 520, 20, w, a, { h }));
    const left = [L.regionOverlap, L.vary, L.consistent], right = [L.insurance, L.fm, L.risk, L.fireProtection, L.loss];
    const y = h + 40, bh = Math.max(panelHeight(760, left), panelHeight(760, right));
    panel(20, y, 760, left, { h: bh }); panel(800, y, 760, right, { h: bh });
    const th = textHeight(L.bottom, 1540, 21); text(L.bottom, 20, y + bh + 20, 1540, th, 21, false, C.text, 'start');
    finish('summit_standards_framework', 4, 6, 1580, y + bh + th + 60);
  }

  // Preserve every voltage and branch of white-paper Figure 2, including both future topologies.
  {
    start('spec_fig2_power_systems', 2, 4); const W = 1820, bw = 208, gap = 74, xs = [130, 412, 694, 976, 1258, 1540], gridLabel = L.grid.split(' / ')[0]; let y = 20;
    const nodes = (at, data, minH = 0) => {
      const h = Math.max(minH, ...data.map(a => panelHeight(bw, a)));
      data.forEach((a, i) => { if (a.length) panel(xs[i], at, bw, a, { h, fill: '#FFFFFF', stroke: C.ink }); });
      return h;
    };
    const branch = (x, at, w, label, attachX, busY) => {
      const h = panelHeight(w, [label], 18);
      panel(x, at, w, [label], { h, size: 18, stroke: C.green, fill: C.pale });
      line(attachX, busY, attachX, at, C.green, 2);
      if (attachX !== x + w / 2) line(attachX, at, x + w / 2, at, C.green, 2);
      return h;
    };
    let th = textHeight(L.typical, 1700, 24, true); text(L.typical, 110, y, 1680, th, 24, true, C.ink, 'start'); y += th + 8;
    const firstY = y, h = nodes(y, [[L.substation, '≤500 kV AC'], [L.mv, '<69 kV AC'], [L.lv, '<1 kV AC'], [L.conversion, `400-480 V AC ${L.to} 50 V DC`], [], [L.it, L.rack50]], 190);
    const cy = y + h / 2;
    panel(20, y, 76, [gridLabel], { h, size: 15, stroke: C.ink, fill: '#FFFFFF' });
    arrow([[96, cy], [130, cy]]);
    for (let i = 0; i < 3; i++) {
      arrow([[xs[i] + bw, cy], [xs[i + 1], cy]]); text('AC', xs[i] + bw, cy - 68, gap, 62, 18, true, C.ink);
    }
    arrow([[1184, cy], [1540, cy]]); text('50 V DC', 1258, cy - 76, 230, 66, 20, true, C.ink);
    const by = y + h + 28;
    const b1 = branch(130, by, 230, L.outdoor, 234, y + h);
    const b2 = branch(400, by, 250, L.outdoor, 516, y + h);
    const b3 = branch(680, by, 270, L.indoorUPSGrid, 798, y + h);
    const b4 = branch(1240, by, 280, L.indoorBBU, 1360, cy);
    line(1360, cy, 1360, by, C.green, 2);
    // Source Figure 2 gives the typical BBU both an AC-side and a DC-bus connection.
    parts.push(`<path d="M940 ${cy} H960 V${by + b4 / 2} H1240" fill="none" stroke="${C.green}" stroke-width="2"/>`);
    const by2 = by + Math.max(b1, b2, b3, b4) + 16;
    const mvH = panelHeight(250, [L.indoorMV], 18), lvH = panelHeight(270, [L.indoorUPS], 18);
    panel(400, by2, 250, [L.indoorMV], { h: mvH, size: 18 });
    panel(680, by2, 270, [L.indoorUPS], { h: lvH, size: 18 });
    for (const [sourceX, routeX, targetX, targetY] of [[516, 390, 400, by2 + mvH / 2], [798, 668, 680, by2 + lvH / 2]]) {
      parts.push(`<path d="M${sourceX} ${y + h} V${y + h + 14} H${routeX} V${targetY} H${targetX}" fill="none" stroke="${C.green}" stroke-width="2"/>`);
    }
    y = by2 + Math.max(panelHeight(250, [L.indoorMV], 18), panelHeight(270, [L.indoorUPS], 18)) + 24;
    line(110, y, 1780, y, C.line, 2); y += 12;
    th = textHeight(L.emerging, 1680, 24, true); text(L.emerging, 110, y, 1680, th, 24, true, C.ink, 'start'); y += th + 8;
    const h2 = nodes(y, [[L.substation, '≤500 kV AC'], [L.mv, '<69 kV AC'], [L.lv, '<1 kV AC'], [L.conversion, `400-480 V AC ${L.to} 800 V ${L.or} ±400 V DC`], [L.dcConversion, `800 V ${L.or} ±400 V DC ${L.to} 50 V DC`], [L.it, L.rack50]], 210);
    const cy2 = y + h2 / 2;
    panel(20, y, 76, [gridLabel], { h: h2, size: 15, stroke: C.ink, fill: '#FFFFFF' }); arrow([[96, cy2], [130, cy2]]);
    for (let i = 0; i < 5; i++) {
      arrow([[xs[i] + bw, cy2], [xs[i + 1], cy2]]);
      if (i < 3) text('AC', xs[i] + bw, cy2 - 68, gap, 62, 18, true, C.ink);
    }
    const by3 = y + h2 + 160;
    const p1 = branch(398, by3, 270, L.outdoor, 670, cy2);
    const p2 = branch(966, by3, 280, L.indoorESS, 1216, cy2);
    const p3 = branch(1260, by3, 240, L.indoorBBU, 1248, cy2);
    const itH = panelHeight(bw, [L.it, L.rack800]);
    panel(1540, by3, bw, [L.it, L.rack800], { h: itH, fill: '#FFFFFF', stroke: C.ink });
    const bypassY = y + h2 + 112;
    arrow([[1184, cy2], [1216, cy2], [1216, bypassY], [1510, bypassY], [1510, by3 + itH / 2], [1540, by3 + itH / 2]]);
    // This explicit label belongs to the DC bypass, not to the AC distribution link.
    text(`800 V ${L.or} ±400 V DC`, 1258, y + h2 + 22, 270, 72, 18, true, C.ink);
    y = by3 + Math.max(p1, p2, p3, itH) + 32;
    line(110, y, 1780, y, C.line, 2); y += 28;
    const sstItems = [L.sst, `12-35 kV AC ${L.to} 800 V DC ${L.or} ±400 V DC`];
    const h3 = Math.max(panelHeight(300, sstItems), panelHeight(bw, [L.it, L.rack800]), 210);
    panel(20, y, 76, [gridLabel], { h: h3, size: 15, stroke: C.ink, fill: '#FFFFFF' });
    panel(130, y, bw, [L.substation, '≤500 kV AC'], { h: h3, fill: '#FFFFFF', stroke: C.ink });
    panel(510, y, 300, sstItems, { h: h3, fill: '#FFFFFF', stroke: C.ink });
    panel(1540, y, bw, [L.it, L.rack800], { h: h3, fill: '#FFFFFF', stroke: C.ink });
    const cy3 = y + h3 / 2; arrow([[96, cy3], [130, cy3]]); arrow([[338, cy3], [510, cy3]]); text('AC', 366, cy3 - 68, 116, 62, 18, true, C.ink);
    arrow([[810, cy3], [1540, cy3]]); text(`800 V ${L.or} ±400 V DC`, 1050, cy3 - 78, 360, 72, 20, true, C.ink);
    const by4 = y + h3 + 28;
    const bh = Math.max(branch(510, by4, 300, L.outdoor, 900, cy3), branch(970, by4, 280, L.indoorESS, 1216, cy3), branch(1270, by4, 260, L.indoorBBU, 1248, cy3));
    finish('spec_fig2_power_systems', 2, 4, W, by4 + bh + 20);
  }

  {
    start('spec_appendix_a_matrix', 4, 7); const width = 1720, widths = [112, 420, 540, 608], starts = [20, 132, 552, 1092]; let y = 20;
    const headers = [L.ref, L.attribute, L.acceptable, L.optimum];
    const hh = Math.max(...headers.map((s, i) => textHeight(s, widths[i], 20, true)));
    headers.forEach((s, i) => { rect(starts[i], y, widths[i], hh, '#EDF0F2', C.gray, 0); text(s, starts[i], y, widths[i], hh, 20, true, C.ink); }); y += hh;
    const sh = textHeight(L.suppression, 1568, 22, true);
    rect(20, y, 1680, sh, '#EAF4E1', C.gray, 0); text('2.3', 20, y, 112, sh, 20, true); text(L.suppression, 132, y, 1568, sh, 22, true, C.ink, 'start'); y += sh;
    const rows = [
      ['2.3-A', L.autoFire, L.complyNFPA, slide(4, 7).bullets[0].text],
      ['2.3-B', L.segregated, L.sprinklers, L.flammables],
      ['2.3-C', L.gasSmoke, L.fireCodes, L.redundant],
      ['2.3-D', L.ventilation, L.electrochemical, L.enhancedVentilation],
      ['2.3-E', L.technology, L.capacity, L.selectTech],
    ];
    rows.forEach(row => {
      const h = Math.max(...row.map((s, i) => textHeight(s, widths[i], 20, i < 2)));
      row.forEach((s, i) => { rect(starts[i], y, widths[i], h, '#FFFFFF', C.gray, 0); text(s, starts[i], y, widths[i], h, 20, i < 2, i === 2 ? '#225BA8' : C.text, i ? 'start' : 'middle'); }); y += h;
    });
    finish('spec_appendix_a_matrix', 4, 7, width, y + 20, 'figures/spec_appendix_a_matrix.png', 'White-paper Appendix A, page 44, rows 2.3-A through 2.3-E. Empty 2.3-F source row omitted. Minimum-compliance sentence reused verbatim from localized learner text (M4S7 bullet 1). Other cells are faithful source-label translations.');
  }

  {
    start('spec_location_and_barriers', 3, 5); const width = 1580; let y = 20;
    const prefH = textHeight(L.preferences, 1560, 24, true); text(L.preferences, 10, y, 1560, prefH, 24, true, C.ink, 'start'); y += prefH + 8;
    const top = y;
    text(L.enclosures, 220, top, 300, 84, 22, true, C.ink);
    rect(240, top + 120, 70, 176, '#FFFFFF', C.gray, 0); text('1', 240, top + 120, 70, 176, 24, true);
    rect(430, top + 120, 70, 176, '#FFFFFF', C.gray, 0); text('1', 430, top + 120, 70, 176, 24, true);
    text(L.critical, 10, top + 150, 180, 130, 20);
    line(210, top + 235, 210, top + 265, C.gray, 2); dim(210, top + 250, 240, top + 250);
    text('FMDS 1-20 HC-3', 10, top + 60, 210, 112, 17);
    text(L.see232, 310, top + 60, 120, 110, 18);
    dim(310, top + 180, 430, top + 180);
    rect(810, top + 62, 360, 390, '#FFFFFF', C.gray, 0);
    rect(1170, top + 62, 64, 64, '#FFFFFF', C.gray, 0); text('3', 1170, top + 62, 64, 64, 18, true);
    rect(1040, top + 310, 130, 142, '#FFFFFF', C.gray, 0); text('4', 1040, top + 310, 130, 142, 24, true);
    rect(880, top + 360, 94, 92, '#FFFFFF', C.gray, 0); text('5', 880, top + 360, 94, 92, 24, true);
    dim(500, top + 218, 810, top + 218); text('FMDS 1-20 HC-3', 500, top + 100, 310, 108, 20);
    rect(360, top + 380, 140, 130, '#FFFFFF', C.gray, 0); text('2', 360, top + 380, 140, 130, 24, true);
    text(L.critical, 10, top + 370, 180, 130, 20); line(210, top + 435, 210, top + 465, C.gray, 2); dim(210, top + 450, 360, top + 450);
    text('FMDS 1-20 HC-3', 120, top + 288, 220, 102, 17);
    dim(500, top + 420, 810, top + 420); text('FMDS 1-20 HC-3', 500, top + 308, 310, 102, 20);
    text(L.dedicated, 290, top + 520, 280, 112, 20);
    text(L.cutoff, 950, top + 464, 300, 100, 20);
    let ly = top + 16;
    for (const s of [L.dedicatedEnclosures, L.dedicatedBuilding, L.exteriorRoom, L.cornerRoom, L.interiorRoom]) {
      const lh = textHeight(s, 310, 19); text(s, 1250, ly, 310, lh, 19, false, C.text, 'start'); ly += lh + 6;
    }
    y = Math.max(top + 650, ly) + 10;
    line(20, y, 1560, y, C.line, 2); y += 10;
    const barrierH = textHeight(L.barriers, 1540, 24, true); text(L.barriers, 20, y, 1540, barrierH, 24, true, C.ink, 'start'); y += barrierH + 4;
    const sy = y; rect(340, sy + 20, 1200, 590, '#FFFFFF', C.gray, 0);
    const rx = 420, rw = 800, cell = 80, rowYs = [sy + 120, sy + 222, sy + 408, sy + 510];
    rowYs.forEach(ry => { for (let i = 0; i < 10; i++) rect(rx + i * cell, ry, cell, 66, '#FFFFFF', C.gray, 0); });
    const wall1 = 684, wall2 = 954;
    for (const bx of [wall1, wall2]) { line(bx, sy + 76, bx, sy + 332, C.ink, 4); line(bx, sy + 370, bx, sy + 590, C.ink, 4); }
    text(L.solidFire, 20, sy + 22, 300, 160, 20, false, C.text);
    arrow([[310, sy + 114], [370, sy + 114], [wall1, sy + 96]], C.gray, 11);
    arrow([[310, sy + 88], [370, sy + 88], [wall2, sy + 76]], C.gray, 11);
    text('x', 615, sy + 288, 68, 70, 18); arrow([[690, sy + 322], [756, sy + 322]], C.gray, 9);
    text('x = 12 in. (0.3 m)', 980, sy + 288, 250, 72, 20);
    line(1236, sy + 288, 1286, sy + 288, C.gray, 2); line(1236, sy + 408, 1286, sy + 408, C.gray, 2);
    dim(1260, sy + 288, 1260, sy + 408); text('6 ft (1.8 m)', 1280, sy + 302, 240, 86, 20);
    for (let i = 0; i < 3; i++) { line(420 + i * 88, sy + 484, 496 + i * 88, sy + 484, C.ink, 3); line(420 + i * 88, sy + 500, 496 + i * 88, sy + 500, C.ink, 3); }
    text(L.solidMetal, 20, sy + 400, 300, 160, 20);
    arrow([[310, sy + 478], [420, sy + 484]], C.gray, 11); arrow([[310, sy + 508], [420, sy + 500]], C.gray, 11);
    // The original brace annotates the final row's 6 ft (1.8 m) depth.
    line(1236, sy + 510, 1286, sy + 510, C.gray, 2); line(1236, sy + 576, 1286, sy + 576, C.gray, 2);
    dim(1260, sy + 510, 1260, sy + 576); text('6 ft (1.8 m)', 1280, sy + 502, 240, 86, 20);
    finish('spec_location_and_barriers', 3, 5, width, sy + 630, 'figures/spec_location_and_barriers.png', 'Faithful reconstruction of white-paper Figures 3 and 4 (PDF pages 26-27); restores the cropped 1-5 location legend from page 26. FMDS 1-20 HC-3, section 2.3.2, 12 in. (0.3 m), and both 6 ft (1.8 m) annotations preserved.');
  }
  return figures;
}
