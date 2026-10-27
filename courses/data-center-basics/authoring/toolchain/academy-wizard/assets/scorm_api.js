/** SCORM 1.2 adapter for this four-SCO Academy course. */
var SCORM = (function() {
  'use strict';
  var api = null, initialized = false, started = 0, lastSaveError = '';
  function succeeded(value) { return value === true || value === 'true'; }
  function reportError(element) {
    lastSaveError = String(element);
    window.dispatchEvent(new CustomEvent('academy:scorm-error', {detail:lastSaveError}));
  }
  function findAPI(win) {
    for (var depth = 0; win && depth < 20; depth++) {
      try {
        if (win.API) return win.API;
        if (!win.parent || win.parent === win) break;
        win = win.parent;
      } catch (_) { break; }
    }
    return null;
  }
  function getAPI() {
    if (api) return api;
    api = findAPI(window);
    try { if (!api && window.opener) api = findAPI(window.opener); } catch (_) {}
    return api;
  }
  function get(element) {
    return initialized && getAPI() ? api.LMSGetValue(String(element)) : '';
  }
  function set(element, value) {
    if (!initialized || !getAPI()) return '';
    value = String(value);
    if (element === 'cmi.suspend_data' && value.length > 4096) {
      reportError('cmi.suspend_data exceeds 4096 characters'); return 'false';
    }
    var result = api.LMSSetValue(String(element), value);
    var committed = api.LMSCommit('');
    if (!succeeded(result) || !succeeded(committed)) {
      reportError(element); return 'false';
    }
    return result;
  }
  return {
    version: '1.2',
    isAvailable: function() { return !!getAPI(); },
    getLastSaveError: function() { return lastSaveError; },
    init: function() {
      if (initialized) return true;
      if (getAPI()) {
        initialized = succeeded(api.LMSInitialize(''));
        if (initialized) started = Date.now(); else reportError('LMSInitialize');
      }
      return initialized;
    },
    finish: function() {
      if (!initialized || !getAPI()) return;
      var seconds = Math.max(0, Math.floor((Date.now()-started)/1000));
      var time = String(Math.floor(seconds/3600)).padStart(4,'0') + ':'
        + String(Math.floor(seconds/60)%60).padStart(2,'0') + ':'
        + String(seconds%60).padStart(2,'0');
      set('cmi.core.session_time', time);
      set('cmi.core.exit', get('cmi.core.lesson_status') === 'completed' ? '' : 'suspend');
      if (succeeded(api.LMSFinish(''))) initialized = false; else reportError('LMSFinish');
    },
    setCompleted: function() { return set('cmi.core.lesson_status', 'completed'); },
    setIncomplete: function() { return set('cmi.core.lesson_status', 'incomplete'); },
    setLocation: function(value) { return set('cmi.core.lesson_location', value); },
    getLocation: function() { return get('cmi.core.lesson_location'); },
    setSuspendData: function(value) { return set('cmi.suspend_data', value); },
    getSuspendData: function() { return get('cmi.suspend_data'); },
    getStatus: function() { return get('cmi.core.lesson_status'); },
    setValue: set,
    getValue: get
  };
})();
