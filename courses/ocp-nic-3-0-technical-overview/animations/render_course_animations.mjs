import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawn,execFileSync} from 'node:child_process';
import {once} from 'node:events';
import {createHash} from 'node:crypto';
import sharp from 'sharp';
import {renderScene} from '../animations/scenes.mjs';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const work=path.resolve(process.env.ACADEMY_ANIMATION_COURSE_DIR||root);
const skill=process.env.ACADEMY_WIZARD_SKILL_DIR||path.resolve(root,'../../skills/academy-wizard');
const plan=JSON.parse(await fs.readFile(path.join(root,'animations/plan.json'),'utf8'));
const course=JSON.parse(await fs.readFile(path.join(work,'course.json'),'utf8'));
const flags=new Set(process.argv.slice(2));
const final=flags.has('--final');
if(final&&(!plan.scripts_approved||!plan.new_single_pass_mode_approved)) throw new Error('Final rendering requires recorded script and synchronized-playback approval');
const encode=flags.has('--encode');
const requested=process.argv.find(arg=>arg.startsWith('--only='))?.slice(7).split(',');
if(requested?.some(id=>!plan.videos.some(video=>video.id===id))) throw new Error('Unknown animation requested');
const ffmpeg=process.env.FFMPEG_BIN||'ffmpeg';

function body(script) {return script.split('\n').filter(line=>!line.trimStart().startsWith('#')).join('\n').trim();}
const hash=value=>createHash('sha256').update(value).digest('hex');
function wavDuration(buffer) {
  if(buffer.toString('ascii',0,4)!=='RIFF'||buffer.toString('ascii',8,12)!=='WAVE') throw new Error('Narration must be a PCM WAV');
  let offset=12,rate=0,data=0;
  while(offset+8<=buffer.length) {
    const name=buffer.toString('ascii',offset,offset+4),size=buffer.readUInt32LE(offset+4);
    if(name==='fmt ') rate=buffer.readUInt32LE(offset+16);
    if(name==='data') data+=size;
    offset+=8+size+(size%2);
  }
  if(!rate||!data) throw new Error('Missing WAV format or samples');
  return data/rate;
}
function normalized(value) {
  const output=[],indices=[];
  for(const [i,c] of Array.from(value).entries()) if(/[a-z0-9]/i.test(c)) {output.push(c.toLowerCase());indices.push(i);}
  return {text:output.join(''),indices};
}
async function timeline(video,slide) {
  const script=body(await fs.readFile(path.join(work,slide.audio.script_file),'utf8'));
  let duration,aligned=null,audioProvenance=null;
  if(final) {
    const wav=await fs.readFile(path.join(work,slide.audio.wav_file));
    duration=wavDuration(wav);
    const alignmentBytes=await fs.readFile(path.join(work,slide.audio.script_file.replace(/\.txt$/,'.alignment.json')));
    const data=JSON.parse(alignmentBytes.toString('utf8'));
    if(data.script_sha256!==hash(script)||data.wav_sha256!==hash(wav)) throw new Error(`Stale narration or timing data: ${video.id}`);
    if(plan.approved_script_sha256?.[slide.audio.script_file]!==hash(script)) throw new Error(`Script differs from its approved version: ${video.id}`);
    if(data.voice_id!==plan.narration.voice_id||data.model_id!==plan.narration.model_id||['speed','stability','similarity_boost'].some(key=>data.voice_settings?.[key]!==plan.narration[key])) throw new Error(`Narration settings differ from the approved voice: ${video.id}`);
    aligned=data.alignment||data.normalized_alignment;
    if(!aligned?.characters?.length||aligned.characters.length!==aligned.character_start_times_seconds?.length||aligned.characters.length!==aligned.character_end_times_seconds?.length) throw new Error(`Invalid alignment for ${video.id}`);
    if(aligned.character_start_times_seconds.some((start,i)=>start<0||start>duration||aligned.character_end_times_seconds[i]<start||aligned.character_end_times_seconds[i]>duration+.1||(i&&start<aligned.character_start_times_seconds[i-1]))) throw new Error(`Invalid character timing for ${video.id}`);
    audioProvenance={script_sha256:hash(script),wav_sha256:hash(wav),alignment_sha256:hash(alignmentBytes),voice_id:data.voice_id,model_id:data.model_id,voice_settings:data.voice_settings};
  } else duration=script.split(/\s+/).length/(170/60)+1;
  const actual=normalized(aligned?aligned.characters.join(''):script);
  const scenes=video.scenes.map((scene,index)=>{
    const match=actual.text.indexOf(normalized(scene.anchor).text);
    if(match<0) throw new Error(`Missing scene anchor: ${video.id}: ${scene.anchor}`);
    const char=actual.indices[match];
    const start=index===0?0:aligned?aligned.character_start_times_seconds[char]:duration*char/script.length;
    return {...scene,start};
  });
  if(scenes.some((scene,i)=>i&&scene.start<=scenes[i-1].start)) throw new Error(`Non-monotonic scene timing: ${video.id}`);
  return {id:video.id,width:plan.width,height:plan.height,fps:plan.fps,duration,poster_time:duration-1/plan.fps,timing:final?'measured narration and provider character alignment':'draft estimate; not final narration synchronization',audio_provenance:audioProvenance,scenes};
}

for(const video of plan.videos) {
  if(requested&&!requested.includes(video.id)) continue;
  const module=course.modules.find(m=>m.id===video.module),slide=module.slides.find(s=>s.id===video.slide);
  const master=await timeline(video,slide);
  const sources=path.join(root,'animations',video.id);
  const qa=path.join(work,'animation-qa',video.id);
  const output=path.join(work,final?'figures':'animation-drafts');
  await fs.mkdir(sources,{recursive:true});await fs.mkdir(qa,{recursive:true});await fs.mkdir(output,{recursive:true});
  for(const [directory,extension] of [[sources,'svg'],[qa,'png']]) {
    for(const file of await fs.readdir(directory)) {
      if(new RegExp(`^\\d{2}_[a-z_]+_\\d+\\.\\d{2}\\.${extension}$`).test(file)) await fs.unlink(path.join(directory,file));
    }
  }
  await fs.writeFile(path.join(sources,'master.json'),JSON.stringify(master,null,2)+'\n');
  const frameCount=Math.round(master.duration*plan.fps);
  const checkpoints=new Set([0,.25,.5,.75,1].map(v=>Math.min(master.duration-1/plan.fps,master.duration*v)));
  for(const [sceneIndex,scene] of master.scenes.entries()) {
    for(const delta of [-.05,.05,.6,2.7,6]) {
      const t=scene.start+delta;
      if(t>=0&&t<master.duration) checkpoints.add(t);
    }
    const end=master.scenes[sceneIndex+1]?.start??master.duration;
    for(const fraction of [.25,.5,.75,.95]) checkpoints.add(scene.start+(end-scene.start)*fraction);
  }
  const reviewed=[];
  let index=0;
  for(const time of [...checkpoints].sort((a,b)=>a-b)) {
    const frame=renderScene(video.id,time,master);
    const stem=`${String(index++).padStart(2,'0')}_${frame.scene}_${time.toFixed(2)}`;
    await fs.writeFile(path.join(sources,`${stem}.svg`),frame.svg);
    await sharp(Buffer.from(frame.svg)).png().toFile(path.join(qa,`${stem}.png`));
    reviewed.push({time,scene:frame.scene,file:`${stem}.png`,texts:frame.texts,bounds:frame.bounds});
  }
  const poster=renderScene(video.id,master.poster_time,master);
  await sharp(Buffer.from(poster.svg)).png().toFile(path.join(output,`${video.id}_poster.png`));
  await fs.writeFile(path.join(qa,'checkpoints.json'),JSON.stringify(reviewed,null,2)+'\n');
  if(encode) {
    execFileSync(process.env.PYTHON||'python3',[path.join(skill,'scripts/check_svg_arrows.py'),sources,'--fail-on-flags'],{stdio:'inherit'});
    const destination=path.join(output,`${video.id}.mp4`);
    const encoder=spawn(ffmpeg,['-hide_banner','-loglevel','warning','-y','-f','image2pipe','-vcodec','png','-framerate',String(plan.fps),'-i','pipe:0','-an','-c:v','libx264','-preset','slow','-tune','animation','-crf','8','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',destination],{stdio:['pipe','ignore','pipe']});
    let errors='';encoder.stderr.on('data',chunk=>{errors+=chunk.toString();});
    const ended=once(encoder,'close');
    let lastSvg='',lastPng=null;
    for(let frameIndex=0;frameIndex<frameCount;frameIndex++) {
      const time=Math.min(master.duration-1/plan.fps,frameIndex/plan.fps);
      const source=renderScene(video.id,time,master).svg;
      if(source!==lastSvg) {lastPng=await sharp(Buffer.from(source)).png().toBuffer();lastSvg=source;}
      if(!encoder.stdin.write(lastPng)) await once(encoder.stdin,'drain');
    }
    encoder.stdin.end();
    const [code]=await ended;
    if(code!==0) throw new Error(`Encoding failed: ${video.id}: ${errors.slice(-2000)}`);
    console.log(`Encoded ${video.id}: ${frameCount} frames, ${(frameCount/plan.fps).toFixed(3)}s, 1920x1080, silent H.264 (${master.timing})`);
  } else console.log(`Prepared ${video.id}: ${reviewed.length} lossless review frames (${master.timing})`);
}
