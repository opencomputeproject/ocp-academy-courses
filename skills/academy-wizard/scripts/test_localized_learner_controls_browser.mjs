// Check both supported narration-label schemas without audible playback or LMS access.
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {chromium} from 'playwright';

const scripts=path.dirname(fileURLToPath(import.meta.url));
const skill=path.dirname(scripts);
const temporary=await fs.mkdtemp(path.join(os.tmpdir(),'academy-label-compat-'));
const render='import json,sys;sys.path.insert(0,sys.argv[1]);from render_module import render_module;print(render_module(json.load(sys.stdin),0))';
const browser=await chromium.launch({headless:true,args:['--mute-audio']});
let checks=0;
const check=(actual,expected,label)=>{assert.deepEqual(actual,expected,label);checks++;};
try{
 await fs.copyFile(path.join(skill,'assets/scorm_api.js'),path.join(temporary,'scorm_api.js'));
 for(const schema of ['current','earlier']){
  const labels={transcript:'Texto del audio',slide_transcript:'Texto de la diapositiva',
   close_transcript:'Cerrar texto',narration_hint:'La narracion empieza automaticamente.'};
  const on='Audio activado',off='Audio desactivado',message='El audio esta desactivado.';
  if(schema==='current')Object.assign(labels,{automatic_narration:'Audio automatico',narration_on:on,narration_off:off,narration_off_hint:message});
  else Object.assign(labels,{toggle_narration:'Audio automatico',narration_on_hint:on,narration_off_hint:off,narration_off_message:message});
  const course={style:'Slides',course_slug:'localized-controls-'+schema,course_title:'Control labels',
   language:'es-419',motion_intro:{enabled:false},ui_labels:labels,
   modules:[{id:1,title:'Control labels',slides:[{id:1,type:'title',title:'Control labels',transcript:'Texto narrado.'}]}]};
  const markup=execFileSync(process.env.PYTHON||'python3',['-c',render,scripts],{input:JSON.stringify(course),encoding:'utf8'});
  const file=path.join(temporary,schema+'.html');await fs.writeFile(file,markup);
  const context=await browser.newContext();
  await context.route(/^https?:/,route=>route.abort());
  await context.addInitScript(()=>{HTMLMediaElement.prototype.play=function(){this.muted=true;return Promise.resolve();};});
  const page=await context.newPage(),errors=[];page.on('pageerror',error=>errors.push(error.message));
  await page.goto(pathToFileURL(file).href);
  const toggle=page.locator('#narrationModeBtn'),hint=page.locator('.hero-start-hint span');
  check(await toggle.getAttribute('aria-label'),'Audio automatico',schema+': localized narration label');
  check(await toggle.getAttribute('title'),on,schema+': on tooltip');
  check(await hint.innerText(),labels.narration_hint,schema+': authored title hint');
  await toggle.click();
  check(await toggle.getAttribute('title'),off,schema+': off tooltip is not the body message');
  check(await hint.innerText(),message,schema+': off body is not the tooltip');
  await page.reload();
  check(await toggle.getAttribute('aria-pressed'),'false',schema+': saved off restored');
  check(await toggle.getAttribute('title'),off,schema+': off tooltip restored');
  check(await hint.innerText(),message,schema+': off body restored');
  await toggle.click();
  check(await hint.innerText(),labels.narration_hint,schema+': original hint restored after enabling');
  check(await toggle.getAttribute('title'),on,schema+': on tooltip restored');
  check(await page.locator('#transcriptBtn').getAttribute('aria-label'),labels.transcript,schema+': transcript label');
  await page.locator('#transcriptBtn').click();
  check(await page.locator('#transcriptPanel').getAttribute('aria-label'),labels.slide_transcript,schema+': transcript panel label');
  check(await page.locator('#transcriptClose').innerText(),labels.close_transcript,schema+': close transcript label');
  check(errors,[],schema+': no JavaScript errors');
  await context.close();
 }
 console.log(`PASS: ${checks} localized-control compatibility assertions; headless and muted.`);
}finally{await browser.close();await fs.rm(temporary,{recursive:true,force:true});}
