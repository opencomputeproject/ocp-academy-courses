import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {renderScene} from '../animations/scenes.mjs';

const root=path.resolve(import.meta.dirname,'..');
const plan=JSON.parse(await fs.readFile(path.join(root,'animations/plan.json'),'utf8'));
let count=0;
const timingModes=new Set();
for(const video of plan.videos) {
  const master=JSON.parse(await fs.readFile(path.join(root,'animations',video.id,'master.json'),'utf8'));
  timingModes.add(master.timing.startsWith('measured')?'measured narration':'draft estimates');
  for(let frame=0;frame<Math.round(master.duration*master.fps);frame++) {
    const scene=renderScene(video.id,Math.min(master.duration-1/master.fps,frame/master.fps),master);
    for(const box of scene.bounds) {
      assert(box.padding>=.75*box.font_size,`${video.id}: ${box.title}: horizontal clearance`);
      assert(box.bottom_clearance>=.75*box.font_size,`${video.id}: ${box.title}: bottom clearance`);
    }
    count++;
  }
  if(video.id==='m3_power_states_synchronized') {
    const final=renderScene(video.id,master.duration-1/master.fps,master);
    assert(final.texts.includes('Back in ID Mode: AUX_PWR_EN = 0 and MAIN_PWR_EN = 0; AUX/Main regulators stay disabled.'));
    assert(!final.texts.includes('Optional branch: MAIN_PWR_EN = 1, but AUX/Main regulators stay disabled.'));
  }
  if(video.id==='m1_host_topologies') {
    const dual=renderScene(video.id,master.scenes.find(scene=>scene.id==='dual').start+3,master);
    assert.equal(dual.texts.filter(text=>text==='One host').length,1);
    assert(dual.texts.includes('Root port 0')&&dual.texts.includes('Root port 1'));
  }
  if(video.id==='m5_airflow_comparison') {
    const final=renderScene(video.id,master.duration-1/master.fps,master);
    assert(!final.svg.includes('<circle'),'Air particles must finish once and not restart in the comparison scene');
  }
  if(video.id==='m4_ncsi_arbitration') {
    const token=master.scenes.find(scene=>scene.id==='token');
    const next=master.scenes[master.scenes.indexOf(token)+1];
    const completed=renderScene(video.id,next.start-1/master.fps,master);
    const position=completed.svg.match(/<circle cx="([\d.]+)" cy="([\d.]+)"/);
    assert(position&&Math.abs(Number(position[1])-690)<.001&&Math.abs(Number(position[2])-774)<.001,'Token must complete its return before the inactive-slot scene');
  }
  console.log(`${video.id}: every frame passed text containment and fixed-padding checks`);
}
console.log(`Checked ${count} frames using ${[...timingModes].join(', ')}; human listening and player acceptance are separate checks.`);
