import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { spawn } from 'node:child_process';
import { here } from './lib.mjs';
import { withLock } from './locks.mjs';

test('five OS workers serialize shared read-modify-write operations', async () => {
  const file = path.join(here, '.cache', `lock-counter-${process.pid}.json`);
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, '0');
  const moduleURL = pathToFileURL(path.join(here, 'locks.mjs')).href;
  const script = `import fs from 'node:fs/promises';import {withLock} from ${JSON.stringify(moduleURL)};for(let i=0;i<10;i++)await withLock('test-counter-${process.pid}',async()=>{const n=JSON.parse(await fs.readFile(${JSON.stringify(file)},'utf8'));await new Promise(r=>setTimeout(r,5));await fs.writeFile(${JSON.stringify(file)},JSON.stringify(n+1));},10000);`;
  const jobs = Array.from({ length: 5 }, () => new Promise((resolve, reject) => {
    const child = spawn(process.execPath, ['--input-type=module', '-e', script], { stdio: ['ignore', 'ignore', 'pipe'] });
    let errors = ''; child.stderr.on('data', data => errors += data);
    child.on('error', reject); child.on('close', code => code ? reject(new Error(errors)) : resolve());
  }));
  try { await Promise.all(jobs); assert.equal(JSON.parse(await fs.readFile(file, 'utf8')), 50); }
  finally { await fs.rm(file, { force: true }); }
});
test('throwing operations release their lock', async () => {
  const name = `test-release-${process.pid}`;
  await assert.rejects(withLock(name, async () => { throw new Error('intentional'); }), /intentional/);
  assert.equal(await withLock(name, async () => 7, 1000), 7);
});
