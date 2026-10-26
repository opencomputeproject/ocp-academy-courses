// AcademyWizard Scrolling video component, reused for standalone Slides recordings.
(function() {
  const labels = __STANDALONE_VIDEO_LABELS__;
  const state = {videoPreferences: {captionLanguage: 'off', playbackRate: 1}};
  function uiText(key, fallback) { return labels[key] || fallback; }
  // Keep preferences in this module session; each fresh launch starts captions off.
  function saveState() {}
  function formatVideoTime(seconds) {
    if (!Number.isFinite(seconds) || seconds < 0) seconds = 0;
    var minutes = Math.floor(seconds / 60);
    var remainder = Math.floor(seconds % 60);
    return minutes + ':' + String(remainder).padStart(2, '0');
  }

  function initVideoPlayer(player) {
    var video = player.querySelector('video');
    var progress = player.querySelector('[data-video-progress]');
    var progressLoaded = player.querySelector('[data-video-loaded]');
    var progressPlayed = player.querySelector('[data-video-played]');
    var remaining = player.querySelector('[data-video-remaining]');
    var rateValue = player.querySelector('[data-video-rate-value]');
    var volume = player.querySelector('[data-video-volume]');
    var mute = player.querySelector('[data-video-action="mute"]');
    var fullscreen = player.querySelector('[data-video-action="fullscreen"]');
    var pictureInPicture = player.querySelector('[data-video-action="picture-in-picture"]');
    var captionDisplay = player.querySelector('[data-video-caption-display]');
    var captionText = player.querySelector('[data-video-caption-text]');
    var captionDataNode = player.querySelector('.academy-video__caption-data');
    var captionTracks = [];
    var activeCaptionIndex = -1;
    var inactivityTimer = 0;
    if (!video) return;
    if (captionDataNode) {
      try { captionTracks = (JSON.parse(captionDataNode.textContent || '{}').tracks || []); }
      catch (e) { captionTracks = []; }
    }

    function closeMenus(except) {
      player.querySelectorAll('[data-video-menu]').forEach(function(menu) {
        if (menu === except) return;
        menu.hidden = true;
        var control = menu.closest('.academy-video__menu-control');
        if (control) control.classList.remove('is-open');
        var button = control && control.querySelector('[data-video-menu-button]');
        if (button) button.setAttribute('aria-expanded', 'false');
      });
    }

    function toggleMenu(name) {
      var menu = player.querySelector('[data-video-menu="' + name + '"]');
      var button = player.querySelector('[data-video-menu-button="' + name + '"]');
      if (!menu || !button) return;
      var open = menu.hidden;
      closeMenus(open ? menu : null);
      menu.hidden = !open;
      var control = menu.closest('.academy-video__menu-control');
      if (control) control.classList.toggle('is-open', open);
      button.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) {
        var selected = menu.querySelector('[aria-checked="true"]');
        if (selected) selected.focus();
      }
    }

    function showControls() {
      player.classList.remove('is-user-inactive');
      window.clearTimeout(inactivityTimer);
      if (!video.paused) {
        inactivityTimer = window.setTimeout(function() {
          if (!player.matches(':focus-within') && !player.querySelector('.academy-video__menu-control.is-open')) {
            player.classList.add('is-user-inactive');
          }
        }, 2000);
      }
    }

    function disableNativeCaptions() {
      Array.from(video.textTracks || []).forEach(function(track) { track.mode = 'disabled'; });
    }

    function updateCaption() {
      if (!captionDisplay || !captionText || activeCaptionIndex < 0 || !captionTracks[activeCaptionIndex]) {
        if (captionDisplay) captionDisplay.hidden = true;
        if (captionText) captionText.textContent = '';
        return;
      }
      var track = captionTracks[activeCaptionIndex];
      var current = Number.isFinite(video.currentTime) ? video.currentTime : 0;
      var cue = (track.cues || []).find(function(item) { return current >= Number(item.start) && current < Number(item.end); });
      if (!cue && video.textTracks && video.textTracks[activeCaptionIndex]) {
        var activeCues = Array.from(video.textTracks[activeCaptionIndex].activeCues || []);
        if (activeCues.length) cue = { text: activeCues.map(function(item) { return item.text; }).join('\n') };
      }
      captionText.textContent = cue ? String(cue.text || '') : '';
      captionDisplay.hidden = !cue || !captionText.textContent;
    }

    function selectCaption(index, persist) {
      activeCaptionIndex = index >= 0 && index < captionTracks.length ? index : -1;
      player.querySelectorAll('[data-video-caption-index]').forEach(function(item) {
        var selected = Number(item.dataset.videoCaptionIndex) === activeCaptionIndex;
        item.classList.toggle('is-selected', selected);
        item.setAttribute('aria-checked', selected ? 'true' : 'false');
      });
      disableNativeCaptions();
      updateCaption();
      if (persist) {
        state.videoPreferences.captionLanguage = activeCaptionIndex >= 0 ? String(captionTracks[activeCaptionIndex].language || '') : 'off';
        saveState();
      }
    }

    function setPlaybackRate(value, persist) {
      var allowed = [2, 1.75, 1.5, 1.25, 1, 0.75, 0.5];
      var rate = Number(value);
      if (allowed.indexOf(rate) === -1) rate = 1;
      video.playbackRate = rate;
      if (rateValue) rateValue.textContent = rate + 'x';
      player.querySelectorAll('[data-video-rate]').forEach(function(item) {
        var selected = Number(item.dataset.videoRate) === rate;
        item.classList.toggle('is-selected', selected);
        item.setAttribute('aria-checked', selected ? 'true' : 'false');
      });
      if (persist) {
        state.videoPreferences.playbackRate = rate;
        saveState();
      }
    }

    function syncState() {
      var duration = Number.isFinite(video.duration) ? video.duration : 0;
      var current = Number.isFinite(video.currentTime) ? video.currentTime : 0;
      player.classList.toggle('is-playing', !video.paused);
      if (current > 0) player.classList.add('is-started');
      player.querySelectorAll('[data-video-action="toggle"]').forEach(function(button) {
        button.setAttribute('aria-label', video.paused ? uiText('play_video', 'Play video') : uiText('pause_video', 'Pause video'));
      });
      if (progress) progress.value = duration ? String(current / duration * 100) : '0';
      if (progressPlayed) progressPlayed.style.width = (duration ? current / duration * 100 : 0) + '%';
      if (progressLoaded) {
        var buffered = video.buffered && video.buffered.length ? video.buffered.end(video.buffered.length - 1) : 0;
        progressLoaded.style.width = (duration ? Math.min(100, buffered / duration * 100) : 0) + '%';
      }
      if (remaining) remaining.textContent = '-' + formatVideoTime(Math.max(0, duration - current));
      if (mute) mute.classList.toggle('is-muted', video.muted || video.volume === 0);
      if (volume && document.activeElement !== volume) volume.value = video.muted ? '0' : String(video.volume);
      updateCaption();
    }

    function togglePlayback() {
      player.classList.add('is-started');
      if (video.paused) {
        var promise = video.play();
        if (promise && promise.catch) promise.catch(function() {});
      } else {
        video.pause();
      }
    }

    player.querySelectorAll('[data-video-action="toggle"]').forEach(function(button) {
      button.addEventListener('click', togglePlayback);
    });
    video.addEventListener('click', togglePlayback);
    video.addEventListener('loadedmetadata', function() { disableNativeCaptions(); syncState(); });
    video.addEventListener('durationchange', syncState);
    video.addEventListener('timeupdate', syncState);
    video.addEventListener('progress', syncState);
    video.addEventListener('play', function() { syncState(); showControls(); });
    video.addEventListener('pause', function() { player.classList.remove('is-user-inactive'); syncState(); });
    video.addEventListener('ended', syncState);
    if (progress) progress.addEventListener('input', function() {
      if (Number.isFinite(video.duration)) video.currentTime = Number(progress.value) / 100 * video.duration;
      syncState();
    });
    player.querySelectorAll('[data-video-menu-button]').forEach(function(button) {
      button.addEventListener('click', function(event) {
        event.stopPropagation();
        toggleMenu(button.dataset.videoMenuButton);
        showControls();
      });
    });
    player.querySelectorAll('[data-video-rate]').forEach(function(item) {
      item.addEventListener('click', function(event) {
        event.stopPropagation();
        setPlaybackRate(item.dataset.videoRate, true);
        closeMenus();
        showControls();
      });
    });
    player.querySelectorAll('[data-video-caption-index]').forEach(function(item) {
      item.addEventListener('click', function(event) {
        event.stopPropagation();
        selectCaption(Number(item.dataset.videoCaptionIndex), true);
        closeMenus();
        showControls();
      });
    });
    if (mute) mute.addEventListener('click', function() {
      video.muted = !video.muted;
      mute.setAttribute('aria-label', video.muted ? uiText('unmute', 'Unmute') : uiText('mute', 'Mute'));
      syncState();
      showControls();
    });
    if (volume) volume.addEventListener('input', function() {
      video.volume = Number(volume.value);
      video.muted = video.volume === 0;
      syncState();
      showControls();
    });
    if (fullscreen) fullscreen.addEventListener('click', function() {
      if (document.fullscreenElement && document.exitFullscreen) document.exitFullscreen();
      else if (player.requestFullscreen) player.requestFullscreen();
    });
    document.addEventListener('fullscreenchange', function() {
      var active = document.fullscreenElement === player;
      player.classList.toggle('is-fullscreen', active);
      if (fullscreen) fullscreen.setAttribute('aria-label', active ? uiText('exit_fullscreen', 'Exit fullscreen') : uiText('fullscreen', 'Fullscreen'));
    });
    if (pictureInPicture) pictureInPicture.addEventListener('click', function() {
      if (document.pictureInPictureElement && document.exitPictureInPicture) {
        document.exitPictureInPicture().catch(function() {});
      } else if (video.requestPictureInPicture) {
        video.requestPictureInPicture().catch(function() {});
      }
    });
    video.addEventListener('enterpictureinpicture', function() { player.classList.add('is-picture-in-picture'); });
    video.addEventListener('leavepictureinpicture', function() { player.classList.remove('is-picture-in-picture'); });
    player.addEventListener('mousemove', showControls);
    player.addEventListener('touchstart', showControls, { passive: true });
    player.addEventListener('keydown', function(event) {
      showControls();
      if (event.key === 'Escape') closeMenus();
    });
    document.addEventListener('click', function(event) {
      if (!player.contains(event.target)) closeMenus();
    });
    var savedRate = Number(state.videoPreferences.playbackRate || 1);
    setPlaybackRate(savedRate, false);
    var savedLanguage = String(state.videoPreferences.captionLanguage || 'off');
    var savedCaptionIndex = captionTracks.findIndex(function(track) { return String(track.language || '') === savedLanguage; });
    selectCaption(savedLanguage === 'off' ? -1 : savedCaptionIndex, false);
    disableNativeCaptions();
    syncState();
  }


  document.querySelectorAll('[data-recorded-player]').forEach(function(player) {
    initVideoPlayer(player);
    // Seeking or adjusting volume on touch must not swipe to another slide.
    player.addEventListener('touchstart', function(event) { event.stopPropagation(); }, {passive: true});
    player.addEventListener('touchend', function(event) { event.stopPropagation(); }, {passive: true});
  });
})();
