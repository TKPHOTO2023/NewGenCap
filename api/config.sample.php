<?php
/**
 * Lead endpoint settings. Copy this file to config.php on the server and fill in
 * the funding@ mailbox password. config.php is never committed to the repository
 * and the web server refuses to serve it (see .htaccess).
 *
 * SMTP details come from the mailbox's "connect a mail client" settings
 * (cPanel → Email Accounts → Connect Devices). Use the outgoing (SMTP) server.
 */
return [
    'smtp' => [
        'host' => 'mail.newgenerationcap.co.za',  // outgoing (SMTP) server
        'port' => 465,                             // 465 with 'ssl', or 587 with 'tls'
        'secure' => 'ssl',                         // 'ssl', 'tls', or '' (local testing only)
        'username' => 'funding@newgenerationcap.co.za',
        'password' => 'PUT-THE-MAILBOX-PASSWORD-HERE',
    ],

    // Leads are sent from the mailbox itself, so they pass SPF/DKIM checks.
    'from_email' => 'funding@newgenerationcap.co.za',
    'from_name' => 'New Generation Capital website',

    // Who receives the leads. Add more addresses to copy other people in.
    'to' => ['funding@newgenerationcap.co.za'],

    // Email the visitor a copy of their calculator report.
    'send_visitor_copy' => true,
    'contact_line' => 'funding@newgenerationcap.co.za  ·  +27 87 742 0831',

    // Only accept submissions from these sites (no trailing slash). Leave empty to skip the check.
    'allowed_origins' => [
        // 'https://newgenerationcap.co.za',
        // 'https://www.newgenerationcap.co.za',
    ],

    // At most 'max' submissions per visitor every 'window' seconds.
    'rate_limit' => ['max' => 8, 'window' => 600],

    'max_files' => 5,
    'max_file_mb' => 10,
    'timezone' => 'Africa/Johannesburg',
];
