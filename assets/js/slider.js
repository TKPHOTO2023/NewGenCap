/* Home header slider. Each slide pairs a message with a backdrop image; the progress bar's
   own animation times autoplay, so the visual timer and the slide change never drift apart. */
(function () {
  'use strict';

  var hero = document.querySelector('.hero--slider');
  if (!hero) return;

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var slides = Array.prototype.slice.call(hero.querySelectorAll('.hero-slide'));
  var media = Array.prototype.slice.call(hero.querySelectorAll('.hero-media__slide'));
  var dots = Array.prototype.slice.call(hero.querySelectorAll('.hero-dot'));
  var toggle = hero.querySelector('[data-hero="toggle"]');
  var counter = document.getElementById('heroCurrent');
  var inner = hero.querySelector('.hero-inner');
  var count = slides.length;
  var current = 0;
  var userPaused = false;
  var introDelay = document.documentElement.classList.contains('has-intro') ? 1500 : 150;

  function pad(n) { return (n < 10 ? '0' : '') + n; }

  function go(index) {
    var next = (index + count) % count;
    if (next === current) return;
    // after the first change, slide text animates in without the page-load delay
    hero.style.setProperty('--intro-delay', '0s');
    [slides, media, dots].forEach(function (set) {
      set[current].classList.remove('is-active');
      set[next].classList.add('is-active');
    });
    slides[current].setAttribute('aria-hidden', 'true');
    slides[next].removeAttribute('aria-hidden');
    dots[current].removeAttribute('aria-current');
    dots[next].setAttribute('aria-current', 'true');
    current = next;
    counter.textContent = pad(current + 1);
  }

  function setPaused(paused) {
    userPaused = paused;
    hero.classList.toggle('is-paused', paused);
    toggle.setAttribute('aria-label', paused ? 'Play slideshow' : 'Pause slideshow');
  }

  // autoplay: the active bar finishing its fill moves to the next slide
  dots.forEach(function (dot) {
    dot.querySelector('.hero-dot__fill').addEventListener('animationend', function () {
      if (dot.classList.contains('is-active')) go(current + 1);
    });
  });

  dots.forEach(function (dot, i) { dot.addEventListener('click', function () { go(i); }); });
  hero.querySelector('[data-hero="prev"]').addEventListener('click', function () { go(current - 1); });
  hero.querySelector('[data-hero="next"]').addEventListener('click', function () { go(current + 1); });
  toggle.addEventListener('click', function () { setPaused(!userPaused); });

  // hold while someone is reading (pointer over the text) or using the controls (focus inside)
  var hovering = false, focused = false;
  function hold() { hero.classList.toggle('is-holding', hovering || focused); }
  inner.addEventListener('mouseenter', function () { hovering = true; hold(); });
  inner.addEventListener('mouseleave', function () { hovering = false; hold(); });
  hero.addEventListener('focusin', function () { focused = true; hold(); });
  hero.addEventListener('focusout', function (e) {
    if (!hero.contains(e.relatedTarget)) { focused = false; hold(); }
  });

  hero.querySelector('.hero-nav').addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { e.preventDefault(); go(current - 1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); go(current + 1); }
  });

  // swipe on touch screens
  var startX = null, startY = null;
  hero.addEventListener('pointerdown', function (e) {
    if (e.pointerType !== 'touch') return;
    startX = e.clientX; startY = e.clientY;
  });
  hero.addEventListener('pointerup', function (e) {
    if (startX === null) return;
    var dx = e.clientX - startX, dy = e.clientY - startY;
    startX = null;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) go(current + (dx < 0 ? 1 : -1));
  });
  hero.addEventListener('pointercancel', function () { startX = null; });

  if (reduceMotion) {
    // no autoplay; people move through the slides themselves
    hero.classList.add('is-static');
    setPaused(true);
    toggle.hidden = true;
  } else {
    setTimeout(function () { hero.classList.add('is-running'); }, introDelay + 900);
  }
})();
