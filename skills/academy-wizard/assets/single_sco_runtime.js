/* Persistent SCORM 1.2 session. The home and module HTML pages are assets,
 * not separate SCOs. Only this host initializes/finishes the real LMS API. */
(function () {
  'use strict';
  const config = JSON.parse(document.getElementById('singleSCOConfig').textContent);
  const frame = document.getElementById('courseFrame');
  const warning = document.getElementById('saveWarning');
  const pageModules = new Map(config.modules.map(m => [m.file, m]));
  const allowed = new Set(['index.html', ...pageModules.keys()]);
  const storageKey = 'academy-single-sco:' + config.slug;
  const reviewMode = new URLSearchParams(location.search).get('review') === '1';
  let inLMS = false;
  let connectionFailed = false;
  let finished = false;
  let interactionIndex = 0;
  let state = {academySingleSCO: 1, modules: [], quizzes: {}, bookmarks: {}, page: 'index.html'};

  function report(message) { warning.textContent = message; warning.hidden = !message; }
  function allComplete() { return config.modules.every(m => state.modules.includes(m.id)); }
  function ok(value) { return value === true || value === 'true'; }
  function parse(value) { try { return JSON.parse(value || 'null'); } catch (_) { return null; } }
  function validPage(url) {
    try {
      const base = new URL('.', location.href);
      const target = new URL(url, base);
      const file = target.pathname.slice(base.pathname.length);
      return target.origin === base.origin && target.pathname.startsWith(base.pathname) && allowed.has(file) ? file : null;
    } catch (_) { return null; }
  }

  if (!reviewMode) {
    try { inLMS = SCORM.init(); connectionFailed = !inLMS && SCORM.isAvailable(); }
    catch (_) { connectionFailed = true; }
    if (connectionFailed) report('The LMS connection could not be opened. Progress cannot be saved. Please reopen the course from the LMS.');
    let saved;
    if (inLMS) saved = parse(SCORM.getSuspendData());
    else if (!connectionFailed) { try { saved = parse(localStorage.getItem(storageKey)); } catch (_) {} }
    if (saved && saved.academySingleSCO === 1) {
      state.modules = Array.isArray(saved.modules) ? saved.modules.filter(id => config.modules.some(m => m.id === id)) : [];
      state.quizzes = saved.quizzes && typeof saved.quizzes === 'object' ? saved.quizzes : {};
      state.bookmarks = saved.bookmarks && typeof saved.bookmarks === 'object' ? saved.bookmarks : {};
      state.page = allowed.has(saved.page) ? saved.page : 'index.html';
    }
    if (inLMS) interactionIndex = parseInt(SCORM.getValue('cmi.interactions._count'), 10) || 0;
  }

  function flush() {
    if (reviewMode || finished) return true;
    if (connectionFailed) return false;
    const serialized = JSON.stringify(state);
    if (serialized.length > 4096) {
      report('Progress exceeds the SCORM 1.2 storage limit and could not be saved. Please contact the course administrator.');
      return false;
    }
    if (!inLMS) {
      try { localStorage.setItem(storageKey, serialized); return true; }
      catch (_) { report('This browser is blocking local progress storage. Your place may not be saved.'); return false; }
    }
    try {
      const saved = SCORM.setValue('cmi.suspend_data', serialized);
      const bookmark = state.page === 'index.html' ? 'index' : (state.bookmarks[pageModules.get(state.page).id] || state.page);
      const located = SCORM.setValue('cmi.core.lesson_location', bookmark);
      if (!ok(saved) || !ok(located)) throw new Error('LMS save failed');
      const status = SCORM.getStatus();
      let marked = true;
      if (allComplete()) {
        if (status !== 'completed' && status !== 'passed') marked = SCORM.setValue('cmi.core.lesson_status', 'completed');
      } else if (status !== 'incomplete') marked = SCORM.setValue('cmi.core.lesson_status', 'incomplete');
      if (!ok(marked)) throw new Error('LMS save failed');
      report('');
      return true;
    } catch (_) {
      report('The LMS could not save your progress. Keep this course open and check your connection before exiting.');
      return false;
    }
  }

  window.AcademySingleSCO = {
    forPage: function (url) {
      const file = validPage(url);
      if (!file) return null;
      const mod = pageModules.get(file);
      return {
        isSingleSCO: true,
        init: function () { state.page = file; flush(); return true; },
        finish: function () { return flush(); },
        getStatus: function () { return mod && state.modules.includes(mod.id) ? 'completed' : 'incomplete'; },
        setIncomplete: function () { return flush(); },
        setCompleted: function () {
          if (!mod) return true; // Home is a menu, never course completion.
          if (!mod.quizzes.every(id => state.quizzes[id] && state.quizzes[id].attempted)) return false;
          if (!state.modules.includes(mod.id)) state.modules.push(mod.id);
          return flush();
        },
        getLocation: function () { return mod ? (state.bookmarks[mod.id] || '') : ''; },
        setLocation: function (value) {
          if (mod && new RegExp('^module' + mod.id + ':slide\\d+$').test(value)) state.bookmarks[mod.id] = String(value);
          return flush();
        },
        getSuspendData: function () { return JSON.stringify(state); },
        setSuspendData: function (value) {
          const incoming = parse(value);
          if (!mod || !incoming || !incoming.quizzes) return false;
          for (const id of mod.quizzes) {
            const entry = incoming.quizzes[id];
            if (entry) state.quizzes[id] = {module: mod.id, selected: entry.selected, correct: !!entry.correct, attempted: !!entry.attempted};
          }
          return flush();
        },
        getValue: function (element) {
          if (element === 'cmi.interactions._count') return String(interactionIndex);
          return inLMS && !finished && !reviewMode ? SCORM.getValue(element) : '';
        },
        setValue: function (element, value) {
          // Module players may report quiz interactions, not override overall status.
          const match = /^cmi\.interactions\.(\d+)\./.exec(element);
          if (!match) return false;
          interactionIndex = Math.max(interactionIndex, Number(match[1]) + 1);
          return inLMS && !finished && !reviewMode ? SCORM.setValue(element, value) : 'true';
        }
      };
    }
  };

  function finish() {
    if (finished) return;
    flush();
    if (inLMS && !reviewMode) {
      SCORM.setValue('cmi.core.exit', 'suspend');
      SCORM.finish();
    }
    finished = true;
  }
  window.addEventListener('beforeunload', finish);
  window.addEventListener('pagehide', finish);
  // A browser Back restore must not keep using the terminated LMS session.
  window.addEventListener('pageshow', e => { if (e.persisted && finished) location.reload(); });
  document.addEventListener('visibilitychange', () => { if (document.hidden) flush(); });
  frame.addEventListener('load', () => {
    try {
      frame.contentWindow.focus();
      if (reviewMode) {
        frame.contentDocument.addEventListener('click', event => {
          if (event.defaultPrevented) return;
          const link = event.target.closest('a[href]');
          if (!link || link.target === '_blank') return;
          const file = validPage(link.href);
          if (!file) return;
          event.preventDefault();
          frame.src = file + '?review=1';
        });
      }
    } catch (_) {}
  });
  frame.src = (reviewMode ? 'index.html' : state.page) + (reviewMode ? '?review=1' : '');
})();
