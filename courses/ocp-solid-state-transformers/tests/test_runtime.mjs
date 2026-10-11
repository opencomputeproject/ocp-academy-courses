// Isolated tests of actual generated player code, not a browser/LMS claim.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
if (!process.argv[2]) throw new Error('Usage: node test_runtime.mjs <built-SST-course>');
const root=path.resolve(process.argv[2]);
const course=JSON.parse(fs.readFileSync(path.join(root,'course.json')));
let checks=0;
const check=(a,b,n)=>{assert.deepEqual(a,b,n);checks++;};
function functionCode(source,name){
  const start=source.indexOf('function '+name+'(');assert.ok(start>=0,name);
  let n=source.indexOf('{',start),level=1,end=n+1;
  while(level){const c=source[end++];if(c==='{')level++;if(c==='}')level--;assert.ok(end<source.length);}
  return source.slice(start,end);
}
function classes(){const values=new Set();return {add:(...v)=>v.forEach(x=>values.add(x)),remove:(...v)=>v.forEach(x=>values.delete(x)),contains:v=>values.has(v),toggle(v,on){if(on===undefined)on=!values.has(v);on?values.add(v):values.delete(v);return on;}};}
for(const module of course.modules){
  const html=fs.readFileSync(path.join(root,`module${module.id}.html`),'utf8');
  for(const code of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g))new vm.Script(code[1]);
  const quiz=html.slice(html.indexOf('  // ===== KNOWLEDGE CHECKS ====='),html.indexOf('  // SCORM integration'));
  const resume=html.slice(html.indexOf('let requested = 1;'),html.indexOf('if (inLMS && !reviewMode && !SCORM.isSingleSCO'));
  const navigation=html.slice(html.indexOf('if (inLMS && !reviewMode && !SCORM.isSingleSCO'),html.indexOf("if (reviewMode) document.addEventListener('click'",html.indexOf('let requested = 1;')));
  const bookmark=`ocp:${course.course_slug}:module${module.id}`;
  const qids=[...html.matchAll(/data-question-id="([^"]+)"/g)].map(m=>m[1]);
  check(new Set(qids).size,2,`M${module.id} retains two questions`);
  check(html.includes('restoreQuizState();')&&html.indexOf('restoreQuizState();')<html.indexOf('let requested = 1;'),true,'Restore before resume');
  for(const mode of ['local','lms','review']){
    const storage=new Map();const lms={status:'incomplete',location:`module${module.id}:slide4`,data:'',writes:0};
    const makeCard=qid=>{
      const feedback={classList:classes(),textContent:''};const buttons={};
      for(const type of ['.quiz-submit','.quiz-retry'])buttons[type]={addEventListener:(event,fn)=>buttons[type].click=fn};
      const inputs=[{value:'a',checked:false,dataset:{correct:'true',feedback:'Correct selection'}},{value:'b',checked:false,dataset:{feedback:'Answer-specific feedback'}}];
      const card={dataset:{questionId:qid,multiple:'false',correctFeedback:'Correct',incorrectFeedback:'Incorrect'},
        querySelectorAll(selector){if(selector==='input:checked')return inputs.filter(i=>i.checked);if(selector==='input[data-correct="true"]')return [inputs[0]];if(selector==='input')return inputs;throw Error(selector);},
        querySelector(selector){if(selector==='.quiz-feedback')return feedback;if(buttons[selector])return buttons[selector];const match=selector.match(/input\[value="(.*)"\]/);return match?inputs.find(i=>i.value===match[1]):null;},
        closest:()=>slides[8],inputs,feedback,buttons};return card;
    };
    const cards=qids.map(makeCard);
    const slides=module.slides.map(s=>({dataset:{slide:String(s.id),quizSlide:String(s.type==='knowledge_check')},classList:classes(),setAttribute(){},querySelectorAll:sel=>sel==='.quiz-card'&&s.type==='knowledge_check'?cards:[],querySelector:()=>({focus(){}})}));
    const links=[{href:'module2.html',getAttribute(){return this.href;},replaceWith(note){this.replacement=note;}},{href:'https://www.opencompute.org/community/power-distribution',getAttribute(){return this.href;},replaceWith(note){this.replacement=note;}}];
    const document={querySelectorAll:sel=>sel==='.quiz-card'?cards:sel==='a[href]'?links:[],createElement:()=>({style:{}}),
      querySelector(sel){if(sel==='.module-badge-text')return {textContent:`MODULE ${module.id}`};if(sel==='.slide.active')return slides.find(s=>s.classList.contains('active'));const match=sel.match(/data-slide="(\d+)"/);return match?slides[Number(match[1])-1]:null;}};
    const ctx=vm.createContext({document,slides,totalSlides:10,reviewMode:mode==='review',inLMS:mode==='lms',directModuleLinks:false,
      existingStatus:'incomplete',BOOKMARK_KEY:bookmark,location:{search:mode==='review'?'?review=1&slide=3':'',href:'https://local.test/module'+module.id+'.html',origin:'https://local.test'},URL,URLSearchParams,CSS:{escape:s=>s},
      localStorage:{getItem:k=>storage.get(k)||null,setItem(k,v){storage.set(k,v);}},
      SCORM:{getLocation:()=>lms.location,setLocation(v){lms.location=v;lms.writes++;},getSuspendData:()=>lms.data,setSuspendData(v){lms.data=v;lms.writes++;},setCompleted(){lms.status='completed';lms.writes++;}},
      updateTranscript(){},updateNarrationMode(){},syncSlideVideos(){},updateControls(){},setTimeout:fn=>fn(),requestAnimationFrame:fn=>fn(),CustomEvent:function(n,o){this.type=n;this.detail=o.detail;},window:{dispatchEvent:()=>vm.runInContext('storeBookmark()',ctx)}});
    vm.runInContext('let currentSlide=1;'+quiz+functionCode(html,'storeBookmark')+functionCode(html,'goToSlide')+functionCode(html,'checkCompletion')+'setupKnowledgeChecks();',ctx);
    const run=code=>vm.runInContext(code,ctx);
    cards[0].inputs[1].checked=true;cards[0].buttons['.quiz-submit'].click();
    cards[0].inputs[1].checked=false;delete cards[0].dataset.attempted;cards[0].feedback.textContent='';
    run('restoreQuizState();');
    if(mode==='review'){
      check(storage.size,0,'Review does not write local state');check(lms.writes,0,'Review does not write LMS');check(cards[0].inputs[1].checked,false,'Review does not restore learner choice');
      run(resume);check(run('currentSlide'),3,'Review explicitly requested slide');
      run(navigation);check(links[0].replacement,undefined,'Review navigation remains functional');
      continue;
    }
    check(cards[0].inputs[1].checked,true,'Incorrect choice restored');check(cards[0].dataset.attempted,'true','Attempted state restored');check(cards[0].feedback.textContent,'Answer-specific feedback','Incorrect feedback restored');
    cards[0].buttons['.quiz-retry'].click();run('restoreQuizState();');check(cards[0].inputs.some(i=>i.checked),false,'Retry does not resurrect answers');
    check(run('getSuspendObject().quizzes['+JSON.stringify(qids[0])+']'),undefined,'Retry cleared persisted record');
    if(mode==='local')storage.set(bookmark,`module${module.id}:slide4`);
    run(resume);check(run('currentSlide'),4,'Unfinished module restores slide');
    run("goToSlide(10,'forward');");check(run('currentSlide'),9,'End-key path cannot bypass quiz');check(lms.status,'incomplete','Unattempted quiz cannot complete');
    for(const card of cards){card.inputs[0].checked=true;card.buttons['.quiz-submit'].click();}
    run("goToSlide(10,'forward');");check(run('currentSlide'),10,'Attempted quiz allows ending');check(lms.status,'completed','Own ending completes own module');
    check(run('getSuspendObject().modules.join()'),String(module.id),'No cross-module completion requirement');
    run("goToSlide(4,'backward');");cards[0].buttons['.quiz-retry'].click();
    ctx.existingStatus=mode==='lms'?'completed':'incomplete';
    run('{'+resume+'}');check(run('currentSlide'),10,'Completed revisit ends even after backtracking/retry');
    run(navigation);check(Boolean(links[0].replacement),mode==='lms','LMS replaces unsafe page link, local keeps it');check(links[1].replacement,undefined,'External links untouched');
  }
}
const home=fs.readFileSync(path.join(root,'index.html'),'utf8');
check((home.match(/<article class="module-card/g)||[]).length,5,'Five informational home tiles');
check(home.includes('SCORM.getSuspendData()'),false,'No misleading cross-SCO status read');
check(home.includes('Start with MODULE 1'),true,'Default first-module start retained');
console.log(`PASS: ${checks} generated-player assertions (isolated DOM/SCORM mocks; not live LMS).`);
