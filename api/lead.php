<?php
/**
 * New Generation Capital: lead endpoint.
 *
 * Receives calculator report leads and project submissions from the website
 * (multipart/form-data), emails them to the funding team through the funding@
 * mailbox over SMTP, and optionally emails the visitor a copy of their report.
 *
 * Settings live in config.php next to this file (copy config.sample.php).
 * Works on PHP 7.4 and later.
 */

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception as MailerException;

require __DIR__ . '/lib/PHPMailer/Exception.php';
require __DIR__ . '/lib/PHPMailer/PHPMailer.php';
require __DIR__ . '/lib/PHPMailer/SMTP.php';

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

function respond($status, array $body)
{
    http_response_code($status);
    echo json_encode($body);
    exit;
}

function fail($status, $message)
{
    respond($status, ['ok' => false, 'error' => $message]);
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    fail(405, 'Use POST.');
}

$configFile = __DIR__ . '/config.php';
if (!is_file($configFile)) {
    error_log('NGC lead endpoint: config.php is missing');
    fail(503, 'The form is not configured yet.');
}
$config = require $configFile;

// An oversized upload empties $_POST entirely; say so instead of "missing fields".
if (empty($_POST) && (int) ($_SERVER['CONTENT_LENGTH'] ?? 0) > 0) {
    fail(413, 'The upload is too large. Please send fewer or smaller files.');
}

/* ---------- origin check (optional) ---------- */
$allowedOrigins = $config['allowed_origins'] ?? [];
if ($allowedOrigins) {
    $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
    if ($origin !== '' && !in_array(rtrim($origin, '/'), $allowedOrigins, true)) {
        fail(403, 'Submissions are only accepted from the New Generation Capital website.');
    }
}

/* ---------- spam trap: real visitors never see or fill this field ---------- */
if (trim((string) ($_POST['website'] ?? '')) !== '') {
    respond(200, ['ok' => true]);
}

/* ---------- rate limit per visitor ---------- */
$limit = $config['rate_limit'] ?? ['max' => 8, 'window' => 600];
$ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$bucket = sys_get_temp_dir() . '/ngc-lead-' . sha1($ip . __DIR__) . '.json';
$now = time();
$hits = [];
if (is_file($bucket)) {
    $hits = json_decode((string) @file_get_contents($bucket), true) ?: [];
}
$hits = array_values(array_filter($hits, function ($t) use ($now, $limit) {
    return $t > $now - (int) $limit['window'];
}));
if (count($hits) >= (int) $limit['max']) {
    fail(429, 'Too many submissions from this connection. Please try again in a few minutes.');
}
$hits[] = $now;
@file_put_contents($bucket, json_encode($hits), LOCK_EX);

/* ---------- fields ---------- */
function field($name, $max)
{
    $value = (string) ($_POST[$name] ?? '');
    $value = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $value);
    $value = trim((string) $value);
    return function_exists('mb_substr') ? mb_substr($value, 0, $max) : substr($value, 0, $max);
}

function oneLine($value)
{
    return trim(preg_replace('/[\r\n\t]+/', ' ', $value));
}

$type = field('lead_type', 40);
$types = ['tool-report' => 'Calculator report', 'project-submission' => 'Project submission'];
if (!isset($types[$type])) {
    fail(400, 'Unknown form.');
}

$name = oneLine(field('name', 120));
$email = oneLine(field('email', 254));
$phone = oneLine(field('phone', 40));
$company = oneLine(field('company', 160));
$errors = [];
if ($name === '') {
    $errors[] = 'your name';
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors[] = 'a valid email address';
}
$phoneDigits = preg_replace('/\D/', '', $phone);
if (strlen($phoneDigits) < 9 || strlen($phoneDigits) > 15) {
    $errors[] = 'a valid phone number';
}
if (field('consent', 10) !== 'yes') {
    $errors[] = 'your consent';
}

$rows = [
    'Name' => $name,
    'Company' => $company !== '' ? $company : 'Not provided',
    'Email' => $email,
    'Phone' => $phone,
];

if ($type === 'tool-report') {
    $tools = ['Funding Readiness Assessment', 'Repayment & DSCR Calculator'];
    $tool = field('tool', 80);
    if (!in_array($tool, $tools, true)) {
        $errors[] = 'the tool used';
    }
    $rows['Tool'] = $tool;
    $rows['Result'] = oneLine(field('summary', 300));
} else {
    $message = field('message', 5000);
    if ($company === '') {
        $errors[] = 'your company';
    }
    if ($message === '') {
        $errors[] = 'a short description';
    }
    $rows['I am a'] = oneLine(field('role', 40));
    $rows['Service of interest'] = oneLine(field('service', 80));
    foreach (['industry' => 'Industry', 'amount' => 'Funding required (R)', 'stage' => 'Project stage'] as $key => $label) {
        $v = oneLine(field($key, 120));
        if ($v !== '') {
            $rows[$label] = $v;
        }
    }
    $rows['Message'] = $message;
}

if ($errors) {
    fail(400, 'Please add ' . implode(', ', $errors) . '.');
}

/* ---------- attachments ---------- */
$allowedDocs = [
    'pdf' => ['application/pdf'],
    'doc' => ['application/msword', 'application/vnd.ms-office', 'application/octet-stream'],
    'docx' => ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/zip', 'application/octet-stream'],
    'xls' => ['application/vnd.ms-excel', 'application/vnd.ms-office', 'application/octet-stream'],
    'xlsx' => ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/zip', 'application/octet-stream'],
    'ppt' => ['application/vnd.ms-powerpoint', 'application/vnd.ms-office', 'application/octet-stream'],
    'pptx' => ['application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/zip', 'application/octet-stream'],
    'csv' => ['text/csv', 'text/plain', 'application/csv'],
];
$maxFiles = (int) ($config['max_files'] ?? 5);
$maxBytes = (int) ($config['max_file_mb'] ?? 10) * 1048576;
$finfo = class_exists('finfo') ? new finfo(FILEINFO_MIME_TYPE) : null;

function cleanFileName($name)
{
    $name = basename(str_replace('\\', '/', $name));
    $name = preg_replace('/[^A-Za-z0-9 ._()-]/', '_', $name);
    return substr($name !== '' ? $name : 'document', 0, 120);
}

function uploadedList($key)
{
    if (empty($_FILES[$key])) {
        return [];
    }
    $f = $_FILES[$key];
    if (!is_array($f['name'])) {
        return [$f];
    }
    $out = [];
    foreach ($f['name'] as $i => $n) {
        $out[] = ['name' => $n, 'type' => $f['type'][$i], 'tmp_name' => $f['tmp_name'][$i], 'error' => $f['error'][$i], 'size' => $f['size'][$i]];
    }
    return $out;
}

$attachments = [];
$documents = uploadedList('documents');
if (count($documents) > $maxFiles) {
    fail(400, 'Please send no more than ' . $maxFiles . ' files.');
}
foreach ($documents as $file) {
    $display = cleanFileName($file['name']);
    if ($file['error'] !== UPLOAD_ERR_OK || !is_uploaded_file($file['tmp_name'])) {
        fail(400, $display . ' could not be uploaded. Please try again.');
    }
    if ($file['size'] > $maxBytes) {
        fail(400, $display . ' is larger than ' . ($maxBytes / 1048576) . ' MB.');
    }
    $ext = strtolower(pathinfo($display, PATHINFO_EXTENSION));
    $mime = $finfo ? $finfo->file($file['tmp_name']) : '';
    if (!isset($allowedDocs[$ext]) || ($finfo && !in_array($mime, $allowedDocs[$ext], true))) {
        fail(400, $display . ' is not a supported file type.');
    }
    $attachments[] = ['path' => $file['tmp_name'], 'name' => $display, 'type' => $mime ?: 'application/octet-stream'];
}

$report = null;
foreach (uploadedList('report') as $file) {
    if ($file['error'] !== UPLOAD_ERR_OK || !is_uploaded_file($file['tmp_name']) || $file['size'] > 5 * 1048576) {
        fail(400, 'The report could not be attached.');
    }
    $head = (string) file_get_contents($file['tmp_name'], false, null, 0, 5);
    if ($head !== '%PDF-') {
        fail(400, 'The report could not be attached.');
    }
    $report = ['path' => $file['tmp_name'], 'name' => cleanFileName($file['name']), 'type' => 'application/pdf'];
    $attachments[] = $report;
}

/* ---------- email ---------- */
date_default_timezone_set($config['timezone'] ?? 'Africa/Johannesburg');
$meta = [
    'Submitted' => date('j F Y, H:i'),
    'Page' => oneLine(field('page', 200)),
    'IP address' => $ip,
];

function esc($v)
{
    return htmlspecialchars($v, ENT_QUOTES, 'UTF-8');
}

function renderTable(array $rows)
{
    $html = '';
    foreach ($rows as $label => $value) {
        $html .= '<tr><td style="padding:8px 16px 8px 0;color:#617083;vertical-align:top;white-space:nowrap">' . esc($label)
            . '</td><td style="padding:8px 0;color:#05152A">' . nl2br(esc($value)) . '</td></tr>';
    }
    return '<table cellspacing="0" cellpadding="0" style="border-collapse:collapse;font-family:Arial,sans-serif;font-size:14px">' . $html . '</table>';
}

function renderText(array $rows)
{
    $text = '';
    foreach ($rows as $label => $value) {
        $text .= $label . ': ' . $value . "\n";
    }
    return $text;
}

function mailer(array $config)
{
    $smtp = $config['smtp'];
    $mail = new PHPMailer(true);
    $mail->isSMTP();
    $mail->Host = $smtp['host'];
    $mail->Port = (int) $smtp['port'];
    $mail->SMTPAuth = ($smtp['username'] ?? '') !== '';
    $mail->Username = $smtp['username'] ?? '';
    $mail->Password = $smtp['password'] ?? '';
    $secure = $smtp['secure'] ?? 'ssl';
    if ($secure === 'ssl') {
        $mail->SMTPSecure = PHPMailer::ENCRYPTION_SMTPS;
    } elseif ($secure === 'tls') {
        $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
    } else {
        $mail->SMTPSecure = '';
        $mail->SMTPAutoTLS = false;
    }
    $mail->Timeout = 20;
    $mail->CharSet = PHPMailer::CHARSET_UTF8;
    $mail->setFrom($config['from_email'], $config['from_name'] ?? 'New Generation Capital');
    return $mail;
}

$label = $types[$type];
$who = $company !== '' ? $company . ', ' . $name : $name;
$subject = $type === 'tool-report'
    ? 'Calculator lead: ' . $who . ' (' . $rows['Tool'] . ')'
    : 'Project submission: ' . $who;

try {
    $mail = mailer($config);
    foreach ((array) $config['to'] as $to) {
        $mail->addAddress($to);
    }
    $mail->addReplyTo($email, $name);
    $mail->Subject = $subject;
    $mail->isHTML(true);
    $mail->Body = '<div style="font-family:Arial,sans-serif;color:#05152A">'
        . '<p style="font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#D96A0B;margin:0 0 6px">' . esc($label) . '</p>'
        . '<h2 style="font-weight:normal;margin:0 0 18px">' . esc($who) . '</h2>'
        . renderTable($rows)
        . '<p style="margin:24px 0 8px;font-size:12px;color:#617083">' . esc(implode('  ·  ', array_map(function ($k) use ($meta) { return $k . ': ' . $meta[$k]; }, array_keys($meta)))) . '</p>'
        . ($attachments ? '<p style="font-size:12px;color:#617083">Attached: ' . esc(implode(', ', array_column($attachments, 'name'))) . '</p>' : '')
        . '<p style="font-size:12px;color:#617083">Reply to this email to respond to ' . esc($name) . ' directly.</p></div>';
    $mail->AltBody = $label . "\n\n" . renderText($rows) . "\n" . renderText($meta);
    foreach ($attachments as $a) {
        $mail->addAttachment($a['path'], $a['name'], PHPMailer::ENCODING_BASE64, $a['type']);
    }
    $mail->send();
} catch (MailerException $e) {
    error_log('NGC lead endpoint: team email failed: ' . $e->getMessage());
    fail(502, 'We could not send your details right now.');
}

/* ---------- copy of the report to the visitor ---------- */
$copied = false;
if ($type === 'tool-report' && $report && !empty($config['send_visitor_copy'])) {
    try {
        $copy = mailer($config);
        $copy->addAddress($email, $name);
        $copy->addReplyTo($config['from_email'], $config['from_name'] ?? 'New Generation Capital');
        $copy->Subject = 'Your ' . $rows['Tool'] . ' report from New Generation Capital';
        $copy->isHTML(true);
        $contact = $config['contact_line'] ?? 'funding@newgenerationcap.co.za  ·  +27 87 742 0831';
        $copy->Body = '<div style="font-family:Arial,sans-serif;color:#05152A;font-size:14px;line-height:1.6">'
            . '<p>Dear ' . esc($name) . ',</p>'
            . '<p>Thank you for using the ' . esc($rows['Tool']) . '. Your report is attached.</p>'
            . '<p>If you would like help taking your project further, reply to this email and our team will be in touch.</p>'
            . '<p style="margin-top:24px">New Generation Capital<br><span style="color:#617083">' . esc($contact) . '</span></p>'
            . '<p style="font-size:12px;color:#617083">Results are indicative only and do not constitute financial advice or an offer of finance.</p></div>';
        $copy->AltBody = "Dear $name,\n\nThank you for using the " . $rows['Tool'] . ". Your report is attached.\n\n"
            . "If you would like help taking your project further, reply to this email and our team will be in touch.\n\n"
            . "New Generation Capital\n$contact\n\nResults are indicative only and do not constitute financial advice or an offer of finance.";
        $copy->addAttachment($report['path'], $report['name'], PHPMailer::ENCODING_BASE64, 'application/pdf');
        $copy->send();
        $copied = true;
    } catch (MailerException $e) {
        // the lead already reached the team; a failed copy must not fail the request
        error_log('NGC lead endpoint: visitor copy failed: ' . $e->getMessage());
    }
}

respond(200, ['ok' => true, 'copied' => $copied]);
