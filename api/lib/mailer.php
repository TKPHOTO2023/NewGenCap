<?php
/**
 * Builds a PHPMailer instance that sends through the funding@ mailbox's SMTP login.
 * Shared by lead.php and mail-check.php.
 */

use PHPMailer\PHPMailer\PHPMailer;

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
