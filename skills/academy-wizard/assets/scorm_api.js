/**
 * SCORM 1.2 API Wrapper for OCP NIC 3.0 Academy
 * Handles communication between the course and the LMS
 */
var SCORM = (function() {
  'use strict';

  // Opt-in Slides shell owns one LMS session across all course pages.
  try {
    if (window.parent !== window && window.parent.AcademySingleSCO) {
      var pageSession = window.parent.AcademySingleSCO.forPage(window.location.href);
      if (pageSession) return pageSession;
    }
  } catch (_) { /* A cross-origin LMS ancestor is not a course session. */ }

  var api = null;
  var initialized = false;

  // Find the SCORM API object from the LMS
  function findAPI(win) {
    var attempts = 0;
    while (win && attempts++ < 10) {
      try { if (win.API) return win.API; } catch (_) {}
      try { if (!win.parent || win.parent === win) break; win = win.parent; }
      catch (_) { break; }
    }
    return null;
  }

  function getAPI() {
    if (api) return api;
    api = findAPI(window);
    if (!api && window.opener) {
      api = findAPI(window.opener);
    }
    return api;
  }

  return {
    isAvailable: function() { return !!getAPI(); },
    init: function() {
      if (initialized) return true;
      var lmsAPI = getAPI();
      if (lmsAPI) {
        var result = lmsAPI.LMSInitialize('');
        initialized = (result === 'true' || result === true);
      }
      return initialized;
    },

    finish: function() {
      var lmsAPI = getAPI();
      if (lmsAPI && initialized) {
        lmsAPI.LMSCommit('');
        lmsAPI.LMSFinish('');
        initialized = false;
      }
    },

    setCompleted: function() {
      var lmsAPI = getAPI();
      if (lmsAPI && initialized) {
        lmsAPI.LMSSetValue('cmi.core.lesson_status', 'completed');
        lmsAPI.LMSCommit('');
      }
    },

    setIncomplete: function() {
      var lmsAPI = getAPI();
      if (lmsAPI && initialized) {
        lmsAPI.LMSSetValue('cmi.core.lesson_status', 'incomplete');
        lmsAPI.LMSCommit('');
      }
    },

    setLocation: function(location) {
      var lmsAPI = getAPI();
      if (lmsAPI && initialized) {
        lmsAPI.LMSSetValue('cmi.core.lesson_location', String(location));
        lmsAPI.LMSCommit('');
      }
    },

    getLocation: function() {
      var lmsAPI = getAPI();
      if (lmsAPI && initialized) {
        return lmsAPI.LMSGetValue('cmi.core.lesson_location');
      }
      return '';
    },

    setSuspendData: function(data) {
      var lmsAPI = getAPI();
      if (lmsAPI && initialized) {
        lmsAPI.LMSSetValue('cmi.suspend_data', String(data));
        lmsAPI.LMSCommit('');
      }
    },

    getSuspendData: function() {
      var lmsAPI = getAPI();
      if (lmsAPI && initialized) {
        return lmsAPI.LMSGetValue('cmi.suspend_data');
      }
      return '';
    },

    getStatus: function() {
      var lmsAPI = getAPI();
      if (lmsAPI && initialized) {
        return lmsAPI.LMSGetValue('cmi.core.lesson_status');
      }
      return '';
    },

    setValue: function(element, value) {
      var lmsAPI = getAPI();
      if (lmsAPI && initialized) {
        var result = lmsAPI.LMSSetValue(String(element), String(value));
        var committed = lmsAPI.LMSCommit('');
        return (committed === 'true' || committed === true) ? result : 'false';
      }
      return '';
    },

    getValue: function(element) {
      var lmsAPI = getAPI();
      if (lmsAPI && initialized) {
        return lmsAPI.LMSGetValue(String(element));
      }
      return '';
    }
  };
})();
