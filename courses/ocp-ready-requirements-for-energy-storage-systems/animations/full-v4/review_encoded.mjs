import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';
import { here, editionRoot, readJSON, writeJSON, option, chromium, run, sha256 } from './lib.mjs';

const locale = option('--locale'), id = option('--slide');
if (!locale || !id) throw new Error('Usage: node review_encoded.mjs --locale en-US --slide M1S3');
const manifest = await readJSON(path.join(here, 'figure-patch-manifest.json'));
const item = manifest.editions[locale].figures[id];
assert(item.encoded, 'Encode must exist before review');
const root = editionRoot(locale), video = path.join(root, item.figure.path);
assert.equal(await sha256(video), item.encoded.sha256, 'Encoded video changed');
const ffmpeg = process.env.FFMPEG_BIN || 'ffmpeg';
const directory = path.join(here, 'qa', locale, id, 'encoded-review');
await fs.mkdir(directory, { recursive: true });
const browser = await (await chromium()).launch({ headless: true, args: ['--mute-audio'] });
try {
  const page = await browser.newPage({ viewport: { width: item.encoded.width, height: item.encoded.height } });
  await page.goto(pathToFileURL(path.join(root, item.source_html)).href);
  const transitions = await page.evaluate(() => window.animationQA().transitions);
  const midpoints = transitions.flatMap((t, i) => i % 2 ? [] : [(t + transitions[i + 1]) / 2000]);
  const duration = item.encoded.duration;
  const frames = [...new Set([0, duration * .25, duration * .5, duration * .75, duration - 1 / 30, ...midpoints, ...transitions.flatMap(t => [(t - 34) / 1000, (t + 34) / 1000])].map(t => Math.max(0, Math.min(Math.round(duration * 30) - 1, Math.floor(t * 30)))))].sort((a, b) => a - b);
  // Select exact decoded indices in one pass, avoiding repeated GOP decoding per sample.
  const extraction = await fs.mkdtemp(path.join(directory, 'extract-'));
  try {
    const select = frames.map(frame => `eq(n\\,${frame})`).join('+');
    run(ffmpeg, ['-y', '-v', 'error', '-i', video, '-vf', `select=${select},zscale=matrixin=709:rangein=limited:matrix=gbr:range=full,format=gbrp,format=rgb24`, '-fps_mode', 'vfr', '-start_number', '0', path.join(extraction, '%05d.png')]);
    assert.equal((await fs.readdir(extraction)).length, frames.length, 'Missing exact-index decoded samples');
    for (const [index, frame] of frames.entries()) await fs.rename(path.join(extraction, `${String(index).padStart(5, '0')}.png`), path.join(directory, `${String(frame).padStart(5, '0')}.png`));
  } finally { await fs.rm(extraction, { recursive: true, force: true }); }
  const samples = [0, .25, .5, .75, .999].map(f => frames.reduce((best, n) => Math.abs(n / 30 - duration * f) < Math.abs(best / 30 - duration * f) ? n : best, 0));
  const images = [];
  for (const frame of samples) images.push(`<section><div>${(frame / 30).toFixed(2)} s</div><img width="768" height="432" src="data:image/png;base64,${(await fs.readFile(path.join(directory, `${String(frame).padStart(5, '0')}.png`))).toString('base64')}"></section>`);
  await page.setViewportSize({ width: 1536, height: 1392 });
  await page.setContent(`<body style="margin:0;background:#eee;display:grid;grid-template-columns:768px 768px;font:16px Arial">${images.join('')}</body>`);
  await page.screenshot({ path: path.join(directory, 'five-frame-contact-sheet.png') });
  for (let start = 0; start < frames.length; start += 12) {
    const tiles = [];
    for (const frame of frames.slice(start, start + 12)) tiles.push(`<section><div>${frame} / ${(frame / 30).toFixed(3)} s</div><img width="640" height="360" src="data:image/png;base64,${(await fs.readFile(path.join(directory, `${String(frame).padStart(5, '0')}.png`))).toString('base64')}"></section>`);
    await page.setViewportSize({ width: 1920, height: Math.ceil(tiles.length / 3) * 384 });
    await page.setContent(`<body style="margin:0;background:#eee;display:grid;grid-template-columns:repeat(3,640px);font:16px/24px Arial">${tiles.join('')}</body>`);
    await page.screenshot({ path: path.join(directory, `transition-sheet-${String(start / 12 + 1).padStart(2, '0')}.png`) });
  }
  const finalPng = path.join(directory, `${String(frames.at(-1)).padStart(5, '0')}.png`);
  const detailOrigin = ({ M1S3: [300, 85], M2S6: [1530, 235], M3S6: [90, 270], M4S8: [160, 230] })[id];
  const sourceScale = item.encoded.width / 1920;
  const detailImages = [];
  for (const [label, image] of [['Lossless source', path.join(root, item.figure.poster)], ['Decoded video', finalPng]]) {
    detailImages.push(`<section><div>${label}, 200% native pixels</div><div style="width:900px;height:400px;overflow:hidden;position:relative"><img style="position:absolute;width:${item.encoded.width * 2}px;height:${item.encoded.height * 2}px;left:${-detailOrigin[0] * sourceScale * 2}px;top:${-detailOrigin[1] * sourceScale * 2}px" src="data:image/png;base64,${(await fs.readFile(image)).toString('base64')}"></div></section>`);
  }
  await page.setViewportSize({ width: 1800, height: 440 });
  await page.setContent(`<body style="margin:0;background:#eee;display:grid;grid-template-columns:900px 900px;font:16px Arial">${detailImages.join('')}</body>`);
  await page.screenshot({ path: path.join(directory, 'detail-200percent.png') });
  const border = JSON.parse(run('python3', ['-c', 'import json,sys; from PIL import Image; a=Image.open(sys.argv[1]).convert("RGB"); w,h=a.size; v=[a.getpixel((x,y)) for x in range(w) for y in (0,h-1)]+[a.getpixel((x,y)) for y in range(h) for x in (0,w-1)]; print(json.dumps({"minimum_channel":min(min(p) for p in v),"maximum_channel":max(max(p) for p in v)}))', path.join(directory, `${String(frames.at(-1)).padStart(5, '0')}.png`)]));
  assert(border.minimum_channel >= 250, 'Outer video pixels are not clean white');
  await writeJSON(path.join(directory, 'review-evidence.json'), { locale, scene: id, video_sha256: item.encoded.sha256, source_html_sha256: await sha256(path.join(root, item.source_html)), geometry_source_sha256: await sha256(path.join(root, item.geometry_snapshot)), sampled_frame_indices: frames, border, native_size: [item.encoded.width, item.encoded.height], human_audio_review: 'pending', visual_review: 'pending', integrated_player_review: 'pending' });
} finally { await browser.close(); }
