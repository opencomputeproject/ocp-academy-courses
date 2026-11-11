const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

function render(workDir, args = process.argv.slice(2)) {
  const [htmlName, outputName, durationArg, posterName] = args;
  if (!htmlName || !outputName || !durationArg) {
    throw new Error('Usage: node render_animation.js <html> <output.webm|mp4> <duration-ms> [poster.png]');
  }
  let recorder;
  const configured = process.env.ACADEMY_WIZARD_SKILL_DIR;
  if (configured) recorder = path.join(configured, 'scripts', 'record_css_animation.mjs');
  for (let folder = workDir; !recorder; folder = path.dirname(folder)) {
    const candidate = path.join(folder, 'skills', 'academy-wizard', 'scripts', 'record_css_animation.mjs');
    if (fs.existsSync(candidate)) recorder = candidate;
    else if (path.dirname(folder) === folder) break;
  }
  if (!recorder || !fs.existsSync(recorder)) {
    throw new Error('Maintained animation recorder not found. Set ACADEMY_WIZARD_SKILL_DIR.');
  }
  const output = path.resolve(workDir, outputName);
  const poster = posterName ? path.resolve(workDir, posterName) : output.replace(/\.(?:webm|mp4|m4v)$/i, '_poster.png');
  if (poster === output) throw new Error('Output must be a .webm, .mp4, or .m4v file.');
  const result = spawnSync(process.execPath, [recorder, path.resolve(workDir, htmlName), output, poster, durationArg], {
    stdio: 'inherit', env: process.env,
  });
  if (result.error) throw result.error;
  if (result.status !== 0) throw new Error('Animation recording failed with exit code ' + result.status);
}

module.exports = { render };
if (require.main === module) render(__dirname);
