import path from 'node:path';
import { here, readJSON, writeJSON, sha256, resolveAudio, option, editionRoot } from './lib.mjs';
import { withLock } from './locks.mjs';
const selections = await readJSON(path.join(here, 'cue-selections.json'));
if (option('--locale') && option('--locales')) throw new Error('Choose --locale or --locales');
const selected = option('--locales')?.split(',') || (option('--locale') ? [option('--locale')] : Object.keys(selections.editions));
selected.forEach(editionRoot);
await withLock('timings', async () => {
const target = path.join(here, 'timings.final.json');
let result;
try { result = await readJSON(target); } catch (error) { if (error.code !== 'ENOENT') throw error; result = { schema_version: 1, method: selections.method, editions: {} }; }
for (const locale of selected) {
  const entries = selections.editions[locale];
  if (!entries) throw new Error(`${locale}: no cue selections`);
  result.editions[locale] = {};
  for (const [id, selection] of Object.entries(entries)) {
    if (!selection.reviewed) continue;
    const audio = await readJSON(path.join(here, 'alignment', locale, `${id}.audio.json`));
    if (selection.narration_sha256 && selection.narration_sha256 !== audio.narration_sha256) throw new Error(`${locale}/${id}: selected cues belong to a different WAV`);
    if (await sha256(resolveAudio(locale, audio.narration_path)) !== audio.narration_sha256) throw new Error(`${locale}/${id}: audio changed; rerun alignment and review cues`);
    result.editions[locale][id] = { ...audio, cues_reviewed: true, cues_ms: selection.cues_ms, anchors: selection.anchors };
  }
}
await writeJSON(target, result);
}, 60000);
console.log(`Updated hash-bound reviewed timing editions: ${selected.join(', ')}`);
