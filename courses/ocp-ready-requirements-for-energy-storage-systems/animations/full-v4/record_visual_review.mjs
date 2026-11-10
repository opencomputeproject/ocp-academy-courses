import path from 'node:path';
import assert from 'node:assert/strict';
import { here, editionRoot, readJSON, writeJSON, option, sha256 } from './lib.mjs';
import { withLock } from './locks.mjs';
import { verifiedScriptHash } from './script_binding.mjs';

const locale = option('--locale'), id = option('--slide');
if (!locale || !id || !process.argv.includes('--record-visual-review')) throw new Error('After visually inspecting encoded states and native/200% detail, use --locale <tag> --slide <id> --record-visual-review');
await withLock('manifest', async () => {
  const manifestPath = path.join(here, 'figure-patch-manifest.json');
  const manifest = await readJSON(manifestPath), item = manifest.editions[locale].figures[id];
  const evidence = await readJSON(path.join(here, 'qa', locale, id, 'encoded-review', 'review-evidence.json'));
  const digest = await sha256(path.join(editionRoot(locale), item.figure.path));
  assert.equal(digest, item.encoded.sha256);
  assert.equal(digest, evidence.video_sha256);
  assert.equal(await sha256(path.join(editionRoot(locale), item.source_html)), evidence.source_html_sha256, 'HTML changed since visual evidence capture');
  assert.equal(await sha256(path.join(editionRoot(locale), item.geometry_snapshot)), evidence.geometry_source_sha256, 'Geometry changed since visual evidence capture');
  const report = await readJSON(path.join(here, 'qa', locale, 'muted-playthrough.json'));
  const playback = report.results.find(result => result.id === id);
  assert(playback?.video_sha256 === digest && playback.ended && playback.muted && playback.reversals === 0, 'Complete hash-bound muted pass required');
  if (id === 'M4S8') {
    assert(playback.independent_loop_boundary, 'Independent loop boundary check required');
  }
  item.encoded.source_html_sha256 = evidence.source_html_sha256;
  item.encoded.geometry_source_sha256 = evidence.geometry_source_sha256;
  delete item.encoded.source_sha256;
  item.encoded.source_binding = 'Complete current HTML and materialized geometry, bound during encoded visual review';
  item.figure.text_inventory = { sha256: digest, entries: item.inventory_candidate.entries };
  item.figure.duration_seconds = item.encoded.duration;
  // Preserve the latest reviewed learner metadata without rewriting source or course JSON.
  const course = await readJSON(path.join(editionRoot(locale), 'course.json'));
  const slide = course.modules[item.module_number - 1].slides[item.slide_number - 1];
  assert.equal(slide.id, item.slide_id, 'Course slide changed since animation mapping');
  for (const key of ['alt', 'caption']) if (typeof slide.figure?.[key] === 'string') item.figure[key] = slide.figure[key];
  if (id !== 'M4S8') item.figure.narration_script_sha256 = await verifiedScriptHash(locale, item.timing);
  item.status = 'encoded-visual-reviewed-player-qa-pending';
  item.visual_review = { reviewer: 'Codex visual inspection', video_sha256: digest, native_and_200percent: true, transition_frames: true, final_hold: true, white_outer_pixels: true, human_audio_review: 'pending', integrated_player_review: 'pending' };
  if (playback) item.visual_review.standalone_muted_playthrough = { video_sha256: digest, duration_seconds: playback.duration, rate: playback.rate, completed: playback.ended, independent_loop_boundary: playback.independent_loop_boundary };
  evidence.visual_review = 'Codex visual inspection completed; human listening and integrated player QA not implied';
  await writeJSON(path.join(here, 'qa', locale, id, 'encoded-review', 'review-evidence.json'), evidence);
  await writeJSON(manifestPath, manifest);
  await writeJSON(path.join(here, 'qa', locale, id, 'encode-receipt.json'), item.encoded);
  const edition = manifest.editions[locale];
  const reviewed = Object.fromEntries(Object.entries(edition.figures).filter(([, f]) => f.status === 'encoded-visual-reviewed-player-qa-pending'));
  const ready = Object.keys(reviewed).length === Object.keys(edition.figures).length;
  await writeJSON(path.join(here, `figure-patch-${locale}.json`), {
    schema_version: 1, course_slug: manifest.course_slug, ready_for_integrated_player_qa: true,
    application: 'Replace only listed reviewed figure objects; omitted figures remain held. Keep global narration.teaching_video_mode unset. Human listening and integrated player/LMS checks remain pending.',
    edition_complete: ready, omitted_slides: Object.keys(edition.figures).filter(key => !reviewed[key]),
    preserved_playback: manifest.preserved_playback, editions: { [locale]: { ...edition, figures: reviewed } }, human_audio_review: 'pending',
  });
  console.log(`${locale}/${id}: recorded encoded visual review; ${ready ? 'complete' : 'partial'} edition figure patch ready for main`);
}, 60000);
