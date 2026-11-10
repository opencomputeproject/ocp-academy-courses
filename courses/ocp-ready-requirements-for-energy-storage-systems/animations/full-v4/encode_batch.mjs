import { spawn } from 'node:child_process';
import path from 'node:path';
import { here, option, editionRoot } from './lib.mjs';

const concurrency = Number(option('--workers') || 3);
if (!Number.isInteger(concurrency) || concurrency < 1 || concurrency > 3) throw new Error('--workers must be 1, 2 or 3');
if (option('--locale') && option('--locales')) throw new Error('Choose --locale or --locales, not both');
const queue = option('--locales') ? [...new Set(option('--locales').split(','))] : option('--locale') ? [option('--locale')] : ['en-US', 'ja-JP', 'ko-KR', 'zh-CN', 'zh-TW', 'vi-VN', 'pt-BR', 'es-419'];
queue.forEach(editionRoot);
const batchFlags = ['--workers', '--locale', '--locales'];
const passed = process.argv.slice(2).filter((arg, index, args) => !batchFlags.includes(arg) && !batchFlags.includes(args[index - 1]));
const results = [];
async function worker() {
  while (queue.length) {
    const locale = queue.shift();
    console.log(`[${locale}] starting locale worker`);
    const child = spawn(process.execPath, [path.join(here, 'encode.mjs'), ...passed, '--locale', locale], { stdio: ['ignore', 'pipe', 'pipe'] });
    child.stdout.on('data', data => process.stdout.write(`[${locale}] ${data}`));
    child.stderr.on('data', data => process.stderr.write(`[${locale}] ${data}`));
    const code = await new Promise((resolve, reject) => { child.on('error', reject); child.on('close', resolve); });
    results.push({ locale, code });
    console.log(`[${locale}] worker finished (${code})`);
  }
}
// Independent OS workers; each job has private cache and output, with brief shared-state locks.
await Promise.all(Array.from({ length: concurrency }, worker));
console.log(JSON.stringify(results, null, 2));
if (results.some(result => result.code !== 0)) process.exitCode = 1;
