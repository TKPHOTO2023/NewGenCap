# New Generation Capital — landing page

Static, single-page site for New Generation Capital (part of the New Generation Group).
No build step: open `index.html` directly, or serve the folder:

```
python3 -m http.server 8000
```

- `index.html` — page content
- `assets/css/styles.css` — design tokens (brand navy `#05152A`, signal orange `#F5831F`) and layout
- `assets/js/main.js` — header state, mobile menu, scroll reveals, enquiry form (opens the visitor's email app) and the deal-flow visual in the Process section
- `assets/js/motion.js` — motion layer: opening curtain (first visit per session), hero word reveal and depth, count-ups, reading progress, active nav, ink-fill sentence, image wipes and parallax, focus-area photo swap, magnetic buttons, back-to-top. All of it respects `prefers-reduced-motion`.
- `assets/img/` — imagery and the NG mark, taken from the July 2026 company profile

Type: Newsreader (display) and Montserrat (brand text), loaded from Google Fonts.
