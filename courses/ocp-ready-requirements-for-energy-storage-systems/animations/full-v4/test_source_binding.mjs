import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { here, sha256, sourcesMatch } from './lib.mjs';

test('HTML/CSS and separate geometry changes invalidate source reuse', async () => {
  const directory = path.join(here, '.cache', `source-binding-test-${process.pid}`);
  await fs.mkdir(directory, { recursive: true });
  const html = path.join(directory, 'scene.html'), svg = path.join(directory, 'geometry.svg');
  const original = '<style>svg{background:white}</style><svg>Original label</svg>';
  await fs.writeFile(html, original); await fs.writeFile(svg, '<svg><circle cx="10" cy="10" r="4"/></svg>');
  const item = { source_html: 'scene.html', geometry_snapshot: 'geometry.svg', encoded: { source_html_sha256: await sha256(html), geometry_source_sha256: await sha256(svg) } };
  try {
    assert.equal(await sourcesMatch(directory, item), true);
    assert.equal(await sourcesMatch(directory, { ...item, encoded: {} }), false);
    await fs.writeFile(html, original.replace('white', 'black'));
    assert.equal(await sourcesMatch(directory, item), false);
    await fs.writeFile(html, original.replace('Original label', 'Revised label'));
    assert.equal(await sourcesMatch(directory, item), false);
    await fs.writeFile(html, original);
    assert.equal(await sourcesMatch(directory, item), true);
    await fs.writeFile(svg, '<svg><circle cx="11" cy="10" r="4"/></svg>');
    assert.equal(await sourcesMatch(directory, item), false);
    await fs.rm(html);
    assert.equal(await sourcesMatch(directory, item), false);
  } finally { await fs.rm(directory, { recursive: true, force: true }); }
});
