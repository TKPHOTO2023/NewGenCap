# HostDigital website

Corporate site for HostDigital, the full name behind hostdigi. It is a static five-page site with no build
step. Open `index.html` directly, or serve the folder:

```
cd hostdigital && python3 -m http.server 8000
```

## Pages

| File | Page | Content |
|---|---|---|
| `index.html` | Home | Hero, the image "window" that opens to full width on scroll, the scroll-filled manifesto, the HostDigital stack (pinned 3D layers), services, tools, process, call to action |
| `about.html` | About us | Why one house, team photos, three principles, the six teams, image break |
| `services.html` | Services | Digital marketing, media buying, multimedia, AI automation and agents, sales, websites, web hosting and domains. A sticky index follows the reader; each "Discuss" link pre-selects that service on the contact form (`contact.html?interest=<id>`) |
| `tools.html` | Tools | Tenderiza (AI tendering), InstantDM (AI lead generation on social media) and hostdigi.co.za (web hosting and AI websites), each with a live HTML product mock |
| `contact.html` | Contact us | Interest chips, enquiry form with validation and a spam trap, contact details |

The header and footer are repeated in every page; change them in all five files.

## Design system

All colours and type are tokens at the top of `assets/css/site.css`.

- **Brand gradient:** `--g-a` cobalt `#2d5bff`, `--g-b` iris `#8a4dff`, `--g-c` lagoon `#00c6e0`. Replace these three
  values with the official hostdigi brand colours and the whole site follows. The logo mark, favicon and the icons
  on the About page hold the same three colours as SVG stops, so update those too (search for `2d5bff`).
- **Type (Google Fonts):** Schibsted Grotesk for headlines, Newsreader italic for accent words, Geist for body text
  and Geist Mono for labels.
- **Signature:** the HostDigital stack on the home page. Six glass layers (hosting at the base, sales at the top) pull
  apart as you scroll and light up one at a time.

## Motion

`assets/js/site.js` handles everything. It has no dependencies.

- Header turns frosted after scrolling and switches to a dark style over dark sections.
- Headline line reveals on load, fade-up reveals on scroll, parallax image breaks (`data-parallax="<px>"`).
- Home: window clip-path expansion, word-by-word manifesto fill, and the pinned stack.
- Everything falls back to static layouts with `prefers-reduced-motion`, and the stack becomes a plain list on phones.

## Contact form

The form opens the visitor's email app with the enquiry filled in, addressed to `data-to` on the `<form>`
(currently `hello@hostdigital.co.za`). To receive enquiries server-side instead, post the form to an endpoint
such as the `api/lead.php` used by the New Generation Capital site in this repository.

## Images

Photos are in `assets/img` as WebP at 900 and 1800 px wide and are served with `srcset`. They are stock images from
this repository's media library, so swap in HostDigital's own studio work when it's available.

## To confirm before go-live

- Official hostdigi brand colours and logo (the current mark is a placeholder in the same spirit: three stacked layers).
- Contact email address, phone number and physical address.
- Product URLs for Tenderiza and InstantDM. The buttons currently lead to the contact form with that product
  pre-selected.
- Product feature copy on the Tools page, to be checked against what each product does today.
- Analytics (GA4) and Search Console.
