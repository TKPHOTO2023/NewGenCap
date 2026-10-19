/* Partner with us: project submission form with document upload. */
(function () {
  'use strict';

  var form = document.getElementById('submitForm');
  if (!form) return;

  var config = window.NGC_CONFIG || {};
  var MAX_FILES = config.maxFiles || 5;
  var MAX_MB = config.maxFileMB || 10;
  var ALLOWED = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'csv'];

  var errorEl = document.getElementById('submitError');
  var doneEl = document.getElementById('submitDone');
  var doneText = document.getElementById('submitDoneText');
  var msgLabel = document.getElementById('s-msg-label');
  var sponsorOnly = form.querySelectorAll('[data-sponsor-only]');
  var fileInput = document.getElementById('s-files');
  var zone = form.querySelector('.upload-zone');
  var list = document.getElementById('uploadList');
  var files = [];

  /* ---------- sponsor / funder switch ---------- */
  function applyRole() {
    var role = form.role.value;
    var sponsor = role === 'Project sponsor';
    Array.prototype.forEach.call(sponsorOnly, function (el) { el.hidden = !sponsor; });
    msgLabel.textContent = role === 'Capital provider' ? 'Tell us about your mandate' : 'Tell us about the project';
  }
  Array.prototype.forEach.call(form.role, function (r) { r.addEventListener('change', applyRole); });
  document.querySelectorAll('[data-role-pick="funder"]').forEach(function (link) {
    link.addEventListener('click', function () {
      form.querySelector('input[name="role"][value="Capital provider"]').checked = true;
      applyRole();
    });
  });
  applyRole();

  // a service chosen on the Services page arrives as ?service=<slug>
  var serviceSelect = form.service;
  var wanted = new URLSearchParams(window.location.search).get('service');
  if (serviceSelect && wanted) {
    Array.prototype.forEach.call(serviceSelect.options, function (opt) {
      if (opt.value === wanted) serviceSelect.value = wanted;
    });
  }
  function serviceName() {
    return serviceSelect && serviceSelect.value ? serviceSelect.options[serviceSelect.selectedIndex].text : 'Not sure yet';
  }

  /* ---------- documents ---------- */
  function sizeLabel(bytes) {
    return bytes > 1048576 ? (bytes / 1048576).toFixed(1) + ' MB' : Math.max(1, Math.round(bytes / 1024)) + ' KB';
  }

  function addFiles(incoming) {
    var problems = [];
    Array.prototype.forEach.call(incoming, function (file) {
      var ext = (file.name.split('.').pop() || '').toLowerCase();
      if (ALLOWED.indexOf(ext) < 0) { problems.push(file.name + ' is not a supported file type'); return; }
      if (file.size > MAX_MB * 1048576) { problems.push(file.name + ' is larger than ' + MAX_MB + ' MB'); return; }
      if (files.length >= MAX_FILES) { problems.push('You can add up to ' + MAX_FILES + ' files'); return; }
      if (files.some(function (f) { return f.name === file.name && f.size === file.size; })) return;
      files.push(file);
    });
    renderFiles();
    showError(problems.length ? problems.join('. ') + '.' : '');
  }

  function renderFiles() {
    list.innerHTML = '';
    files.forEach(function (file, i) {
      var li = document.createElement('li');
      var name = document.createElement('span');
      name.className = 'upload-name';
      name.textContent = file.name;
      var size = document.createElement('span');
      size.className = 'upload-size';
      size.textContent = sizeLabel(file.size);
      var remove = document.createElement('button');
      remove.type = 'button';
      remove.className = 'upload-remove';
      remove.setAttribute('aria-label', 'Remove ' + file.name);
      remove.textContent = '×';
      remove.addEventListener('click', function () { files.splice(i, 1); renderFiles(); });
      li.appendChild(name); li.appendChild(size); li.appendChild(remove);
      list.appendChild(li);
    });
  }

  fileInput.addEventListener('change', function () {
    addFiles(fileInput.files);
    fileInput.value = '';
  });
  ['dragenter', 'dragover'].forEach(function (type) {
    zone.addEventListener(type, function (e) { e.preventDefault(); zone.classList.add('is-over'); });
  });
  ['dragleave', 'drop'].forEach(function (type) {
    zone.addEventListener(type, function (e) { e.preventDefault(); zone.classList.remove('is-over'); });
  });
  zone.addEventListener('drop', function (e) {
    if (e.dataTransfer && e.dataTransfer.files) addFiles(e.dataTransfer.files);
  });

  /* ---------- submit ---------- */
  function showError(text) {
    errorEl.textContent = text;
    errorEl.hidden = !text;
  }

  function finish(text) {
    form.hidden = true;
    doneText.textContent = text;
    doneEl.hidden = false;
    doneEl.focus();
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var sponsor = form.role.value === 'Project sponsor';
    var missing = [];
    if (!form.name.value.trim()) missing.push('your name');
    if (!form.company.value.trim()) missing.push('your company');
    if (!window.NGC.isEmail(form.email.value.trim())) missing.push('a valid email address');
    if (!window.NGC.isPhone(form.phone.value)) missing.push('a phone number we can reach you on');
    if (!form.message.value.trim()) missing.push(sponsor ? 'a short description of the project' : 'a short description of your mandate');
    if (missing.length) { showError('Please add ' + missing.join(', ') + '.'); return; }
    if (!form.consent.checked) { showError('Please confirm that we may use your details to assess your enquiry.'); return; }
    showError('');

    var fields = {
      role: form.role.value,
      name: form.name.value.trim(),
      company: form.company.value.trim(),
      email: form.email.value.trim(),
      phone: form.phone.value.trim(),
      service: serviceName(),
      message: form.message.value.trim(),
      consent: 'yes',
      website: form.website ? form.website.value : ''
    };
    if (sponsor) {
      fields.industry = form.industry.value;
      fields.amount = form.amount.value.trim();
      fields.stage = form.stage.value;
    }

    var button = form.querySelector('button[type="submit"]');
    var label = button.querySelector('span');
    button.disabled = true;
    label.textContent = 'Sending…';

    function emailFallback() {
      var lines = [
        'I am a: ' + fields.role,
        'Name: ' + fields.name,
        'Company: ' + fields.company,
        'Email: ' + fields.email,
        'Phone: ' + fields.phone,
        'Service of interest: ' + fields.service
      ];
      if (sponsor) {
        lines.push('Industry: ' + fields.industry, 'Funding required: R ' + (fields.amount || 'Not provided'), 'Stage: ' + fields.stage);
      }
      lines.push('', fields.message);
      if (files.length) {
        lines.push('', 'Documents to attach: ' + files.map(function (f) { return f.name; }).join(', '));
      }
      window.NGC.openEmail('Project submission: ' + fields.company, lines.join('\n'));
      finish(files.length
        ? 'Your email app has opened with your details. Please attach your documents to that email before you send it.'
        : 'Your email app has opened with your details. Send the email and our team will come back to you with next steps.');
    }

    window.NGC.submitLead('project-submission', fields, files).then(function (result) {
      if (result.sent) finish('Our team will review your submission and come back to you with next steps.');
      else emailFallback();
    }).catch(function (err) {
      // problems the visitor can fix are shown; if the server is unreachable, email keeps the lead
      if (err.userMessage) showError(err.userMessage);
      else emailFallback();
    }).then(function () {
      button.disabled = false;
      label.textContent = 'Submit';
    });
  });
})();
