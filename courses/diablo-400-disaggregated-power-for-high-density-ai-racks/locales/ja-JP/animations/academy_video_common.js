(function () {
  'use strict';

  var canvas = document.getElementById('scene');
  var ctx = canvas.getContext('2d');
  var previewFrame = null;
  var COLORS = {
    bg: '#eef1f3',
    panel: '#ffffff',
    text: '#3d3d3f',
    muted: '#6f7378',
    border: '#d6dadd',
    green: '#8DC63F',
    greenDark: '#6FA030',
    greenPale: '#f2f8ea',
    blue: '#343895',
    bluePale: '#eff0fb',
    amber: '#e6a23c',
    amberPale: '#fff7e7',
    red: '#c74b50',
    redPale: '#fff0f0',
    dim: '#aeb4b8'
  };

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function progress(t, start, end) {
    var x = clamp((t - start) / (end - start), 0, 1);
    return x * x * (3 - (2 * x));
  }

  function pulse(t, period) {
    return 0.5 + (0.5 * Math.sin((t / period) * Math.PI * 2));
  }

  function roundedRect(x, y, w, h, radius, fill, stroke, lineWidth) {
    ctx.beginPath();
    ctx.roundRect(x, y, w, h, radius);
    ctx.fillStyle = fill;
    ctx.fill();
    if (stroke) {
      ctx.lineWidth = lineWidth || 1;
      ctx.strokeStyle = stroke;
      ctx.stroke();
    }
  }

  function text(value, x, y, size, weight, color, align, maxWidth) {
    ctx.font = (weight || 400) + ' ' + size + 'px Arial, sans-serif';
    ctx.fillStyle = color || COLORS.text;
    ctx.textAlign = align || 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText(value, x, y, maxWidth);
  }

  function line(x1, y1, x2, y2, color, width, amount) {
    var p = amount === undefined ? 1 : clamp(amount, 0, 1);
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x1 + ((x2 - x1) * p), y1 + ((y2 - y1) * p));
    ctx.lineWidth = width;
    ctx.lineCap = 'round';
    ctx.strokeStyle = color;
    ctx.stroke();
  }

  function arrow(x1, y1, x2, y2, color, width, amount) {
    var p = amount === undefined ? 1 : clamp(amount, 0, 1);
    var ex = x1 + ((x2 - x1) * p);
    var ey = y1 + ((y2 - y1) * p);
    if (p > 0.96) {
      var angle = Math.atan2(y2 - y1, x2 - x1);
      var len = 15;
      var backOffset = len * Math.cos(Math.PI / 6);
      var bx = ex - (backOffset * Math.cos(angle));
      var by = ey - (backOffset * Math.sin(angle));
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(bx, by);
      ctx.lineWidth = width;
      ctx.lineCap = 'butt';
      ctx.strokeStyle = color;
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(ex, ey);
      ctx.lineTo(ex - (len * Math.cos(angle - Math.PI / 6)), ey - (len * Math.sin(angle - Math.PI / 6)));
      ctx.lineTo(ex - (len * Math.cos(angle + Math.PI / 6)), ey - (len * Math.sin(angle + Math.PI / 6)));
      ctx.closePath();
      ctx.fillStyle = color;
      ctx.fill();
    } else {
      line(x1, y1, x2, y2, color, width, p);
    }
  }

  function movingDot(x1, y1, x2, y2, t, start, duration, color, radius) {
    if (t < start) return;
    var p = ((t - start) % duration) / duration;
    var x = x1 + ((x2 - x1) * p);
    var y = y1 + ((y2 - y1) * p);
    ctx.save();
    ctx.shadowColor = color;
    ctx.shadowBlur = 12;
    ctx.beginPath();
    ctx.arc(x, y, radius || 7, 0, Math.PI * 2);
    ctx.fillStyle = '#ffffff';
    ctx.fill();
    ctx.lineWidth = 3;
    ctx.strokeStyle = color;
    ctx.stroke();
    ctx.restore();
  }

  function header(titleValue) {
    ctx.fillStyle = COLORS.bg;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    roundedRect(38, 28, 16, 62, 8, COLORS.green);
    text(titleValue, 76, 60, 34, 700, COLORS.text, 'left', 1150);
  }

  function panel(x, y, w, h, label, tone) {
    var fill = COLORS.panel;
    var stroke = COLORS.border;
    if (tone === 'green') {
      fill = COLORS.greenPale;
      stroke = '#dbe9cb';
    } else if (tone === 'blue') {
      fill = COLORS.bluePale;
      stroke = '#d7d8f1';
    } else if (tone === 'amber') {
      fill = COLORS.amberPale;
      stroke = '#f0d29e';
    } else if (tone === 'red') {
      fill = COLORS.redPale;
      stroke = '#efc2c4';
    }
    roundedRect(x, y, w, h, 18, fill, stroke, 2);
    if (label) text(label, x + 28, y + 38, 17, 700, COLORS.greenDark);
  }

  function install(renderFrame, durationMs, posterTimeMs) {
    document.body.dataset.durationMs = durationMs;
    document.body.dataset.posterMs = posterTimeMs;
    window.__videoDurationMs = durationMs;
    window.__posterTimeMs = posterTimeMs;

    function startPreview() {
      var start = performance.now();
      function draw(now) {
        var elapsed = Math.min(now - start, durationMs);
        renderFrame(elapsed);
        if (elapsed < durationMs) previewFrame = requestAnimationFrame(draw);
      }
      previewFrame = requestAnimationFrame(draw);
    }

    window.setTeachingTime = function (time) {
      if (previewFrame !== null) cancelAnimationFrame(previewFrame);
      previewFrame = null;
      var scale = Math.max(1, window.innerWidth * window.devicePixelRatio / 1280);
      var width = Math.round(1280 * scale);
      var height = Math.round(720 * scale);
      if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width;
        canvas.height = height;
      }
      ctx.setTransform(width / 1280, 0, 0, height / 720, 0, 0);
      renderFrame(clamp(time, 0, durationMs));
    };

    if (new URLSearchParams(window.location.search).has('poster')) window.setTeachingTime(posterTimeMs);
    else startPreview();
  }

  window.AcademyVideo = {
    canvas: canvas,
    ctx: ctx,
    C: COLORS,
    clamp: clamp,
    progress: progress,
    pulse: pulse,
    roundedRect: roundedRect,
    text: text,
    line: line,
    arrow: arrow,
    movingDot: movingDot,
    header: header,
    panel: panel,
    install: install
  };
}());
