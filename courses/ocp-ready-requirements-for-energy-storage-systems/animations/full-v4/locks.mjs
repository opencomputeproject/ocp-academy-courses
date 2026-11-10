import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), '.cache', 'locks');
const pause = ms => new Promise(resolve => setTimeout(resolve, ms));

export async function withLock(name, operation, timeoutMs = 7200000) {
  if (!/^[A-Za-z0-9_-]+$/.test(name)) throw new Error('Unsafe lock name');
  await fs.mkdir(root, { recursive: true });
  const lock = path.join(root, name), started = Date.now();
  for (;;) {
    try {
      await fs.mkdir(lock);
      await fs.writeFile(path.join(lock, 'owner.json'), JSON.stringify({ pid: process.pid, started_ms: Date.now() }));
      break;
    } catch (error) {
      if (error.code !== 'EEXIST') throw error;
      try {
        const owner = JSON.parse(await fs.readFile(path.join(lock, 'owner.json'), 'utf8'));
        try { process.kill(owner.pid, 0); } catch (signalError) {
          if (signalError.code === 'ESRCH') throw new Error(`Dead owner for ${name}; stop workers and remove this stale lock before retrying`);
        }
      } catch (ownerError) {
        // A live creator may not have written owner.json yet. Never steal an unowned-looking lock.
        if (!['ENOENT', 'ENOTDIR'].includes(ownerError.code) && !(ownerError instanceof SyntaxError)) throw ownerError;
      }
      if (Date.now() - started > timeoutMs) throw new Error(`Timed out waiting for ${name}`);
      await pause(100);
    }
  }
  try { return await operation(); }
  finally { await fs.rm(lock, { recursive: true, force: true }); }
}
