/* Funding tools: Funding Readiness Assessment, Telecoms Readiness Assessment, Repayment & DSCR Calculator,
   and the branded PDF report for each. Results are indicative only. */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(pointer: fine)').matches;

  function $(id) { return document.getElementById(id); }
  function groupDigits(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); }
  function money(v) {
    var sign = v < 0 ? '-' : '';
    return sign + 'R ' + groupDigits(Math.round(Math.abs(v)));
  }
  function ratio(v) { return isFinite(v) ? v.toFixed(2) + '×' : 'n/a'; }

  /* =========================================================
     1. Readiness assessments (general funding, and telecoms)
     Both run on the same engine; each section is marked data-assessment="<key>".
     ========================================================= */
  var BANDS = [
    { min: 85, name: 'Funding-ready', text: 'Your project looks ready to present to funders. Submit it and we will review it with you.' },
    { min: 65, name: 'Nearly ready', text: 'A few gaps to close before funders will engage. Most of them can be fixed in weeks, not months.' },
    { min: 40, name: 'Developing', text: 'The foundations are there. Closing the gaps below will materially improve your chances of funding.' },
    { min: 0, name: 'Early stage', text: 'It is early days. Use the list below as your roadmap. We can help you build the case.' }
  ];

  var ASSESSMENTS = {
    readiness: {
      tool: 'Funding Readiness Assessment',
      report: 'Funding Readiness Report',
      file: 'NGC-Funding-Readiness-Report',
      areas: [
        { name: 'Project & plan', qs: ['stage', 'plan', 'ask'] },
        { name: 'Commercial strength', qs: ['revenue', 'equity'] },
        { name: 'Team & track record', qs: ['team', 'financials'] },
        { name: 'Technical & approvals', qs: ['technical', 'permits'] },
        { name: 'Risk management', qs: ['risk'] }
      ],
      gaps: {
        stage: 'Complete a feasibility study that confirms the project can be built and run as planned.',
        plan: 'Prepare a business plan and a detailed financial model covering income, costs, funding and repayments.',
        revenue: 'Secure signed contracts, offtake agreements or letters of intent that show where income will come from.',
        equity: 'Plan your own contribution. Funders usually expect sponsors to fund part of the cost, often 10% to 30%.',
        team: 'Strengthen the team with partners, contractors or advisors who have delivered similar projects.',
        technical: 'Commission an independent technical or engineering study and get supplier or contractor quotes.',
        permits: 'Start land, permit and licence applications early. They are often the longest lead item.',
        financials: 'Get up-to-date management accounts and, where possible, audited financial statements.',
        risk: 'Write a risk register covering construction, market, financial and regulatory risk, with mitigations.',
        ask: 'Build a detailed budget and decide on the mix of debt and equity you are looking for.'
      }
    },
    telecoms: {
      tool: 'Telecoms Readiness Assessment',
      report: 'Telecoms Readiness Report',
      file: 'NGC-Telecoms-Readiness-Report',
      areas: [
        { name: 'Network design & build', qs: ['tc_design', 'tc_vendor', 'tc_rollout'] },
        { name: 'Rights & regulation', qs: ['tc_rights', 'tc_licence', 'tc_approvals'] },
        { name: 'Demand & revenue', qs: ['tc_demand', 'tc_anchor'] },
        { name: 'Delivery & operations', qs: ['tc_team', 'tc_ops'] }
      ],
      gaps: {
        tc_design: 'Firm up the network design and get contractor quotes, so build costs can be verified.',
        tc_vendor: 'Select equipment vendors and secure supply terms and lead times for the critical equipment.',
        tc_rollout: 'Plan the rollout in phases with milestones that funding drawdowns can be tied to.',
        tc_rights: 'Secure site access, wayleaves and rights of way along the route before funders review the project.',
        tc_licence: 'Confirm the ICASA licences the network needs, held directly or through a licensed partner.',
        tc_approvals: 'Start municipal, environmental and building approvals for trenching and tower sites early.',
        tc_demand: 'Evidence demand on the route or sites: surveys, pre-registrations or signed take-up.',
        tc_anchor: 'Secure anchor tenants or wholesale and ISP agreements that underpin early revenue.',
        tc_team: 'Strengthen the team with partners or contractors who have built similar networks.',
        tc_ops: 'Define how the network will be run: network operations, maintenance, service levels and support.'
      }
    }
  };
  var results = {};

  Array.prototype.forEach.call(document.querySelectorAll('[data-assessment]'), function (root) {
    var key = root.getAttribute('data-assessment');
    var def = ASSESSMENTS[key];
    if (!def) return;
    function el(role) { return root.querySelector('[data-role="' + role + '"]'); }

    var form = el('form');
    var questions = Array.prototype.slice.call(form.querySelectorAll('.q'));
    var nextBtn = el('next');
    var backBtn = el('back');
    var nextLabel = nextBtn.querySelector('span');
    var bar = el('bar');
    var count = el('count');
    var resultEl = el('result');
    var current = 0;
    var pointerDown = false;

    function answerOf(q) {
      var checked = q.querySelector('input:checked');
      return checked ? parseInt(checked.value, 10) : null;
    }

    function show(i) {
      current = i;
      questions.forEach(function (q, k) { q.classList.toggle('is-current', k === i); });
      count.textContent = 'Question ' + (i + 1) + ' of ' + questions.length;
      bar.style.transform = 'scaleX(' + (i / questions.length) + ')';
      backBtn.disabled = i === 0;
      nextBtn.disabled = answerOf(questions[i]) === null;
      nextLabel.textContent = i === questions.length - 1 ? 'See my score' : 'Next';
    }

    function advance() {
      if (answerOf(questions[current]) === null) return;
      if (current < questions.length - 1) {
        show(current + 1);
        var first = questions[current].querySelector('input:checked') || questions[current].querySelector('input');
        if (first && !pointerDown) first.focus({ preventScroll: true });
      } else {
        score();
      }
    }

    form.addEventListener('pointerdown', function () { pointerDown = true; });
    form.addEventListener('keydown', function () { pointerDown = false; });
    form.addEventListener('change', function (e) {
      if (!e.target.matches('input[type="radio"]')) return;
      nextBtn.disabled = false;
      // a mouse or touch choice moves on by itself; keyboard users press Next
      if (pointerDown) setTimeout(advance, 320);
    });
    nextBtn.addEventListener('click', advance);
    backBtn.addEventListener('click', function () { if (current > 0) show(current - 1); });

    function score() {
      var answers = {};
      var total = 0;
      questions.forEach(function (q) {
        var v = answerOf(q);
        answers[q.getAttribute('data-q')] = v;
        total += v;
      });
      var pct = Math.round(total / (questions.length * 3) * 100);
      var band = BANDS.filter(function (b) { return pct >= b.min; })[0];
      var areas = def.areas.filter(function (a) { return a.qs.every(function (k) { return k in answers; }); }).map(function (a) {
        var sum = a.qs.reduce(function (t, k) { return t + answers[k]; }, 0);
        return { name: a.name, pct: Math.round(sum / (a.qs.length * 3) * 100) };
      });
      var gaps = Object.keys(answers)
        .filter(function (k) { return answers[k] < 2; })
        .sort(function (a, b) { return answers[a] - answers[b]; })
        .map(function (k) { return def.gaps[k]; });
      var detail = questions.map(function (q) {
        var checked = q.querySelector('input:checked');
        return { question: q.querySelector('legend').textContent.trim(), answer: checked.parentNode.textContent.trim() };
      });
      results[key] = { pct: pct, band: band, areas: areas, gaps: gaps, detail: detail };
      renderResult(results[key]);
    }

    function renderResult(r) {
      form.hidden = true;
      resultEl.hidden = false;
      el('band').textContent = r.band.name;
      el('summary').textContent = r.band.text;

      var areasEl = el('areas');
      areasEl.innerHTML = '';
      r.areas.forEach(function (a) {
        var row = document.createElement('div');
        row.className = 'area';
        row.innerHTML = '<span class="area-name"></span><span class="area-bar"><span></span></span><span class="area-pct"></span>';
        row.querySelector('.area-name').textContent = a.name;
        row.querySelector('.area-pct').textContent = a.pct + '%';
        areasEl.appendChild(row);
        requestAnimationFrame(function () {
          requestAnimationFrame(function () { row.querySelector('.area-bar span').style.transform = 'scaleX(' + a.pct / 100 + ')'; });
        });
      });

      var gapsEl = el('gaps');
      gapsEl.innerHTML = '';
      (r.gaps.length ? r.gaps : ['No major gaps. Submit your project and we will review it with you.']).forEach(function (g) {
        var li = document.createElement('li');
        li.textContent = g;
        gapsEl.appendChild(li);
      });

      // score ring and number
      var arc = el('arc');
      var C = 2 * Math.PI * 52;
      arc.style.strokeDasharray = C.toFixed(2);
      arc.style.strokeDashoffset = C.toFixed(2);
      var num = el('num');
      requestAnimationFrame(function () {
        requestAnimationFrame(function () { arc.style.strokeDashoffset = (C * (1 - r.pct / 100)).toFixed(2); });
      });
      if (reduceMotion) {
        num.textContent = r.pct;
      } else {
        var start = performance.now();
        (function tick(now) {
          var t = Math.min(1, (now - start) / 1400);
          num.textContent = Math.round(r.pct * (1 - Math.pow(1 - t, 3)));
          if (t < 1) requestAnimationFrame(tick);
        })(start);
      }
      resultEl.focus({ preventScroll: true });
      resultEl.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
    }

    el('restart').addEventListener('click', function () {
      form.reset();
      delete results[key];
      resultEl.hidden = true;
      form.hidden = false;
      show(0);
      questions[0].querySelector('input').focus({ preventScroll: true });
    });

    show(0);
  });

  /* =========================================================
     2. Repayment & DSCR Calculator
     ========================================================= */
  var cForm = $('dscrForm');
  var dscrResult = null;

  function parseNum(v) {
    var n = parseFloat(String(v).replace(/[\s,R%]/g, ''));
    return isFinite(n) ? n : NaN;
  }

  function verdictFor(d) {
    if (!isFinite(d)) return 'No debt: the project is fully equity funded.';
    if (d < 0) return 'Operating costs are higher than income, so there is nothing to repay the loan from.';
    if (d < 1) return 'Income does not cover the repayments. Lenders will not fund this structure as it stands.';
    if (d < 1.2) return 'Tight. Income covers repayments, but most lenders will want more headroom.';
    if (d < 1.35) return 'Within the range some lenders accept. More headroom would strengthen the case.';
    return 'Comfortable cover. Income comfortably exceeds the loan repayments.';
  }

  function markerPos(d) {
    if (!isFinite(d)) return 100;
    var pts = [[0.5, 0], [1.0, 25], [1.2, 50], [1.35, 75], [2.0, 100]];
    if (d <= pts[0][0]) return 0;
    for (var i = 1; i < pts.length; i++) {
      if (d <= pts[i][0]) {
        var a = pts[i - 1], b = pts[i];
        return a[1] + (d - a[0]) / (b[0] - a[0]) * (b[1] - a[1]);
      }
    }
    return 100;
  }

  function calculate() {
    var cost = parseNum(cForm.cost.value);
    var debtPct = parseNum(cForm.debt.value);
    var rate = parseNum(cForm.rate.value);
    var years = parseNum(cForm.term.value);
    var revenue = parseNum(cForm.revenue.value);
    var opex = parseNum(cForm.opex.value);
    var growth = parseNum(cForm.growth.value);
    var grace = parseNum(cForm.grace.value);
    var profile = cForm.profile.value;

    var problems = [];
    if (!(cost > 0)) problems.push('a project cost above zero');
    if (!(debtPct >= 0 && debtPct <= 100)) problems.push('a debt portion between 0% and 100%');
    if (!(rate >= 0 && rate <= 50)) problems.push('an interest rate between 0% and 50%');
    if (!(years >= 1 && years <= 40 && Math.round(years) === years)) problems.push('a loan term of 1 to 40 whole years');
    if (!(revenue >= 0)) problems.push('expected annual income');
    if (!(opex >= 0)) problems.push('annual operating costs');
    if (!(growth >= -20 && growth <= 50)) problems.push('annual growth between -20% and 50%');
    if (!(grace >= 0 && grace <= 60 && Math.round(grace) === grace && grace < years * 12)) problems.push('a grace period of 0 to 60 whole months, shorter than the loan term');
    if (problems.length) {
      $('dscrError').textContent = 'Please enter ' + problems.join(', ') + '.';
      $('dscrError').hidden = false;
      $('dscrResults').classList.add('is-stale');
      dscrResult = null;
      return;
    }
    $('dscrError').hidden = true;
    $('dscrResults').classList.remove('is-stale');

    var loan = cost * debtPct / 100;
    var equity = cost - loan;
    var r = rate / 100 / 12;
    var n = years * 12;
    var cfads1 = revenue - opex;
    // repayments may rise each year with income (never fall); level repayments stay flat
    var step = profile === 'growing' ? Math.max(0, growth) / 100 : 0;

    // first repayment after the grace period, sized so the loan is repaid exactly at the end of the term
    var after = n - grace;
    var pv = 0;
    for (var k = 0; k < after; k++) pv += Math.pow(1 + step, Math.floor(k / 12)) / Math.pow(1 + r, k + 1);
    var firstPayment = loan === 0 ? 0 : loan / pv;

    // month-by-month schedule: interest only during the grace period, then capital and interest
    var schedule = [];
    var balance = loan;
    var totalInterest = 0;
    for (var y = 1; y <= years; y++) {
      var opening = balance, interest = 0, principal = 0, service = 0;
      for (var m = 0; m < 12; m++) {
        var month = (y - 1) * 12 + m;
        var i = balance * r;
        var pay = month < grace ? i : firstPayment * Math.pow(1 + step, Math.floor((month - grace) / 12));
        var p = Math.max(0, Math.min(balance, pay - i));
        interest += i; principal += p; balance -= p; service += i + p;
      }
      if (y === years && balance > 0) { principal += balance; service += balance; balance = 0; }
      totalInterest += interest;
      var cfads = cfads1 * Math.pow(1 + growth / 100, y - 1);
      schedule.push({ year: y, opening: opening, interest: interest, principal: principal, closing: Math.max(0, balance), service: service, dscr: service > 0 ? cfads / service : Infinity });
    }
    var annualService = schedule[0].service;
    var dscr1 = schedule[0].dscr;
    var minDscr = schedule.reduce(function (mn, s) { return Math.min(mn, s.dscr); }, Infinity);

    // debt the year-1 cash flow can support at a 1.30× cover, with level repayments
    var capacity = Math.max(0, cfads1 / 1.3 / 12);
    var maxDebt = r === 0 ? capacity * n : capacity * (1 - Math.pow(1 + r, -n)) / r;

    var notes = [];
    if (grace > 0 && loan > 0) notes.push('Interest only for the first ' + grace + ' months (' + money(loan * r) + ' a month).');
    if (step > 0 && loan > 0) notes.push((grace > 0 ? 'Repayments then rise by ' : 'Repayments rise by ') + (step * 100).toFixed(step * 100 % 1 ? 1 : 0) + '% a year, in line with income.');
    var note = notes.join(' ');

    dscrResult = {
      inputs: { cost: cost, debtPct: debtPct, rate: rate, years: years, revenue: revenue, opex: opex, growth: growth, grace: grace,
                profile: step > 0 ? 'Increasing with income (' + growth + '% a year)' : 'Level' },
      loan: loan, equity: equity, monthly: firstPayment, annualService: annualService, totalInterest: totalInterest,
      dscr1: dscr1, minDscr: minDscr, maxDebt: maxDebt, schedule: schedule, verdict: verdictFor(dscr1), note: note
    };

    $('r-dscr').textContent = ratio(dscr1);
    $('r-verdict').textContent = dscrResult.verdict;
    $('r-marker').style.left = markerPos(dscr1).toFixed(1) + '%';
    $('r-monthly').textContent = money(firstPayment);
    $('r-loan').textContent = money(loan);
    $('r-equity').textContent = money(equity);
    $('r-interest').textContent = money(totalInterest);
    $('r-min').textContent = ratio(minDscr);
    $('r-max').textContent = money(maxDebt);
    $('r-note').textContent = note;
    $('r-note').hidden = !note;

    var level = !isFinite(dscr1) ? 'good' : dscr1 < 1 ? 'low' : dscr1 < 1.2 ? 'tight' : dscr1 < 1.35 ? 'ok' : 'good';
    $('dscrResults').setAttribute('data-level', level);

    var rows = schedule.map(function (s) {
      return '<tr><td>' + s.year + '</td><td>' + money(s.opening) + '</td><td>' + money(s.interest) + '</td><td>' +
        money(s.principal) + '</td><td>' + money(s.closing) + '</td><td>' + ratio(s.dscr) + '</td></tr>';
    });
    $('r-schedule').innerHTML = rows.join('');
  }

  if (cForm) {
    cForm.addEventListener('input', calculate);
    cForm.addEventListener('change', calculate);
    cForm.addEventListener('submit', function (e) { e.preventDefault(); });
    Array.prototype.forEach.call(cForm.querySelectorAll('[data-money]'), function (input) {
      input.addEventListener('blur', function () {
        var v = parseNum(input.value);
        if (isFinite(v)) input.value = groupDigits(Math.round(v));
      });
      input.addEventListener('focus', function () { input.value = input.value.replace(/\s/g, ''); });
    });
    calculate();
  }

  /* =========================================================
     3. PDF reports
     ========================================================= */
  var dialog = $('reportDialog');
  var reportForm = $('reportForm');
  var reportError = $('reportError');
  var reportType = null;
  var opener = null;

  function closeDialog() {
    if (dialog.open) dialog.close();
    if (opener) opener.focus();
  }

  document.querySelectorAll('[data-report]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      reportType = btn.getAttribute('data-report');
      if (ASSESSMENTS[reportType] && !results[reportType]) return;
      if (reportType === 'dscr' && !dscrResult) {
        $('dscrError').textContent = 'Please complete the calculator before downloading a report.';
        $('dscrError').hidden = false;
        return;
      }
      opener = btn;
      reportError.hidden = true;
      if (typeof dialog.showModal === 'function') dialog.showModal(); else dialog.setAttribute('open', '');
      $('rp-name').focus();
    });
  });
  if (dialog) {
    $('reportClose').addEventListener('click', closeDialog);
    dialog.addEventListener('click', function (e) { if (e.target === dialog) closeDialog(); });
  }

  if (reportForm) {
    reportForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = reportForm.name.value.trim();
      var email = reportForm.email.value.trim();
      var company = reportForm.company.value.trim();
      var phone = reportForm.phone.value.trim();
      var problems = [];
      if (!name) problems.push('your name');
      if (!window.NGC.isEmail(email)) problems.push('a valid email address');
      if (!window.NGC.isPhone(phone)) problems.push('a phone number we can reach you on');
      if (problems.length) {
        var list = problems.length > 1 ? problems.slice(0, -1).join(', ') + ' and ' + problems[problems.length - 1] : problems[0];
        reportError.textContent = 'Please add ' + list + '.'; reportError.hidden = false; return;
      }
      if (!reportForm.consent.checked) { reportError.textContent = 'Please confirm that we may contact you about your project.'; reportError.hidden = false; return; }
      reportError.hidden = true;

      var person = { name: name, email: email, company: company };
      var assessment = ASSESSMENTS[reportType];
      var summary = assessment
        ? 'Readiness score ' + results[reportType].pct + '% (' + results[reportType].band.name + ')'
        : 'Year 1 DSCR ' + ratio(dscrResult.dscr1) + ', loan ' + money(dscrResult.loan);

      var tool = assessment ? assessment.tool : 'Repayment & DSCR Calculator';
      var honeypot = reportForm.website ? reportForm.website.value : '';

      // the visitor gets the PDF straight away; the same PDF then goes to the team with the lead
      buildPdf(reportType, person).then(function (pdf) {
        closeDialog();
        var label = opener ? opener.querySelector('span') : null;
        var original = label ? label.textContent : '';
        if (label) label.textContent = 'Report downloaded';
        window.NGC.submitLead('tool-report', {
          tool: tool, name: name, email: email, phone: phone, company: company,
          summary: summary, consent: 'yes', website: honeypot
        }, null, { blob: pdf.blob, name: pdf.name }).then(function (result) {
          if (label && result.copied) label.textContent = 'Report downloaded and emailed';
        }).catch(function (err) {
          if (window.console) console.warn('Lead not delivered:', err.message);
        });
        if (label) setTimeout(function () { label.textContent = original; }, 6000);
      }).catch(function () {
        reportError.textContent = 'We could not create the PDF in this browser. Please try another browser, or contact us for a copy.';
        reportError.hidden = false;
      });
    });
  }

  function loadImage(src) {
    return new Promise(function (resolve) {
      var img = new Image();
      img.onload = function () {
        try {
          var c = document.createElement('canvas');
          c.width = img.naturalWidth; c.height = img.naturalHeight;
          c.getContext('2d').drawImage(img, 0, 0);
          resolve({ data: c.toDataURL('image/png'), w: img.naturalWidth, h: img.naturalHeight });
        } catch (err) { resolve(null); }
      };
      img.onerror = function () { resolve(null); };
      img.src = src;
    });
  }

  function clean(text) { return String(text).replace(/[   ]/g, ' '); }

  function buildPdf(type, person) {
    if (!window.jspdf || !window.jspdf.jsPDF) return Promise.reject(new Error('PDF library missing'));
    return loadImage('assets/img/ng-mark-light.png').then(function (logo) {
      var doc = new window.jspdf.jsPDF({ unit: 'mm', format: 'a4' });
      var W = 210, M = 18, y = 0;
      var INK = [5, 21, 42], SLATE = [97, 112, 131], SIGNAL = [245, 131, 31], RULE = [213, 220, 228];
      var assessment = ASSESSMENTS[type];
      var title = assessment ? assessment.report : 'Repayment & DSCR Report';
      var today = new Date().toLocaleDateString('en-ZA', { day: 'numeric', month: 'long', year: 'numeric' });

      function header() {
        doc.setFillColor.apply(doc, INK); doc.rect(0, 0, W, 38, 'F');
        doc.setFillColor.apply(doc, SIGNAL); doc.rect(0, 38, W, 1.2, 'F');
        var x = M;
        if (logo) { var lh = 11; doc.addImage(logo.data, 'PNG', M, 12, lh * logo.w / logo.h, lh); x = M + lh * logo.w / logo.h + 5; }
        doc.setTextColor(255, 255, 255); doc.setFont('helvetica', 'bold'); doc.setFontSize(9);
        doc.text('NEW GENERATION', x, 16.5);
        doc.setTextColor.apply(doc, SIGNAL); doc.text('CAPITAL', x, 21.5);
        doc.setTextColor(255, 255, 255); doc.setFont('helvetica', 'normal'); doc.setFontSize(15);
        doc.text(title, W - M, 18, { align: 'right' });
        doc.setFontSize(8.5); doc.setTextColor(169, 180, 194);
        doc.text(clean(today), W - M, 24, { align: 'right' });
        y = 52;
      }
      function footer() {
        var pages = doc.getNumberOfPages();
        for (var p = 1; p <= pages; p++) {
          doc.setPage(p);
          doc.setDrawColor.apply(doc, RULE); doc.line(M, 280, W - M, 280);
          doc.setFont('helvetica', 'normal'); doc.setFontSize(7.5); doc.setTextColor.apply(doc, SLATE);
          doc.text('Indicative only. This report does not constitute financial advice or an offer of finance.', M, 285);
          doc.text('New Generation Capital  ·  funding@newgenerationcap.co.za  ·  +27 87 742 0831', M, 289);
          doc.text('Page ' + p + ' of ' + pages, W - M, 289, { align: 'right' });
        }
      }
      function ensure(h) { if (y + h > 272) { doc.addPage(); header(); } }
      function heading(text) {
        ensure(16);
        doc.setFont('helvetica', 'bold'); doc.setFontSize(8); doc.setTextColor.apply(doc, SIGNAL);
        doc.text(text.toUpperCase(), M, y); y += 7;
      }
      function para(text, size, color) {
        doc.setFont('helvetica', 'normal'); doc.setFontSize(size || 10); doc.setTextColor.apply(doc, color || INK);
        var lines = doc.splitTextToSize(clean(text), W - 2 * M);
        lines.forEach(function (line) { ensure(6); doc.text(line, M, y); y += (size || 10) * 0.48; });
        y += 2;
      }
      function rows(pairs) {
        pairs.forEach(function (pair) {
          ensure(8);
          doc.setFont('helvetica', 'normal'); doc.setFontSize(9.5); doc.setTextColor.apply(doc, SLATE);
          doc.text(clean(pair[0]), M, y);
          doc.setTextColor.apply(doc, INK); doc.setFont('helvetica', 'bold');
          doc.text(clean(pair[1]), W - M, y, { align: 'right' });
          y += 2.5; doc.setDrawColor.apply(doc, RULE); doc.line(M, y, W - M, y); y += 5;
        });
        y += 3;
      }

      header();
      doc.setFont('helvetica', 'normal'); doc.setFontSize(9); doc.setTextColor.apply(doc, SLATE);
      doc.text(clean('Prepared for ' + person.name + (person.company ? ', ' + person.company : '')), M, y); y += 10;

      if (assessment) {
        var r = results[type];
        doc.setFont('helvetica', 'normal'); doc.setFontSize(40); doc.setTextColor.apply(doc, INK);
        doc.text(r.pct + '%', M, y + 10);
        doc.setFontSize(14); doc.setTextColor.apply(doc, SIGNAL); doc.text(r.band.name, M + 48, y + 3);
        doc.setFontSize(9.5); doc.setTextColor.apply(doc, INK);
        doc.text(doc.splitTextToSize(r.band.text, W - 2 * M - 48), M + 48, y + 9);
        y += 24;

        heading('Score by area');
        r.areas.forEach(function (a) {
          ensure(9);
          doc.setFont('helvetica', 'normal'); doc.setFontSize(9.5); doc.setTextColor.apply(doc, INK);
          doc.text(a.name, M, y);
          doc.setFillColor.apply(doc, RULE); doc.rect(M + 60, y - 3, 90, 3.2, 'F');
          doc.setFillColor.apply(doc, a.pct >= 67 ? INK : SIGNAL); doc.rect(M + 60, y - 3, 90 * a.pct / 100, 3.2, 'F');
          doc.text(a.pct + '%', W - M, y, { align: 'right' });
          y += 8;
        });
        y += 4;

        heading('What to work on');
        (r.gaps.length ? r.gaps : ['No major gaps. Submit your project and we will review it with you.']).forEach(function (g, i) {
          para((i + 1) + '.  ' + g, 9.5);
        });
        y += 2;

        heading('Your answers');
        r.detail.forEach(function (d) {
          ensure(14);
          doc.setFont('helvetica', 'normal'); doc.setFontSize(8.5); doc.setTextColor.apply(doc, SLATE);
          doc.text(doc.splitTextToSize(clean(d.question), W - 2 * M), M, y); y += 4.5;
          doc.setFontSize(9.5); doc.setTextColor.apply(doc, INK); doc.setFont('helvetica', 'bold');
          doc.text(doc.splitTextToSize(clean(d.answer), W - 2 * M), M, y); y += 7;
        });
      } else {
        var d = dscrResult, inp = d.inputs;
        heading('Your inputs');
        rows([
          ['Total project cost', money(inp.cost)],
          ['Portion funded by debt', inp.debtPct + '%'],
          ['Interest rate', inp.rate + '% a year'],
          ['Loan term', inp.years + ' years'],
          ['Expected annual income', money(inp.revenue)],
          ['Annual operating costs', money(inp.opex)],
          ['Annual growth in income and costs', inp.growth + '%'],
          ['Grace period', inp.grace ? inp.grace + ' months, interest only' : 'None'],
          ['Repayment profile', inp.profile]
        ]);
        heading('Results');
        rows([
          ['Year 1 DSCR', ratio(d.dscr1)],
          ['Lowest DSCR over the term', ratio(d.minDscr)],
          ['First monthly repayment', money(d.monthly)],
          ['Year 1 debt service', money(d.annualService)],
          ['Loan amount', money(d.loan)],
          ['Your equity', money(d.equity)],
          ['Total interest over the term', money(d.totalInterest)],
          ['Debt supportable at 1.30x cover (level repayments)', money(d.maxDebt)]
        ]);
        para(d.verdict, 10);
        if (d.note) para(d.note, 9.5);
        para('DSCR (debt service coverage ratio) is the cash a project has available each year divided by its loan repayments for that year. Many lenders look for at least 1.20x to 1.35x, depending on the sector and risk.', 8.5, SLATE);
        y += 2;

        heading('Year-by-year schedule');
        // year is left-aligned; every other column is right-aligned on these edges
        var cols = [M, M + 46, M + 78, M + 112, M + 150, W - M];
        var labels = ['Year', 'Opening balance', 'Interest', 'Capital repaid', 'Closing balance', 'DSCR'];
        function cell(text, i) { doc.text(clean(text), cols[i], y, { align: i === 0 ? 'left' : 'right' }); }
        function tableHead() {
          doc.setFont('helvetica', 'bold'); doc.setFontSize(8); doc.setTextColor.apply(doc, SLATE);
          labels.forEach(cell);
          y += 2.5; doc.setDrawColor.apply(doc, INK); doc.line(M, y, W - M, y); y += 5;
        }
        tableHead();
        d.schedule.forEach(function (s) {
          if (y + 6 > 272) { doc.addPage(); header(); tableHead(); }
          doc.setFont('helvetica', 'normal'); doc.setFontSize(8.5); doc.setTextColor.apply(doc, INK);
          var vals = [String(s.year), money(s.opening), money(s.interest), money(s.principal), money(s.closing), ratio(s.dscr)];
          vals.forEach(cell);
          y += 2.2; doc.setDrawColor.apply(doc, RULE); doc.line(M, y, W - M, y); y += 4.3;
        });
      }

      y += 6;
      heading('Next step');
      para('Ready to take the project further? Submit it through the Partner with us page on our website, or email funding@newgenerationcap.co.za, and our team will review it with you.', 9.5);

      footer();
      var file = (assessment ? assessment.file : 'NGC-Repayment-DSCR-Report') + '.pdf';
      doc.save(file);
      return { blob: doc.output('blob'), name: file };
    });
  }
})();
