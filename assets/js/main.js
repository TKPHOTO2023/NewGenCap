(function () {
  'use strict';

  var doc = document.documentElement;
  doc.classList.add('js');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- header state ---------- */
  var header = document.querySelector('.site-header');
  function onScroll() {
    header.classList.toggle('is-solid', window.scrollY > 40);
  }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- mobile menu ---------- */
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('nav');
  function setMenu(open) {
    document.body.classList.toggle('nav-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  toggle.addEventListener('click', function () {
    setMenu(!document.body.classList.contains('nav-open'));
  });
  nav.addEventListener('click', function (e) {
    if (e.target.closest('a')) setMenu(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') setMenu(false);
  });

  /* ---------- reveal on scroll ---------- */
  var reveals = document.querySelectorAll('.reveal:not(.wipe)');
  if ('IntersectionObserver' in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---------- enquiry form → opens the visitor's mail app ---------- */
  var form = document.getElementById('enquiry');
  var formError = document.getElementById('formError');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = form.name.value.trim();
    var email = form.email.value.trim();
    var message = form.message.value.trim();
    var missing = [];
    if (!name) missing.push('your name');
    if (!/^\S+@\S+\.\S+$/.test(email)) missing.push('a valid email address');
    if (!message) missing.push('a short message');
    if (missing.length) {
      formError.textContent = 'Please add ' + missing.join(', ') + ' so we can respond.';
      formError.hidden = false;
      return;
    }
    formError.hidden = true;
    var subject = 'Enquiry — ' + form.role.value;
    var body = message + '\n\n' + name + '\n' + email;
    window.location.href = 'mailto:selwynw@newgenerationcap.co.za?subject=' +
      encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  });

  document.getElementById('year').textContent = new Date().getFullYear();

  /* ---------- deal-flow visual ----------
     Opportunities enter at Find and thin out through Screen and Validate.
     Only those that pass the decision gate become the single funded line
     through Package, Fund and Deliver. */
  var canvas = document.getElementById('flowCanvas');
  if (!canvas || !canvas.getContext) return;
  var ctx = canvas.getContext('2d');
  var W = 0, H = 0, dpr = 1;
  var particles = [];
  var spawnClock = 0;
  var running = false;
  var last = 0;
  var focusStage = -1;        // stage column highlighted while its card is hovered

  var INK = [5, 21, 42];
  var SLATE = [97, 112, 131];
  var SIGNAL = [245, 131, 31];
  var GATE = 0.5;             // decision gate sits between Validate and Package
  var CROSS_SECONDS = 9;      // time for a deal to travel the full band
  var SPAWN_EVERY = 0.075;

  function resize() {
    var rect = canvas.getBoundingClientRect();
    if (!rect.width) return false;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = rect.width; H = rect.height;
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return true;
  }

  function spawn() {
    var r = Math.random();
    // where this opportunity stops: 1 = after Find, 2 = after Screen, 3 = at the gate, 0 = passes
    var exit = r < 0.38 ? 1 : r < 0.66 ? 2 : r < 0.86 ? 3 : 0;
    particles.push({
      p: 0,
      off: (Math.random() * 2 - 1),
      wob: Math.random() * Math.PI * 2,
      exit: exit,
      fall: 0,
      size: 1.4 + Math.random() * 1.4
    });
  }

  function spread(p) {
    // band narrows as diligence progresses, collapses to a single line after the gate
    if (p < GATE) return 1 - (p / GATE) * 0.62;
    var t = Math.min(1, (p - GATE) / 0.06);
    return 0.38 * (1 - t);
  }

  function step(dt) {
    spawnClock += dt;
    while (spawnClock > SPAWN_EVERY) { spawnClock -= SPAWN_EVERY; spawn(); }
    var v = dt / CROSS_SECONDS;
    for (var i = particles.length - 1; i >= 0; i--) {
      var q = particles[i];
      var stopAt = q.exit ? q.exit / 6 : 2;
      if (q.p >= stopAt) {
        q.fall += dt;
        q.p += v * 0.25;
        if (q.fall > 1.1) particles.splice(i, 1);
      } else {
        q.p += v;
        q.wob += dt * 1.6;
        if (q.p > 1.02) particles.splice(i, 1);
      }
    }
  }

  function rgba(c, a) { return 'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + a + ')'; }
  function mix(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t].map(Math.round); }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    var mid = H * 0.56;
    var half = H * 0.4;

    // highlighted stage column
    if (focusStage >= 0) {
      var fx = W * focusStage / 6;
      var band = ctx.createLinearGradient(0, 24, 0, H);
      var tint = focusStage >= 3 ? SIGNAL : INK;
      band.addColorStop(0, rgba(tint, 0));
      band.addColorStop(1, rgba(tint, focusStage >= 3 ? 0.09 : 0.05));
      ctx.fillStyle = band;
      ctx.fillRect(fx, 24, W / 6, H - 24);
    }

    // stage dividers
    ctx.lineWidth = 1;
    for (var k = 1; k < 6; k++) {
      if (k === 3) continue;
      var x = Math.round(W * k / 6) + 0.5;
      ctx.strokeStyle = rgba(INK, 0.08);
      ctx.setLineDash([2, 5]);
      ctx.beginPath(); ctx.moveTo(x, 24); ctx.lineTo(x, H); ctx.stroke();
    }
    ctx.setLineDash([]);

    // the funded line
    var gx = W * GATE;
    var grad = ctx.createLinearGradient(gx, 0, W, 0);
    grad.addColorStop(0, rgba(SIGNAL, 0.35));
    grad.addColorStop(1, rgba(SIGNAL, 1));
    ctx.strokeStyle = grad;
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(gx, mid); ctx.lineTo(W, mid); ctx.stroke();

    // opportunities
    for (var i = 0; i < particles.length; i++) {
      var q = particles[i];
      var px = q.p * W;
      var py = mid + (q.off * spread(q.p) * half) + Math.sin(q.wob) * 2.5 * (q.p < GATE ? 1 : 0);
      var alpha, color;
      if (q.fall > 0) {
        py += q.fall * q.fall * 46;
        alpha = Math.max(0, 0.5 * (1 - q.fall / 1.1));
        color = SLATE;
      } else if (q.p < GATE) {
        alpha = Math.min(1, q.p * 30) * 0.62;
        color = mix(SLATE, INK, q.p / GATE * 0.6);
      } else {
        alpha = 1;
        color = mix(INK, SIGNAL, Math.min(1, (q.p - GATE) / 0.05));
      }
      var inFocus = focusStage >= 0 && Math.floor(q.p * 6) === focusStage && !q.fall;
      ctx.fillStyle = rgba(inFocus && q.p < GATE ? INK : color, inFocus ? Math.min(1, alpha + 0.35) : alpha);
      ctx.beginPath();
      ctx.arc(px, py, (q.p >= GATE && !q.fall ? 3 : q.size) * (inFocus ? 1.35 : 1), 0, Math.PI * 2);
      ctx.fill();
    }

    // end-point marker: delivered
    ctx.fillStyle = rgba(SIGNAL, 1);
    ctx.beginPath(); ctx.arc(W - 5, mid, 5, 0, Math.PI * 2); ctx.fill();
  }

  function prewarm() {
    particles = [];
    for (var t = 0; t < CROSS_SECONDS * 1.1; t += 1 / 30) step(1 / 30);
  }

  function frame(now) {
    if (!running) return;
    var dt = Math.min(0.05, (now - last) / 1000 || 0);
    last = now;
    step(dt);
    draw();
    requestAnimationFrame(frame);
  }

  function start() {
    if (running || reduceMotion) return;
    running = true;
    last = performance.now();
    requestAnimationFrame(frame);
  }
  function stop() { running = false; }

  function init() {
    if (!resize()) return;
    prewarm();
    draw();
  }

  init();

  var stageList = document.getElementById('stages');
  if (stageList) {
    Array.prototype.forEach.call(stageList.children, function (li, i) {
      li.addEventListener('mouseenter', function () { focusStage = i; if (!running) draw(); });
      li.addEventListener('mouseleave', function () { focusStage = -1; if (!running) draw(); });
    });
  }

  window.addEventListener('resize', function () {
    if (!resize()) return;
    if (!particles.length) prewarm();
    draw();
  });

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          if (!W && resize()) { prewarm(); }
          start();
        } else {
          stop();
        }
      });
    }).observe(canvas);
  } else {
    start();
  }
})();
