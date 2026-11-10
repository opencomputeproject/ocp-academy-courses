import fs from 'node:fs/promises';
import path from 'node:path';
import { here, locales, scenes, readJSON, writeJSON, probe, sha256, option, resolveAudio } from './lib.mjs';

const catalog = await readJSON(path.join(here, 'labels.json'));
const result = { schema_version: 1, instructions: 'Fill cues_ms from the final WAV, review them against approved narration, then set cues_reviewed=true. Do not scale preview cues proportionally. Empty values are intentionally not encodeable.', editions: {} };
for (const locale of option('--locale') ? [option('--locale')] : locales) {
  result.editions[locale] = {};
  for (const [id, scene] of Object.entries(scenes)) {
    if (id === 'M4S8' || (option('--slide') && option('--slide') !== id)) continue;
    const audioRelative = catalog.editions[locale][id].audio.replace(/\.[^.]+$/, '.wav');
    const filename = resolveAudio(locale, audioRelative);
    let exists = true;
    try { await fs.access(filename); } catch { exists = false; }
    result.editions[locale][id] = {
      narration_path: audioRelative, narration_sha256: exists ? await sha256(filename) : null,
      duration_ms: exists ? Number(probe(filename).format.duration) * 1000 : null,
      final_audio_verified: false, human_audio_review: 'pending', cues_reviewed: false,
      cues_ms: Object.fromEntries(scene.cues.map(cue => [cue, null])),
    };
  }
}
const out = path.resolve(option('--output') || path.join(here, 'timings.template.json'));
await writeJSON(out, result);
console.log(out);
