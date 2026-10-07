/* New Generation Capital — motion layer.
   Everything here is progressive: without it the page is complete and static. */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var root = document.documentElement;
  var introDelay = root.classList.contains('has-intro') ? 1500 : 150;

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }

  /* ---------- split hero headline into masked words ---------- */
  $$('[data-split]').forEach(function (el) {
    var i = 0;
    function wrapText(node) {
      var frag = document.createDocumentFragment();
      node.textContent.split(/(\s+)/).forEach(function (part) {
        if (!part) return;
        if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
        var w = document.createElement('span');
        w.className = 'w';
        var wi = document.createElement('span');
        wi.className = 'wi';
        wi.style.setProperty('--i', i++);
        wi.textContent = part;
        w.appendChild(wi);
        frag.appendChild(w);
      });
      return frag;
    }
    Array.prototype.slice.call(el.childNodes).forEach(function (node) {
      if (node.nodeType === 3) {
        el.replaceChild(wrapText(node), node);
      } else if (node.nodeType === 1) {
        var inner = wrapText(node);
        node.textContent = '';
        node.appendChild(inner);
      }
    });
    el.setAttribute('aria-label', el.textContent.replace(/\s+/g, ' ').trim());
  });

  /* ---------- split the ink-fill sentence into words ---------- */
  var inkWords = [];
  var inkEl = $('[data-ink]');
  if (inkEl) {
    var words = inkEl.textContent.trim().split(/\s+/);
    inkEl.textContent = '';
    words.forEach(function (word, idx) {
      var s = document.createElement('span');
      s.className = 'iw';
      s.textContent = word;
      inkEl.appendChild(s);
      if (idx < words.length - 1) inkEl.appendChild(document.createTextNode(' '));
      inkWords.push(s);
    });
  }

  /* ---------- stagger indices ---------- */
  $$('.stagger').forEach(function (list) {
    Array.prototype.forEach.call(list.children, function (child, i) { child.style.setProperty('--i', i); });
  });
  $$('#nav > *').forEach(function (a, i) { a.style.setProperty('--i', i); });

  /* ---------- count-up figures ---------- */
  function countUp(el, delay) {
    var to = parseFloat(el.getAttribute('data-count'));
    var decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
    if (reduceMotion) { el.textContent = to.toFixed(decimals); return; }
    var duration = 1800;
    el.textContent = (0).toFixed(decimals);
    setTimeout(function () {
      var start = performance.now();
      (function tick(now) {
        var t = clamp((now - start) / duration, 0, 1);
        var eased = 1 - Math.pow(1 - t, 4);
        el.textContent = (to * eased).toFixed(decimals);
        if (t < 1) requestAnimationFrame(tick);
      })(start);
    }, delay || 0);
  }

  /* ---------- observe things that animate in ---------- */
  // A fully clipped element never reports as visible, so wipes are watched
  // through their parent and revealed from there.
  var watched = $$('.stagger, [data-count]');
  var wipes = $$('.wipe');
  wipes.forEach(function (w) { if (watched.indexOf(w.parentElement) < 0) watched.push(w.parentElement); });
  if ('IntersectionObserver' in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        if (el.hasAttribute('data-count')) {
          countUp(el, el.closest('.hero') ? Math.max(150, introDelay + 900 - performance.now()) : 150);
        } else {
          if (!el.classList.contains('wipe')) el.classList.add('is-in');
          wipes.forEach(function (w) { if (w.parentElement === el) w.classList.add('is-in'); });
        }
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
    watched.forEach(function (el) {
      if (el.hasAttribute('data-count')) el.textContent = '0';
      io.observe(el);
    });
  } else {
    watched.concat(wipes).forEach(function (el) {
      if (el.hasAttribute('data-count')) countUp(el);
      else el.classList.add('is-in');
    });
  }

  /* ---------- focus areas: hover brings the matching photo forward ---------- */
  var focusMedia = $('.focus-media');
  var focusItems = $$('.focus-item');
  function setFocus(item) {
    focusItems.forEach(function (it) { it.classList.toggle('is-active', it === item); });
    if (focusMedia) focusMedia.setAttribute('data-view', item.getAttribute('data-view'));
  }
  if (focusItems.length) {
    setFocus(focusItems[0]);
    focusItems.forEach(function (item) {
      item.addEventListener('mouseenter', function () { setFocus(item); });
      item.addEventListener('click', function () { setFocus(item); });
    });
  }

  /* ---------- magnetic buttons ---------- */
  if (finePointer && !reduceMotion) {
    $$('[data-magnetic]').forEach(function (btn) {
      btn.addEventListener('mousemove', function (e) {
        var r = btn.getBoundingClientRect();
        var x = (e.clientX - r.left - r.width / 2) * 0.22;
        var y = (e.clientY - r.top - r.height / 2) * 0.32;
        btn.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px)';
      });
      btn.addEventListener('mouseleave', function () {
        btn.style.transition = 'transform .6s cubic-bezier(.2,.7,.2,1)';
        btn.style.transform = '';
        setTimeout(function () { btn.style.transition = ''; }, 600);
      });
    });
  }

  /* ---------- scroll-driven effects ---------- */
  var header = $('.site-header');
  var hero = $('#hero');
  var heroMedia = $('.hero-media');
  var heroInner = $('.hero-inner');
  var toTop = $('.to-top');
  var parallaxEls = $$('[data-parallax]');
  var navLinks = $$('#nav a[href^="#"]:not(.btn)');
  var sections = navLinks.map(function (a) { return $(a.getAttribute('href')); });
  var pointerX = 0, pointerY = 0;
  var ticking = false;

  function update() {
    ticking = false;
    var y = window.scrollY;
    var vh = window.innerHeight;
    var docH = document.documentElement.scrollHeight - vh;

    header.style.setProperty('--progress', docH > 0 ? (y / docH).toFixed(4) : 0);
    if (toTop) toTop.classList.toggle('is-shown', y > vh * 1.1);

    // active nav link
    var active = -1;
    sections.forEach(function (sec, i) {
      if (sec && sec.getBoundingClientRect().top < vh * 0.4) active = i;
    });
    navLinks.forEach(function (a, i) { a.classList.toggle('is-active', i === active); });

    if (reduceMotion) return;

    // hero depth
    if (hero && y < hero.offsetHeight) {
      var p = y / hero.offsetHeight;
      heroMedia.style.transform = 'translate3d(' + (pointerX * -14).toFixed(1) + 'px,' + (y * 0.28 + pointerY * -10).toFixed(1) + 'px,0)';
      heroInner.style.transform = 'translate3d(0,' + (y * 0.14).toFixed(1) + 'px,0)';
      heroInner.style.opacity = clamp(1 - p * 1.4, 0, 1).toFixed(3);
    }

    // image parallax
    parallaxEls.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var t = (r.top + r.height / 2 - vh / 2) / vh;
      el.style.setProperty('--py', (t * -60).toFixed(1) + 'px');
    });

    // ink-fill sentence
    if (inkEl) {
      var ir = inkEl.getBoundingClientRect();
      var prog = clamp((vh * 0.82 - ir.top) / (vh * 0.45), 0, 1);
      var lit = Math.round(prog * inkWords.length);
      inkWords.forEach(function (w, i) { w.classList.toggle('on', i < lit); });
    }
  }

  function requestUpdate() {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }
  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', requestUpdate);
  update();

  if (finePointer && !reduceMotion && hero) {
    hero.addEventListener('mousemove', function (e) {
      pointerX = e.clientX / window.innerWidth - 0.5;
      pointerY = e.clientY / window.innerHeight - 0.5;
      requestUpdate();
    });
  }

  /* ---------- form: confirm the hand-off to the mail app ---------- */
  var form = $('#enquiry');
  if (form) {
    form.addEventListener('submit', function () {
      var err = $('#formError');
      if (err && !err.hidden) return;
      var label = $('button[type="submit"] span', form);
      if (!label) return;
      label.textContent = 'Opening your email app…';
      setTimeout(function () { label.textContent = 'Send enquiry'; }, 4000);
    });
  }
})();
