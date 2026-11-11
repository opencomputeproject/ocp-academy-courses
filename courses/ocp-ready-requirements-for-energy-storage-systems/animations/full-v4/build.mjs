import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { here, courseRoot, locales, scenes, editionRoot, readJSON, writeJSON, timingFor, sourcesMatch, encodingPermitted } from './lib.mjs';
import { withLock } from './locks.mjs';

async function buildUnlocked({ timings, selectedLocales = locales, selectedScenes = Object.keys(scenes) } = {}) {
  const catalog = await readJSON(path.join(here, 'labels.json'));
  const policy = await readJSON(path.join(here, 'encoding-policy.json'));
  const qualifiers = await readJSON(path.join(here, 'qualifiers.json'));
  const script = await fs.readFile(path.join(here, 'scene.js'), 'utf8');
  const manifestPath = path.join(here, 'figure-patch-manifest.json');
  let manifest;
  try { manifest = await readJSON(manifestPath); } catch { manifest = { schema_version: 1, course_slug: path.basename(courseRoot), application: 'Replace only listed slide.figure objects after encoding and review. Preserve every other field. This tool never edits course.json.', editions: {} }; }
  delete manifest.course_metadata_merge;
  delete manifest.approved_exceptions;
  manifest.global_teaching_video_mode = 'Leave unset: mixed narration-synchronized and retained independent-loop media; rely on explicit figure flags.';
  manifest.preserved_playback = [{ slide: 'M4S8', mode: 'independent-loop', duration_ms: 14000, reason: 'Preserve existing approved course loop:true behavior during rebuild. No new approval of cyclic purpose is asserted.' }];
  manifest.localized_encoding_hold = policy.localized_encoding_hold;
  for (const locale of selectedLocales) {
    const root = editionRoot(locale);
    manifest.editions[locale] ||= { course_json: path.relative(courseRoot, path.join(root, 'course.json')), figures: {} };
    for (const id of selectedScenes) {
      const descriptor = scenes[id];
      const labels = catalog.editions[locale][id];
      const timing = await timingFor(locale, id, timings);
      const previous = manifest.editions[locale].figures[id];
      const config = { scene: id, locale, labels, timing, qualifier: qualifiers[locale] };
      const prefix = `figures/${descriptor.stem}`;
      const html = `<!doctype html>\n<html lang="${locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${id} editable teaching animation</title><style>html,body{margin:0;padding:0;width:100%;height:100%;background:#fff;overflow:hidden}svg{display:block;width:100%;height:100%;letter-spacing:0}</style></head><body data-duration-ms="${timing.duration_ms}" data-poster-ms="${timing.poster_ms}"><svg id="scene" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" role="img" aria-label="${labels.alt.replaceAll('&', '&amp;').replaceAll('"', '&quot;')}"></svg><script>window.SCENE=${JSON.stringify(config).replaceAll('<', '\\u003c')};</script><script>${script}</script></body></html>\n`;
      await fs.mkdir(path.join(root, 'figures'), { recursive: true });
      await fs.writeFile(path.join(root, `${prefix}_source.html`), html);
      const figure = { source: 'custom', path: `${prefix}.mp4`, media_type: 'video', poster: `${prefix}_poster.png`, alt: labels.alt, caption: labels.caption, sync_to_narration: id !== 'M4S8', autoplay: id === 'M4S8', loop: id === 'M4S8', muted: true };
      manifest.editions[locale].figures[id] = {
        module_number: descriptor.module, slide_number: descriptor.slide, slide_id: labels.slide_id, slug: labels.slug,
        operation: 'replace-figure-after-encode-qa', figure,
        source_html: `${prefix}_source.html`, geometry_snapshot: `${prefix}_geometry.svg`,
        expected_audio: { root_argument: '--audio-root', locale, course_slug: path.basename(courseRoot), path: labels.audio.replace(/\.[^.]+$/, '.wav') },
        timing, render: { width: 1920, height: 1080, fps: 30, lossless_input: 'PNG', encoder: 'libx264', crf: 8, preset: 'slow', audio_streams: 0 },
        visible_text: id === 'M4S8' ? labels.steps.flatMap(s => [s.label, s.detail]).concat(labels.loop_label, Array.from({ length: 8 }, (_, i) => String(i + 1).padStart(2, '0'))) : labels.labels.concat(['M1S3', 'M2S6'].includes(id) ? qualifiers[locale] : []),
        source_refs: labels.source_refs,
        status: timing.mode === 'preview-only' ? 'source-ready-awaiting-final-audio-and-cues' : 'source-ready-awaiting-encode',
      };
      const current = manifest.editions[locale].figures[id];
      const sameSource = await sourcesMatch(root, { ...current, encoded: previous?.encoded });
      if (sameSource) {
        current.encoded = previous.encoded;
        current.inventory_candidate = previous.inventory_candidate;
        current.render = previous.render;
        current.status = previous.status;
        if (previous.visual_review) current.visual_review = previous.visual_review;
        if (previous.figure.text_inventory) current.figure.text_inventory = previous.figure.text_inventory;
        current.figure.duration_seconds = previous.encoded.duration;
        if (previous.figure.narration_script_sha256) current.figure.narration_script_sha256 = previous.figure.narration_script_sha256;
      }
      if (!encodingPermitted(policy, locale, id)) current.status = 'held-for-localized-text-and-audio-review';
    }
  }
  await writeJSON(manifestPath, manifest);
  return manifest;
}

export async function build(options) { return withLock('manifest', () => buildUnlocked(options), 60000); }

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const value = flag => args.includes(flag) ? args[args.indexOf(flag) + 1] : undefined;
  const timings = value('--timings') ? await readJSON(path.resolve(value('--timings'))) : undefined;
  await build({ timings, selectedLocales: value('--locale') ? [value('--locale')] : locales, selectedScenes: value('--slide') ? [value('--slide')] : Object.keys(scenes) });
  console.log('Built editable sources and figure-patch-manifest.json. No course.json or videos were changed.');
}
