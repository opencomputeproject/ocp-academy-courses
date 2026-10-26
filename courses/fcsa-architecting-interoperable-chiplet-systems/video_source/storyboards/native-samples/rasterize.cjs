const fs=require('fs');const path=require('path');
const dir=__dirname;const root=path.resolve(dir,'../../..');
fs.writeFileSync(path.join(dir,'fonts.conf'),`<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd"><fontconfig><dir>${root}/fonts</dir><cachedir>${dir}/fontcache</cachedir></fontconfig>`);
process.env.FONTCONFIG_FILE=path.join(dir,'fonts.conf');
const sharp=require('/Users/jameskelly/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
(async()=>{for(const f of fs.readdirSync(dir).filter(f=>f.endsWith('.svg')))await sharp(path.join(dir,f)).png().toFile(path.join(dir,f.replace('.svg','.png')));})();
