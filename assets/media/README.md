# Media uploads

Upload original images and videos into this folder. The site never serves these originals: each
image is turned into web copies in `assets/img/site/<name>-<width>.jpg` (800, 1400, 1600 and
2200 px wide), and browsers download only the size they need (phones get the 800 px copy).

## Recommended formats

| Type | Format | Size |
|---|---|---|
| Header slider and break images | JPG | at least 2400 px wide |
| Video backdrops | MP4 (H.264), no sound, 10–20 s seamless loop | 1920 × 1080 (or 1280 × 720), under 8 MB each |
| Service and audience images | JPG | at least 1600 px wide |

Darker, uncluttered footage works best behind text; the site adds a navy overlay on top.
GitHub's web upload refuses files over 25 MB.

## Image names

| Name | Original upload |
|---|---|
| `brand-path` | `assets/img/hero-path.jpg` (company profile) |
| `solar-aerial` | `aerial-view-solar-power-plant.jpg` |
| `solar-site` | `solar-power-plant-field-aerial-view-solar-panels.jpg` |
| `solar-wind` | `solar-panels-field-wind-turbines-horizon-renewable-green-energy.jpg` |
| `team-meeting` | `colleagues-working-together-project.jpg` |
| `office-colleagues` | `couple-cheerful-business-colleagues-….jpg` |
| `office-analysis` | `couple-focused-business-colleagues-….jpg` |
| `sandton-dusk` | `sandton.jpg` |
| `sandton-day` | `sandton.png` |
| `sponsor-model` | `smiley-man-working-project.jpg` |
| `growth-capital` | `stacked-coins-with-dirt-plant.jpg` |
| `city-night` | `building-area-east-river-travel-city-landscape.jpg` |
| `data-campus`, `secured-site` | company profile images in `assets/img/` |

Not used: `unsuitable-furious-woman-gets-angry-after-getting-rejected-from-job-offer.jpg`.

## Slots

| Slot | Where it appears | Image | Video |
|---|---|---|---|
| `hero-1` | Home slider 1: "We turn ideas into investable projects." | `brand-path` | — |
| `hero-2` | Home slider 2: Energy & infrastructure | `solar-aerial` | — |
| `hero-3` | Home slider 3: Capital solutions | `team-meeting` | — |
| `hero-4` | Home slider 4: Every industry | `sandton-dusk` | — |
| `backdrop-heritage` | Home and About: "Built on the New Generation Group" | `solar-wind` | open — construction, energy, telecoms footage |
| `backdrop-cta` | Sponsor / funder band near the foot of most pages | `city-night` | open — slow aerial of a city |
| `backdrop-about` | About us header | `office-colleagues` | open — team at work |
| `backdrop-what-we-do` | What we do header | `solar-site` | open — projects being built |
| `backdrop-services` | Services header | `sandton-day` | — |
| `backdrop-funding-tools` | Funding tools header | `office-analysis` | — |
| `backdrop-partner` | Partner with us header | `sponsor-model` | — |
| `break-home` | Home, between Industries and How we work | `data-campus` | — |
| `break-about` | About, before the Board | `solar-site` | — |
| `break-what-we-do` | What we do, before the process | `growth-capital` | — |
| `break-services` | Services, after the services | `sandton-dusk` | — |
| `break-partner` | Partner, before the submission form | `solar-wind` | — |
| `service-project-fundraising` | Services: Project Fundraising | `team-meeting` | — |
| `service-bridging-finance` | Services: Bridging Finance | `growth-capital` | — |
| `service-acquisitions-mergers` | Services: Acquisitions & Mergers | `office-analysis` | — |
| `service-greenfield-fundraising` | Services: Greenfield Project Fundraising | `solar-aerial` | — |
| `service-short-term-insurance` | Services: Short-Term Insurance | `secured-site` | — |
| `audience-sponsors` | Partner: "For project sponsors" card | `solar-site` | — |
| `audience-funders` | Partner: "For capital providers" card | `team-meeting` | — |

Still welcome: construction-site imagery (the Group's construction heritage is not yet pictured), a
fintech image, and up to four backdrop videos for the slots marked "open".
