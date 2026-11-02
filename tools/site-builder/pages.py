import sys
from shared import (ARROW, head, header, page_hero, cta_band, footer,
                    stages_list, industries_grid, people, SERVICES,
                    MEDIA, backdrop, photo_break, pic, ALL_SERVICES, DEAL_SIZES,
                    tbc, response_time)

OUT = sys.argv[1]

INTRO = """
<div class="intro" aria-hidden="true">
  <img class="intro-mark" src="assets/img/ng-mark-light.png" alt="" width="240" height="162">
  <span class="intro-rule"></span>
</div>
"""

HERITAGE = """
  <section class="section heritage has-backdrop">__BACKDROP__
    <div class="wrap heritage-grid">
      <div class="reveal">
        <p class="label label--light">Built on the New Generation Group</p>
        <h2 class="display display--light">Operating depth from companies that build, power and connect.</h2>
      </div>
      <div class="heritage-body reveal">
        <p>New Generation Capital is part of the New Generation Group. Our sister companies work in construction, energy, infrastructure and telecoms, so we know what it takes to deliver a project on the ground.</p>
        <p>We bring that understanding to every deal we structure, whether the project is a solar plant, a fintech platform or a factory expansion.</p>
        <ul class="heritage-list stagger">
          <li>Construction</li>
          <li>Energy</li>
          <li>Infrastructure</li>
          <li>Telecoms &amp; ICT</li>
        </ul>
      </div>
    </div>
  </section>
"""

WHO = """
  <section class="section approach" id="approach">
    <div class="wrap approach-grid">
      <div class="approach-statement reveal">
        <p class="label">Who we are</p>
        <h2 class="display">Many advisors can model cash flows. <span class="ink-fill" data-ink>We know what it takes to build, power and run the projects behind them.</span></h2>
      </div>
      <div class="approach-body reveal">
        <p>We are a project finance and advisory firm. We source opportunities, test feasibility, package projects and structure the funding for sponsors in any industry, and for the capital providers who back them.</p>
        <ul class="pillars stagger">
          <li>
            <h3>Operational lens</h3>
            <p>Delivery experience from across the Group informs every diligence decision.</p>
          </li>
          <li>
            <h3>Early risk visibility</h3>
            <p>Delivery issues surface before they undermine the case.</p>
          </li>
          <li>
            <h3>Funder alignment</h3>
            <p>Evidence is packaged the way capital providers decide.</p>
          </li>
        </ul>
      </div>
    </div>
    <figure class="wrap approach-figure reveal wipe" data-parallax>
      <img __WHO_IMG__ loading="lazy" decoding="async">
    </figure>
  </section>
"""


WHO_ALT = {
    'home': 'The New Generation Capital team reviewing project plans and financial dashboards',
    'about': 'A project team discussing plans and figures around a table',
}


def who(page):
    img = pic('who-' + page, '(max-width: 1240px) 100vw, 1200px') + f' alt="{WHO_ALT[page]}"'
    return WHO.replace('__WHO_IMG__', img)


def heritage(page):
    return HERITAGE.replace('__BACKDROP__', backdrop('heritage-' + page))


MODEL = """
  <section class="section funders" id="model">
    <div class="wrap">
      <div class="section-head reveal">
        <p class="label label--light">The model</p>
        <h2 class="display display--light">We sit between projects and capital, and protect both.</h2>
      </div>
      <div class="model reveal">
        <span class="model-pulse" aria-hidden="true"></span>
        <div class="model-col">
          <h3>Project sponsors &amp; clients</h3>
          <ul><li>Projects, sites and ambitions</li><li>Need funding to grow</li></ul>
        </div>
        <div class="model-col model-col--us">
          <h3>New Generation Capital</h3>
          <ul><li>Find and originate</li><li>Screen and validate</li><li>Package the deal</li><li>Monitor delivery</li></ul>
        </div>
        <div class="model-col">
          <h3>Capital providers</h3>
          <ul><li>Provide the funding</li><li>Earn their return</li><li>Receive de-risked, managed deals</li></ul>
        </div>
      </div>
      <p class="aligned reveal">We earn when a deal funds <em>and</em> when it is delivered well. Our incentives mirror the funder’s own.</p>
    </div>
  </section>
"""

TOOLS_TEASER = f"""
  <section class="section tools-teaser" id="tools">
    <div class="wrap">
      <div class="section-head section-head--split reveal">
        <div>
          <p class="label">Free funding tools</p>
          <h2 class="display">Test your project before you pitch it.</h2>
        </div>
        <p class="section-head__aside">Three free tools give you an instant answer, and a detailed PDF report you can share with your team.</p>
      </div>
      <div class="tool-cards stagger">
        <a class="tool-card-link" href="funding-tools.html#readiness">
          <span class="tool-card-link__meta">10 questions · about 3 minutes</span>
          <h3>Funding Readiness Assessment</h3>
          <p>Score how ready your project is for funding, and see exactly what is missing before funders will engage.</p>
          <span class="tool-card-link__cta">Check my readiness {ARROW}</span>
        </a>
        <a class="tool-card-link" href="funding-tools.html#telecoms">
          <span class="tool-card-link__meta">10 questions · about 3 minutes</span>
          <h3>Telecoms Readiness Assessment</h3>
          <p>For fibre, tower, wireless and data centre projects: see how ready your network build is for funders.</p>
          <span class="tool-card-link__cta">Assess my network project {ARROW}</span>
        </a>
        <a class="tool-card-link" href="funding-tools.html#dscr">
          <span class="tool-card-link__meta">Instant result · year-by-year schedule</span>
          <h3>Repayment &amp; DSCR Calculator</h3>
          <p>Estimate loan repayments and the debt service coverage ratio lenders will look at, from your project’s numbers.</p>
          <span class="tool-card-link__cta">Calculate repayments {ARROW}</span>
        </a>
      </div>
    </div>
  </section>
"""


# (media slot, label, title, lede); the first slide carries the page's h1
HERO_SLIDES = [
    ('hero-1', 'Project finance &amp; advisory &nbsp;·&nbsp; South Africa',
     'We turn ideas into <em class="hero-em">investable</em> projects.',
     'New Generation Capital originates, structures and funds viable projects across every industry, from energy and construction to fintech. We bring the operating insight of the New Generation Group to every deal.'),
    ('hero-2', 'Energy &amp; infrastructure',
     'Power and infrastructure, <em class="hero-em">structured</em> to be funded.',
     'Our roots are in the New Generation Group’s construction, energy and infrastructure companies, so we know what it takes to build what we finance.'),
    ('hero-3', 'Capital solutions',
     'From bridging finance to <em class="hero-em">financial close</em>.',
     'Project and greenfield fundraising, bridging finance, and acquisitions and mergers: the right capital for the stage you are at.'),
    ('hero-4', 'Every industry',
     'Any industry. One <em class="hero-em">disciplined</em> process.',
     'From fintech platforms to factories and farms: if a project is viable, our seven-step process gets it ready for funders.'),
]


def hero_media():
    out = []
    for i, (slot, _l, _t, _d) in enumerate(HERO_SLIDES):
        attrs = 'fetchpriority="high"' if i == 0 else 'loading="lazy" decoding="async"'
        active = ' is-active' if i == 0 else ''
        out.append(f'''      <div class="hero-media__slide{active}"><img {pic(slot)} alt="" {attrs}></div>''')
    return '\n'.join(out)


def hero_slides():
    out = []
    n = len(HERO_SLIDES)
    for i, (_s, label, title, lede) in enumerate(HERO_SLIDES):
        tag = 'h1' if i == 0 else 'h2'
        active = ' is-active' if i == 0 else ''
        hidden = '' if i == 0 else ' aria-hidden="true"'
        out.append(f'''        <div class="hero-slide{active}" role="group" aria-roledescription="slide" aria-label="{i + 1} of {n}"{hidden}>
          <p class="label label--light">{label}</p>
          <{tag} class="hero-title" data-split>{title}</{tag}>
          <p class="hero-lede">{lede}</p>
        </div>''')
    return '\n'.join(out)


def hero_dots():
    out = []
    for i, (_s, label, _t, _d) in enumerate(HERO_SLIDES):
        name = label.split('&nbsp;')[0].replace('&amp;', 'and').strip()
        current = ' aria-current="true"' if i == 0 else ''
        active = ' is-active' if i == 0 else ''
        out.append(f'''            <button class="hero-dot{active}" type="button" aria-label="Show slide {i + 1}: {name}"{current}><span class="hero-dot__fill"></span></button>''')
    return '\n'.join(out)


DIGITAL_SPOTLIGHT = f"""
  <section class="section spotlight" id="digital">
    <div class="wrap spotlight-grid">
      <div class="spotlight-copy reveal">
        <p class="label">Digital infrastructure</p>
        <h2 class="display">Our deepest expertise: the networks behind the digital economy.</h2>
        <p>Fibre, towers, edge data centres and the power and security around them. Our directors have built and run these networks, and South Africa needs R140bn+ of digital infrastructure by 2035.</p>
        <ul class="spotlight-tags">
          <li>Connectivity &amp; fibre</li>
          <li>Edge &amp; micro data centres</li>
          <li>Energy for digital sites</li>
          <li>Security &amp; surveillance</li>
          <li>Supporting value chains</li>
        </ul>
        <a class="btn" href="digital-telecoms.html"><span>Explore Digital &amp; Telecoms</span>{ARROW}</a>
      </div>
      <a class="case-card reveal" href="case-study-joburg-broadband.html">
        <div class="case-card__media"><img {pic('spotlight-home', '(max-width: 900px) 100vw, 45vw')} alt="" loading="lazy" decoding="async"></div>
        <div class="case-card__body">
          <p class="label label--light">Case study</p>
          <p class="case-card__figure">R1.2bn</p>
          <h3>City of Johannesburg broadband project</h3>
          <p>A city-wide broadband build led by our COO, Jeffrey de Wee. The delivery experience behind how we check build costs and verify progress.</p>
          <span class="case-card__cta">Read the case study {ARROW}</span>
        </div>
      </a>
    </div>
  </section>
"""


def home():
    return (head('New Generation Capital | Project finance and advisory across industries',
                 'New Generation Capital originates, structures and funds viable projects across every industry, from energy and construction to fintech. Part of the New Generation Group.',
                 intro=True)
            + INTRO + header('index.html') + f"""
<main id="main">

  <section class="hero hero--slider" id="hero" aria-roledescription="carousel" aria-label="New Generation Capital highlights">
    <div class="hero-media" aria-hidden="true">
{hero_media()}
    </div>
    <div class="wrap hero-inner">
      <div class="hero-slides reveal">
{hero_slides()}
      </div>
      <div class="hero-bar reveal">
        <div class="hero-actions">
          <a class="btn" href="partner.html#submit" data-magnetic><span>Submit a project</span>{ARROW}</a>
          <a class="btn btn--ghost" href="funding-tools.html" data-magnetic><span>Try our funding tools</span>{ARROW}</a>
        </div>
        <div class="hero-nav" role="group" aria-label="Slideshow controls">
          <p class="hero-nav__count" aria-hidden="true"><span id="heroCurrent">01</span> / {len(HERO_SLIDES):02d}</p>
          <div class="hero-nav__dots">
{hero_dots()}
          </div>
          <button class="hero-nav__btn" type="button" data-hero="prev" aria-label="Previous slide"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5"/></svg></button>
          <button class="hero-nav__btn" type="button" data-hero="next" aria-label="Next slide"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg></button>
          <button class="hero-nav__btn" type="button" data-hero="toggle" aria-label="Pause slideshow"><svg class="i-pause" viewBox="0 0 16 16" aria-hidden="true"><path d="M5.5 3v10M10.5 3v10"/></svg><svg class="i-play" viewBox="0 0 16 16" aria-hidden="true"><path d="M5 3v10l8-5z"/></svg></button>
        </div>
      </div>
    </div>
    <div class="wrap hero-credentials reveal">
      <dl>
        <div><dt><span data-count="30">30</span>+ years</dt><dd>Hands-on experience across finance, telecoms and infrastructure</dd></div>
        <div><dt>USD <span data-count="380">380</span>M+</dt><dd>Raised by our leadership in debt, equity and project finance</dd></div>
        <div><dt>R<span data-count="1.2" data-decimals="1">1.2</span>bn</dt><dd><a href="case-study-joburg-broadband.html">City of Johannesburg broadband project</a> led by our COO</dd></div>
      </dl>
      <p class="group-note">Part of the <strong>New Generation Group</strong></p>
    </div>
  </section>
{DIGITAL_SPOTLIGHT}{who('home')}{heritage('home')}
  <section class="section industries-section" id="industries">
    <div class="wrap">
      <div class="section-head section-head--split reveal">
        <div>
          <p class="label">Industries we fund</p>
          <h2 class="display">Not one sector. Any project that stands up.</h2>
        </div>
        <p class="section-head__aside">Our roots are in construction, energy and infrastructure. Our funding is not limited to them. If a project is viable, we want to see it.</p>
      </div>
{industries_grid(with_text=False)}
      <p class="section-link reveal"><a class="text-link" href="what-we-do.html#industries">See what we do in each industry {ARROW}</a></p>
    </div>
  </section>

{photo_break('break-home', 'Technical and operational insight, built into every structure.')}
  <section class="section process" id="process">
    <div class="wrap">
      <div class="section-head section-head--split reveal">
        <div>
          <p class="label">How we work</p>
          <h2 class="display">From origination to funding, and beyond.</h2>
        </div>
        <p class="section-head__aside">Only deals that are credible, commercially viable and deliverable pass our decision gate. After funding, we stay on the project until it is complete.</p>
      </div>
{stages_list()}
      <p class="section-link reveal"><a class="text-link" href="what-we-do.html#process">See the full process {ARROW}</a></p>
    </div>
  </section>
{TOOLS_TEASER}
  <section class="section leadership" id="leadership">
    <div class="wrap">
      <div class="section-head section-head--split reveal">
        <div>
          <p class="label">Leadership</p>
          <h2 class="display">Origination, technical delivery and finance under one roof.</h2>
        </div>
        <p class="section-head__aside">Our board brings national-scale operating experience and cross-border capital raising to every mandate.</p>
      </div>
{people(brief=True)}
      <p class="section-link reveal"><a class="text-link" href="about.html#board">Meet the board {ARROW}</a></p>
    </div>
  </section>
{cta_band('home')}
</main>
""" + footer(['assets/js/slider.js']))


def about():
    return (head('About us | New Generation Capital',
                 'Who we are, our edge and the Board of Directors of New Generation Capital, a project finance and advisory firm in the New Generation Group.')
            + header('about.html') + '\n<main id="main">\n'
            + page_hero('About us', 'Finance people who have built real projects.',
                        'New Generation Capital is a project finance and advisory firm in the New Generation Group. We combine capital-raising expertise with hands-on delivery experience, for sponsors and funders in every industry.',
                        'backdrop-about')
            + who('about') + heritage('about') + f"""
  <section class="section edge">
    <div class="wrap">
      <div class="section-head reveal">
        <p class="label">Our edge</p>
        <h2 class="display">Delivery realism, not modelling in isolation.</h2>
      </div>
      <div class="edge-grid stagger">
        <div class="edge-item">
          <h3>We have delivered, not just advised</h3>
          <p>Our directors have launched telecoms operations, led a R1.2bn municipal broadband build and raised more than USD 380M across debt, equity and project finance.</p>
        </div>
        <div class="edge-item">
          <h3>Insight built into the structure</h3>
          <p>Technical and operational insight is part of the financial structuring from day one, not added after the model is built.</p>
        </div>
        <div class="edge-item">
          <h3>We stay after funding</h3>
          <p>Milestone drawdowns, monthly reporting and on-the-ground monitoring keep projects on track through to completion.</p>
        </div>
      </div>
    </div>
  </section>
{MODEL}{photo_break('break-about', 'Delivery experience informs every diligence decision.')}
  <section class="section leadership" id="board">
    <div class="wrap">
      <div class="section-head section-head--split reveal">
        <div>
          <p class="label">Board of Directors</p>
          <h2 class="display">Origination, technical delivery and finance under one roof.</h2>
        </div>
        <p class="section-head__aside">Our board brings national-scale operating experience, ICT entrepreneurship and cross-border capital raising to every mandate.</p>
      </div>
{people()}
    </div>
  </section>
{cta_band('about')}
</main>
""" + footer())


def what_we_do():
    return (head('What we do | New Generation Capital',
                 'Project finance and advisory across industries: how New Generation Capital structures capital, the seven-step process from origination to monitoring, and how funders are protected.')
            + header('what-we-do.html') + '\n<main id="main">\n'
            + page_hero('What we do', 'We find, structure and fund viable projects in any industry.',
                        'From first screening to final completion, we prepare projects for funding and protect the capital behind them.',
                        'backdrop-what-we-do')
            + f"""
  <section class="section industries-section" id="industries">
    <div class="wrap">
      <div class="section-head section-head--split reveal">
        <div>
          <p class="label">Industries we fund</p>
          <h2 class="display">Deep roots, broad reach.</h2>
        </div>
        <p class="section-head__aside">We understand construction, energy and infrastructure from the New Generation Group’s own companies. We apply the same discipline to projects in every sector.</p>
      </div>
{industries_grid()}
      <p class="industries-note reveal">Don’t see your industry? If the project is viable, <a class="text-link" href="partner.html#submit">we want to hear about it</a>.</p>
    </div>
  </section>

  <section class="section services" id="services">
    <div class="wrap">
      <div class="section-head section-head--split reveal">
        <div>
          <p class="label">Our services</p>
          <h2 class="display">Capital for every stage of a project.</h2>
        </div>
        <p class="section-head__aside">From raising the capital to bridging timing gaps and completing a transaction.</p>
      </div>
{services_preview()}
      <p class="section-link reveal"><a class="text-link" href="services.html">Explore our services {ARROW}</a></p>
    </div>
  </section>
{photo_break('break-what-we-do', 'Only credible, viable and deliverable deals pass the decision gate.')}
  <section class="section process" id="process">
    <div class="wrap">
      <div class="section-head section-head--split reveal">
        <div>
          <p class="label">Our process</p>
          <h2 class="display">From origination to funding: one disciplined process.</h2>
        </div>
        <p class="section-head__aside">Many opportunities come in. Only deals that are credible, commercially viable and deliverable pass the decision gate and are presented for funding.</p>
      </div>

      <div class="flow reveal" aria-hidden="true">
        <canvas class="flow-canvas" id="flowCanvas"></canvas>
        <div class="flow-gate"><span>Decision gate</span></div>
      </div>

{stages_list()}
    </div>
  </section>

  <section class="section funders" id="governance">
    <div class="wrap">
      <div class="section-head reveal">
        <p class="label label--light">Governance &amp; reporting</p>
        <h2 class="display display--light">How capital is protected after funding.</h2>
      </div>
      <ul class="safeguards safeguards--grid stagger">
        <li><h3>Screening gate</h3><p>Standard credibility and viability criteria applied before any deal is presented.</p></li>
        <li><h3>Milestone drawdowns</h3><p>Funds released against verified project progress, not upfront.</p></li>
        <li><h3>Monthly reporting</h3><p>Progress, spend against plan, risks and early warnings, reported to the funder.</p></li>
        <li><h3>Independent monitoring</h3><p>We oversee delivery on the ground through to completion.</p></li>
      </ul>
    </div>
  </section>
{cta_band('what-we-do')}
</main>
""" + footer())


def tool_q(num, name, question, options, hint='', track=''):
    opts = '\n'.join(
        f'              <label class="choice"><input type="radio" name="{name}" value="{score}"><span>{text}</span></label>'
        for score, text in options)
    hint_html = f'\n            <p class="q-hint">{hint}</p>' if hint else ''
    track_attr = f' data-track="{track}"' if track else ''
    return f"""          <fieldset class="q" data-q="{name}"{track_attr}>
            <legend>{question}</legend>{hint_html}
            <div class="choices">
{opts}
            </div>
          </fieldset>"""


QUESTIONS = [
    ('stage', 'What stage is your project at?', [(0, 'Idea or concept'), (1, 'Feasibility under way'), (2, 'Feasibility complete'), (3, 'Ready to build, or operating and expanding')], ''),
    ('plan', 'Do you have a business plan and financial model?', [(0, 'Not yet'), (1, 'A draft plan, no model'), (2, 'A plan and a basic model'), (3, 'A full plan and a detailed financial model')], ''),
    ('revenue', 'How certain is the project’s income?', [(0, 'No customers yet'), (1, 'Letters of intent or early customers'), (2, 'Signed contracts for part of the income'), (3, 'Long-term contracts for most of the income')], 'For example offtake agreements, leases or customer contracts.'),
    ('equity', 'How much of the project cost will you contribute?', [(0, 'None'), (1, 'Less than 10%'), (2, '10% to 25%'), (3, 'More than 25%')], 'Your own equity, in cash or assets.'),
    ('team', 'What is your team’s track record?', [(0, 'This is our first project'), (1, 'Some related experience'), (2, 'We have delivered a similar project'), (3, 'We have delivered several similar projects')], ''),
    ('technical', 'How far is the technical work?', [(0, 'Not started'), (1, 'Desktop study only'), (2, 'Independent feasibility or engineering study'), (3, 'Final design with supplier or contractor quotes')], ''),
    ('permits', 'Are land, permits and licences in place?', [(0, 'Not started'), (1, 'Applications in progress'), (2, 'Mostly secured'), (3, 'All secured, or none required')], ''),
    ('financials', 'What financial records does the company have?', [(0, 'New company, no statements yet'), (1, 'Management accounts'), (2, '1 to 2 years of audited statements'), (3, '3 or more years of audited statements')], ''),
    ('risk', 'Have you assessed the project’s risks?', [(0, 'Not yet'), (1, 'Informally'), (2, 'A written risk register'), (3, 'A risk register and an environmental and social assessment')], ''),
    ('ask', 'How clear is your funding requirement?', [(0, 'Not sure yet'), (1, 'A rough estimate'), (2, 'A detailed budget'), (3, 'A detailed budget and a preferred debt and equity mix')], ''),
]


# Telecoms Readiness Assessment questions (score 0 to 3), for New Generation Capital to refine.
TELECOMS_QUESTIONS = [
    ('tc_design', 'How firm are the network design and build cost?', [(0, 'Concept only'), (1, 'High-level design'), (2, 'Detailed design with estimates'), (3, 'Detailed design with contractor quotes')], ''),
    ('tc_vendor', 'Have equipment vendors and supply been secured?', [(0, 'Not yet'), (1, 'Shortlisted'), (2, 'Selected, terms under negotiation'), (3, 'Contracted, with lead times confirmed')], 'For example fibre, active equipment, towers, power and cooling.'),
    ('tc_rollout', 'Is there a phased rollout plan with milestones?', [(0, 'No'), (1, 'A draft plan'), (2, 'A phased plan'), (3, 'A phased plan tied to funding drawdowns')], ''),
    ('tc_rights', 'Are site access, wayleaves and rights of way secured?', [(0, 'Not started'), (1, 'Applications submitted'), (2, 'Secured for part of the rollout'), (3, 'Secured for the full rollout')], ''),
    ('tc_licence', 'Does the project hold the ICASA licences it needs?', [(0, 'Not yet'), (1, 'Applied for'), (2, 'Through a licensed partner'), (3, 'Held directly')], ''),
    ('tc_approvals', 'Are municipal, environmental and building approvals in place?', [(0, 'Not started'), (1, 'Applications in progress'), (2, 'Mostly approved'), (3, 'All approved, or none required')], 'For example trenching permits and tower site approvals.'),
    ('tc_demand', 'How proven is demand on the planned route or sites?', [(0, 'Not assessed'), (1, 'Desktop study'), (2, 'Surveys or pre-registrations'), (3, 'Signed take-up or customer orders')], ''),
    ('tc_anchor', 'Are there anchor tenants or wholesale agreements?', [(0, 'None yet'), (1, 'In discussion'), (2, 'Letters of intent'), (3, 'Signed agreements')], 'For example ISPs, mobile operators, municipalities or enterprise clients.'),
    ('tc_team', 'What is your team’s network build track record?', [(0, 'This is our first network'), (1, 'Some related experience'), (2, 'We have built a similar network'), (3, 'We have built several similar networks')], ''),
    ('tc_ops', 'How will the network be operated and maintained?', [(0, 'Not decided'), (1, 'Outline plan'), (2, 'Operating model defined'), (3, 'Operator or NOC and maintenance contracts in place')], ''),
]


def assessment(key, num, title, intro, points, questions, alt=False):
    qs = '\n'.join(tool_q(i, n, q, o, h) for i, (n, q, o, h) in enumerate(questions, 1))
    pts = '\n'.join(f'          <li>{p}</li>' for p in points)
    return f"""
  <section class="section tool{' tool--alt' if alt else ''}" id="{key}" data-assessment="{key}">
    <div class="wrap tool-grid">
      <div class="tool-intro reveal">
        <p class="label">Tool {num:02d}</p>
        <h2 class="display">{title}</h2>
        <p>{intro}</p>
        <ul class="tool-points">
{pts}
        </ul>
      </div>

      <div class="tool-panel reveal">
        <form class="readiness" data-role="form" novalidate>
          <div class="readiness-progress" aria-hidden="true"><span data-role="bar"></span></div>
          <p class="readiness-count" data-role="count" aria-live="polite">Question 1 of {len(questions)}</p>
{qs}
          <div class="readiness-nav">
            <button class="btn btn--quiet" type="button" data-role="back">Back</button>
            <button class="btn" type="button" data-role="next" disabled><span>Next</span>{ARROW}</button>
          </div>
        </form>

        <div class="result" data-role="result" hidden tabindex="-1">
          <div class="result-head">
            <div class="score-ring" aria-hidden="true">
              <svg viewBox="0 0 120 120"><circle class="score-ring__track" cx="60" cy="60" r="52"/><circle class="score-ring__value" data-role="arc" cx="60" cy="60" r="52"/></svg>
              <span class="score-ring__num" data-role="num">0</span>
            </div>
            <div>
              <p class="result-band" data-role="band"></p>
              <p class="result-summary" data-role="summary"></p>
            </div>
          </div>
          <div class="result-areas" data-role="areas"></div>
          <div class="result-gaps">
            <h3>What to work on</h3>
            <ul data-role="gaps"></ul>
          </div>
          <div class="result-actions">
            <button class="btn" type="button" data-report="{key}"><span>Get the PDF report</span>{ARROW}</button>
            <a class="btn btn--outline" href="partner.html#submit"><span>Submit your project</span>{ARROW}</a>
            <button class="btn btn--quiet" type="button" data-role="restart">Start again</button>
          </div>
        </div>
      </div>
    </div>
  </section>
"""


def funding_tools():
    return (head('Funding tools | New Generation Capital',
                 'Free project finance tools: a Funding Readiness Assessment, a Telecoms Readiness Assessment and a Repayment and DSCR Calculator, each with an instant result and a PDF report.')
            + header('funding-tools.html') + '\n<main id="main">\n'
            + page_hero('Funding tools', 'Know where your project stands before you pitch it.',
                        'Three free tools with instant results. Download a detailed PDF report to share with your team, or send your project to us for review.',
                        'backdrop-funding-tools')
            + f"""
  <nav class="tool-switch wrap" aria-label="Funding tools">
    <a href="#readiness" class="tool-switch__link"><span>01</span> Funding Readiness Assessment</a>
    <a href="#telecoms" class="tool-switch__link"><span>02</span> Telecoms Readiness Assessment</a>
    <a href="#dscr" class="tool-switch__link"><span>03</span> Repayment &amp; DSCR Calculator</a>
  </nav>
"""
            + assessment('readiness', 1, 'Funding Readiness Assessment',
                         'Answer ten short questions about your project. You will get a readiness score, a breakdown by area and a list of what to prepare before funders will engage.',
                         ['About 3 minutes', 'No sign-up needed to see your score', 'Optional PDF report to share'],
                         QUESTIONS)
            + assessment('telecoms', 2, 'Telecoms Readiness Assessment',
                         'For fibre, tower, wireless and data centre projects. Ten questions on the things funders check in a network build: design and build cost, rights and licences, demand and operations.',
                         ['About 3 minutes', 'Built from our directors’ network delivery experience', 'Optional PDF report to share'],
                         TELECOMS_QUESTIONS, alt=True)
            + f"""
  <section class="section tool" id="dscr">
    <div class="wrap tool-grid">
      <div class="tool-intro reveal">
        <p class="label">Tool 03</p>
        <h2 class="display">Repayment &amp; DSCR Calculator</h2>
        <p>Estimate loan repayments and your debt service coverage ratio (DSCR): how many times the project’s income covers its loan repayments. Lenders use it to size the debt they will offer.</p>
        <ul class="tool-points">
          <li>Results update as you type</li>
          <li>Year-by-year repayment schedule</li>
          <li>Optional PDF report to share</li>
        </ul>
      </div>

      <div class="tool-panel reveal">
        <form class="calc" id="dscrForm" novalidate>
          <div class="calc-grid">
            <div class="calc-field">
              <label for="c-cost">Total project cost</label>
              <div class="calc-input calc-input--prefix"><span>R</span><input id="c-cost" name="cost" inputmode="decimal" data-money value="50 000 000"></div>
            </div>
            <div class="calc-field">
              <label for="c-debt">Portion funded by debt</label>
              <div class="calc-input calc-input--suffix"><input id="c-debt" name="debt" inputmode="decimal" value="70"><span>%</span></div>
            </div>
            <div class="calc-field">
              <label for="c-rate">Interest rate</label>
              <div class="calc-input calc-input--suffix"><input id="c-rate" name="rate" inputmode="decimal" value="12.5"><span>% a year</span></div>
            </div>
            <div class="calc-field">
              <label for="c-term">Loan term</label>
              <div class="calc-input calc-input--suffix"><input id="c-term" name="term" inputmode="numeric" value="10"><span>years</span></div>
            </div>
            <div class="calc-field">
              <label for="c-rev">Expected annual income</label>
              <div class="calc-input calc-input--prefix"><span>R</span><input id="c-rev" name="revenue" inputmode="decimal" data-money value="18 000 000"></div>
            </div>
            <div class="calc-field">
              <label for="c-opex">Annual operating costs</label>
              <div class="calc-input calc-input--prefix"><span>R</span><input id="c-opex" name="opex" inputmode="decimal" data-money value="8 500 000"></div>
            </div>
            <div class="calc-field">
              <label for="c-growth">Income growth</label>
              <div class="calc-input calc-input--suffix"><input id="c-growth" name="growth" inputmode="decimal" value="5"><span>% a year</span></div>
            </div>
            <div class="calc-field">
              <label for="c-grace">Grace period</label>
              <div class="calc-input calc-input--suffix"><input id="c-grace" name="grace" inputmode="numeric" value="0"><span>months</span></div>
            </div>
            <div class="calc-field calc-field--wide">
              <span class="calc-label" id="c-profile-label">Repayment profile</span>
              <div class="profile-pick" role="radiogroup" aria-labelledby="c-profile-label">
                <label><input type="radio" name="profile" value="level" checked><span>Level repayments</span></label>
                <label><input type="radio" name="profile" value="growing"><span>Increase with income</span></label>
              </div>
              <p class="calc-hint">Network builds take time to reach full revenue. Repayments that rise with income, after an interest-only grace period, match that ramp-up.</p>
            </div>
          </div>
          <p class="form-error" id="dscrError" role="alert" hidden></p>
        </form>

        <div class="calc-results" id="dscrResults" aria-live="polite">
          <div class="dscr-gauge">
            <div class="dscr-gauge__head">
              <span>Year 1 DSCR</span>
              <strong id="r-dscr">0.00×</strong>
            </div>
            <div class="dscr-gauge__track" aria-hidden="true">
              <span class="dscr-gauge__zone dscr-gauge__zone--low"></span>
              <span class="dscr-gauge__zone dscr-gauge__zone--tight"></span>
              <span class="dscr-gauge__zone dscr-gauge__zone--ok"></span>
              <span class="dscr-gauge__zone dscr-gauge__zone--good"></span>
              <span class="dscr-gauge__marker" id="r-marker"></span>
            </div>
            <div class="dscr-gauge__scale" aria-hidden="true"><span>0.5×</span><span>1.0×</span><span>1.2×</span><span>1.35×</span><span>2.0×+</span></div>
            <p class="dscr-verdict" id="r-verdict"></p>
            <p class="calc-note" id="r-note" hidden></p>
          </div>
          <dl class="calc-kpis">
            <div><dt>First monthly repayment</dt><dd id="r-monthly">R 0</dd></div>
            <div><dt>Loan amount</dt><dd id="r-loan">R 0</dd></div>
            <div><dt>Your equity</dt><dd id="r-equity">R 0</dd></div>
            <div><dt>Total interest</dt><dd id="r-interest">R 0</dd></div>
            <div><dt>Lowest DSCR over the term</dt><dd id="r-min">0.00×</dd></div>
            <div><dt>Debt supportable at 1.30× (level)</dt><dd id="r-max">R 0</dd></div>
          </dl>
          <details class="schedule">
            <summary>Show the year-by-year schedule</summary>
            <div class="schedule-scroll">
              <table>
                <thead><tr><th scope="col">Year</th><th scope="col">Opening balance</th><th scope="col">Interest</th><th scope="col">Capital repaid</th><th scope="col">Closing balance</th><th scope="col">DSCR</th></tr></thead>
                <tbody id="r-schedule"></tbody>
              </table>
            </div>
          </details>
          <div class="result-actions">
            <button class="btn" type="button" data-report="dscr"><span>Get the PDF report</span>{ARROW}</button>
            <a class="btn btn--outline" href="partner.html#submit"><span>Submit your project</span>{ARROW}</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="disclaimer">
    <div class="wrap">
      <p><strong>Indicative only.</strong> These tools give general estimates based on the information you enter. They do not constitute financial advice or an offer of finance. Lenders apply their own criteria, rates and terms.</p>
    </div>
  </section>

  <dialog class="report-dialog" id="reportDialog" aria-labelledby="reportTitle">
    <form class="form form--light" id="reportForm" method="dialog" novalidate>
      <button class="dialog-close" type="button" id="reportClose" aria-label="Close">×</button>
      <p class="label">Your PDF report</p>
      <h2 id="reportTitle">Where should we send your report?</h2>
      <p class="dialog-lede">Your report downloads straight away, and we will email you a copy. We ask for a phone number in case the email does not reach you.</p>
      <div class="field">
        <label for="rp-name">Full name</label>
        <input id="rp-name" name="name" autocomplete="name" required>
      </div>
      <div class="field">
        <label for="rp-email">Email</label>
        <input id="rp-email" name="email" type="email" autocomplete="email" required>
      </div>
      <div class="field">
        <label for="rp-phone">Phone</label>
        <input id="rp-phone" name="phone" type="tel" autocomplete="tel" required>
      </div>
      <div class="field">
        <label for="rp-company">Company</label>
        <input id="rp-company" name="company" autocomplete="organization">
      </div>
      <div class="hp" aria-hidden="true">
        <label for="rp-website">Leave this field empty</label>
        <input id="rp-website" name="website" tabindex="-1" autocomplete="off">
      </div>
      <label class="check">
        <input type="checkbox" name="consent" required>
        <span>I agree that New Generation Capital may contact me about my project. My details are handled in line with POPIA.</span>
      </label>
      <p class="form-error" id="reportError" role="alert" hidden></p>
      <button class="btn btn--block" type="submit"><span>Download my report</span>{ARROW}</button>
    </form>
  </dialog>
</main>
""" + footer(['assets/vendor/jspdf.umd.min.js', 'assets/js/leads.js', 'assets/js/tools.js']))


def partner():
    service_opts = '\n'.join(['              <option value="">Not sure yet</option>'] + [f'              <option value="{slug}">{title}</option>' for slug, title, _d, _t in SERVICES])
    industries = ['Energy &amp; power', 'Construction &amp; civil works', 'Infrastructure', 'Digital &amp; telecoms',
                  'Fintech &amp; financial services', 'Property &amp; real estate', 'Agriculture &amp; agro-processing',
                  'Manufacturing &amp; industry', 'Other']
    ind_opts = '\n'.join(f'              <option>{i}</option>' for i in industries)
    return (head('Partner with us | New Generation Capital',
                 'Submit a project for funding or partner with New Generation Capital as a capital provider. Secure project submission with document upload.')
            + header('partner.html') + '\n<main id="main">\n'
            + page_hero('Partner with us', 'Two sides of one deal. We work for both.',
                        'Project sponsors get a clear path to funding. Capital providers get pre-screened, monitored deals. Tell us which side you are on.',
                        'backdrop-partner')
            + f"""
  <section class="section audiences">
    <div class="wrap audience-grid">
      <article class="audience reveal" id="sponsors">
        <div class="audience__media wipe"><img {pic('audience-sponsors', '(max-width: 900px) 100vw, 50vw')} alt="" loading="lazy" decoding="async"></div>
        <p class="label">For project sponsors</p>
        <h2 class="display">Get your project funder-ready.</h2>
        <ul class="audience-list">
          <li><h3>An honest first screen</h3><p>We tell you early whether a project is fundable, and what it needs if it is not there yet.</p></li>
          <li><h3>A funder-ready package</h3><p>We test feasibility, build the investment case and structure the right mix of debt and equity.</p></li>
          <li><h3>Access to capital</h3><p>We present your project to capital providers who fund your type of deal.</p></li>
          <li><h3>Support through delivery</h3><p>We stay involved through construction and operation, so milestones and drawdowns stay on track.</p></li>
        </ul>
        <a class="btn" href="#submit"><span>Submit your project</span>{ARROW}</a>
      </article>
      <article class="audience audience--dark reveal" id="funders">
        <div class="audience__media wipe"><img {pic('audience-funders', '(max-width: 900px) 100vw, 50vw')} alt="" loading="lazy" decoding="async"></div>
        <p class="label label--light">For capital providers</p>
        <h2 class="display display--light">Grow your book without growing your risk.</h2>
        <ul class="audience-list">
          <li><h3>Pre-screened deal flow</h3><p>Only commercially viable, deliverable projects reach you, de-risked before capital is committed.</p></li>
          <li><h3>Technical due diligence</h3><p>We check build costs against the design and quotes, and verify progress on site before each drawdown is released.</p></li>
          <li><h3>Lower post-funding risk</h3><p>Active project management and milestone oversight reduce default and completion risk.</p></li>
          <li><h3>Extended reach, no fixed cost</h3><p>Added origination capacity and a managed pipeline without additional overhead.</p></li>
          <li><h3>Protected returns</h3><p>Early warning on delivery risk protects interest income and capital.</p></li>
        </ul>
        <a class="btn btn--ghost" href="#submit" data-role-pick="funder"><span>Start a conversation</span>{ARROW}</a>
      </article>
    </div>
  </section>

  <section class="section engage">
    <div class="wrap">
      <div class="section-head reveal">
        <p class="label">Working together</p>
        <h2 class="display">Three steps to a repeatable, de&#8209;risked pipeline.</h2>
      </div>
      <ol class="steps steps--row stagger">
        <li><h3>Align</h3><p>Confirm shared priorities and put an NDA and a simple MOU or fee agreement in place.</p></li>
        <li><h3>Pilot</h3><p>Select one or two near-term opportunities to run through the full process together.</p></li>
        <li><h3>Scale</h3><p>Agree a reporting cadence and grow the pipeline as delivery confidence builds.</p></li>
      </ol>
    </div>
  </section>

{photo_break('break-partner')}
  <section class="section contact" id="submit">
    <div class="wrap contact-grid">
      <div class="reveal">
        <p class="label">Submit a project</p>
        <h2 class="display">Tell us about your project.</h2>
        <p class="contact-lede">Share the basics and any documents you have, such as a business plan, financial model or feasibility study. Our team reviews every submission and replies {response_time()}.</p>
        <p class="contact-lede">Not sure you are ready? <a class="text-link" href="funding-tools.html#readiness">Take the Funding Readiness Assessment</a> first.</p>
        <dl class="contact-details contact-details--light">
          <div><dt>Email</dt><dd><a href="mailto:funding@newgenerationcap.co.za">funding@newgenerationcap.co.za</a></dd></div>
          <div><dt>Telephone</dt><dd><a href="tel:+27877420831">+27 87 742 0831</a></dd></div>
          <div><dt>Office</dt><dd>Imagine House, 2 Mellis Road, Rivonia, Sandton, 2191</dd></div>
          <div><dt>Postal</dt><dd>PO Box 3895, Rivonia, 2128</dd></div>
        </dl>
      </div>

      <div class="contact-card reveal">
        <form class="form" id="submitForm" novalidate>
          <fieldset class="role-pick">
            <legend>I am a</legend>
            <label><input type="radio" name="role" value="Project sponsor" checked><span>Project sponsor</span></label>
            <label><input type="radio" name="role" value="Capital provider"><span>Capital provider</span></label>
            <label><input type="radio" name="role" value="Other"><span>Other</span></label>
          </fieldset>
          <div class="form-row">
            <div class="field">
              <label for="s-name">Full name</label>
              <input id="s-name" name="name" autocomplete="name" required>
            </div>
            <div class="field">
              <label for="s-company">Company</label>
              <input id="s-company" name="company" autocomplete="organization" required>
            </div>
          </div>
          <div class="form-row">
            <div class="field">
              <label for="s-email">Email</label>
              <input id="s-email" name="email" type="email" autocomplete="email" required>
            </div>
            <div class="field">
              <label for="s-phone">Phone</label>
              <input id="s-phone" name="phone" type="tel" autocomplete="tel" required>
            </div>
          </div>
          <div class="form-row" data-sponsor-only>
            <div class="field">
              <label for="s-industry">Industry</label>
              <select id="s-industry" name="industry">
{ind_opts}
              </select>
            </div>
            <div class="field">
              <label for="s-amount">Funding required (R)</label>
              <input id="s-amount" name="amount" inputmode="decimal" placeholder="e.g. 25 000 000">
            </div>
          </div>
          <div class="field" id="subsectorField" hidden>
            <label for="s-subsector">Digital &amp; telecoms sub-sector</label>
            <select id="s-subsector" name="subsector">
              <option>Fibre to the home or business</option>
              <option>Metro and long-haul fibre</option>
              <option>Towers and wireless</option>
              <option>Edge and micro data centres</option>
              <option>Energy for digital sites</option>
              <option>Security and surveillance</option>
              <option>Supporting value chains</option>
              <option>Other</option>
            </select>
          </div>
          <div class="field" data-sponsor-only>
            <label for="s-stage">Project stage</label>
            <select id="s-stage" name="stage">
              <option>Idea or concept</option>
              <option>Feasibility under way</option>
              <option>Feasibility complete</option>
              <option>Ready to build</option>
              <option>Operating and expanding</option>
            </select>
          </div>
          <div class="field">
            <label for="s-service">Service of interest</label>
            <select id="s-service" name="service">
{service_opts}
            </select>
          </div>
          <div class="field">
            <label for="s-msg" id="s-msg-label">Tell us about the project</label>
            <textarea id="s-msg" name="message" rows="4" required></textarea>
          </div>
          <div class="upload" id="upload">
            <input type="file" id="s-files" name="documents" multiple accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.csv">
            <label for="s-files" class="upload-zone">
              <strong>Add documents</strong>
              <span>Drag files here or browse. PDF, Word, Excel or PowerPoint, up to 10 MB each, 5 files.</span>
            </label>
            <ul class="upload-list" id="uploadList"></ul>
          </div>
          <div class="hp" aria-hidden="true">
                <label for="s-website">Leave this field empty</label>
                <input id="s-website" name="website" tabindex="-1" autocomplete="off">
          </div>
          <label class="check">
            <input type="checkbox" name="consent" required>
            <span>I agree that New Generation Capital may use these details and documents to assess my enquiry, in line with POPIA. We treat everything you share as confidential.</span>
          </label>
          <p class="form-error" id="submitError" role="alert" hidden></p>
          <button class="btn btn--block" type="submit"><span>Submit</span>{ARROW}</button>
        </form>
        <div class="form-done" id="submitDone" hidden tabindex="-1" data-sent="Our team will review your submission and reply {response_time() if 'tbc' not in response_time() else 'with next steps'}.">
          <h3>Thank you, we have your details.</h3>
          <p id="submitDoneText">Our team will review your submission and reply {response_time()}.</p>
        </div>
      </div>
    </div>
  </section>
</main>
""" + footer(['assets/js/leads.js', 'assets/js/partner.js']))



def services_preview():
    items = '\n'.join(
        f"""        <li><a href="services.html#{slug}"><span class="services-list__tag">{tag}</span><h3>{title}</h3></a></li>"""
        for slug, title, _desc, tag in SERVICES)
    return '      <ul class="services-list services-list--links stagger">\n' + items + '\n      </ul>'


def services():
    rows = '\n'.join(f"""      <article class="service-block{' service-block--flip' if i % 2 else ''}" id="{slug}">
        <div class="service-block__media wipe" data-parallax="40"><img {pic('service-' + slug, '(max-width: 900px) 100vw, 50vw')} alt="" loading="lazy" decoding="async"></div>
        <div class="service-block__text reveal">
          <p class="service-block__tag">{tag}</p>
          <h2 class="service-block__title">{title}</h2>
          <p>{desc}</p>
          <dl class="deal-size">
            <div><dt>Minimum deal size</dt><dd>{tbc(DEAL_SIZES[slug][0])}</dd></div>
            <div><dt>Maximum deal size</dt><dd>{tbc(DEAL_SIZES[slug][1])}</dd></div>
          </dl>
          <a class="text-link" href="partner.html?service={slug}#submit">Enquire about {title} {ARROW}</a>
        </div>
      </article>""" for i, (slug, title, desc, tag) in enumerate(SERVICES))
    return (head('Services | New Generation Capital',
                 'Project fundraising, bridging finance, acquisitions and mergers, and greenfield project fundraising from New Generation Capital.')
            + header('services.html') + '\n<main id="main">\n'
            + page_hero('Services', 'Capital for every stage of a project.',
                        'From raising the capital to bridging timing gaps and completing a transaction: one partner across the funding lifecycle.',
                        'backdrop-services')
            + f"""
  <section class="section service-index">
    <nav class="wrap service-jump" aria-label="Services on this page">
{chr(10).join(f'      <a href="#{slug}">{title}</a>' for slug, title, _d, _t in SERVICES)}
    </nav>
    <div class="wrap service-blocks">
{rows}
    </div>
  </section>
{photo_break('break-services', 'One partner across the funding lifecycle.')}{cta_band('services')}
</main>
""" + footer())



DIGITAL_AREAS = [
    ('a', 'Connectivity &amp; fibre', 'Fibre-to-the-home and business, metro and long-haul fibre, towers and fixed wireless: the networks every digital service runs on.'),
    ('a', 'Edge &amp; micro data centres', 'Feasibility, site selection, power integration and financing for low-latency infrastructure supporting 5G, AI, IoT and enterprise.'),
    ('a', 'Energy for digital sites', 'Renewable, hybrid and micro-grid power for data centres, towers and edge sites. Critical to uptime, bankability and ESG performance.'),
    ('b', 'Security &amp; surveillance', 'Physical security, smart surveillance and critical infrastructure protection, increasingly enhanced by digital and AI capabilities.'),
    ('b', 'Supporting value chains', 'Logistics, civil works and the ancillary assets needed to build and run telecommunications and digital infrastructure.'),
]


def digital_telecoms():
    areas = '\n'.join(f"""          <li class="focus-item" data-view="{v}">
            <h3>{t}</h3>
            <p>{d}</p>
          </li>""" for v, t, d in DIGITAL_AREAS)
    return (head('Digital &amp; Telecoms | New Generation Capital',
                 'Project finance for digital and telecoms infrastructure in South Africa: fibre and connectivity, edge and micro data centres, energy for digital sites, security and supporting value chains.')
            + header('digital-telecoms.html') + '\n<main id="main">\n'
            + page_hero('Digital &amp; Telecoms', 'Financing the networks behind South Africa’s digital economy.',
                        'Fibre, data centres, towers and the power and security around them. Our directors have built and run these networks, and we structure the capital to build the next ones.',
                        'backdrop-digital')
            + f"""
  <section class="section market">
    <div class="wrap market-grid">
      <div class="market-figure reveal">
        <p class="label">The opportunity</p>
        <p class="figure">R<span data-count="140">140</span><span class="figure-unit">bn+</span></p>
        <p class="figure-caption">Between R140 billion and more than R200 billion is needed by 2035 for high-speed broadband and digital connectivity in South Africa.</p>
        <p class="source">Source: DBSA Digital Infrastructure Investment Study, 2025</p>
      </div>
      <div class="market-copy reveal">
        <p class="pull">The gap is not appetite for capital. It is a pipeline of technically viable, fundable projects.</p>
        <p>That pipeline is what we build: disciplined packaging of digital infrastructure projects, from first screening to a funder-ready deal.</p>
      </div>
    </div>
  </section>

  <section class="section focus" id="focus">
    <div class="wrap">
      <div class="section-head reveal">
        <p class="label">What we finance</p>
        <h2 class="display">Five areas that make digital infrastructure resilient.</h2>
      </div>
      <div class="focus-grid">
        <div class="focus-media reveal wipe" data-view="a">
          <img class="focus-media__a" {pic('digital-a', '(max-width: 900px) 100vw, 50vw')} alt="Aerial view of a data centre campus with substation and solar array" loading="lazy" decoding="async">
          <img class="focus-media__b" {pic('digital-b', '(max-width: 900px) 60vw, 30vw')} alt="Secured telecoms site with mast and surveillance cameras at dusk" loading="lazy" decoding="async">
        </div>
        <ul class="focus-list stagger">
{areas}
        </ul>
      </div>
    </div>
  </section>
{photo_break('break-digital', 'Infrastructure realism, not modelling in isolation.')}
  <section class="section approach">
    <div class="wrap approach-grid">
      <div class="approach-statement reveal">
        <p class="label">Why New Generation Capital</p>
        <h2 class="display">We have deployed and operated these networks. <span>Our diligence starts on the ground.</span></h2>
      </div>
      <div class="approach-body reveal">
        <p>Our directors bring decades in South African and African telecoms, and the New Generation Group operates in connectivity through CircleTel. That experience shapes how we screen, structure and monitor every digital project.</p>
        <ul class="pillars stagger">
          <li><h3>R1.2bn broadband build</h3><p>Our COO led the City of Johannesburg broadband project. <a class="text-link" href="case-study-joburg-broadband.html">Read the case study</a></p></li>
          <li><h3>Operator experience</h3><p>Vodacom (FTTX), MTN, Ericsson, Airtel Nigeria and Ceragon among our directors’ former roles.</p></li>
          <li><h3>Early risk visibility</h3><p>Deployment issues surface before they undermine the investment case.</p></li>
          <li><h3>Funder alignment</h3><p>Evidence is packaged the way capital providers decide, and monitored after funding.</p></li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section process" id="process">
    <div class="wrap">
      <div class="section-head section-head--split reveal">
        <div>
          <p class="label">How we work</p>
          <h2 class="display">From site to financial close, and beyond.</h2>
        </div>
        <p class="section-head__aside">Every digital project runs through the same seven steps. Only credible, viable and deliverable deals pass our decision gate.</p>
      </div>
{stages_list()}
      <p class="section-link reveal"><a class="text-link" href="funding-tools.html#telecoms">Take the Telecoms Readiness Assessment {ARROW}</a></p>
    </div>
  </section>
{cta_band('digital')}
</main>
""" + footer())



# R1.2bn City of Johannesburg broadband case study. Facts confirmed so far are filled in;
# None shows "To be confirmed" until New Generation Capital supplies the detail.
CASE = {
    'value': 'R1.2 billion',
    'client': 'City of Johannesburg',
    'led_by': 'Jeffrey de Wee, now COO of the New Generation Group and a director of New Generation Capital',
    'sector': 'Digital &amp; telecoms: municipal broadband',
    'period': None,          # e.g. '2010 to 2014'
    'network': None,         # e.g. 'about 900 km of fibre'
    'challenge': None,       # paragraph: what the City needed and why
    'delivered': None,       # paragraph: what was built and how
    'results': None,         # list of outcomes, e.g. ['x sites connected', 'y km of fibre']
}


def case_study():
    def fact(label, value):
        return f'          <div><dt>{label}</dt><dd>{tbc(value)}</dd></div>'
    facts = '\n'.join([
        fact('Project value', CASE['value']),
        fact('Client', CASE['client']),
        fact('Sector', CASE['sector']),
        fact('Period', CASE['period']),
        fact('Network', CASE['network']),
    ])
    results = CASE['results']
    results_html = ('\n'.join(f'          <li>{r}</li>' for r in results) if results
                    else '          <li><span class="tbc">To be confirmed</span></li>')
    return (head('Case study: City of Johannesburg broadband | New Generation Capital',
                 'Case study: the R1.2 billion City of Johannesburg broadband project, led by Jeffrey de Wee, director of New Generation Capital.')
            + header('case-study-joburg-broadband.html') + '\n<main id="main">\n'
            + page_hero('Case study &nbsp;·&nbsp; Digital &amp; Telecoms', 'R1.2bn City of Johannesburg broadband project.',
                        'A city-wide broadband build led by Jeffrey de Wee, now our COO. The experience behind how we assess, structure and monitor digital infrastructure today.',
                        'backdrop-case')
            + f"""
  <section class="section case-facts">
    <div class="wrap">
      <dl class="facts-grid reveal">
{facts}
      </dl>
    </div>
  </section>

  <section class="section case-body">
    <div class="wrap case-grid">
      <aside class="case-aside reveal">
        <p class="label">Led by</p>
        <p class="case-aside__lead">{CASE['led_by']}.</p>
        <a class="text-link" href="about.html#board">Meet the board {ARROW}</a>
      </aside>
      <div class="case-sections">
        <article class="case-section reveal">
          <h2>The challenge</h2>
          <p>{tbc(CASE['challenge'])}</p>
        </article>
        <article class="case-section reveal">
          <h2>What was delivered</h2>
          <p>{tbc(CASE['delivered'])}</p>
        </article>
        <article class="case-section reveal">
          <h2>Results</h2>
          <ul class="case-results">
{results_html}
          </ul>
        </article>
        <article class="case-section reveal">
          <h2>What it means for our clients</h2>
          <p>Delivering a network at this scale shows what it takes to build digital infrastructure in South Africa: wayleaves, phased rollouts, contractor management and the gap between planned and actual build costs. We bring that experience to every project we assess. For capital providers, it means build costs checked against the design and quotes, and progress verified on site before each drawdown.</p>
        </article>
      </div>
    </div>
  </section>
{photo_break('break-case', 'Built on delivery, not modelling in isolation.')}
  <section class="section case-next">
    <div class="wrap case-next__inner reveal">
      <h2 class="display">Planning a digital infrastructure project?</h2>
      <div class="case-next__actions">
        <a class="btn" href="partner.html#submit"><span>Submit your project</span>{ARROW}</a>
        <a class="btn btn--outline" href="digital-telecoms.html"><span>Digital &amp; Telecoms</span>{ARROW}</a>
      </div>
    </div>
  </section>
{cta_band('case')}
</main>
""" + footer())


PAGES = {
    'index.html': home,
    'about.html': about,
    'what-we-do.html': what_we_do,
    'services.html': services,
    'digital-telecoms.html': digital_telecoms,
    'case-study-joburg-broadband.html': case_study,
    'funding-tools.html': funding_tools,
    'partner.html': partner,
}

for name, fn in PAGES.items():
    with open(f'{OUT}/{name}', 'w') as f:
        f.write(fn())
    print('wrote', name)
