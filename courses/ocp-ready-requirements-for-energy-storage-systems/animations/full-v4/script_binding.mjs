import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import { audioRoot, editionRoot, readJSON, resolveAudio, run, sha256 } from './lib.mjs';

export function scriptHash(filename) {
  // Match the course build guard's comment stripping and Python whitespace rules exactly.
  return run('python3', ['-c', "import hashlib,pathlib,sys; text='\\n'.join(line for line in pathlib.Path(sys.argv[1]).read_text(encoding='utf-8').splitlines() if not line.startswith('#')).strip(); print(hashlib.sha256(text.encode('utf-8')).hexdigest())", filename]).trim();
}

export async function verifyScriptReceipt(script, narrationHash, receiptRoot) {
  const digest = scriptHash(script);
  for (const entry of await fs.readdir(receiptRoot, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    let receipt;
    try { receipt = await readJSON(path.join(receiptRoot, entry.name, 'receipt.json')); }
    catch (error) { if (error.code === 'ENOENT') continue; throw error; }
    if (receipt.output_sha256 === narrationHash && receipt.text_sha256 === digest && receipt.model_id === 'eleven_v4') return digest;
  }
  throw new Error('Current script and final WAV do not match a full-v4 generation receipt; regenerate narration and review cues before encoding');
}

export async function verifiedScriptHash(locale, timing) {
  const audio = resolveAudio(locale, timing.narration_path);
  assert.equal(await sha256(audio), timing.narration_sha256, 'Narration changed since cue review');
  return verifyScriptReceipt(
    path.join(editionRoot(locale), timing.narration_path.replace(/\.wav$/, '.txt')),
    timing.narration_sha256,
    path.join(path.resolve(audioRoot), '_narration_masters', locale),
  );
}
