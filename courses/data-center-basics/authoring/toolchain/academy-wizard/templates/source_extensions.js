// Functions are hoisted into the maintained module closure, preserving one state owner.
function matchingValues(card, correct) {
  const selects=Array.from(card.querySelectorAll('select[data-prompt-id]'));
  if (!correct && selects.some(s=>!s.value)) return [];
  return selects.map(s=>s.dataset.promptId+'[.]'+(correct?s.dataset.promptId:s.value)).sort();
}
function showScormSaveError(){lmsNote.textContent='Progress could not be saved. Keep this window open and contact your LMS support team before leaving.';lmsNote.hidden=false}
window.addEventListener('academy:scorm-error',showScormSaveError);
if(SCORM.getLastSaveError && SCORM.getLastSaveError()) showScormSaveError();
function matchingFeedback(card, isCorrect) {
  const box=card.querySelector('.quiz-feedback');box.replaceChildren();
  box.classList.remove('correct','incorrect');box.classList.add(isCorrect?'correct':'incorrect');
  const summary=document.createElement('p');summary.textContent=isCorrect?card.dataset.correctFeedback:card.dataset.incorrectFeedback;box.append(summary);
  const pairs=JSON.parse(card.dataset.pairs);const byId=Object.fromEntries(pairs.map(p=>[p.id,p]));
  const list=document.createElement('ul');list.className='matching-results';
  pairs.forEach(pair=>{const selected=card.querySelector('select[data-prompt-id="'+CSS.escape(pair.id)+'"]').value;const li=document.createElement('li');li.textContent=(selected===pair.id?'Correct: ':'Review: ')+pair.prompt+' → '+(byId[selected]?.match||'No match');const explain=document.createElement('span');explain.textContent=(selected===pair.id?'':'Expected: '+pair.match+'. ')+pair.feedback;li.append(explain);list.append(li)});box.append(list);
}
if(inLMS&&SCORM.requestChoice){
  document.querySelectorAll('a.next-module-link[href]').forEach(link=>{
    const match=link.getAttribute('href').match(/^module(\d+)\.html$/);if(!match)return;
    if(!SCORM.canChoose('ITEM_MODULE'+match[1])){link.hidden=true;const note=document.createElement('p');note.className='lms-next-instruction';note.textContent='Open Module '+match[1]+' using your LMS course navigation.';link.parentElement.append(note)}
  });
}
