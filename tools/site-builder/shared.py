"""Shared head, header and footer for the New Generation Capital pages."""

ARROW = '<svg class="btn-arrow" viewBox="0 0 16 10" aria-hidden="true"><path d="M0 5h14M10 1l4 4-4 4"/></svg>'

NAV = [
    ('index.html', 'Home'),
    ('about.html', 'About us'),
    ('what-we-do.html', 'What we do'),
    ('services.html', 'Services'),
    ('digital-telecoms.html', 'Digital &amp; Telecoms'),
    ('funding-tools.html', 'Funding tools'),
    ('partner.html', 'Partner with us'),
]

# (slug, title, description, tag), client-supplied wording
ALL_SERVICES = [
    ('project-fundraising', 'Project Fundraising',
     'Sourcing and structuring debt, equity and blended capital to fund infrastructure and enterprise projects through to financial close.',
     'Capital raising'),
    ('bridging-finance', 'Bridging Finance',
     'Short-term funding that bridges timing gaps (between a commitment and drawdown, or transaction and settlement) to keep projects moving.',
     'Short-term capital'),
    ('acquisitions-mergers', 'Acquisitions &amp; Mergers',
     'Advisory and funding for buy-side and sell-side transactions, from target identification and structuring to deal execution.',
     'M&amp;A advisory'),
    ('greenfield-fundraising', 'Greenfield Project Fundraising',
     'Capital structuring for new-build developments from the ground up, backing promoters of greenfield infrastructure and energy projects.',
     'New development'),
    ('short-term-insurance', 'Short-Term Insurance',
     'Short-term insurance broking services, providing cover and risk solutions that complement our clients’ projects and operations.',
     'Risk &amp; cover'),
]

# ---------- settings awaiting confirmation from New Generation Capital ----------
# Short-term insurance stays unpublished until the FSP number or licensed partner is confirmed.
HIDDEN_SERVICES = {'short-term-insurance'}
SERVICES = [s for s in ALL_SERVICES if s[0] not in HIDDEN_SERVICES]

# Deal sizes per service: (minimum, maximum) as display text, e.g. ('R5 million', 'R500 million').
# None shows "To be confirmed".
DEAL_SIZES = {slug: (None, None) for slug, _t, _d, _g in ALL_SERVICES}

# Working days within which we reply to a submission, e.g. '3 to 5'. None shows "To be confirmed".
RESPONSE_DAYS = '3 to 5'



def tbc(value):
    """A confirmed value, or a clearly marked placeholder until it is confirmed."""
    return value if value else '<span class="tbc">To be confirmed</span>'


def response_time(short=False):
    if RESPONSE_DAYS:
        return f'within {RESPONSE_DAYS} working days'
    return '<span class="tbc">within X working days</span>'



# ---------- media slots ----------
# Every image and video on the site is chosen here, by image name. Web copies of each image live in
# assets/img/site/<name>-<width>.jpg (made from the uploads in assets/media/); images.json lists the
# widths available. Videos are optional per backdrop slot: while a slot's video is None its image shows.
import json, os
SITE = 'assets/img/site/'
IMAGES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images.json')))

MEDIA = {
    # home header slider (home page only)
    'hero-1': 'brand-path',
    'hero-2': 'solar-aerial',
    'hero-3': 'futuristic-office',
    'hero-4': 'sandton-dusk',
    # "Who we are" photo and Group heritage backdrop, per page
    'who-home': 'team-review',
    'who-about': 'team-discussion',
    'heritage-home': ('sandton-day', None),
    'heritage-about': ('solar-site', None),
    # sponsor / funder band, a different dark image per page
    'cta-home': ('tech-tunnel', None),
    'cta-about': ('liquid-metal', None),
    'cta-what-we-do': ('city-night', None),
    'cta-services': ('optical-fiber', None),
    'cta-digital': ('tech-tunnel', None),
    'backdrop-case': ('sandton-dusk', None),
    'break-case': 'optical-fiber',
    'cta-case': ('city-night', None),
    'spotlight-home': 'optical-fiber',
    'case-feature': 'futuristic-office',
    'backdrop-digital': ('optical-fiber', None),
    'break-digital': 'futuristic-office',
    'digital-a': 'data-campus',
    'digital-b': 'secured-site',
    # page headers
    'backdrop-about': ('office-colleagues', None),
    'backdrop-what-we-do': ('analytics-meeting', None),
    'backdrop-services': ('meeting-devices', None),
    'backdrop-funding-tools': ('office-workers', None),
    'backdrop-partner': ('sponsor-model', None),
    # parallax image breaks, one per page
    'break-home': 'data-campus',
    'break-about': 'solar-wind',
    'break-what-we-do': 'growth-capital',
    'break-services': 'sandton-dusk',
    'break-partner': 'solar-wind',
    # images beside text
    'service-project-fundraising': 'team-meeting',
    'service-bridging-finance': 'growth-capital',
    'service-acquisitions-mergers': 'office-analysis',
    'service-greenfield-fundraising': 'solar-site',
    'service-short-term-insurance': 'secured-site',
    'audience-sponsors': 'office-colleagues',
    'audience-funders': 'analytics-meeting',
}

# where the subject of a photo sits, so cropping keeps it in frame
FOCUS = {
    'brand-path': '70% center',
    'team-meeting': '72% center',
    'sandton-dusk': 'center 62%',
    'sandton-day': 'center 60%',
    'sponsor-model': '58% center',
    'office-colleagues': '35% center',
    'office-analysis': '55% center',
    'growth-capital': '45% 70%',
    'solar-wind': 'center 70%',
    'futuristic-office': '68% center',
    'team-review': 'center 40%',
    'team-discussion': 'center 35%',
    'meeting-devices': '55% center',
    'office-workers': '45% center',
}


# photos shown mirrored (and slightly enlarged) so their people sit in the right third, clear of
# the text on the left; the origin keeps the scaled image covering its whole frame
MIRROR = {}


def image_name(slot):
    value = MEDIA[slot]
    return value[0] if isinstance(value, tuple) else value


def pic(slot, sizes='100vw'):
    """src, srcset, sizes and focal point for an image slot."""
    name = image_name(slot)
    widths = IMAGES[name]['widths']
    srcset = ', '.join(f'{SITE}{name}-{w}.jpg {w}w' for w in widths)
    fallback = 1400 if 1400 in widths else widths[-1]
    rules = []
    if FOCUS.get(name):
        rules.append(f'object-position: {FOCUS[name]}')
    if name in MIRROR:
        rules.append(MIRROR[name])
    style = f' style="{"; ".join(rules)}"' if rules else ''
    return f'src="{SITE}{name}-{fallback}.jpg" srcset="{srcset}" sizes="{sizes}"{style}'


def backdrop(slot, cls='backdrop', eager=False):
    """Full-bleed image, with an optional muted looping video over it (loaded only when in view)."""
    name, video = MEDIA[slot]
    poster = f'{SITE}{name}-1400.jpg' if 1400 in IMAGES[name]['widths'] else f'{SITE}{name}-{IMAGES[name]["widths"][-1]}.jpg'
    video_html = ''
    if video:
        video_html = f'''
      <video class="backdrop__video" muted loop playsinline preload="none" poster="{poster}" data-src="{video}"></video>'''
    return f'''
    <div class="{cls}" aria-hidden="true">
      <img class="backdrop__poster" {pic(slot)} alt="" {'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'}>{video_html}
    </div>'''


def photo_break(slot, text=''):
    """A full-width image band that scrolls slower than the page, between two sections."""
    text_html = ''
    if text:
        text_html = f'''
    <div class="wrap photo-break__inner">
      <p class="photo-break__text reveal">{text}</p>
    </div>'''
    return f'''
  <div class="photo-break{' photo-break--text' if text else ''}"{'' if text else ' aria-hidden="true"'}>
    <div class="photo-break__media" data-parallax="110">
      <img {pic(slot)} alt="" loading="lazy" decoding="async">
    </div>{text_html}
  </div>
'''


def head(title, description, intro=False):
    intro_script = ''
    if intro:
        intro_script = """
<script>
  (function (d) {
    d.classList.add('js');
    try {
      var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (!reduce && !sessionStorage.getItem('ngc-intro')) {
        d.classList.add('has-intro');
        sessionStorage.setItem('ngc-intro', '1');
      }
    } catch (e) {}
  })(document.documentElement);
</script>"""
    else:
        intro_script = """
<script>
  document.documentElement.classList.add('js');
  try { sessionStorage.setItem('ngc-intro', '1'); } catch (e) {}
</script>"""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GHDWLZN32V"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-GHDWLZN32V');
</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#05152A">
<link rel="icon" type="image/png" href="assets/img/ng-mark.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,200;0,300;0,400;0,500;0,600;1,300&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">{intro_script}
</head>
<body>
"""


def header(active):
    links = []
    for href, label in NAV:
        current = ' aria-current="page"' if href == active else ''
        links.append(f'      <a href="{href}"{current}>{label}</a>')
    links_html = '\n'.join(links)
    return f"""
<a class="skip" href="#main">Skip to content</a>

<header class="site-header" id="top">
  <span class="scroll-progress" aria-hidden="true"></span>
  <div class="wrap header-inner">
    <a class="brand" href="index.html" aria-label="New Generation Capital home page">
      <img class="brand-mark brand-mark--light" src="assets/img/ng-mark-light.png" alt="" width="240" height="162">
      <img class="brand-mark brand-mark--dark" src="assets/img/ng-mark.png" alt="" width="240" height="162">
      <span class="brand-word">
        <span class="brand-word__top">New Generation</span>
        <span class="brand-word__bottom">Capital</span>
      </span>
    </a>
    <nav class="nav" id="nav" aria-label="Primary">
{links_html}
      <a class="btn btn--small" href="partner.html#submit">Submit a project</a>
    </nav>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav" aria-label="Open menu">
      <span></span><span></span>
    </button>
  </div>
</header>
"""


def page_hero(label, title, lede, slot=None):
    media = backdrop(slot, 'page-hero__media backdrop', eager=True) if slot else ''
    return f"""
  <section class="page-hero">{media}
    <div class="wrap page-hero__inner">
      <p class="label label--light reveal">{label}</p>
      <h1 class="page-hero__title reveal">{title}</h1>
      <p class="page-hero__lede reveal">{lede}</p>
    </div>
  </section>
"""


def cta_band(page):
    return f"""
  <section class="section cta-band has-backdrop">{backdrop('cta-' + page)}
    <div class="wrap cta-grid">
      <div class="cta-col reveal">
        <p class="label label--light">For project sponsors</p>
        <h2 class="cta-title">Have a project that needs funding?</h2>
        <p>Tell us about it and share your documents. We will review it and come back to you with next steps.</p>
        <a class="btn" href="partner.html#submit"><span>Submit your project</span>{ARROW}</a>
      </div>
      <div class="cta-col reveal">
        <p class="label label--light">For capital providers</p>
        <h2 class="cta-title">Looking for pre-screened deal flow?</h2>
        <p>We extend your origination reach, check build costs and verify progress before each drawdown, so your capital stays protected.</p>
        <a class="btn btn--ghost" href="partner.html#funders"><span>Partner with us</span>{ARROW}</a>
      </div>
    </div>
  </section>
"""


def footer(scripts=()):
    company = '\n'.join(f'        <li><a href="{h}">{l}</a></li>' for h, l in NAV)
    services = '\n'.join(f'        <li><a href="services.html#{slug}">{title}</a></li>' for slug, title, _d, _t in SERVICES)
    extra = '\n'.join(f'<script src="{s}" defer></script>' for s in scripts)
    return f"""
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <a class="brand footer-logo" href="index.html" aria-label="New Generation Capital home page">
        <img class="brand-mark" src="assets/img/ng-mark-light.png" alt="" width="240" height="162">
        <span class="brand-word">
          <span class="brand-word__top">New Generation</span>
          <span class="brand-word__bottom">Capital</span>
        </span>
      </a>
      <p>Project finance and advisory across industries. A member of the New Generation Group.</p>
    </div>
    <nav class="footer-col" aria-label="Company">
      <h2 class="footer-title">Company</h2>
      <ul>
{company}
        <li><a href="case-study-joburg-broadband.html">Case study</a></li>
        <li><a href="partner.html#submit">Submit a project</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="Services">
      <h2 class="footer-title">Services</h2>
      <ul>
{services}
      </ul>
    </nav>
    <div class="footer-col">
      <h2 class="footer-title">Contact</h2>
      <ul>
        <li><a href="tel:+27877420831">+27 87 742 0831</a></li>
        <li><a href="mailto:funding@newgenerationcap.co.za">funding@newgenerationcap.co.za</a></li>
        <li>Imagine House, 2 Mellis Road,<br>Rivonia, Sandton, 2191</li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <p>© <span id="year">2026</span> New Generation Capital (Pty) Ltd. All rights reserved.</p>
    <p>Registration No. 2015/421630/07</p>
  </div>
</footer>

<a class="to-top" href="#top" aria-label="Back to top"><svg viewBox="0 0 10 16" aria-hidden="true"><path d="M5 15V1M1 5l4-4 4 4"/></svg></a>

<script src="assets/js/config.js" defer></script>
<script src="assets/js/main.js" defer></script>
<script src="assets/js/motion.js" defer></script>
{extra}
</body>
</html>
"""


# ---------- reusable content blocks ----------

STAGES = [
    ('Find', 'Source clients who need funding for viable projects.', ''),
    ('Screen', 'Assess credibility, scalability and business potential.', ''),
    ('Validate', 'Establish commercial viability and the investment case.', ''),
    ('Package', 'Structure a funder-ready deal and present it for funding.', 'stage--gated'),
    ('Fund', 'The capital provider funds approved projects.', 'stage--funder'),
    ('Deliver', 'Project-manage delivery through to profitable completion.', ''),
    ('Monitor', 'Report progress, spend and risks to the funder every month, with early warnings.', ''),
]


def stages_list():
    items = []
    for i, (name, text, cls) in enumerate(STAGES, 1):
        cls_attr = f' class="{cls}"' if cls else ''
        tag = '\n          <span class="stage-tag">Funder’s role</span>' if cls == 'stage--funder' else ''
        items.append(f"""        <li{cls_attr}>
          <span class="stage-num">{i:02d}</span>
          <h3>{name}</h3>
          <p>{text}</p>{tag}
        </li>""")
    return '      <ol class="stages stagger" id="stages">\n' + '\n'.join(items) + '\n      </ol>'


INDUSTRIES = [
    ('Energy &amp; power', 'Solar, wind, hybrid and micro-grid generation, storage and energy efficiency.'),
    ('Construction &amp; civil works', 'Building and civil contracts, plant, equipment and contractor growth.'),
    ('Infrastructure', 'Public and private infrastructure, logistics, water and transport assets.'),
    ('Digital &amp; telecoms', 'Fibre, towers, connectivity, and edge and micro data centres.'),
    ('Fintech &amp; financial services', 'Payments, lending and digital finance platforms ready to scale.'),
    ('Property &amp; real estate', 'Commercial, residential and mixed-use developments.'),
    ('Agriculture &amp; agro-processing', 'Farming operations, processing facilities and food value chains.'),
    ('Manufacturing &amp; industry', 'Plant expansion, equipment and new industrial capacity.'),
]


def industries_grid(with_text=True):
    items = []
    for name, text in INDUSTRIES:
        body = f'\n          <p>{text}</p>' if with_text else ''
        if name.startswith('Digital'):
            items.append(f"""        <li class="industry industry--link">
          <a href="digital-telecoms.html"><h3>{name}</h3>{body}<span class="industry__more">Explore {ARROW}</span></a>
        </li>""")
        else:
            items.append(f"""        <li class="industry">
          <h3>{name}</h3>{body}
        </li>""")
    return '      <ul class="industries stagger">\n' + '\n'.join(items) + '\n      </ul>'


PEOPLE = [
    ('melvin-watkins', 'Melvin Watkins', 'Director · Founder &amp; Group CEO, New Generation Group', [
        '34+ years across telecoms, banking, mining, manufacturing and IT',
        'Former MTN Nigeria, International Flavors &amp; Fragrances, Carrier SA',
        'MTN &amp; Vodacom Partner of the Year, 2016',
        'B.Comm, University of the Western Cape',
    ]),
    ('jeffrey-de-wee', 'Jeffrey de Wee', 'Director · COO, New Generation Group', [
        '25+ years in telecommunications and ICT',
        'Former Vodacom (FTTX), Ericsson SA, Airtel Nigeria',
        'Led the R1.2bn City of Johannesburg broadband project',
        'B. Financial Management, UNISA · National Diploma, Electrical Engineering',
    ]),
    ('selwyn-watkins', 'Selwyn Watkins', 'Managing Director', [
        '29+ years across telecoms, FMCG and transportation in Africa, the Middle East and the Americas',
        'USD 380M+ raised in debt, equity, syndicated and project finance',
        'Former MTN, Ceragon, ADC, Coca-Cola, SABMiller, Nampak',
        'ACCA (UK) · B.Comm (Accounting), University of the Western Cape',
    ]),
]


def people(brief=False):
    out = []
    for slug, name, role, facts in PEOPLE:
        facts_html = ''
        if not brief:
            facts_html = '\n          <ul>\n' + '\n'.join(f'            <li>{f}</li>' for f in facts) + '\n          </ul>'
        out.append(f"""        <article class="person">
          <div class="person-photo wipe"><img src="assets/img/board-{slug}-framed.webp" alt="Portrait of {name}" width="600" height="600" loading="lazy"></div>
          <h3>{name}</h3>
          <p class="role">{role}</p>{facts_html}
        </article>""")
    cls = 'people people--brief stagger' if brief else 'people stagger'
    return f'      <div class="{cls}">\n' + '\n'.join(out) + '\n      </div>'
