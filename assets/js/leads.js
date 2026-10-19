/* Lead capture: one place where every form and tool hands over its data. */
(function () {
  'use strict';

  var config = window.NGC_CONFIG || {};

  // Sends a lead to the configured endpoint. Resolves { sent: true } when the
  // endpoint accepted it, or { sent: false } when no endpoint is configured.
  function submitLead(type, fields, files) {
    if (!config.leadEndpoint) return Promise.resolve({ sent: false });
    var data = new FormData();
    data.append('lead_type', type);
    data.append('page', window.location.pathname);
    Object.keys(fields).forEach(function (key) {
      var value = fields[key];
      if (value !== undefined && value !== null) data.append(key, value);
    });
    (files || []).forEach(function (file) { data.append('documents', file, file.name); });
    return fetch(config.leadEndpoint, { method: 'POST', body: data })
      .then(function (res) {
        if (!res.ok) throw new Error('The server responded with ' + res.status);
        return { sent: true };
      });
  }

  function openEmail(subject, body) {
    window.location.href = 'mailto:' + (config.enquiryEmail || '') +
      '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  }

  function isEmail(value) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value); }

  window.NGC = window.NGC || {};
  window.NGC.submitLead = submitLead;
  window.NGC.openEmail = openEmail;
  window.NGC.isEmail = isEmail;
})();
