/** Behavioral checks: long-title fitting, rejected overflow, English-only posters and check immutability. */
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const scripts=path.dirname(fileURLToPath(import.meta.url));
const temp=await fs.mkdtemp(path.join(os.tmpdir(),'academy-poster-test-'));
try{
  const course=path.join(temp,'courses/test');await fs.mkdir(course,{recursive:true});
  await fs.writeFile(path.join(course,'mark.svg'),'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="#8dc63f"/></svg>');
  const base={schema_version:1,language:'en-US',badge:'OCP TEST',title_lines:['INTEGRATING QUANTUM','PROCESSING UNITS','INTO DATA CENTER','INFRASTRUCTURE'],support_lines:['A readable long title'],mark:'mark.svg',mark_alt:'Test mark'};
  async function run(data,extra=[]){
    await fs.writeFile(path.join(course,'poster.json'),JSON.stringify(data));
    return spawnSync(process.execPath,[path.join(scripts,'render_lms_posters.mjs'),'--repo-root',temp,...extra],{encoding:'utf8'});
  }
  const locale=path.join(course,'locales/ko-KR');await fs.mkdir(locale,{recursive:true});
  await fs.writeFile(path.join(locale,'poster.json'),'deliberately invalid: must not be discovered');
  let result=await run(base);assert.equal(result.status,0,result.stderr);
  const report=JSON.parse(await fs.readFile(path.join(temp,'build/poster-qa/report.json'),'utf8'));
  assert.equal(report.posters.length,1,'Translations must not create duplicate catalog posters');
  assert.equal(report.posters[0].titleSize,32);
  const original=await fs.readFile(path.join(course,'thumbnail.png'));
  result=await run(base,['--check']);assert.equal(result.status,0,result.stderr);
  result=await run({...base,title_lines:['UNBREAKABLE'.repeat(30)]});assert.notEqual(result.status,0);assert.match(result.stderr,/Title exceeds/);
  assert.ok(original.equals(await fs.readFile(path.join(course,'thumbnail.png'))),'Overflow must not replace accepted artwork');
  result=await run(base,['--course',locale]);assert.notEqual(result.status,0);assert.match(result.stderr,/canonical English poster/);
  result=await run({...base,language:'ko-KR',badge:'뷁'});assert.notEqual(result.status,0);assert.match(result.stderr,/posters must be in English/);
  result=await run({...base,title_lines:['DIFFERENT TITLE']},['--check']);assert.notEqual(result.status,0);assert.match(result.stderr,/thumbnail differs/);
  assert.ok(original.equals(await fs.readFile(path.join(course,'thumbnail.png'))),'Check must not overwrite a stale image');
  console.log('PASS: long titles fit; overflow and translated posters fail; locale folders are excluded; --check detects drift without changing accepted images.');
}finally{await fs.rm(temp,{recursive:true,force:true});}
