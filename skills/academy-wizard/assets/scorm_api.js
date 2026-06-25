/**
 * SCORM 1.2 API Wrapper for OCP NIC 3.0 Academy
 * Handles communication between the course and the LMS
 */
var SCORM = (function() {
  'use strict';

  var api = null;
  var initialized = false;

  // Find the SCORM API object from the LMS
  function findAPI(win) {
    var attempts = 0;
    while ((!win.API) && (win.parent) && (win.parent !== win)) {
      attempts++;
      if (attempts > 10) return null;
      win = win.parent;
    }
    return win.API || null;
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
    init: function() {
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
        lmsAPI.LMSCommit('');
        return result;
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
