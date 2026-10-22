/* HostDigital: header, menu, reveals and scroll-driven scenes. No dependencies. */
(function () {
  "use strict";

  var doc = document.documentElement;
  doc.classList.remove("no-js");
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var clamp = function (v, a, b) { return Math.min(b, Math.max(a, v)); };

  // Progress of an element through the viewport while it is pinned: 0 at its top, 1 at its end.
  function pinProgress(el) {
    var r = el.getBoundingClientRect();
    var span = r.height - window.innerHeight;
    return span > 0 ? clamp(-r.top / span, 0, 1) : 0;
  }

  requestAnimationFrame(function () { document.body.classList.add("is-loaded"); });

  /* Header */
  var hd = document.querySelector(".hd");
  var sheet = document.querySelector(".sheet");
  var toggle = document.querySelector(".hd__toggle");
  var darkZones = document.querySelectorAll(".on-dark:not(.cta)");
  function onHeader() {
    if (!hd) return;
    hd.classList.toggle("is-scrolled", window.scrollY > 12);
    var dark = false;
    darkZones.forEach(function (z) { var r = z.getBoundingClientRect(); if (r.top <= 34 && r.bottom >= 34) dark = true; });
    hd.classList.toggle("is-dark", dark && window.scrollY > 12);
  }
  onHeader();
  window.addEventListener("scroll", onHeader, { passive: true });

  function setMenu(open) {
    hd.classList.toggle("is-open", open);
    sheet.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  }
  if (toggle && sheet) {
    toggle.addEventListener("click", function () { setMenu(!hd.classList.contains("is-open")); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && hd.classList.contains("is-open")) { setMenu(false); toggle.focus(); } });
    sheet.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
  }

  /* Reveals */
  var revealables = document.querySelectorAll(".rv, .step, .stage");
  if ("IntersectionObserver" in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.08 });
    revealables.forEach(function (el) { io.observe(el); });
  } else {
    revealables.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* Manifesto: split into words once */
  var manifesto = document.querySelector(".manifesto");
  var words = [];
  if (manifesto) {
    var text = manifesto.querySelector(".manifesto__text");
    var html = "";
    text.childNodes.forEach(function (node) {
      var isKey = node.nodeType === 1;
      var parts = node.textContent.split(/(\s+)/);
      parts.forEach(function (p) {
        if (!p) return;
        if (/^\s+$/.test(p)) { html += " "; return; }
        html += '<span class="w' + (isKey ? " k" : "") + '">' + p + "</span>";
      });
    });
    text.setAttribute("aria-label", text.textContent.replace(/\s+/g, " ").trim());
    text.innerHTML = html;
    Array.prototype.forEach.call(text.children, function (c) { c.setAttribute("aria-hidden", "true"); });
    words = text.querySelectorAll(".w");
  }

  /* Scroll-driven scenes */
  var windowEl = document.querySelector(".window");
  var frame = windowEl && windowEl.querySelector(".window__frame");
  var stack = document.querySelector(".stack");
  var plates = stack ? stack.querySelectorAll(".plate") : [];
  var items = stack ? stack.querySelectorAll(".stack__list li") : [];
  var tower = stack && stack.querySelector(".stack__tower");
  var bar = stack && stack.querySelector(".stack__progress");
  var parallax = document.querySelectorAll("[data-parallax]");
  var stackDesktop = window.matchMedia("(min-width: 921px)");
  var lastLayer = -1;

  function setLayer(n) {
    if (n === lastLayer) return;
    lastLayer = n;
    plates.forEach(function (p, i) { p.classList.toggle("is-on", i === n); p.classList.toggle("is-below", i < n); });
    items.forEach(function (li) { li.classList.toggle("is-on", Number(li.dataset.layer) === n); });
  }

  function frameTick() {
    if (frame) frame.style.setProperty("--p", pinProgress(windowEl).toFixed(4));

    if (words.length) {
      var p = clamp(pinProgress(manifesto) * 1.25, 0, 1);
      var lit = Math.round(p * words.length);
      for (var i = 0; i < words.length; i++) words[i].classList.toggle("is-on", i < lit);
    }

    if (stack && stackDesktop.matches) {
      var sp = pinProgress(stack);
      // First 15% spreads the plates apart, the rest walks up the layers.
      var spread = clamp(sp / 0.15, 0, 1);
      tower.style.setProperty("--spread", spread.toFixed(3));
      bar.style.setProperty("--sp", sp.toFixed(3));
      var layer = Math.min(plates.length - 1, Math.floor(clamp((sp - 0.12) / 0.84, 0, 0.9999) * plates.length));
      setLayer(layer);
    }

    parallax.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      var c = (r.top + r.height / 2 - window.innerHeight / 2) / window.innerHeight;
      el.style.transform = "translate3d(0," + (c * -parseFloat(el.dataset.parallax || 60)).toFixed(1) + "px,0)";
    });
  }

  var ticking = false;
  function requestTick() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { ticking = false; frameTick(); });
  }

  if (!reduced) {
    window.addEventListener("scroll", requestTick, { passive: true });
    window.addEventListener("resize", requestTick);
    frameTick();
  } else if (stack) {
    setLayer(plates.length - 1);
    items.forEach(function (li) { li.classList.add("is-on"); });
  }
  if (stack && !stackDesktop.matches) items.forEach(function (li) { li.classList.add("is-on"); });

  /* Services page: highlight the section in view */
  var svcLinks = document.querySelectorAll(".svc-nav a");
  if (svcLinks.length && "IntersectionObserver" in window) {
    var map = {};
    svcLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        svcLinks.forEach(function (a) { a.classList.remove("is-on"); });
        var a = map[en.target.id];
        if (a) a.classList.add("is-on");
      });
    }, { rootMargin: "-40% 0px -55% 0px" });
    document.querySelectorAll(".svc").forEach(function (s) { so.observe(s); });
  }

  /* Contact form */
  var form = document.querySelector("#enquiry");
  if (form) {
    var params = new URLSearchParams(location.search);
    var pre = params.get("interest");
    if (pre) {
      var box = form.querySelector('input[name="interest"][value="' + pre.replace(/[^a-z-]/g, "") + '"]');
      if (box) box.checked = true;
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.querySelector(".hp input").value) return;
      var ok = true;
      form.querySelectorAll("[required]").forEach(function (input) {
        var field = input.closest(".field");
        var err = field.querySelector(".field__err");
        var bad = !input.value.trim() || (input.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim()));
        field.classList.toggle("has-error", bad);
        err.textContent = bad ? input.dataset.error : "";
        if (bad && ok) { input.focus(); ok = false; }
      });
      if (!ok) return;

      var data = new FormData(form);
      var interests = data.getAll("interest");
      var body = [
        "Name: " + data.get("name"),
        "Company: " + (data.get("company") || "-"),
        "Email: " + data.get("email"),
        "Phone: " + (data.get("phone") || "-"),
        "Interested in: " + (interests.length ? interests.join(", ") : "Not specified"),
        "Budget: " + (data.get("budget") || "-"),
        "",
        data.get("message")
      ].join("\n");
      var to = form.dataset.to;
      var subject = "New enquiry from " + data.get("name") + (data.get("company") ? " (" + data.get("company") + ")" : "");
      window.location.href = "mailto:" + to + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);

      var status = form.querySelector(".form__status");
      status.textContent = "Your email app should now open with the enquiry filled in. Send it from there and we'll get back to you. If nothing opened, email " + to + " directly.";
      status.classList.add("is-shown");
    });
  }

  var year = document.querySelector("[data-year]");
  if (year) year.textContent = new Date().getFullYear();
})();
