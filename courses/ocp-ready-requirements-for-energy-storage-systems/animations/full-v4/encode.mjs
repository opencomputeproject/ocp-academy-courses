import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { spawn, spawnSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import assert from 'node:assert/strict';
import { here, repoRoot, courseRoot, audioRoot, editionRoot, locales, scenes, readJSON, writeJSON, chromium, sha256, option, run, timingFor, sourcesMatch, encodingPermitted } from './lib.mjs';
import { withLock } from './locks.mjs';
import { build } from './build.mjs';
import { qa } from './qa.mjs';
import { verifiedScriptHash } from './script_binding.mjs';

const selectedLocales = option('--locale') ? [option('--locale')] : locales;
const selectedScenes = option('--slide') ? [option('--slide')] : Object.keys(scenes);
let timings = option('--timings') ? await readJSON(path.resolve(option('--timings'))) : undefined;
if (!timings && selectedScenes.some(id => id !== 'M4S8')) throw new Error('Final timing file required: --timings <reviewed.json>. Preview clocks cannot be encoded.');
const recorder = path.resolve(option('--recorder') || path.join(repoRoot, 'skills/academy-wizard/scripts/record_css_animation.mjs'));
const recorderHash = await sha256(recorder);
const moduleDir = process.env.PLAYWRIGHT_NODE_MODULES || path.join(os.homedir(), '.codex/skills/academy-wizard/node_modules');
const ffmpeg = process.env.FFMPEG_BIN || 'ffmpeg';
run(ffmpeg, ['-version']);
const rgbDecode = 'zscale=matrixin=709:rangein=limited:matrix=gbr:range=full,format=gbrp,format=rgb24';
function metric(name, reference, decoded) {
  const r = spawnSync(ffmpeg, ['-hide_banner', '-i', reference, '-i', decoded, '-lavfi', `[0:v]format=gbrp[a];[1:v]format=gbrp[b];[a][b]${name}`, '-f', 'null', '-'], { encoding: 'utf8' });
  if (r.status !== 0) throw new Error(r.stderr);
  const match = r.stderr.match(name === 'ssim' ? /All:([\d.]+)/ : /average:([\d.]+|inf)/);
  if (!match) throw new Error(`Cannot read ${name} result`);
  return match[1] === 'inf' ? 999 : Number(match[1]);
}

async function selectScale(source, duration, cache) {
  const browser = await (await chromium()).launch({ headless: true, args: ['--mute-audio'] });
  try {
    for (const scale of option('--scale') ? [Number(option('--scale'))] : [1, 1.5, 2]) {
      assert(scale >= 1 && scale <= 3, 'Scale must be between 1 and 3');
      const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: scale });
      await page.goto(pathToFileURL(source).href);
      await page.evaluate(() => document.fonts.ready);
      await page.evaluate(t => window.setTeachingTime(t), duration);
      const reference = path.join(cache, 'resolution-reference.png'), encoded = path.join(cache, 'resolution-test.mp4'), decoded = path.join(cache, 'resolution-decoded.png');
      await page.screenshot({ path: reference });
      await page.close();
      run(ffmpeg, ['-y', '-v', 'error', '-i', reference, '-vf', 'scale=out_color_matrix=bt709:out_range=tv:flags=bicubic+accurate_rnd', '-c:v', 'libx264', '-preset', 'slow', '-tune', 'animation', '-crf', '8', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-frames:v', '1', encoded]);
      run(ffmpeg, ['-y', '-v', 'error', '-i', encoded, '-vf', rgbDecode, '-frames:v', '1', decoded]);
      const ssim = metric('ssim', reference, decoded), psnr = metric('psnr', reference, decoded);
      console.log(`Resolution preflight ${1920 * scale}x${1080 * scale}: SSIM ${ssim}, RGB PSNR ${psnr} dB`);
      if (ssim >= .995 && psnr >= 45) return scale;
    }
    throw new Error('Resolution preflight failed; inspect source and decoded calibration frames before encoding');
  } finally { await browser.close(); }
}

async function encodeOne(locale, id) {
  const policy = await readJSON(path.join(here, 'encoding-policy.json'));
  if (!encodingPermitted(policy, locale, id)) {
    console.log(`${locale}/${id}: deferred by localized editorial/audio hold`);
    return;
  }
  if (option('--timings')) timings = await readJSON(path.resolve(option('--timings')));
  if (!scenes[id]) throw new Error(`Unknown scene: ${id}`);
  if (locale !== 'en-US' && id !== 'M4S8') {
    assert(audioRoot, 'External final audio root required');
    const summary = await readJSON(path.join(path.resolve(audioRoot), 'semantic-regeneration-summary.json'));
    const readiness = summary.find(entry => entry.locale === locale);
    assert(readiness?.status === 'verified' && readiness.clips.every(clip => clip.generated && clip.audio_qa_flags.length === 0), `${locale}: revised semantic generation is not verified`);
  }
  if (id !== 'M4S8' && !timings?.editions?.[locale]?.[id]?.cues_reviewed && process.argv.includes('--ready-only')) {
    console.log(`${locale}/${id}: deferred (final cues pending)`);
    return;
  }
  const manifestPath = path.join(here, 'figure-patch-manifest.json');
  const currentTiming = await timingFor(locale, id, timings);
  const scriptHash = id === 'M4S8' ? null : await verifiedScriptHash(locale, currentTiming);
  const sourceRoot = editionRoot(locale);
  const outputRoot = option('--output-root') ? path.join(path.resolve(option('--output-root')), locale, path.basename(courseRoot)) : sourceRoot;
  if (process.argv.includes('--resume')) {
    const existing = (await readJSON(manifestPath)).editions[locale].figures[id];
    if (existing.encoded) {
      const sameTiming = existing.encoded.narration_sha256 === (currentTiming.narration_sha256 || null) && JSON.stringify(existing.timing.cues_ms) === JSON.stringify(currentTiming.cues_ms);
      const sameScript = (existing.figure.narration_script_sha256 || null) === scriptHash;
      try {
        const validSource = await sourcesMatch(sourceRoot, existing);
        if (sameTiming && sameScript && validSource && await sha256(path.join(sourceRoot, existing.figure.path)) === existing.encoded.sha256) {
          if (outputRoot !== sourceRoot) {
            await fs.mkdir(path.join(outputRoot, 'figures'), { recursive: true });
            for (const relative of [existing.figure.path, existing.figure.poster, existing.source_html, existing.geometry_snapshot]) await fs.copyFile(path.join(sourceRoot, relative), path.join(outputRoot, relative));
          }
          console.log(`${locale}/${id}: retained matching verified encode`);
          return;
        }
      } catch (error) { if (error.code !== 'ENOENT') throw error; }
    }
  }
  await build({ timings, selectedLocales: [locale], selectedScenes: [id] });
  const manifest = await readJSON(manifestPath), item = manifest.editions[locale].figures[id];
  assert(item.timing.mode !== 'preview-only', `${locale}/${id}: preview timing is not encodeable`);
  await fs.mkdir(path.join(outputRoot, 'figures'), { recursive: true });
  const source = path.join(sourceRoot, item.source_html);
  const output = path.join(outputRoot, item.figure.path), poster = path.join(outputRoot, item.figure.poster);
  const cache = path.join(here, '.cache', 'jobs', locale, id);
  await fs.mkdir(cache, { recursive: true });
  const localRecorder = path.join(cache, 'record_css_animation.mjs');
  await fs.copyFile(recorder, localRecorder);
  try { await fs.symlink(moduleDir, path.join(cache, 'node_modules'), 'dir'); } catch (error) { if (error.code !== 'EEXIST') throw error; }
  await qa({ selectedLocales: [locale], selectedScenes: [id] });
  const partial = output.replace(/\.mp4$/, '.partial.mp4');
  const scale = await selectScale(source, item.timing.duration_ms, cache);
  console.log(`Encoding ${locale}/${id}: ${item.timing.duration_ms.toFixed(3)} ms; PNG -> H.264; maintained recorder ${recorderHash.slice(0, 12)}`);
  const child = spawn(process.execPath, [localRecorder, source, partial, poster, String(item.timing.duration_ms), String(item.timing.poster_ms), '30'], { stdio: 'inherit', env: { ...process.env, FFMPEG_BIN: ffmpeg, ACADEMY_ANIMATION_SCALE: String(scale) } });
  const code = await new Promise((resolve, reject) => { child.on('error', reject); child.on('close', resolve); });
  if (code !== 0) throw new Error(`Recorder failed (${code}); existing approved output was not replaced`);

  const browser = await (await chromium()).launch({ headless: true, args: ['--mute-audio'] });
  let media;
  try {
    const page = await browser.newPage();
    await page.goto(pathToFileURL(source).href);
    media = await page.evaluate(async url => {
      const video = document.createElement('video');
      video.muted = true;
      video.src = url;
      document.body.appendChild(video);
      await new Promise((resolve, reject) => { video.onloadedmetadata = resolve; video.onerror = () => reject(new Error('Video metadata failed')); });
      return { duration: video.duration, width: video.videoWidth, height: video.videoHeight };
    }, pathToFileURL(partial).href);
  } finally { await browser.close(); }
  assert(media.width >= 1920 && media.height >= 1080, 'Encoded dimensions below 1080p');
  assert(Math.abs(media.duration * 1000 - item.timing.duration_ms) <= 1000 / 30 + 1, 'Encoded duration differs by more than one frame');
  const noAudio = spawnSync(ffmpeg, ['-v', 'error', '-i', partial, '-map', '0:a:0', '-f', 'null', '-'], { encoding: 'utf8' });
  assert(noAudio.status !== 0 && /matches no streams|does not contain any stream/i.test(noAudio.stderr), `Expected silent media: ${noAudio.stderr}`);
  const qaDir = path.join(here, 'qa', locale, id);
  const decoded = path.join(qaDir, 'decoded-final.png');
  run(ffmpeg, ['-y', '-v', 'error', '-ss', String(Math.max(0, media.duration - 0.1)), '-i', partial, '-frames:v', '1', '-vf', rgbDecode, decoded]);
  const metrics = { ssim: metric('ssim', poster, decoded), psnr_db: metric('psnr', poster, decoded), comparison: 'Full-range RGB; decoded from BT.709 limited range with zscale' };
  await writeJSON(path.join(qaDir, 'encode-quality.json'), { ...media, ...metrics, duration_error_ms: media.duration * 1000 - item.timing.duration_ms, decoded_frame: path.relative(here, decoded), reference_frame: item.figure.poster });
  assert(metrics.ssim >= .995 && metrics.psnr_db >= 45, `Fidelity review required: ${JSON.stringify(metrics)}. Partial retained for diagnosis.`);
  if (scriptHash) assert.equal(await verifiedScriptHash(locale, item.timing), scriptHash, 'Script/audio changed during encoding');
  await fs.rename(partial, output);
  if (outputRoot !== sourceRoot) {
    await fs.copyFile(source, path.join(outputRoot, item.source_html));
    await fs.copyFile(path.join(sourceRoot, item.geometry_snapshot), path.join(outputRoot, item.geometry_snapshot));
  }
  item.status = 'encoded-awaiting-visual-and-player-review';
  item.render.width = media.width;
  item.render.height = media.height;
  item.figure.duration_seconds = media.duration;
  if (scriptHash) item.figure.narration_script_sha256 = scriptHash;
  item.encoded = { ...media, ...metrics, path: item.figure.path, poster: item.figure.poster, sha256: await sha256(output), source_html_sha256: await sha256(source), geometry_source_sha256: await sha256(path.join(sourceRoot, item.geometry_snapshot)), narration_sha256: item.timing.narration_sha256 || null, recorder: path.relative(repoRoot, recorder), recorder_sha256: recorderHash, fps: 30, audio_streams: 0, human_audio_review: 'pending' };
  item.inventory_candidate = { review_required: true, sha256: item.encoded.sha256, entries: item.visible_text.map(text => ({ text, at_seconds: Math.max(0, media.duration - 0.5) })) };
  await withLock('manifest', async () => {
    const latestManifest = await readJSON(manifestPath);
    latestManifest.editions[locale].figures[id] = item;
    await writeJSON(manifestPath, latestManifest);
  }, 60000);
  await writeJSON(path.join(qaDir, 'encode-receipt.json'), item.encoded);
  console.log(`${locale}/${id}: encoded ${media.width}x${media.height}, SSIM ${metrics.ssim}, PSNR ${metrics.psnr_db} dB; visual/player review pending`);
}

for (const locale of selectedLocales) for (const id of selectedScenes) {
  editionRoot(locale);
  if (!scenes[id]) throw new Error(`Unknown scene ${id}`);
  await withLock(`job-${locale}-${id}`, () => encodeOne(locale, id));
}
