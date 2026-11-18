const { execFileSync } = require('node:child_process');
const { homedir } = require('node:os');
const path = require('node:path');

const skill = process.env.ACADEMY_WIZARD_SKILL_DIR ||
  path.join(homedir(), '.codex', 'skills', 'academy-wizard');
const recorder = path.join(skill, 'scripts', 'record_css_animation.mjs');
const figures = path.resolve(__dirname, '..', 'figures');
const animations = [
  ['module1_current_loss.html', 'current_copper_loss'],
  ['diablo_power_path_animation.html', 'ride_through_output_model'],
  ['module3_interface_path.html', 'serviceable_interface_path'],
  ['module4_coordinated_lvdc.html', 'coordinated_lvdc_response'],
];

const selected = animations.filter(([, name]) =>
  !process.env.VIDEO_FILTER || name.includes(process.env.VIDEO_FILTER));
if (!selected.length) throw new Error('VIDEO_FILTER did not match a teaching video.');
for (const [html, name] of selected) {
  execFileSync(process.execPath, [
    recorder,
    path.join(__dirname, html),
    path.join(figures, name + '.webm'),
    path.join(figures, name + '_poster.png'),
  ], { stdio: 'inherit' });
}
