import { test, after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const directory = path.dirname(fileURLToPath(import.meta.url));
const fixture = path.join(directory, '.cache', `timing-tests-${process.pid}`);
process.env.ESS_AUDIO_ROOT = fixture;
const { timingFor, sha256, courseRoot } = await import('./lib.mjs');
const relative = 'audio/module1/test.wav';
const filename = path.join(fixture, 'en-US', path.basename(courseRoot), relative);
await fs.mkdir(path.dirname(filename), { recursive: true });
const rate = 8000, bytes = rate * 2 * 10;
const wav = Buffer.alloc(44 + bytes);
wav.write('RIFF', 0); wav.writeUInt32LE(36 + bytes, 4); wav.write('WAVEfmt ', 8);
wav.writeUInt32LE(16, 16); wav.writeUInt16LE(1, 20); wav.writeUInt16LE(1, 22);
wav.writeUInt32LE(rate, 24); wav.writeUInt32LE(rate * 2, 28); wav.writeUInt16LE(2, 32);
wav.writeUInt16LE(16, 34); wav.write('data', 36); wav.writeUInt32LE(bytes, 40);
await fs.writeFile(filename, wav);
const valid = { narration_path: relative, narration_sha256: await sha256(filename), duration_ms: 10000, final_audio_verified: true, human_audio_review: 'pending', cues_reviewed: true, cues_ms: { centralized: 0, distributed: 2000, placements: 4000 } };
const input = (patch = {}, id = 'M1S3') => ({ editions: { 'en-US': { [id]: { ...valid, ...patch } } } });
after(async () => fs.rm(fixture, { recursive: true, force: true }));

test('preview clocks are explicit and cannot claim final readiness', async () => {
  const t = await timingFor('en-US', 'M1S3');
  assert.equal(t.mode, 'preview-only'); assert.equal(t.final_audio_verified, false);
});
test('valid final audio can remain pending human listening', async () => {
  const t = await timingFor('en-US', 'M1S3', input());
  assert.equal(t.duration_ms, 10000); assert.equal(t.human_audio_review, 'pending');
});
test('changed WAV hash is rejected', async () => assert.rejects(timingFor('en-US', 'M1S3', input({ narration_sha256: 'stale' })), /changed/));
test('unverified generation is rejected', async () => assert.rejects(timingFor('en-US', 'M1S3', input({ final_audio_verified: false })), /verified final audio/));
test('unreviewed cues are rejected', async () => assert.rejects(timingFor('en-US', 'M1S3', input({ cues_reviewed: false })), /reviewed cues/));
test('absolute and escaping audio paths are rejected', async () => {
  await assert.rejects(timingFor('en-US', 'M1S3', input({ narration_path: filename })), /course-relative/);
  await assert.rejects(timingFor('en-US', 'M1S3', input({ narration_path: 'audio/../test.wav' })), /course-relative/);
});
test('duration mismatch is rejected', async () => assert.rejects(timingFor('en-US', 'M1S3', input({ duration_ms: 9500 })), /does not match/));
test('out-of-order cues are rejected', async () => assert.rejects(timingFor('en-US', 'M1S3', input({ cues_ms: { centralized: 0, distributed: 3000, placements: 2000 } })), /out-of-order/));
test('last transition must leave a stable final hold', async () => assert.rejects(timingFor('en-US', 'M1S3', input({ cues_ms: { centralized: 0, distributed: 2000, placements: 8000 } })), /final hold/));
test('stack layers cannot detach by overlapping growth windows', async () => assert.rejects(timingFor('en-US', 'M2S6', input({ cues_ms: { it: 0, facility: 500, recharge: 4000 } }, 'M2S6')), /underlying stack/));
test('existing workflow remains independently looped at 14 seconds', async () => {
  const t = await timingFor('en-US', 'M4S8');
  assert.equal(t.duration_ms, 14000); assert.equal(t.mode, 'retained-independent-loop');
});
