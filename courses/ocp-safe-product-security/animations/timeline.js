/* A finite, deterministic Web Animations timeline. record_css_animation.mjs
   seeks every animation to a common time. No audio, timers or infinite loops. */
(() => {
  const config=JSON.parse(document.getElementById('timeline').textContent);
  const query=new URLSearchParams(location.search);
  const duration=Number(query.get('durationMs')||config.durationMs);
  if(!Number.isFinite(duration)||duration<=0) throw Error('Invalid master duration');
  document.body.dataset.durationMs=duration;
  document.body.dataset.posterMs=Math.round(duration*config.posterFraction);
  const timelines=[];
  for(const el of document.querySelectorAll('[data-beat]')){
    const key=el.dataset.beat, f=config.beatMs?.[key] !== undefined ? config.beatMs[key]/duration : config.beats[key];
    if(f===undefined) throw Error('Missing beat: '+key);
    const start=Math.max(0,Math.min(.98,f));
    const end=Math.min(1,start+.012);
    const frames=start===0?[{opacity:1,offset:0},{opacity:1,offset:1}]:[
      {opacity:0,offset:0},{opacity:0,offset:start},{opacity:1,offset:end},{opacity:1,offset:1}];
    timelines.push(el.animate(frames,{duration,iterations:1,fill:'both',easing:'linear'}));
  }
  window.academyTimeline={durationMs:duration,beats:Object.fromEntries(Object.entries(config.beats).map(([key,value])=>[key,config.beatMs?.[key] !== undefined ? config.beatMs[key]/duration : value])),seek(ms){for(const a of timelines){a.pause();a.currentTime=Math.max(0,Math.min(duration,ms));}},play(){for(const a of timelines)a.play();},pause(){for(const a of timelines)a.pause();}};
  if(query.has('timeMs')) window.academyTimeline.seek(Number(query.get('timeMs')));
  else if(matchMedia('(prefers-reduced-motion: reduce)').matches)window.academyTimeline.seek(duration);
})();
