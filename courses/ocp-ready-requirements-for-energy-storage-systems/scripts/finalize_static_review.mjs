#!/usr/bin/env node
// Finalizes a hash-bound inventory only after a separate visual-review attestation.
import fs from 'node:fs/promises';
import crypto from 'node:crypto';

const [candidateFile, approvalFile, destination = '/tmp/ess_static_media_manifest.json'] = process.argv.slice(2);
if (!candidateFile || !approvalFile) throw new Error('Usage: node finalize_static_review.mjs candidates.json visual-approval.json [manifest.json]');
const digest = data => crypto.createHash('sha256').update(data).digest('hex');
const bytes = await fs.readFile(candidateFile);
const candidates = JSON.parse(bytes);
const approval = JSON.parse(await fs.readFile(approvalFile, 'utf8'));
if (approval.candidates_sha256 !== digest(bytes)) throw new Error('Review attestation does not match the current candidate manifest. Review the new renders.');
if (!approval.reviewer || !approval.method || !Array.isArray(approval.accepted_keys)) throw new Error('Missing explicit visual-review attestation.');
const accepted = new Set(approval.accepted_keys);
const byLocale = {}, assets = [];
for (const item of candidates.assets) {
  const key = `${item.locale}/M${item.module}S${item.slide}`;
  if (!accepted.has(key)) throw new Error(`No visual approval for ${key}`);
  const assetBytes = await fs.readFile(item.absolute_path);
  if (digest(assetBytes) !== item.candidate_text_inventory.sha256) throw new Error(`Asset changed since rendering: ${key}`);
  if (item.geometry_checks.violations) throw new Error(`Geometry violations: ${key}`);
  if (item.candidate_text_inventory.entries.some(e => !e.text || /[\u0080-\u009f\ufffd]/u.test(e.text))) throw new Error(`Invalid visible text: ${key}`);
  const images = {};
  for (const [view, file] of Object.entries(item.review_images)) images[view] = { path: file, sha256: digest(await fs.readFile(file)) };
  const text_inventory = item.candidate_text_inventory;
  const record = { locale: item.locale, module: item.module, slide: item.slide,
    figure: { source: 'custom', path: item.figure.path, text_inventory },
    remove_figure_fields: ['svg'], absolute_path: item.absolute_path, previous_path: item.previous_path,
    review_status: 'visually_reviewed',
    review: { reviewer: approval.reviewer, method: approval.method, images, notes: approval.notes || [] },
    geometry_checks: item.geometry_checks, provenance: item.provenance, source_text_repairs: item.source_text_repairs };
  assets.push(record);
  ((byLocale[item.locale] ||= {})[`module${item.module}`] ||= {})[`slide${item.slide}`] = record.figure;
}
if (accepted.size !== assets.length) throw new Error('The approval set contains unknown or duplicate asset keys.');
const manifest = { schema_version: 1, course_root: candidates.course_root,
  scope: 'Static figures only; no course.json, animations, generated videos/posters, or audio writes.',
  integration: 'Merge each figure object into the matching slide, remove figure.svg, retain existing alt/caption. Do not refresh these hashes after changing an SVG without visual review.',
  candidate_manifest_sha256: digest(bytes), count: assets.length, by_locale: byLocale, assets };
const pending = `${destination}.${process.pid}.pending`;
await fs.writeFile(pending, JSON.stringify(manifest, null, 2) + '\n');
await fs.rename(pending, destination);
console.log(`Wrote ${assets.length} visually reviewed static figure inventories: ${destination}`);
