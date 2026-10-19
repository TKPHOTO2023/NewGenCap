/* Lead capture: one place where every form and tool hands over its data. */
(function () {
  'use strict';

  var config = window.NGC_CONFIG || {};

  // Sends a lead to the configured endpoint (api/lead.php).
  // Resolves { sent: true, copied } when the endpoint accepted it, or { sent: false } when
  // no endpoint is configured. Rejects with an Error carrying `status` and, for problems the
  // visitor can fix (400, 413, 429), `userMessage`.
  function submitLead(type, fields, files, report) {
    if (!config.leadEndpoint) return Promise.resolve({ sent: false });
    var data = new FormData();
    data.append('lead_type', type);
    data.append('page', window.location.pathname);
    Object.keys(fields).forEach(function (key) {
      var value = fields[key];
      if (value !== undefined && value !== null) data.append(key, value);
    });
    (files || []).forEach(function (file) { data.append('documents[]', file, file.name); });
    if (report) data.append('report', report.blob, report.name);

    return fetch(config.leadEndpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
      .then(function (res) {
        return res.json().catch(function () { return {}; }).then(function (body) {
          if (res.ok && body.ok) return { sent: true, copied: !!body.copied };
          var err = new Error(body.error || ('The server responded with ' + res.status));
          err.status = res.status;
          if ([400, 413, 429].indexOf(res.status) >= 0 && body.error) err.userMessage = body.error;
          throw err;
        });
      });
  }

  function openEmail(subject, body) {
    window.location.href = 'mailto:' + (config.enquiryEmail || '') +
      '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  }

  function isEmail(value) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value); }

  // 9 to 15 digits, ignoring spaces, brackets, dashes and a leading +
  function isPhone(value) {
    var digits = String(value).replace(/\D/g, '');
    return digits.length >= 9 && digits.length <= 15;
  }

  window.NGC = window.NGC || {};
  window.NGC.submitLead = submitLead;
  window.NGC.openEmail = openEmail;
  window.NGC.isEmail = isEmail;
  window.NGC.isPhone = isPhone;
})();
