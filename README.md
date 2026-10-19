# New Generation Capital — website

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

- `assets/js/config.js` — site settings. **Set `leadEndpoint`** to the form handler (ZOHO CRM webform
  handler or a CircleTel-hosted endpoint) to receive submissions and calculator leads as
  `multipart/form-data`. Each request carries `lead_type` (`project-submission` or `tool-report`),
  the form fields and, for submissions, the uploaded `documents`. While it is empty, the submission
  form opens the visitor's email app instead, and calculator reports still download.
- `assets/js/leads.js` — sends leads to the endpoint.
- `assets/js/partner.js` — submission form: sponsor/funder switch, file checks (PDF, Word, Excel,
  PowerPoint, CSV; up to 5 files of 10 MB), validation and POPIA consent.
- `assets/js/tools.js` — the two calculators and the branded PDF reports (built in the browser with
  jsPDF). Results are indicative only.
- `assets/js/main.js` — header, mobile menu, scroll reveals and the deal-flow canvas.
- `assets/js/motion.js` — motion layer (respects `prefers-reduced-motion`).
- `assets/vendor/jspdf.umd.min.js` — jsPDF 2.5.1 (MIT, see `jspdf.LICENSE`).

## Still to connect for go-live

- Lead endpoint (ZOHO CRM or email delivery), including emailing the PDF report to the visitor.
- Google Analytics 4 and Search Console.
- Final imagery for page headers and sections.

Type: Poppins (the New Generation Group typeface) throughout, loaded from Google Fonts.
