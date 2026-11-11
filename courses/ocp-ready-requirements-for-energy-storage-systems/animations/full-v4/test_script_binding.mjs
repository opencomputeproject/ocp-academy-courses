import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { scriptHash, verifyScriptReceipt } from './script_binding.mjs';

test('script binding matches comment-stripped transcript and final-v4 receipt', async t => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'ess-script-binding-'));
  t.after(() => fs.rm(root, { recursive: true, force: true }));
  const script = path.join(root, 'script.txt');
  await fs.writeFile(script, '# Heading\r\n\r\nApproved narration.\r\n# Note\r\nSecond line.\r\n');
  const expected = createHash('sha256').update('Approved narration.\nSecond line.').digest('hex');
  assert.equal(scriptHash(script), expected);
  const receiptDir = path.join(root, 'receipts', 'generation');
  await fs.mkdir(receiptDir, { recursive: true });
  const receiptPath = path.join(receiptDir, 'receipt.json');
  const receipt = { model_id: 'eleven_v4', text_sha256: expected, output_sha256: 'final-wav-hash' };
  await fs.writeFile(receiptPath, JSON.stringify(receipt));
  assert.equal(await verifyScriptReceipt(script, 'final-wav-hash', path.dirname(receiptDir)), expected);
  await assert.rejects(verifyScriptReceipt(script, 'changed-wav-hash', path.dirname(receiptDir)), /do not match/);
  await fs.writeFile(receiptPath, JSON.stringify({ ...receipt, model_id: 'other-model' }));
  await assert.rejects(verifyScriptReceipt(script, 'final-wav-hash', path.dirname(receiptDir)), /do not match/);
  await fs.writeFile(receiptPath, JSON.stringify(receipt));
  await fs.writeFile(script, 'Changed narration.');
  await assert.rejects(verifyScriptReceipt(script, 'final-wav-hash', path.dirname(receiptDir)), /do not match/);
});
