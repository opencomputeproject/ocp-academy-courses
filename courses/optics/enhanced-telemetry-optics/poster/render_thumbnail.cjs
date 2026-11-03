// Compatibility entrypoint: the shared Academy poster renderer owns the layout.
const fs=require('node:fs'), path=require('node:path');
const {spawnSync}=require('node:child_process');
const here=__dirname;
function ancestor(start,file){
  for(let p=start;;p=path.dirname(p)){
    if(fs.existsSync(path.join(p,file)))return p;
    if(path.dirname(p)===p)throw new Error(`Cannot find ${file}`);
  }
}
const course=ancestor(here,'poster.json');
const repo=ancestor(course,'skills/academy-wizard/scripts/render_lms_posters.mjs');
const result=spawnSync(process.execPath,[path.join(repo,'skills/academy-wizard/scripts/render_lms_posters.mjs'),'--repo-root',repo,'--course',course,...process.argv.slice(2)],{stdio:'inherit'});
if(result.error)throw result.error;
process.exit(result.status??1);
