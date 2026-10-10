// Sentence-boundary cues measured against the approved English narration.
const C = { ink: '#26332f', muted: '#64726d', line: '#d3dcd7', green: '#17865b', purple: '#5851a8', orange: '#b66a16', pale: '#f3f7f4' };
const escape = (s) => String(s).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('"', '&quot;');
const text = (x, y, s, size = 30, color = C.ink, anchor = 'start', weight = 400) => `<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}" font-weight="${weight}">${escape(s)}</text>`;
const rect = (x, y, w, h, color = C.line, fill = 'white', radius = 8) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${radius}" fill="${fill}" stroke="${color}" stroke-width="3"/>`;
function box(x, y, w, h, title, lines, active = false, color = C.green) {
  const titles = Array.isArray(title) ? title : [title];
  const small = w < 300;
  return `<g data-text-box="${x},${y},${w},${h}">${rect(x, y, w, h, active ? color : C.line, active ? C.pale : 'white')}${titles.map((s,i)=>text(x + 28, y + 54 + i * 32, s, small ? 28 : 32, C.ink, 'start', 600)).join('')}${lines.map((s, i) => text(x + 28, y + 99 + (titles.length-1)*32 + i * 38, s, small ? 26 : 27, C.muted)).join('')}</g>`;
}
const defs = `<defs>${['green','purple','orange','line'].map((key) => `<marker id="${key}" markerUnits="userSpaceOnUse" markerWidth="20" markerHeight="16" refX="1" refY="8" orient="auto"><path d="M1 1 L19 8 L1 15 Z" fill="${C[key]}"/></marker>`).join('')}</defs>`;
const arrow = (d, color = 'purple', width = 6, dash = '', id = '') => `<path ${id ? `id="${escape(id)}"` : ''} d="${d}" fill="none" stroke="${C[color]}" stroke-width="${width}" ${dash ? `stroke-dasharray="${dash}"` : ''} marker-end="url(#${color})"/>`;
const line = (d, color, width = 4, dash = '') => `<path d="${d}" fill="none" stroke="${color}" stroke-width="${width}" ${dash ? `stroke-dasharray="${dash}"` : ''}/>`;
const circle = (x, y, r, color, hollow = false) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${hollow ? 'white' : color}" stroke="${color}" stroke-width="4"/>`;
function stage(t, cues) { return cues.reduce((last, cue) => t >= cue[0] ? cue : last, cues[0]); }
function heading(s) { return text(120, 104, s, 38, C.ink, 'start', 600); }
const clamp = (x) => Math.max(0, Math.min(1, x));
function pathDot(t, start, stop, pathId, { period = 4, radius = 7, color = C.purple, hollow = true, count = 1, range = null, strokeWidth = 2 } = {}) {
  if (t < start || t >= stop) return '';
  return Array.from({ length: count }, (_, i) => {
    const progress = ((t - start) / period + i / count) % 1;
    const opacity = Math.min(1, progress / 0.12, (1 - progress) / 0.12);
    return `<circle data-motion-path="${escape(pathId)}" data-motion-progress="${progress}" ${range ? `data-motion-start="${range[0]}" data-motion-end="${range[1]}"` : ''} r="${radius}" fill="${hollow ? 'white' : color}" stroke="${color}" stroke-width="${strokeWidth}" opacity="${opacity}"/>`;
  }).join('');
}
function positionPathDots(svg) {
  // Resolve motion against the displayed shaft, after arrowhead clearance is applied.
  for (const dot of svg.querySelectorAll('[data-motion-path]')) {
    const path = svg.querySelector(`#${dot.dataset.motionPath}`);
    const length = path.getTotalLength();
    const inset = Number(dot.getAttribute('r')) + Number(dot.getAttribute('stroke-width')) / 2 + 2;
    const start = Number(dot.dataset.motionStart || 0);
    const stop = dot.dataset.motionEnd ? Math.min(length, Number(dot.dataset.motionEnd)) : length;
    const distance = start + inset + Number(dot.dataset.motionProgress) * (stop - start - 2 * inset);
    const point = path.getPointAtLength(distance);
    dot.setAttribute('cx', point.x);
    dot.setAttribute('cy', point.y);
    dot.dataset.motionDistance = distance;
  }
}
function nested(t, cues) {
  const title = stage(t, cues)[1];
  const phase = t >= 21.34;
  const final = t >= 68.08;
  const xs = [200, 530, 860, 1190];
  let s = heading(title) + text(1780, 156, 'Arrows trace heat, not a shared fluid circuit', 27, C.purple, 'end');
  s += line('M120 488 H1800', C.muted, 3, '12 10');
  s += text(170, 460, 'Above boundary: technology and rack side', 29, C.muted);
  s += text(170, 536, 'Below boundary: facility water and heat rejection', 29, C.muted);
  const titles = ['Silicon heat', phase ? ['Two-phase', 'cold plate'] : 'Cold plate', 'TCS loop', 'CDU boundary'];
  const labels = [['Highest heat flux'], [phase ? 'Boil near die' : 'Receives chip heat'], [phase ? 'Liquid and vapor' : 'Single-phase liquid'], ['Separate fluids']];
  xs.forEach((x, i) => { s += box(x, 250, 280, 164, titles[i], labels[i], final || t >= [3.89, 5.83, 14.04, 35.61][i]); });
  for (let i = 0; i < 3; i++) s += arrow(`M${xs[i] + 280} 332 H${xs[i + 1]}`, t >= [5.83, 14.04, 35.61][i] ? 'purple' : 'line', 6, '', `nested-short-${i}`);
  s += box(1520, 406, 280, 164, 'FWS loop', ['Facility water'], t >= 47.26);
  s += arrow('M1470 332 H1660 V406', t >= 47.26 ? 'purple' : 'line', 6, '', 'nested-to-fws');
  s += box(720, 690, 500, 164, 'Heat rejection or reuse path', ['Dry cooler, chiller, tower, reuse'], t >= 47.26);
  s += arrow('M1660 570 V650 Q1660 772 1538 772 H1220', t >= 47.26 ? 'purple' : 'line', 6, '', 'nested-to-rejection');
  s += pathDot(t, 5.83, 35.61, 'nested-short-0', { period: 2.8, radius: 5 });
  s += pathDot(t, 14.04, 35.61, 'nested-short-1', { period: 2.8, radius: 5 });
  s += pathDot(t, 27.31, 47.26, 'nested-short-2', { period: 2.8, radius: 5 });
  s += pathDot(t, 47.26, 68.08, 'nested-to-fws', { period: 5 });
  s += pathDot(t, 47.26, 68.08, 'nested-to-rejection', { period: 6 });
  if (t >= 14.04 && t < 21.34) s += text(1000, 210, 'Sensible heat: liquid warms', 29, C.green, 'middle');
  if (t >= 21.34) s += text(1000, 210, 'Latent heat: boil, return, condense', 29, C.purple, 'middle');
  if (t >= 35.61) {
    s += text(960, 944, 'The CDU transfers heat; TCS working fluid and FWS water stay separate.', 31, C.ink, 'middle', 600);
  }
  return s;
}
function controlled(t, cues) {
  let s = heading(stage(t, cues)[1]);
  const final = t >= 63.26;
  s += box(120, 310, 340, 230, 'Receiver / buffer', ['Liquid inventory'], t >= 28.55 || final);
  s += box(715, 310, 380, 230, 'Cold plates', ['Boiling at the heat source'], t >= 11.59 || final);
  s += box(1390, 310, 380, 230, 'Condenser / CDU', ['Vapor becomes liquid'], t >= 20.72 || final);
  s += arrow('M460 450 H715', t >= 6.43 ? 'green' : 'line', 6, '', 'controlled-feed');
  s += arrow('M1095 450 H1390', t >= 15.79 ? 'purple' : 'line', 6, '', 'controlled-vapor');
  s += arrow('M1580 540 V760 Q1580 790 1550 790 H320 Q290 790 290 760 V540', t >= 20.72 ? 'green' : 'line', 6, '', 'controlled-return');
  s += text(588, 404, 'Liquid feed', 28, C.green, 'middle');
  s += text(1242, 404, 'Vapor-rich return', 28, C.purple, 'middle');
  s += text(1330, 738, 'Condensed liquid', 28, C.green, 'middle');
  s += rect(150, 452, 280, 58, C.line, '#e2f2e8', 4);
  if (t >= 28.55) {
    s += line('M420 462 H370 M420 500 H370', C.green, 3);
  }
  if (t >= 11.59) {
    const n = t < 15.79 ? Math.floor(clamp((t - 11.59) / 3) * 5) + 1 : 6;
    for (let i = 0; i < n; i++) s += circle(764 + i * 52, 490 - (i % 2) * 14, 9, C.purple);
  }
  if (t >= 20.72) {
    s += line('M1460 463 H1680 M1460 487 H1680', C.purple, 5);
    s += line('M1460 506 H1680', C.green, 5);
    s += text(1580, 239, 'Heat to FWS, air, or another path', 27, C.muted, 'middle');
    s += arrow('M1580 310 V260', 'orange');
  }
  if (t >= 34.35 && t < 40.30) {
    s += `<circle cx="588" cy="450" r="33" fill="white" stroke="${C.green}" stroke-width="4"/><path d="M577 435 L604 450 L577 465 Z" fill="${C.green}"/>`;
    s += text(588, 536, 'Pump', 26, C.green, 'middle');
    s += text(890, 645, 'Pumped: subcooled liquid at the pump inlet', 29, C.green, 'middle', 600);
  }
  if (t >= 40.30) s += text(890, 645, 'Passive designs use a different circulation mechanism', 29, C.muted, 'middle');
  if (t >= 34.35) s += text(890, 858, 'Liquid circulation is design dependent', 29, C.muted, 'middle');
  if (t >= 46.20) {
    s += line('M1770 342 H1820 V176 H905 V310', C.purple, 4, '10 8');
    s += rect(570, 149, 610, 58, C.line, 'white', 4);
    s += text(875, 189, 'Pressure sets saturation temperature', 29, C.purple, 'middle', 600);
  }
  if (t >= 55.01) {
    s += text(120, 945, 'Monitor: vapor P / T and liquid P / T', 30, C.ink, 'start', 600);
    s += text(120, 991, 'Manage phase, pressure, charge, and returning liquid', 28, C.muted);
  }
  if (t >= 34.35 && t < 40.30) {
    s += pathDot(t, 34.35, 40.30, 'controlled-feed', { color: C.green, hollow: false, radius: 6, range: [0, 93] });
    s += pathDot(t, 34.35, 40.30, 'controlled-feed', { color: C.green, hollow: false, radius: 6, range: [163, 255] });
  } else s += pathDot(t, 6.43, 63.26, 'controlled-feed', { color: C.green, hollow: false, radius: 8 });
  s += pathDot(t, 15.79, 63.26, 'controlled-vapor', { hollow: false, radius: 8 });
  s += pathDot(t, 20.72, 63.26, 'controlled-return', { period: 12, color: C.green, hollow: false, radius: 8, count: 3 });
  return s;
}
function purging(t, cues) {
  let s = heading(stage(t, cues)[1]);
  const flowing = t >= 16.69;
  const purge = t >= 43.44;
  const final = t >= 53.43;
  s += box(120, 300, 330, 230, 'Liquid supply', ['Fill systematically', 'Prime before flow'], t >= 5.74);
  s += box(720, 300, 370, 230, 'Server cold plates', ['Service can admit air'], flowing);
  s += box(1400, 300, 390, 230, 'CDU / buffer', ['Gas collection space'], flowing);
  s += arrow('M450 430 H720', flowing ? 'green' : 'line', 6, '', 'purging-feed');
  s += arrow('M1090 430 H1400', flowing ? 'purple' : 'line', 6, '', 'purging-vapor');
  s += arrow('M1595 530 V660 Q1595 690 1565 690 H315 Q285 690 285 660 V530', flowing ? 'green' : 'line', 6, '', 'purging-return');
  s += text(585, 383, 'Liquid feed', 28, C.green, 'middle');
  s += text(1245, 383, 'Working-fluid vapor', 27, C.purple, 'middle');
  s += text(860, 742, 'Condensed liquid returns', 28, C.green, 'middle');
  s += rect(150, 463, 268, 37, C.line, 'white', 3);
  s += `<rect x="153" y="466" width="${262 * clamp((t - 5.74) / 7.57)}" height="31" fill="#e2f2e8"/>`;
  if (t >= 16.69 && t < 31.69) {
    s += text(720, 186, 'Server added or replaced', 29, C.orange);
    s += arrow('M905 212 V300', 'orange', 6, '', 'purging-service');
    s += pathDot(t, 19.59, 31.69, 'purging-service', { period: 5, color: C.orange, radius: 6 });
  }
  const arrived = t < 19.59 ? 0 : Math.min(6, Math.floor((t - 19.59) / 1.85) + 1);
  const remaining = purge ? Math.max(0, 6 - Math.floor((t - 43.44) / 1.35)) : arrived;
  for (let i = 0; i < remaining; i++) s += circle(1442 + i * 57, 461 + (i % 2) * 20, 10, C.orange, true);
  if (t >= 24 && t < 43.44) s += pathDot(t, 24, 43.44, 'purging-vapor', { period: 6, color: C.orange, radius: 8 });
  if (t >= 31.69 && t < 53.43) {
    s += text(1595, 181, 'Non-critical alarm', 31, C.orange, 'middle', 600);
    s += text(1595, 224, 'Purging required', 28, C.orange, 'middle');
  }
  if (t >= 38.19) {
    s += box(1370, 820, 420, 164, 'Dedicated purge system', ['Connected to buffer port'], purge, C.orange);
    s += circle(1790, 466, 7, C.orange);
    s += arrow('M1797 466 H1830 V720 Q1830 750 1800 750 H1760 V820', 'orange', 6, '', 'purging-port');
    s += text(1740, 590, 'Purge port', 26, C.orange, 'end');
  }
  if (purge && !final) {
    s += pathDot(t, 43.44, 53.43, 'purging-port', { period: 4.5, color: C.orange, radius: 8, count: 3 });
    s += text(120, 845, 'Cooling continues during purging', 32, C.green, 'start', 600);
  }
  if (final) {
    s += text(120, 845, 'Non-condensable gas removed', 32, C.green, 'start', 600);
    s += text(120, 890, 'Condensation and heat transfer protected', 29, C.muted);
  }
  s += pathDot(t, 16.69, 53.43, 'purging-feed', { color: C.green, hollow: false, radius: 8 });
  s += pathDot(t, 16.69, 53.43, 'purging-vapor', { hollow: false, radius: 8 });
  s += pathDot(t, 16.69, 53.43, 'purging-return', { period: 10, color: C.green, hollow: false, radius: 8, count: 3 });
  s += circle(134, 972, 9, C.green) + text(159, 983, 'Liquid', 26, C.muted);
  s += circle(319, 972, 9, C.purple) + text(344, 983, 'Working-fluid vapor', 26, C.muted);
  s += circle(654, 972, 10, C.orange, true) + text(680, 983, 'Air / non-condensable gas', 26, C.muted);
  return s;
}
export const storyboards = [
  { slide: 'M1S4', stem: 'nested_loops_synced', duration: 75.00045351473923, audio: 'audio/module1/slide_04_nested_loops.wav', script: 'audio/module1/slide_04_nested_loops.txt', draw: nested, cues: [[0,'Separate the technology and facility loops'],[3.89,'Heat begins at the silicon'],[14.04,'Single-phase liquid warms'],[21.34,'Two-phase fluid absorbs latent heat'],[35.61,'The CDU decouples the fluid circuits'],[47.26,'Facility water carries heat upstream'],[68.08,'Two-phase complexity stays within TCS / CDU']] },
  { slide: 'M2S5', stem: 'controlled_two_phase_loop_synced', duration: 71.98185941043084, audio: 'audio/module2/slide_05_controlled_loop.wav', script: 'audio/module2/slide_05_controlled_loop.txt', draw: controlled, cues: [[0,'A controlled two-phase cooling loop'],[6.43,'Liquid feeds the cold plates'],[11.59,'Device heat boils part of the liquid'],[15.79,'Vapor-rich return carries heat to the CDU'],[20.72,'The condenser returns vapor to liquid'],[28.55,'The receiver manages charge and inventory'],[34.35,'Pumped systems need liquid at the inlet'],[40.30,'Passive systems circulate fluid differently'],[46.20,'Pressure and saturation temperature are linked'],[55.01,'Pressure and temperature inform thermal control'],[63.26,'Facility: remove heat. TCS: manage the working fluid.']] },
  { slide: 'M4S4', stem: 'filling_purging_synced', duration: 65.84, audio: 'audio/module4/slide_04_filling_purging.wav', script: 'audio/module4/slide_04_filling_purging.txt', draw: purging, cues: [[0,'Filling protects long-term thermal performance'],[5.74,'Fill systematically and prime before flow'],[13.31,'Prime the loop before flow'],[16.69,'Service events can introduce air'],[31.69,'Accumulation triggers a non-critical purge alarm'],[38.19,'Connect a dedicated purge system at the buffer'],[43.44,'Remove gas while cooling continues'],[53.43,'Protect condensation and heat transfer']] },
];
export function createHtml(item) {
  return `<!doctype html><html lang="en"><meta charset="utf-8"><style>html,body{margin:0;width:1920px;height:1080px;background:#fff}svg{display:block;font-family:Arial,sans-serif;letter-spacing:0}</style><body data-duration-ms="${item.duration * 1000}" data-poster-ms="${(item.duration - 2) * 1000}"><svg id="scene" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080"></svg><script>const draw=${item.draw.toString()};${[escape,text,rect,box,arrow,line,circle,clamp,stage,heading,pathDot,positionPathDots].map((f) => `const ${f.name}=${f.toString()};`).join('')}const C=${JSON.stringify(C)},defs=${JSON.stringify(defs)},cues=${JSON.stringify(item.cues)};window.setAcademyVideoTime=(seconds)=>{const svg=document.querySelector('#scene');svg.innerHTML=defs+draw(Math.max(0,Math.min(${item.duration},seconds)),cues);for(const p of svg.querySelectorAll('path[marker-end]')){const q=p.getPointAtLength(p.getTotalLength()-18);p.setAttribute('d',p.getAttribute('d').replace(/([HV])\\s*[-+.0-9]+$/,(_,axis)=>axis+(axis==='H'?q.x:q.y)));}positionPathDots(svg);};window.setAcademyVideoTime(0);</script></body></html>`;
}
