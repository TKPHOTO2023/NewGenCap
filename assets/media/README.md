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
| `liquid-metal` | `elegant-black-ferromagnetic-liquid-metal-with-copy-space.jpg` |
| `tech-tunnel` | `futuristic-time-machine.jpg` |
| `optical-fiber` | `optical-fiber-background.jpg` |
| `meeting-devices` | `people-using-digital-device-while-meeting.jpg` |
| `office-workers` | `people-working-their-office.jpg` |
| `futuristic-office` | `person-working-futuristic-office.jpg` |
| `analytics-meeting` | `tablet-shows-analytics-data-meeting.jpg` |
| `team-discussion` | `team-diverse-coworkers-modern-office-discuss-their-project-together.jpg` |
| `team-review`, `data-campus`, `secured-site` | company profile images in `assets/img/` |

Not used: `unsuitable-furious-woman-gets-angry-after-getting-rejected-from-job-offer.jpg`.

## Placement

No image appears twice on the same page. With 23 images for 29 spots, six images appear on two
different pages, always in secondary positions (never a slider slide or a page header).

| Slot | Where it appears | Image |
|---|---|---|
| `hero-1` … `hero-4` | Home slider | `brand-path`, `solar-aerial`, `futuristic-office`, `sandton-dusk` |
| `who-home`, `who-about` | "Who we are" photo on Home / About | `team-review`, `team-discussion` |
| `heritage-home`, `heritage-about` | "Built on the New Generation Group" backdrop (video-ready) | `sandton-day`, `solar-site` |
| `cta-home`, `cta-about`, `cta-what-we-do`, `cta-services` | Sponsor / funder band (video-ready) | `tech-tunnel`, `liquid-metal`, `city-night`, `optical-fiber` |
| `backdrop-about` | About header | `sponsor-model` |
| `backdrop-what-we-do` | What we do header | `analytics-meeting` |
| `backdrop-services` | Services header | `meeting-devices` |
| `backdrop-funding-tools` | Funding tools header | `office-workers` |
| `backdrop-partner` | Partner header | `office-colleagues` (shown mirrored so the couple sits right of the text) |
| `break-home` / `-about` / `-what-we-do` / `-services` / `-partner` | Parallax breaks | `data-campus`, `solar-wind`, `growth-capital`, `sandton-dusk`, `solar-wind` |
| `service-…` | Services: Project Fundraising, Bridging, M&A, Greenfield, Insurance | `team-meeting`, `growth-capital`, `office-analysis`, `solar-site`, `secured-site` |
| `audience-sponsors`, `audience-funders` | Partner audience cards | `solar-aerial`, `analytics-meeting` |

Still welcome: construction-site imagery, a fintech image, and backdrop videos (MP4) for the heritage
and sponsor / funder sections.
