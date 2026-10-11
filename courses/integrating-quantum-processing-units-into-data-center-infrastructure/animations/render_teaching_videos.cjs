const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const { once } = require('events');
const sharp = require('sharp');

const ffmpeg = process.env.FFMPEG_BIN || 'ffmpeg';
const root = path.resolve(__dirname, '..', 'figures');
const fps = 15;
const duration = 10;
const frames = fps * duration;

function base(content) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 960 540">
    <rect width="960" height="540" fill="#ffffff"/>
    ${content}
  </svg>`;
}

function card(x, y, w, h, title, lines, active, accent = '#8dc63f', titleSize = 25, detailSize = 19) {
  const stroke = active ? accent : '#b8c0ca';
  const fill = active ? '#f3f9e9' : '#f9fafb';
  const middle = x + w / 2;
  const titleY = y + (h > 140 ? 63 : 42);
  const details = lines.map((line, i) => `<text x="${middle}" y="${titleY + 31 + i * 26}" text-anchor="middle" font-family="Avenir Next, Arial" font-size="${detailSize}" fill="#4b5563">${line}</text>`).join('');
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="10" fill="${fill}" stroke="${stroke}" stroke-width="${active ? 4 : 2.5}"/>
    <text x="${middle}" y="${titleY}" text-anchor="middle" font-family="Avenir Next, Arial" font-size="${titleSize}" font-weight="700" fill="#222831">${title}</text>${details}`;
}

function link(d, active, dash = '') {
  return `<path d="${d}" fill="none" stroke="${active ? '#8dc63f' : '#b6bec9'}" stroke-width="${active ? 5 : 3}" stroke-linecap="round" ${dash ? `stroke-dasharray="${dash}"` : ''}/>`;
}

function progressDot(x, y, visible) {
  return visible ? `<circle cx="${x}" cy="${y}" r="8" fill="#8dc63f" stroke="#fff" stroke-width="3"/>` : '';
}

function bezier(points, p) {
  const q = 1 - p;
  return [0, 1].map(axis => q ** 3 * points[0][axis] + 3 * q ** 2 * p * points[1][axis] + 3 * q * p ** 2 * points[2][axis] + p ** 3 * points[3][axis]);
}

function hybrid(t) {
  const stage = Math.min(4, Math.floor(t / 2));
  const phase = (t % 2) / 2;
  const lines = [
    link('M285 201H345', stage >= 1),
    link('M540 201C615 201 633 263 700 263', stage >= 2),
    link('M700 298C630 377 510 374 415 360', stage >= 3),
    link('M220 360C136 354 117 304 117 248', stage >= 4),
  ].join('');
  const dots = [
    progressDot(290 + phase * 50, 201, stage === 0),
    progressDot(...bezier([[540, 201], [615, 201], [633, 263], [700, 263]], phase), stage === 1),
    progressDot(...bezier([[700, 298], [630, 377], [510, 374], [415, 360]], phase), stage === 2),
    progressDot(...bezier([[220, 360], [136, 354], [117, 304], [117, 248]], phase), stage === 3),
  ].join('');
  return base(`
    <rect x="55" y="88" width="560" height="386" rx="16" fill="#f8fafc" stroke="#d9dfe6" stroke-width="2"/>
    <text x="90" y="124" font-family="Avenir Next, Arial" font-size="22" font-weight="700" fill="#343895">CLASSICAL INFRASTRUCTURE</text>
    ${lines}
    ${card(95, 155, 190, 93, 'Orchestrate', ['CPU / GPU'], stage >= 0)}
    ${card(345, 155, 195, 93, 'Prepare + control', ['Signals + timing'], stage >= 1, '#8dc63f', 19)}
    ${card(220, 315, 195, 93, 'Measure + decode', ['Classical feedback'], stage >= 3, '#8dc63f', 16)}
    ${card(700, 191, 205, 143, 'QPU execution', ['Specialized quantum', 'resource'], stage >= 2, '#343895', 23, 17)}
    ${dots}
    <path d="M95 430H555" stroke="#d9dfe6" stroke-width="2"/>
    <text x="325" y="447" text-anchor="middle" font-family="Avenir Next, Arial" font-size="17" fill="#5c6672">Network · storage · facility services</text>
  `);
}

function critical(t) {
  const stage = Math.min(4, Math.floor(t / 2));
  const phase = (t % 2) / 2;
  const routes = [
    [[264, 253], [320, 253], [320, 170], [352, 170]],
    [[590, 170], [642, 170], [642, 253], [678, 253]],
    [[806, 305], [806, 382], [648, 382], [608, 382]],
    [[370, 382], [310, 382], [310, 275], [282, 275]],
  ];
  const cards = [
    [44, 201, 'Orchestrate', ['Schedule, allocate, compile,', 'and dispatch the job.']],
    [370, 118, 'Control', ['Prepare pulses and coordinate', 'real-time classical logic.']],
    [696, 201, 'Execute', ['The QPU performs the', 'quantum operation.']],
    [370, 322, 'Measure + adapt', ['Decode results and update', 'the next circuit.']],
  ];
  const paths = routes.map((p, i) => `<path d="M${p[0]} C${p[1]} ${p[2]} ${p[3]}" fill="none" stroke="${i === 3 ? '#8dc63f' : '#b9c1cb'}" stroke-width="3" ${i === 3 ? 'stroke-dasharray="8 8"' : ''} marker-end="url(#arrow-${i === 3 ? 'green' : 'gray'})"/>`).join('');
  const boxes = cards.map(([x, y, title, lines], i) => {
    const active = stage === 4 || stage === i;
    return `<rect x="${x}" y="${y}" width="220" height="104" rx="8" fill="${active ? '#f3f9e9' : '#fff'}" stroke="${active ? '#8dc63f' : '#c6ccd4'}" stroke-width="${active ? 4 : 2}"/>
      <text x="${x + 18}" y="${y + 32}" font-family="Avenir Next, Arial" font-size="21" font-weight="700" fill="#24262b">${title}</text>
      ${lines.map((line, j) => `<text x="${x + 18}" y="${y + 60 + 22 * j}" font-family="Avenir Next, Arial" font-size="13.5" fill="#5f6062">${line}</text>`).join('')}`;
  }).join('');
  return base(`<defs>${['gray', 'green'].map((name, i) => `<marker id="arrow-${name}" viewBox="0 0 20 18" refX="1" refY="9" markerWidth="20" markerHeight="18" markerUnits="userSpaceOnUse" orient="auto"><path d="M1 1 L19 9 L1 17 Z" fill="${i ? '#8dc63f' : '#b9c1cb'}"/></marker>`).join('')}</defs>
    ${paths}${boxes}
    <rect x="382" y="236" width="196" height="66" rx="8" fill="#343895"/>
    <text x="480" y="263" text-anchor="middle" font-family="Avenir Next, Arial" font-size="16" font-weight="700" fill="#fff">Low-latency</text>
    <text x="480" y="285" text-anchor="middle" font-family="Avenir Next, Arial" font-size="16" font-weight="700" fill="#fff">round trip</text>
    ${stage < 4 ? progressDot(...bezier(routes[stage], phase), true) : ''}`);
}

function site(t) {
  const stage = Math.min(4, Math.floor(t / 2));
  const phase = (t % 2) / 2;
  const connectors = [
    link('M309 166L372 214', stage >= 1),
    link('M651 166L588 214', stage >= 2),
    link('M309 374L372 327', stage >= 3),
    link('M651 374L588 327', stage >= 4),
  ].join('');
  const dotPositions = [
    [309 + phase * 63, 166 + phase * 48],
    [651 - phase * 63, 166 + phase * 48],
    [309 + phase * 63, 374 - phase * 47],
    [651 - phase * 63, 374 - phase * 47],
  ];
  return base(`
    ${connectors}
    ${card(78, 108, 231, 116, 'Vibration', ['Seismic + transport'], stage >= 1)}
    ${card(651, 108, 231, 116, 'Electromagnetic', ['Nearby sources + EMI'], stage >= 2, '#8dc63f', 22)}
    ${card(78, 316, 231, 116, 'Utilities', ['Power + cooling'], stage >= 3)}
    ${card(651, 316, 231, 116, 'Physical access', ['Delivery + service'], stage >= 4)}
    <rect x="372" y="196" width="216" height="148" rx="16" fill="#343895"/>
    <text x="480" y="253" text-anchor="middle" font-family="Avenir Next, Arial" font-size="27" font-weight="700" fill="#fff">QPU site</text>
    <text x="480" y="289" text-anchor="middle" font-family="Avenir Next, Arial" font-size="19" fill="#fff">Survey first</text>
    ${stage < 4 ? progressDot(...dotPositions[stage], true) : ''}
  `);
}

function production(t) {
  const stage = Math.min(3, Math.floor(t / 2.5));
  const phase = (t % 2.5) / 2.5;
  const links = link('M291 255H368', stage >= 1) + link('M592 255H669', stage >= 2);
  const dots = stage === 0 ? progressDot(300 + phase * 58, 255, true)
    : stage === 1 ? progressDot(600 + phase * 58, 255, true) : '';
  return base(`
    ${links}
    ${card(69, 160, 222, 190, 'Pilot deployment', ['One site', 'Bespoke conditions'], true, '#8dc63f', 22)}
    ${card(368, 160, 224, 190, 'Common envelope', ['Power + cooling', 'Access + interfaces'], stage >= 1, '#8dc63f', 21)}
    ${card(669, 160, 222, 190, 'Repeatable operations', ['Monitoring + service', 'across future sites'], stage >= 2, '#8dc63f', 17)}
    ${dots}
  `);
}

const scenes = {
  hybrid: [hybrid, 'hybrid_infrastructure_context'],
  critical: [critical, 'hybrid_quantum_classical_loop'],
  site: [site, 'quantum_site_readiness'],
  production: [production, 'pilot_to_repeatable_operations'],
};

function writeReferenceState(name) {
  const [scene, filename] = scenes[name];
  const review = path.join(__dirname, 'reference-states');
  fs.mkdirSync(review, { recursive: true });
  fs.writeFileSync(path.join(review, `${filename}.svg`), scene(duration - 1 / fps).replace(/[ \t]+$/gm, ''));
}

async function render(name) {
  const [scene, filename] = scenes[name];
  const output = path.join(root, `${filename}.webm`);
  const poster = path.join(root, `${filename}_poster.png`);
  fs.mkdirSync(root, { recursive: true });
  writeReferenceState(name);
  const child = spawn(ffmpeg, [
    '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps),
    '-vcodec', 'png', '-i', 'pipe:0', '-frames:v', String(frames), '-an',
    '-c:v', 'libvpx-vp9', '-b:v', '0', '-lossless', '1', '-row-mt', '1',
    '-pix_fmt', 'yuv444p', output,
  ], { stdio: ['pipe', 'ignore', 'pipe'] });
  let errors = '';
  child.stderr.on('data', chunk => { errors += chunk.toString(); });
  for (let frame = 0; frame < frames; frame++) {
    const svg = Buffer.from(scene(frame / fps));
    const png = await sharp(svg).png().toBuffer();
    if (!child.stdin.write(png)) await once(child.stdin, 'drain');
  }
  child.stdin.end();
  const [code] = await once(child, 'close');
  if (code !== 0) throw new Error(`${name}: ffmpeg exit ${code}: ${errors}`);
  await sharp(Buffer.from(scene(duration - 0.1))).resize(960, 540).png().toFile(poster);
  console.log(`${name}: ${path.basename(output)} and poster created`);
}

module.exports = { scenes, fps, duration };

if (require.main === module) (async () => {
  const args = process.argv.slice(2);
  const statesOnly = args.includes('--states-only');
  const requested = args.filter(arg => arg !== '--states-only');
  for (const name of requested.length ? requested : Object.keys(scenes)) {
    if (!scenes[name]) throw new Error(`Unknown scene: ${name}`);
    if (statesOnly) writeReferenceState(name);
    else await render(name);
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
