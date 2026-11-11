import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';

export const here = path.dirname(fileURLToPath(import.meta.url));
export const option = flag => process.argv.includes(flag) ? process.argv[process.argv.indexOf(flag) + 1] : undefined;
export const courseRoot = path.resolve(option('--course-root') || path.resolve(here, '../..'));
export const repoRoot = path.resolve(here, '../../../..');
export const locales = ['en-US', 'es-419', 'ja-JP', 'ko-KR', 'pt-BR', 'vi-VN', 'zh-CN', 'zh-TW'];
export const audioRoot = option('--audio-root') || process.env.ESS_AUDIO_ROOT;
export function encodingPermitted(policy, locale, id) {
  return !policy.localized_encoding_hold || policy.permitted_locales.includes(locale)
    || (id === 'M4S8' && policy.permitted_independent_loops?.M4S8?.includes(locale));
}
export const scenes = {
  M1S3: { module: 1, slide: 3, stem: 'ess_m1_deployment_shift', cues: ['centralized', 'distributed', 'placements'], preview: [0, 8000, 14000] },
  M2S6: { module: 2, slide: 6, stem: 'ess_m2_charging_load', cues: ['it', 'facility', 'recharge'], preview: [0, 6000, 12000] },
  M3S6: { module: 3, slide: 6, stem: 'ess_m3_safety_controls', cues: ['detection', 'ventilation', 'backup', 'suppression', 'coordination'], preview: [0, 13000, 23000, 32000, 45000] },
  M4S8: { module: 4, slide: 8, stem: 'ess_m4_requirement_to_evidence_workflow', cues: [...Array.from({ length: 8 }, (_, i) => `step${i + 1}`), 'feedback'], preview: [900, 2050, 3200, 4350, 5500, 6650, 7800, 8950, 9900] },
};
export function editionRoot(locale) {
  if (!locales.includes(locale)) throw new Error(`Unknown locale ${locale}`);
  return locale === 'en-US' ? courseRoot : path.join(courseRoot, 'locales', locale);
}
export const readJSON = async p => JSON.parse(await fs.readFile(p, 'utf8'));
export async function writeJSON(p, value) {
  await fs.mkdir(path.dirname(p), { recursive: true });
  const temporary = `${p}.tmp-${process.pid}`;
  await fs.writeFile(temporary, JSON.stringify(value, null, 2) + '\n');
  await fs.rename(temporary, p);
}
export function run(command, args, options = {}) {
  const result = spawnSync(command, args, { encoding: 'utf8', ...options });
  if (result.error || result.status !== 0) throw new Error(`${command}: ${result.error || result.stderr || result.stdout}`);
  return result.stdout;
}
export async function chromium() {
  const candidates = [process.env.PLAYWRIGHT_MODULE, path.join(repoRoot, 'skills/academy-wizard/node_modules/playwright/index.mjs'), path.join(os.homedir(), '.codex/skills/academy-wizard/node_modules/playwright/index.mjs')].filter(Boolean);
  for (const candidate of candidates) {
    try { return (await import(pathToFileURL(candidate))).chromium; } catch (error) {
      if (error.code !== 'ERR_MODULE_NOT_FOUND') throw error;
    }
  }
  throw new Error('Set PLAYWRIGHT_MODULE to an installed playwright/index.mjs');
}
export function probe(filename) {
  if (path.extname(filename).toLowerCase() === '.wav' && !process.env.FFPROBE_BIN) {
    return JSON.parse(run('python3', ['-c', 'import wave,json,sys; w=wave.open(sys.argv[1]); print(json.dumps({"streams":[{"codec_type":"audio","sample_rate":w.getframerate(),"channels":w.getnchannels()}],"format":{"duration":w.getnframes()/w.getframerate()}}))', filename]));
  }
  return JSON.parse(run(process.env.FFPROBE_BIN || 'ffprobe', ['-v', 'error', '-show_streams', '-show_format', '-of', 'json', filename]));
}
export async function sha256(filename) { return createHash('sha256').update(await fs.readFile(filename)).digest('hex'); }
export async function sourcesMatch(root, item) {
  if (!item.encoded?.source_html_sha256 || !item.encoded.geometry_source_sha256) return false;
  try {
    return item.encoded.source_html_sha256 === await sha256(path.join(root, item.source_html)) && item.encoded.geometry_source_sha256 === await sha256(path.join(root, item.geometry_snapshot));
  } catch (error) { if (error.code === 'ENOENT') return false; throw error; }
}
export function resolveAudio(locale, relativePath) {
  if (!audioRoot) throw new Error('Supply --audio-root or ESS_AUDIO_ROOT for final audio verification');
  if (path.isAbsolute(relativePath) || relativePath.split(/[\\/]/).includes('..') || !relativePath.startsWith('audio/')) throw new Error('Narration paths must be safe course-relative audio/ paths');
  return path.join(path.resolve(audioRoot), locale, path.basename(courseRoot), relativePath);
}

export async function timingFor(locale, id, timings) {
  const scene = scenes[id];
  if (!scene) throw new Error(`Unknown scene ${id}`);
  if (id === 'M4S8') return { duration_ms: 14000, poster_ms: 13900, cues_ms: Object.fromEntries(scene.cues.map((key, i) => [key, scene.preview[i]])), mode: 'retained-independent-loop', final_audio_verified: false, human_audio_review: 'pending' };
  const t = timings?.editions?.[locale]?.[id];
  if (!t) return { duration_ms: 60000, poster_ms: 59000, cues_ms: Object.fromEntries(scene.cues.map((key, i) => [key, scene.preview[i]])), mode: 'preview-only', final_audio_verified: false, human_audio_review: 'pending' };
  if (!t.final_audio_verified || !t.cues_reviewed || !t.narration_path || !t.narration_sha256) throw new Error(`${locale}/${id}: verified final audio, reviewed cues, path and SHA-256 are required`);
  const audio = resolveAudio(locale, t.narration_path);
  if (await sha256(audio) !== t.narration_sha256) throw new Error(`${locale}/${id}: narration changed after cue review`);
  const media = probe(audio);
  if (!media.streams.some(s => s.codec_type === 'audio')) throw new Error(`${locale}/${id}: no audio stream`);
  const duration = Number(media.format.duration) * 1000;
  if (!Number.isFinite(t.duration_ms) || Math.abs(duration - t.duration_ms) > 1000 / 30) throw new Error(`${locale}/${id}: duration does not match final narration (${duration} ms)`);
  let previous = -1;
  for (const cue of scene.cues) {
    const time = t.cues_ms?.[cue];
    if (!Number.isFinite(time) || time < 0 || time < previous || time + 1800 > duration - 1500) throw new Error(`${locale}/${id}: invalid/out-of-order cue ${cue}; reserve transition and final hold`);
    previous = time;
  }
  if (id === 'M2S6' && (t.cues_ms.facility - t.cues_ms.it < 1300 || t.cues_ms.recharge - t.cues_ms.facility < 1300)) throw new Error(`${locale}/${id}: complete each underlying stack layer before adding the next`);
  return { ...t, duration_ms: duration, poster_ms: duration - 100, mode: 'narration-synchronized' };
}
