import test from 'node:test';
import assert from 'node:assert/strict';
import { encodingPermitted, here, readJSON, locales } from './lib.mjs';
import path from 'node:path';

test('only released paired editions and listed independent loops may encode', async () => {
  const policy = await readJSON(path.join(here, 'encoding-policy.json'));
  for (const locale of locales) {
    for (const id of ['M1S3', 'M2S6', 'M3S6']) assert.equal(Boolean(encodingPermitted(policy, locale, id)), ['en-US', 'es-419', 'pt-BR', 'zh-CN', 'ja-JP', 'ko-KR', 'zh-TW', 'vi-VN'].includes(locale));
    assert.equal(Boolean(encodingPermitted(policy, locale, 'M4S8')), true);
  }
});
