# New Generation Capital website

Static six-page site for New Generation Capital (part of the New Generation Group), following the
CircleDesign scope of work. No build step: open `index.html` directly, or serve the folder:

```
python3 -m http.server 8000
```

## Pages

| File | Page | Content |
|---|---|---|
| `index.html` | Home | Positioning, key figures, Group heritage, industries, process, funding tools, board, calls to action |
| `about.html` | About us | Who we are, our edge, the model, Board of Directors |
| `what-we-do.html` | What we do | Industries, a preview of our services, the seven-step process (with the deal-flow visual), governance |
| `services.html` | Services | Project Fundraising, Bridging Finance, Acquisitions & Mergers, Greenfield Project Fundraising, Short-Term Insurance; each links to the submission form with the service pre-selected (`partner.html?service=<slug>`) |
| `funding-tools.html` | Funding tools | Funding Readiness Assessment and Repayment & DSCR Calculator, each with a PDF report |
| `partner.html` | Partner with us | Sponsors and capital providers, engagement steps, project submission form with document upload |

The header and footer are repeated in each page; change them in all six files.

## Scripts

- `assets/js/config.js`: site settings. `leadEndpoint` points at `api/lead.php`. If it cannot be
  reached, the project form falls back to the visitor's email app; calculator reports download either way.
- `assets/js/leads.js`: sends leads (fields, uploaded documents and the PDF report) to the endpoint.
- `assets/js/partner.js`: submission form: sponsor/funder switch, file checks (PDF, Word, Excel,
  PowerPoint, CSV; up to 5 files of 10 MB), validation (phone required) and POPIA consent.
- `assets/js/tools.js`: the two calculators and the branded PDF reports (built in the browser with
  jsPDF). Name, email, phone and company are required before a report downloads. Results are indicative only.
- `assets/js/slider.js`: home header slider (home page only): 7-second autoplay with progress bars, pause button,
  hold on hover or focus, arrows, swipe and keyboard. No autoplay with `prefers-reduced-motion`.
- `assets/js/main.js`: header, mobile menu, scroll reveals and the deal-flow canvas.
- `assets/js/motion.js`: motion layer (respects `prefers-reduced-motion`), parallax image breaks, and backdrop
  videos that load only when scrolled near, play only while visible, and are skipped for reduced-motion or
  data-saver visitors (the still image shows instead).
- `assets/vendor/jspdf.umd.min.js`: jsPDF 2.5.1 (MIT, see `jspdf.LICENSE`).

## Media

Every image and video slot (home slider, video backdrops, parallax breaks, service and audience images) is listed
in `assets/media/README.md` with the stand-in used now and the recommended format. Upload files to `assets/media/`.

## Lead emails (`api/`)

`api/lead.php` receives every calculator report and project submission and emails it to
funding@newgenerationcap.co.za through that mailbox's SMTP login:

- **Calculator leads:** name, company, email, phone, tool and result, with the visitor's PDF report attached.
  The visitor also receives their report by email (`send_visitor_copy`).
- **Project submissions:** every form field, with the uploaded documents attached.
- Reply-To is the visitor, so replying in the mail client answers them directly.
- Protection: hidden spam-trap field, per-visitor rate limit (8 per 10 minutes), server-side validation,
  file type checks by content (not just extension), header-injection safe fields.
- Mail is sent with PHPMailer 6.12.0 (LGPL 2.1, `api/lib/PHPMailer`). Needs PHP 7.4 or later.

### Go-live on CircleTel Hosting

1. Upload the whole folder, including `api/` and its `.htaccess` files.
2. On the server, copy `api/config.sample.php` to `api/config.php` and enter the funding@ mailbox
   password. Check the SMTP host and port against the mailbox's "Connect Devices" settings in cPanel
   (usually `mail.newgenerationcap.co.za`, port 465 with `ssl`, or 587 with `tls`).
3. Once the domain is live, add it to `allowed_origins` in `config.php`.
4. Confirm `https://<domain>/api/config.php` returns 403 Forbidden.
5. Submit one calculator report and one project to check both emails arrive.

`api/config.php` is listed in `.gitignore` and must never be committed.

## Still to connect for go-live

- `api/config.php` with the funding@ mailbox password on the server (see above).
- Google Analytics 4 and Search Console.
- Final images and videos for the media slots (see `assets/media/README.md`).

Type: Poppins (the New Generation Group typeface) throughout, loaded from Google Fonts.
