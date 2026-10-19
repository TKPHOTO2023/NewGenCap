/* Site settings.
   leadEndpoint: the script that emails leads to the funding team (api/lead.php, configured in
   api/config.php on the server). If it cannot be reached, the project form falls back to the
   visitor's email app; calculator reports download either way. */
window.NGC_CONFIG = {
  leadEndpoint: 'api/lead.php',
  enquiryEmail: 'funding@newgenerationcap.co.za',
  maxFiles: 5,
  maxFileMB: 10
};
