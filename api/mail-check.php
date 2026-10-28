<?php
/**
 * New Generation Capital: email set-up check.
 *
 * Sends one test email to the funding team with the settings in config.php and reports
 * whether it worked, so the SMTP details can be confirmed after deployment.
 *
 *   From a terminal:  php api/mail-check.php
 *   From a browser:   set 'check_key' in config.php, then open
 *                     https://<domain>/api/mail-check.php?key=<that key>
 *                     and clear 'check_key' again afterwards.
 *
 * Without a matching key the page answers 404, so it is invisible on the live site.
 */

use PHPMailer\PHPMailer\Exception as MailerException;

require __DIR__ . '/lib/PHPMailer/Exception.php';
require __DIR__ . '/lib/PHPMailer/PHPMailer.php';
require __DIR__ . '/lib/PHPMailer/SMTP.php';
require __DIR__ . '/lib/mailer.php';

$cli = PHP_SAPI === 'cli';
$configFile = __DIR__ . '/config.php';
$config = is_file($configFile) ? require $configFile : null;

if (!$cli) {
    $key = (string) ($config['check_key'] ?? '');
    if (strlen($key) < 16 || !hash_equals($key, (string) ($_GET['key'] ?? ''))) {
        http_response_code(404);
        exit;
    }
    header('Content-Type: text/plain; charset=utf-8');
    header('Cache-Control: no-store');
}

function line($ok, $text)
{
    echo ($ok ? '[ OK ]  ' : '[FAIL]  ') . $text . "\n";
}

echo "New Generation Capital: email set-up check\n\n";

line(version_compare(PHP_VERSION, '7.4', '>='), 'PHP ' . PHP_VERSION . ' (7.4 or later needed)');
line(extension_loaded('openssl'), 'OpenSSL extension (needed for ssl/tls)');
line(extension_loaded('fileinfo'), 'Fileinfo extension (checks uploaded file types)');

if (!$config) {
    line(false, 'api/config.php not found. Copy api/config.sample.php to api/config.php and fill it in.');
    exit(1);
}
line(true, 'api/config.php found');

$password = (string) ($config['smtp']['password'] ?? '');
if ($password === '' || $password === 'PUT-THE-MAILBOX-PASSWORD-HERE') {
    line(false, 'The mailbox password in api/config.php has not been filled in.');
    exit(1);
}

$smtp = $config['smtp'];
echo "\nSending a test email through {$smtp['host']}:{$smtp['port']} ({$smtp['secure']}) as {$smtp['username']}\n";
echo 'to ' . implode(', ', (array) $config['to']) . " ...\n\n";

try {
    $mail = mailer($config);
    foreach ((array) $config['to'] as $to) {
        $mail->addAddress($to);
    }
    $mail->Subject = 'Website email check: working';
    $mail->Body = "This is a test from the New Generation Capital website.\n\n"
        . "Calculator reports and project submissions will arrive in this mailbox.\n"
        . 'Sent ' . date('j F Y, H:i') . ' from ' . ($cli ? 'the server command line' : ($_SERVER['HTTP_HOST'] ?? 'the website')) . '.';
    $mail->send();
    line(true, 'Test email sent. Check the funding@ inbox (and spam folder).');
    exit(0);
} catch (MailerException $e) {
    $error = $e->getMessage();
    line(false, 'Sending failed: ' . $error);
    echo "\nWhat to check:\n";
    if (stripos($error, 'authenticate') !== false) {
        echo "- The password in api/config.php (re-type it; it is case-sensitive).\n";
        echo "- 'username' must be the full address: funding@newgenerationcap.co.za.\n";
    } elseif (stripos($error, 'connect') !== false) {
        echo "- 'host' must match the outgoing server in cPanel > Email Accounts > Connect Devices.\n";
        echo "- Try port 465 with 'ssl', or port 587 with 'tls'.\n";
        echo "- Some hosts only allow 'localhost' as the SMTP host from their own servers.\n";
    } else {
        echo "- Compare host, port and security with cPanel > Email Accounts > Connect Devices.\n";
    }
    exit(1);
}
