# As You Like It Painting Company: Website Rebuild

Static, multi-page site for As You Like It Painting Company (Jupiter, FL). Plain HTML, CSS, and JS. No framework, no build step needed to host. Ready for GitHub Pages or Netlify.

## Structure

```
site/               <- deploy this folder (it is the web root)
  index.html, services.html, residential-painting.html, about.html,
  gallery.html, reviews.html, financing.html, contact.html, 404.html,
  9 service pages, service-areas.html + 13 city pages,
  sitemap.xml, robots.txt
  css/styles.css    <- all styles + design tokens at the top
  js/main.js        <- all behavior; CONFIG constants at the top
  img/              <- favicon.svg, og-image.png, put project photos here
build/
  content.py        <- ALL copy, services, cities, business facts
  build.py          <- generates every HTML page from content.py
AUDIT.md            <- what was wrong with the old site and what changed
```

## Editing

Pages are generated. Do not hand-edit HTML that build.py produces. Change `build/content.py` (or templates in `build/build.py`) and run:

```bash
python3 build/build.py
```

CSS and JS in `site/` are hand-maintained and never overwritten.

## Config (js/main.js)

| Constant | Purpose |
|---|---|
| `FORM_ENDPOINT` | Where the estimate form POSTs JSON. Empty = demo mode (validates and shows success, sends nothing). Set to a Formspree/Getform URL before launch. |
| `PHONE_DISPLAY`, `PHONE_TEL`, `EMAIL` | Used in form success/error messages |
| `FINANCING_URL`, `GALLERY_URL`, `REVIEWS_URL` | External links |

Business facts in markup (phone, license numbers, links) come from `BIZ` in `build/content.py`.

## Functional features
- Estimate form: required-field validation on blur/submit, inline errors, honeypot spam trap, loading state, success/error message, `?service=<slug>` preselects a service (used by every service page CTA)
- Services dropdown (click, Escape to close, outside-click close)
- Mobile slide-in nav and sticky Call / Text / Estimate bar
- Gallery filter (Interior, Exterior, Cabinets, Faux, Commercial) with live count
- FAQ accordions (native details/summary) with FAQPage schema
- HousePainter LocalBusiness schema on home, canonical + OG tags on every page
- Scroll reveal that respects `prefers-reduced-motion`

## Before launch (open items)
1. **Photos.** Every `<!-- PHOTO SLOT -->` comment marks a placeholder. Drop images in `site/img/` and add `<img src="img/..." alt="...">` inside the `.photo-slot` div (the CSS already covers it). Gallery tiles in `content.py` > `GALLERY` have placeholder captions; replace with real projects.
2. **Reviews.** reviews.html has an `<!-- EDIT -->` slot for real, permitted customer reviews or a Google reviews widget. Do not invent testimonials.
3. **Form endpoint.** Set `FORM_ENDPOINT` in `js/main.js`.
4. **About timeline.** Confirm milestones with the owner (marked `<!-- EDIT -->`).
5. **City URLs.** New city pages use `painters-<city>-fl.html`. Match the old site's city filenames or add redirects so existing rankings carry over.
6. **Fonts.** Young Serif + Figtree load from Google Fonts.

## Deploy (GitHub Pages)
GitHub Pages only serves from the repo root or `/docs`. Either rename `site/` to `docs/` (and update `ROOT` in build.py), or use a Pages GitHub Action that publishes `site/`. On Netlify, set the publish directory to `site`.

## Logo
New mark: the Jupiter Lighthouse with a gold brushstroke beam over Intracoastal waves. Source lives in `LOGO_INNER` in `build/build.py`. Files in `site/img/`: `logo.svg`, `logo-light.svg`, `logo-mark.svg`, `logo-mark-512.png`, `favicon.svg`, `apple-touch-icon.png`, `og-image.png`. Presented on `brand.html`.

## Design system
- Colors: gesso `#f7f3ec`, inlet green `#1f4a44` / `#12302c`, lighthouse red `#b23e27` (CTA), sage `#9db3a6`, sand `#ebe2d1`, ink `#14231f`
- Type: Young Serif (display), Figtree (body), 16px base, 1.6 line-height
- Signature element: paint-chip cards (No. / swatch name / service)
- Accessibility: 4.5:1+ text contrast, visible focus rings, 44px+ touch targets, skip link, labeled form fields with adjacent errors, reduced-motion support
