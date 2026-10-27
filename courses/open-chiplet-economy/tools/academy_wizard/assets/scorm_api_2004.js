/** SCORM 2004 3rd Edition adapter for standalone AcademyWizard courses. */
var SCORM = (function() {
  'use strict';
  var api = null;
  var initialized = false;
  function findAPI(win) {
    for (var depth = 0; win && depth < 20; depth++) {
      try {
        if (win.API_1484_11) return win.API_1484_11;
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
  function succeeded(value) { return value === true || value === 'true'; }
  function get(element) {
    return initialized && getAPI() ? api.GetValue(String(element)) : '';
  }
  function set(element, value) {
    if (!initialized || !getAPI()) return '';
    var result = api.SetValue(String(element), String(value));
    var committed = api.Commit('');
    return succeeded(committed) ? result : 'false';
  }
  return {
    isAvailable: function() { return !!getAPI(); },
    init: function() {
      if (initialized) return true;
      if (getAPI()) initialized = succeeded(api.Initialize(''));
      return initialized;
    },
    finish: function() {
      if (!initialized || !getAPI()) return;
      api.SetValue('cmi.exit', get('cmi.completion_status') === 'completed' ? 'normal' : 'suspend');
      api.Commit('');
      if (succeeded(api.Terminate(''))) initialized = false;
    },
    setCompleted: function() { return set('cmi.completion_status', 'completed'); },
    setIncomplete: function() { return set('cmi.completion_status', 'incomplete'); },
    setLocation: function(value) { return set('cmi.location', value); },
    getLocation: function() { return get('cmi.location'); },
    setSuspendData: function(value) {
      if (String(value).length > 64000) throw new Error('SCORM 2004 saved state exceeds 64000 characters');
      return set('cmi.suspend_data', value);
    },
    getSuspendData: function() { return get('cmi.suspend_data'); },
    getStatus: function() { return get('cmi.completion_status'); },
    setValue: set,
    getValue: get
  };
})();
