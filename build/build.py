#!/usr/bin/env python3
"""
Static site generator for As You Like It Painting Company.
Edit content in content.py, then run:  python3 build/build.py
Output goes to ./site (HTML only; css/js/img are hand-maintained there).
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from content import (BIZ, SERVICES, CITIES, ICONS, REVIEW_THEMES, HOME_FAQ,
                     GALLERY, STRIPES)

ROOT = pathlib.Path(__file__).resolve().parent.parent / "site"


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


LOGO_INNER = """<rect x="2" y="2" width="44" height="44" rx="11" fill="#1f4a44"/>
  <path d="M21.5 12.6C28 10.2 35 8.4 42.4 7.6c1.4 1.3 1.5 3.4.2 4.8-7.2.6-14.2 2-21.1 4.1z" fill="#e0a526"/>
  <path d="M33 10.2l9.6-1.3M35 13.4l7.4-.6" stroke="#f3c75a" stroke-width=".9" stroke-linecap="round"/>
  <path d="M14.6 11.2L19 6.8l4.4 4.4z" fill="#f7f3ec"/>
  <rect x="16" y="11.2" width="6" height="4.4" rx=".8" fill="#e0a526"/>
  <rect x="14.4" y="15.4" width="9.2" height="1.8" rx=".9" fill="#f7f3ec"/>
  <path d="M16.2 17.2h5.6l2.7 19.6h-11z" fill="#b23e27"/>
  <path d="M15.4 23h7.2l.4 3h-8z" fill="#f7f3ec"/>
  <rect x="17.8" y="30.6" width="2.4" height="6.2" rx="1.2" fill="#12302c"/>
  <path d="M7 38.4c2.6-1.8 5.4-1.8 8 0s5.4 1.8 8 0 5.4-1.8 8 0 5.4 1.8 8 0" stroke="#9db3a6" stroke-width="2.2" stroke-linecap="round" fill="none"/>
  <path d="M11 42.4c2.6-1.6 5.4-1.6 8 0s5.4 1.6 8 0 5.4-1.6 8 0" stroke="#9db3a6" stroke-width="1.8" stroke-linecap="round" fill="none" opacity=".6"/>"""

LOGO = f'''<svg class="brand__mark" viewBox="0 0 48 48" aria-hidden="true">
  {LOGO_INNER}
</svg>'''


def brand_lockup(uid, href="index.html", label=True):
    """Company logo icon + name + animated brush that paints a stroke under the name."""
    aria = ' aria-label="As You Like It Painting Company, home"' if label else ""
    return f"""<a class="brand" href="{href}"{aria}>
      <span class="brand__logo-wrap"><img class="brand__logo" src="img/logo-icon.png" width="235" height="301" alt=""></span>
      <span class="brand__text">
        <span class="brand__name">As You Like It</span>
        <span class="brand__paint" aria-hidden="true">
          <svg class="brand__stroke-svg" viewBox="0 0 150 12" preserveAspectRatio="none">
            <defs><linearGradient id="bp-{uid}" x1="0" x2="1" y1="0" y2="0">
              <stop offset="0" stop-color="#2493aa"/><stop offset=".55" stop-color="#f2a032"/><stop offset="1" stop-color="#dc4a30"/>
            </linearGradient></defs>
            <path class="brand__stroke" d="M4 7.2C28 4.2 52 9.6 78 6.6S124 5 146 6.4" stroke="url(#bp-{uid})" pathLength="100"/>
          </svg>
          <svg class="brand__brush" viewBox="0 0 32 32">
            <rect x="17.5" y="1" width="5" height="15" rx="2.5" transform="rotate(28 20 8.5)" fill="#064d6f"/>
            <rect x="12.2" y="12.6" width="7.4" height="5" rx="1" transform="rotate(28 16 15)" fill="#9aa7ad"/>
            <path d="M9.6 17.4l6.6 3.5-2.3 5.6c-.7 1.6-2.8 2.1-4.6 1.2-1.8-1-2.4-3-1.7-4.6z" fill="#f2a032"/>
            <path d="M8.2 24.6c-.6 1.4-.2 2.6 1 3.2" stroke="#dc4a30" stroke-width="1.6" stroke-linecap="round" fill="none"/>
          </svg>
        </span>
        <span class="brand__sub">Painting Company</span>
      </span>
    </a>"""


def stripes(cls):
    return f'<div class="{cls}" aria-hidden="true">' + "".join(
        f'<span style="background:{c}"></span>' for c in STRIPES) + "</div>"


# ---------------------------------------------------------------- layout
def head(title, desc, path, extra=""):
    canon = BIZ["url"] + ("" if path == "index.html" else path)
    return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BIZ['url']}img/og-image.png">
<meta name="theme-color" content="#12302c">
<link rel="icon" href="img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&family=Young+Serif&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css">
{extra}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""


def header(active=""):
    def cur(key):
        return ' aria-current="page"' if key == active else ""

    drop = "".join(
        f'<a href="{s["slug"]}.html"><span class="chip-dot" style="background:{s["color"]}"></span>{s["name"]}</a>'
        for s in SERVICES)
    return f"""<div class="topbar">
  <div class="wrap">
    <div class="topbar__creds">
      <span>Family owned since 1983</span>
      <span>Licensed &amp; insured in Palm Beach and Martin County</span>
    </div>
    <a href="tel:{BIZ['tel']}">Call or text {BIZ['phone']}</a>
  </div>
</div>
<header class="site-header">
  <div class="wrap">
    {brand_lockup('h')}
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
      {icon('menu')}
    </button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul class="nav__list">
        <li class="nav__item">
          <button class="nav__trigger" aria-expanded="false" aria-controls="menu-services">Services {icon('chevron')}</button>
          <div class="dropdown" id="menu-services">{drop}<a class="dropdown__all" href="services.html">All services {icon('arrow')}</a></div>
        </li>
        <li><a class="nav__link" href="residential-painting.html"{cur('residential')}>Homeowners</a></li>
        <li><a class="nav__link" href="commercial-painting.html"{cur('commercial')}>HOA &amp; Commercial</a></li>
        <li><a class="nav__link" href="gallery.html"{cur('gallery')}>Our Work</a></li>
        <li><a class="nav__link" href="service-areas.html"{cur('areas')}>Areas</a></li>
        <li><a class="nav__link" href="about.html"{cur('about')}>About</a></li>
      </ul>
      <a class="btn nav__cta" href="contact.html">Free Estimate</a>
    </nav>
  </div>
</header>
<main id="main">
"""


def cta_band(title="Ready for a fresh coat?", sub="Tell us about the job. We'll come out, look at it in person, and give you a written estimate for free."):
    return f"""<section class="cta-band" aria-labelledby="cta-title">
  {stripes('cta-band__stripes')}
  <div class="wrap">
    <div>
      <h2 id="cta-title">{title}</h2>
      <p>{sub}</p>
    </div>
    <div class="btn-row">
      <a class="btn btn--light" href="contact.html">Get my free estimate</a>
      <a class="btn btn--ghost-light" href="tel:{BIZ['tel']}">{icon('phone')} {BIZ['phone']}</a>
    </div>
  </div>
</section>
"""


def footer():
    svc = "".join(f'<li><a href="{s["slug"]}.html">{s["name"]}</a></li>' for s in SERVICES[:6])
    top_cities = "".join(f'<li><a href="{c["slug"]}.html">{c["name"]}</a></li>' for c in CITIES[:6])
    return f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        {brand_lockup('f', label=False)}
        <p>Family-owned interior and exterior painting for homes, condos, HOAs, and commercial properties across Palm Beach and Martin County since 1983.</p>
        <p class="mb-0"><a href="tel:{BIZ['tel']}"><strong>{BIZ['phone']}</strong></a> (call or text)<br><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></p>
      </div>
      <div>
        <h4>Services</h4>
        <ul>{svc}<li><a href="services.html">All services</a></li></ul>
      </div>
      <div>
        <h4>Areas</h4>
        <ul>{top_cities}<li><a href="service-areas.html">All service areas</a></li></ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="about.html">About us</a></li>
          <li><a href="gallery.html">Our work</a></li>
          <li><a href="reviews.html">Reviews</a></li>
          <li><a href="financing.html">Financing</a></li>
          <li><a href="contact.html">Free estimate</a></li>
          <li><a href="brand.html">Our logo</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> As You Like It Painting Company, Inc.</span>
      <span>Palm Beach County Cert. #{BIZ['lic_pbc']} &middot; Martin County Cert. #{BIZ['lic_martin']}</span>
    </div>
  </div>
  {stripes('footer-stripes')}
</footer>
<nav class="action-bar" aria-label="Quick contact">
  <a href="tel:{BIZ['tel']}">{icon('phone')}Call</a>
  <a href="sms:{BIZ['tel']}">{icon('message')}Text</a>
  <a class="is-primary" href="contact.html">{icon('clipboard')}Free Estimate</a>
</nav>
<script src="js/main.js" defer></script>
</body>
</html>
"""


def page_hero(eyebrow, title, lede, crumbs, buttons=True, palette=None, photo=None, photo_alt="", stock=True):
    crumb_html = "".join(
        f'<li><a href="{href}">{label}</a></li>' if href else f'<li aria-current="page">{label}</li>'
        for label, href in crumbs)
    stripe_cols = palette or STRIPES
    spans = "".join(f'<span style="background:{c}"></span>' for c in stripe_cols)
    btns = f"""<div class="btn-row">
      <a class="btn" href="contact.html">Get a free estimate</a>
      <a class="btn btn--ghost" href="tel:{BIZ['tel']}">{icon('phone')} Call or text</a>
    </div>""" if buttons else ""
    text = f"""<div class="page-hero__text">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>{crumb_html}</ol></nav>
    <p class="eyebrow">{eyebrow}</p>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
    {btns}
    </div>"""
    if photo:
        tag = '<span class="photo-slot__tag">Stock photo</span>' if stock else ""
        return f"""<section class="page-hero page-hero--photo">
  <div class="wrap page-hero__grid">
    {text}
    <figure class="page-hero__media">
      <div class="page-hero__img"><img src="{photo}" alt="{photo_alt}" width="1200" height="800" fetchpriority="high">{tag}</div>
      <div class="page-hero__chipbar" aria-hidden="true">{spans}</div>
    </figure>
  </div>
</section>
"""
    return f"""<section class="page-hero">
  <div class="page-hero__stripe" aria-hidden="true">{spans}</div>
  <div class="wrap">
    {text}
  </div>
</section>
"""


def _mix(hex_color, target, amt):
    h = hex_color.lstrip("#")
    r, g, bl = (int(h[k:k + 2], 16) for k in (0, 2, 4))
    t = 255 if target == "white" else 0
    return "#%02x%02x%02x" % tuple(round(v + (t - v) * amt) for v in (r, g, bl))


def _is_light(hex_color):
    h = hex_color.lstrip("#")
    r, g, bl = (int(h[k:k + 2], 16) / 255 for k in (0, 2, 4))
    return (0.2126 * r + 0.7152 * g + 0.0722 * bl) > 0.55


def chip_card(s, i):
    base = s["color"]
    # paint-strip scheme: two deeper shades, the base color, two lighter tints
    scheme = [_mix(base, "black", .38), _mix(base, "black", .18), base, _mix(base, "white", .35), _mix(base, "white", .62)]
    strip = "".join(f'<span style="background:{c}"></span>' for c in scheme)
    light = " chip__badge--light" if _is_light(base) else ""
    ink = "chip__swatch--light" if _is_light(base) else ""
    return f"""<a class="chip reveal" href="{s['slug']}.html">
  <div class="chip__swatch chip__swatch--paint {ink}" style="--swatch:{base};--swatch-deep:{scheme[0]}">
    <span class="chip__photo"><img src="img/colors/{s['slug']}.jpg" alt="" loading="lazy" decoding="async" width="900" height="600"></span>
    <span class="chip__badge{light}">{icon(s['icon'])}</span>
    <span class="chip__scheme" aria-hidden="true">{strip}</span>
  </div>
  <div class="chip__body">
    <span class="chip__no">No. {i:02d} &middot; {s['swatch']}</span>
    <h3 class="chip__name">{s['name']}</h3>
    <p class="chip__desc">{s['short']}</p>
    <span class="chip__more">See the details {icon('arrow')}</span>
  </div>
</a>"""


def checks(items, cls="checks"):
    return f'<ul class="{cls}">' + "".join(f"<li>{icon('check')}<span>{x}</span></li>" for x in items) + "</ul>"


def faq(items):
    return '<div class="faq">' + "".join(
        f"<details><summary>{q}</summary><div><p>{a}</p></div></details>" for q, a in items) + "</div>"


def faq_schema(items):
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
    return f'<script type="application/ld+json">{json.dumps(data)}</script>'


def areas_list(cities=CITIES):
    return '<ul class="areas">' + "".join(
        f'<li><a href="{c["slug"]}.html">{c["name"]} <small>{c["county"]}</small></a></li>' for c in cities) + "</ul>"


TRUST = f"""<section class="trust" aria-label="Why customers trust us">
  <div class="wrap">
    <div class="trust__item">{icon('calendar')}<div><b>Since 1983</b><span>Family owned, 40+ years</span></div></div>
    <div class="trust__item">{icon('shield')}<div><b>Licensed &amp; insured</b><span>Palm Beach + Martin County</span></div></div>
    <div class="trust__item">{icon('clipboard')}<div><b>Free written estimates</b><span>Clear scope, no surprises</span></div></div>
    <div class="trust__item">{icon('card')}<div><b>Financing available</b><span>Through Acorn Finance</span></div></div>
  </div>
</section>
"""

PROCESS = f"""<section class="section section--ink" aria-labelledby="process-title">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">How a job runs</p>
      <h2 id="process-title">Most of a good paint job happens before the paint comes out.</h2>
      <p class="lede">Prep is where cheap jobs cut corners. It's also where we spend the most time.</p>
    </div>
    <ol class="steps">
      <li class="step reveal"><h3>Free estimate visit</h3><p>We walk the property with you, talk colors and sheen, and note any repairs.</p></li>
      <li class="step reveal"><h3>Written estimate</h3><p>You get a clear written scope and price. What's included is spelled out.</p></li>
      <li class="step reveal"><h3>Protect and prep</h3><p>Masking, drop cloths, caulking, sanding, patching, and priming where it's needed.</p></li>
      <li class="step reveal"><h3>Finish and walkthrough</h3><p>Finish coats, cleanup, and a final walkthrough together before we call it done.</p></li>
    </ol>
  </div>
</section>
"""


def review_section(head_level="h2"):
    themes = "".join(
        f'<div class="theme reveal"><div class="theme__icon">{icon(t["icon"])}</div><h3>{t["title"]}</h3><p>{t["body"]}</p></div>'
        for t in REVIEW_THEMES)
    return f"""<section class="section section--sand" aria-labelledby="reviews-title">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">What customers say</p>
      <{head_level} id="reviews-title">The same things come up in our reviews, year after year.</{head_level}>
    </div>
    <div class="themes">{themes}</div>
    <div class="review-cta">
      <p>Read reviews from homeowners across Jupiter, Tequesta, and the Gardens.</p>
      <a class="btn btn--light" href="{BIZ['reviews']}" target="_blank" rel="noopener">See our Google reviews {icon('external')}</a>
    </div>
  </div>
</section>
"""


def write(path, html):
    (ROOT / path).write_text(html, encoding="utf-8")
    print("built", path)


# ---------------------------------------------------------------- pages
def build_home():
    chips = "".join(chip_card(s, i + 1) for i, s in enumerate(SERVICES))
    deck = "".join(
        f'<div class="deck__chip"><div class="deck__swatch" style="background:{s["color"]}"></div>'
        f'<div class="deck__label"><b>{s["swatch"]}</b><span>{s["name"]}</span></div></div>'
        for s in [SERVICES[1], SERVICES[3], SERVICES[0], SERVICES[2], SERVICES[5]])
    schema = {
        "@context": "https://schema.org", "@type": "HousePainter",
        "name": "As You Like It Painting Company, Inc.", "url": BIZ["url"], "telephone": BIZ["tel"],
        "email": BIZ["email"], "foundingDate": "1983", "image": BIZ["url"] + "img/og-image.png",
        "address": {"@type": "PostalAddress", "streetAddress": BIZ["street"], "addressLocality": "West Palm Beach",
                    "addressRegion": "FL", "postalCode": "33407", "addressCountry": "US"},
        "areaServed": [c["name"] + ", FL" for c in CITIES],
        "sameAs": [BIZ["gallery"]],
    }
    html = head("As You Like It Painting | Jupiter & Palm Beach Painters Since 1983",
                "Family-owned interior and exterior painting in Jupiter, Palm Beach Gardens, Tequesta and all of Palm Beach and Martin County since 1983. Licensed, insured, free written estimates.",
                "index.html", f'<script type="application/ld+json">{json.dumps(schema)}</script>' + faq_schema(HOME_FAQ))
    html += header("home")
    html += f"""<section class="hero">
  <div class="wrap">
    <div>
      <p class="eyebrow">Palm Beach &amp; Martin County painters</p>
      <h1>Painted right, <em>since 1983.<svg viewBox="0 0 300 20" preserveAspectRatio="none" aria-hidden="true"><path d="M3 14c60-8 140-11 294-6" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round"/></svg></em></h1>
      <p class="hero__lede">Interior and exterior painting for homes, condos, HOAs, and commercial properties. Same family, same standards, 40+ years of North County jobs behind us.</p>
      <div class="btn-row">
        <a class="btn" href="contact.html">Get my free estimate</a>
        <a class="btn btn--ghost" href="tel:{BIZ['tel']}">{icon('phone')} Call or text {BIZ['phone']}</a>
      </div>
      <div class="hero__proof">
        <div class="proof"><strong>1983</strong><span>Family owned since</span></div>
        <div class="proof"><strong>13</strong><span>Cities we serve</span></div>
        <div class="proof"><strong>9</strong><span>Specialty services</span></div>
      </div>
    </div>
    <div class="deck" aria-hidden="true">
      {deck}
      <div class="deck__badge"><span><b>40+</b>Years on<br>the job</span></div>
    </div>
  </div>
</section>
{TRUST}
<section class="section" aria-labelledby="services-title">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Services</p>
      <h2 id="services-title">One crew for the whole job, from drywall patch to final coat.</h2>
      <p class="lede">Painting is the core of what we do. The trim, cabinets, floors, and prep work around it are handled in-house too, so you're not juggling three contractors.</p>
    </div>
    <div class="chips">{chips}</div>
  </div>
</section>
<section class="section section--paper" aria-labelledby="who-title">
  <div class="wrap split">
    <div class="photo-slot reveal" style="--slot:linear-gradient(160deg,#1f4a44,#12302c)">
      <img src="img/gallery/commercial-lift.jpg" alt="As You Like It painters on a boom lift repainting a stucco office building" loading="lazy" width="1024" height="768">
      <span class="photo-slot__cap">Our crew on a commercial repaint</span>
    </div>
    <div>
      <p class="eyebrow">Homes, condos, HOAs, commercial</p>
      <h2 id="who-title">Built for Florida sun, salt air, and summer storms.</h2>
      <p class="lede">A paint job in North County takes a beating. We prep and choose products for coastal conditions, so the finish holds up after the first rainy season.</p>
      {checks(["Single-family homes, inside and out", "Condos and apartments, including occupied units", "HOA communities and property managers", "Light commercial: offices, retail, rentals"])}
      <div class="btn-row"><a class="btn btn--ghost" href="residential-painting.html">For homeowners</a><a class="btn btn--ghost" href="commercial-painting.html">For HOAs &amp; commercial</a></div>
    </div>
  </div>
</section>
{PROCESS}
{review_section()}
<section class="section section--paper" aria-labelledby="areas-title">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Service areas</p>
      <h2 id="areas-title">Based in Jupiter. Working from Wellington to Jensen Beach.</h2>
      <p class="lede">We cover all of Palm Beach County and Martin County. Pick your city for local details.</p>
    </div>
    {areas_list()}
  </div>
</section>
<section class="section" aria-labelledby="faq-title">
  <div class="wrap split split--top">
    <div>
      <p class="eyebrow">Questions</p>
      <h2 id="faq-title">Before you call</h2>
      <p class="lede">Quick answers to what people ask us most. Anything else, just call or text.</p>
      <a class="btn btn--ghost" href="tel:{BIZ['tel']}">{icon('phone')} {BIZ['phone']}</a>
    </div>
    {faq(HOME_FAQ)}
  </div>
</section>
"""
    html += cta_band()
    html += footer()
    write("index.html", html)


def build_service(s, idx):
    others = [x for x in SERVICES if x["slug"] != s["slug"]][:3]
    other_chips = "".join(chip_card(o, SERVICES.index(o) + 1) for o in others)
    sections = "".join(f"<h2>{h}</h2>" + "".join(f"<p>{p}</p>" for p in ps) for h, ps in s["sections"])
    palette = [s["color"], "#e0a526", s["color"], "#1f4a44"]
    html = head(f"{s['name']} in Jupiter & Palm Beach County | As You Like It Painting",
                s["meta"], f"{s['slug']}.html", faq_schema(s["faq"]))
    html += header()
    html += page_hero(f"Service No. {idx:02d} &middot; {s['swatch']}", s["h1"], s["intro"],
                      [("Home", "index.html"), ("Services", "services.html"), (s["name"], None)], palette=palette,
                      **({"photo": "img/gallery/commercial-lift.jpg", "photo_alt": "As You Like It painters on a boom lift repainting a stucco office building", "stock": False}
                         if s["slug"] == "commercial-painting" else {"photo": s["photo"], "photo_alt": s["name"] + " project"}))
    html += f"""<section class="section">
  <div class="wrap service-layout">
    <div class="prose">
      <h2>What's included</h2>
      {checks(s['includes'], 'checks checks--2col')}
      {sections}
      <h2>Common questions</h2>
      {faq(s['faq'])}
    </div>
    <aside class="aside-card" aria-label="Request an estimate">
      <h3>Get a price on your {s['name'].lower()} job</h3>
      <p class="muted">Free in-person estimate with a written scope. We usually call back within one business day.</p>
      <a class="btn" href="contact.html?service={s['slug']}">Request free estimate</a>
      <a class="btn btn--ghost" href="tel:{BIZ['tel']}">{icon('phone')} {BIZ['phone']}</a>
      <hr>
      {checks(['Family owned since 1983', 'Licensed &amp; insured', 'Financing available'])}
      <p class="note mb-0">Palm Beach Co. #{BIZ['lic_pbc']} &middot; Martin Co. #{BIZ['lic_martin']}</p>
    </aside>
  </div>
</section>
<section class="section section--paper" aria-labelledby="more-title">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Often paired with</p><h2 id="more-title">Related services</h2></div>
    <div class="chips">{other_chips}</div>
  </div>
</section>
"""
    html += cta_band(f"Let's look at your {s['name'].lower()} project.")
    html += footer()
    write(f"{s['slug']}.html", html)


def build_services():
    chips = "".join(chip_card(s, i + 1) for i, s in enumerate(SERVICES))
    html = head("Painting Services | As You Like It Painting, Jupiter FL",
                "Interior and exterior painting, cabinet refinishing, HOA and commercial painting, epoxy floors, faux wood graining, trim carpentry, pressure cleaning and popcorn ceiling removal.",
                "services.html")
    html += header()
    html += page_hero("Services", "Everything around the paint, handled by one crew.",
                      "Pick a service to see what's included, how we do it, and answers to common questions.",
                      [("Home", "index.html"), ("Services", None)])
    html += f'<section class="section"><div class="wrap"><div class="chips">{chips}</div></div></section>'
    html += PROCESS + cta_band() + footer()
    write("services.html", html)


def build_residential():
    home_svcs = [s for s in SERVICES if s["slug"] in ("interior-painting", "exterior-painting", "cabinet-refinishing",
                                                      "popcorn-ceiling-removal", "trim-carpentry", "epoxy-coatings")]
    chips = "".join(chip_card(s, SERVICES.index(s) + 1) for s in home_svcs)
    q = [("Do I need to move my furniture?", "We move and cover furniture as part of the job. We just ask that you put away small breakables, wall art, and anything valuable before we arrive."),
         ("Can you help me pick colors?", "Yes. We bring our experience with what works in Florida light and can bring samples. Many customers test two or three colors on the wall first."),
         ("Do you handle HOA paint approvals?", "We've worked inside plenty of North County HOAs and can help you put together what your board needs, including approved color schemes."),
         ("Can I live in the house while you paint?", "Yes. Most of our interior jobs are in occupied homes. We work room by room and keep a clean path through the house.")]
    html = head("Residential House Painters in Jupiter & Palm Beach | As You Like It Painting",
                "House painting for Jupiter, Palm Beach Gardens, Tequesta and surrounding homeowners. Interior, exterior, cabinets, and repairs from a family-owned company since 1983.",
                "residential-painting.html", faq_schema(q))
    html += header("residential")
    html += page_hero("For homeowners", "Your house, painted like it's ours.",
                      "We've been painting North County homes since 1983. Clean crews, real prep, and a finish that holds up to Florida weather.",
                      [("Home", "index.html"), ("Homeowners", None)],
                      photo="img/stock/res-exterior.jpg", photo_alt="White two-story home with a wraparound porch")
    html += f"""<section class="section">
  <div class="wrap split">
    <div>
      <p class="eyebrow">What to expect</p>
      <h2>Clean, respectful crews in your home.</h2>
      <p class="lede">The reviews we're proudest of aren't about the paint. They're about crews who showed up on time, kept the house clean, and treated it with care.</p>
      {checks(["Floors, furniture, and fixtures protected before work starts", "Daily cleanup, no paint cans left in your hallway", "One point of contact from estimate to walkthrough", "We tell you what's wrong before we cover it up"])}
    </div>
    <div class="photo-slot reveal" style="--slot:linear-gradient(160deg,#d9cbb1,#b7a98f)">
      <img src="img/stock/home-interior.jpg" alt="Bright living room with freshly painted white walls" loading="lazy" width="1200" height="800">
      <span class="photo-slot__tag">Stock photo</span>
    </div>
  </div>
</section>
<section class="section section--paper"><div class="wrap">
  <div class="section-head"><p class="eyebrow">Homeowner services</p><h2>Popular with homeowners</h2></div>
  <div class="chips">{chips}</div>
</div></section>
{PROCESS}
<section class="section"><div class="wrap split split--top">
  <div><p class="eyebrow">Questions</p><h2>Homeowner FAQ</h2></div>
  {faq(q)}
</div></section>
"""
    html += cta_band() + footer()
    write("residential-painting.html", html)


def build_city(c):
    near = [x for x in CITIES if x["slug"] != c["slug"] and x["county"] == c["county"]][:6]
    svc_links = "".join(chip_card(s, SERVICES.index(s) + 1) for s in SERVICES[:3])
    html = head(f"Painters in {c['name']}, FL | As You Like It Painting",
                f"Interior and exterior painting in {c['name']}, FL. Family-owned since 1983, licensed in {c['county']}. Free written estimates. Call or text {BIZ['phone']}.",
                f"{c['slug']}.html")
    html += header("areas")
    html += page_hero(f"{c['county']}", f"Painting contractors in {c['name']}, FL",
                      c["blurb"], [("Home", "index.html"), ("Service areas", "service-areas.html"), (c["name"], None)])
    html += f"""<section class="section">
  <div class="wrap split split--top">
    <div class="prose">
      <h2>What we paint in {c['name']}</h2>
      <p>{c['detail']}</p>
      {checks(["Interior repaints, walls, ceilings, trim, and doors", "Exterior stucco, block, wood, and trim", "Cabinet refinishing and faux wood graining", "HOA, condo, and commercial repaints", "Pressure cleaning before exterior work"])}
      <p>We're licensed in both Palm Beach County (#{BIZ['lic_pbc']}) and Martin County (#{BIZ['lic_martin']}), and fully insured.</p>
    </div>
    <div class="card">
      <h3>Free estimate in {c['name']}</h3>
      <p class="muted">We'll come to the property, look at the job, and send you a written estimate.</p>
      <div class="btn-row"><a class="btn" href="contact.html">Request estimate</a><a class="btn btn--ghost" href="tel:{BIZ['tel']}">{icon('phone')} Call</a></div>
    </div>
  </div>
</section>
<section class="section section--paper"><div class="wrap">
  <div class="section-head"><p class="eyebrow">Most requested in {c['name']}</p><h2>Popular services</h2></div>
  <div class="chips">{svc_links}</div>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><p class="eyebrow">Nearby</p><h2>Also serving</h2></div>
  {areas_list(near)}
</div></section>
"""
    html += cta_band(f"Painting in {c['name']}? Let's talk.") + footer()
    write(f"{c['slug']}.html", html)


def build_areas():
    pbc = [c for c in CITIES if c["county"] == "Palm Beach County"]
    mc = [c for c in CITIES if c["county"] == "Martin County"]
    html = head("Service Areas | Painters in Palm Beach & Martin County | As You Like It Painting",
                "As You Like It Painting serves Jupiter, Jupiter Farms, Palm Beach Gardens, North Palm Beach, Tequesta, Juno Beach, Singer Island, West Palm Beach, Wellington, Hobe Sound, Stuart, Palm City and Jensen Beach.",
                "service-areas.html")
    html += header("areas")
    html += page_hero("Service areas", "All of Palm Beach County and Martin County.",
                      "We're based in Jupiter and licensed in both counties. If your town isn't listed, call anyway. We probably work there.",
                      [("Home", "index.html"), ("Service areas", None)])
    html += f"""<section class="section"><div class="wrap">
  <div class="section-head"><h2>Palm Beach County</h2></div>{areas_list(pbc)}
  <div class="section-head" style="margin-top:3rem"><h2>Martin County</h2></div>{areas_list(mc)}
</div></section>"""
    html += cta_band() + footer()
    write("service-areas.html", html)


def build_about():
    html = head("About Us | Family-Owned Painters Since 1983 | As You Like It Painting",
                "As You Like It Painting Company has been a family-owned painting contractor in Jupiter, FL since 1983, serving Palm Beach and Martin County.",
                "about.html")
    html += header("about")
    html += page_hero("About us", "Same family. Same standards. Since 1983.",
                      "As You Like It Painting Company started in North County more than 40 years ago and has stayed family owned the whole way.",
                      [("Home", "index.html"), ("About", None)])
    html += f"""<section class="section">
  <div class="wrap split split--top">
    <div class="prose">
      <h2>What 40 years teaches you</h2>
      <p>Paint is the easy part. What makes a job last is everything that happens first: the scraping, caulking, sanding, patching, and priming that nobody sees when it's done right.</p>
      <p>That's the part we refuse to rush. It's why homeowners, condo boards, and property managers across Palm Beach and Martin County keep calling us back, and why so much of our work comes from referrals.</p>
      <h2>How we work</h2>
      {checks(["Proper preparation on every surface", "Premium materials suited to Florida conditions", "Clear written estimates, so you know exactly what you're paying for", "Clean, respectful, professional crews", "We protect your property and stand behind finished work"])}
    </div>
    <div>
      <figure class="team-photo">
        <div class="photo-slot"><img src="img/gallery/team.jpg" alt="Three members of the As You Like It Painting family standing in front of the company truck" loading="lazy" width="895" height="768"></div>
        <figcaption>The family behind As You Like It, with the company truck.</figcaption>
      </figure>
      <div class="stat-row" style="grid-template-columns:1fr 1fr">
        <div class="stat"><b>1983</b><span>Founded in North County</span></div>
        <div class="stat"><b>40+</b><span>Years of experience</span></div>
        <div class="stat"><b>2</b><span>Counties licensed</span></div>
        <div class="stat"><b>13</b><span>Cities served</span></div>
      </div>
      <ol class="timeline">
        <li><b>1983</b><p>As You Like It Painting Company opens its doors serving Jupiter and North Palm Beach County.</p></li>
        <li><b>Growing the trade</b><p>Services expand beyond paint into faux finishes, wood graining, cabinet refinishing, and trim carpentry.</p></li>
        <li><b>Two counties</b><p>Licensed in Palm Beach County (#{BIZ['lic_pbc']}) and Martin County (#{BIZ['lic_martin']}).</p></li>
        <li><b>Today</b><p>Homes, condos, HOAs, and commercial properties from Wellington to Jensen Beach.</p></li>
      </ol>
      <!-- EDIT: confirm/replace timeline milestones with Tim before launch -->
    </div>
  </div>
</section>
{review_section()}
"""
    html += cta_band() + footer()
    write("about.html", html)


def build_gallery():
    cats = [("all", "All"), ("interior", "Interior"), ("exterior", "Exterior"), ("cabinets", "Cabinets"),
            ("faux", "Faux &amp; graining"), ("commercial", "Commercial")]
    btns = "".join(f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{v}</button>' for k, v in cats)
    tiles = "".join(
        f"""<figure class="tile reveal" data-cat="{g['cat']}">
  <div class="photo-slot"><img src="img/{g['img']}" alt="{g['alt']}" loading="lazy" decoding="async">{'' if g.get('real') else '<span class="photo-slot__tag">Stock photo</span>'}</div>
  <figcaption><b>{g['title']}</b><span>{g['place']}</span></figcaption>
</figure>""" for g in GALLERY)
    html = head("Our Work | Painting Project Gallery | As You Like It Painting",
                "Photos of interior, exterior, cabinet, faux wood graining and commercial painting projects across Palm Beach and Martin County.",
                "gallery.html")
    html += header("gallery")
    html += page_hero("Our work", "Recent projects", "Real jobs from our crews, plus sample photos of the work we do while we add more of our own. The full archive lives on our gallery site.",
                      [("Home", "index.html"), ("Our work", None)], buttons=False)
    html += f"""<section class="section"><div class="wrap">
  <div class="filters" role="group" aria-label="Filter projects">{btns}</div>
  <p class="note" id="gallery-count" aria-live="polite">Showing {len(GALLERY)} projects</p>
  <div class="gallery">{tiles}</div>
  <div class="review-cta" style="margin-top:2.5rem">
    <p>Want to see more? Browse the full photo archive.</p>
    <a class="btn btn--light" href="{BIZ['gallery']}" target="_blank" rel="noopener">Open full gallery {icon('external')}</a>
  </div>
</div></section>"""
    html += cta_band() + footer()
    write("gallery.html", html)


def build_reviews():
    html = head("Reviews | As You Like It Painting, Jupiter FL",
                "What homeowners and property managers say about As You Like It Painting Company. Read our reviews and leave your own.",
                "reviews.html")
    html += header()
    html += page_hero("Reviews", "Most of our work comes from referrals.",
                      "That's the best review a contractor can get. Here's what customers mention most, and where to read reviews in full.",
                      [("Home", "index.html"), ("Reviews", None)], buttons=False)
    html += review_section("h2")
    html += f"""<section class="section"><div class="wrap grid-2">
  <div class="card">
    <h3>Read our reviews</h3>
    <p class="muted">See what customers across Palm Beach and Martin County have written about us.</p>
    <a class="btn" href="{BIZ['reviews']}" target="_blank" rel="noopener">Google reviews {icon('external')}</a>
  </div>
  <div class="card">
    <h3>Worked with us?</h3>
    <p class="muted">A short review helps other homeowners find a painter they can trust. We read every one.</p>
    <a class="btn btn--ghost" href="{BIZ['reviews']}" target="_blank" rel="noopener">Leave a review {icon('external')}</a>
  </div>
</div>
<!-- EDIT: add 3 to 6 real customer reviews here (with permission), or embed a Google reviews widget. -->
</section>"""
    html += cta_band() + footer()
    write("reviews.html", html)


def build_financing():
    q = [("Does checking my options affect my credit?", "Acorn Finance lets you check offers from its lending partners. Their site explains how pre-qualification works and whether it affects your credit."),
         ("What jobs can I finance?", "Any project we quote, from a single room to a full exterior repaint or cabinet refinishing."),
         ("Who do I talk to about loan terms?", "Loan terms come from Acorn Finance's lending partners, not from us. Questions about rates or payments go to them. Questions about the job come to us.")]
    html = head("Painting Financing | As You Like It Painting", "Finance your painting project through Acorn Finance. Check offers in minutes and spread the cost of your project over time.", "financing.html", faq_schema(q))
    html += header()
    html += page_hero("Financing", "Paint now, pay over time.",
                      "We've partnered with Acorn Finance so you don't have to wait on a project that can't wait, like peeling exterior paint before storm season.",
                      [("Home", "index.html"), ("Financing", None)], buttons=False)
    html += f"""<section class="section"><div class="wrap split split--top">
  <div>
    <ol class="steps" style="grid-template-columns:1fr">
      <li class="step"><h3>Get your estimate</h3><p>We price the job first so you know the amount to finance.</p></li>
      <li class="step"><h3>Check offers with Acorn</h3><p>Fill out one short application on Acorn Finance's site to see offers from their lenders.</p></li>
      <li class="step"><h3>Pick a plan, book the job</h3><p>Choose the offer that fits and we'll get you on the schedule.</p></li>
    </ol>
    <div class="btn-row" style="margin-top:1.5rem">
      <a class="btn" href="{BIZ['financing']}" target="_blank" rel="noopener">Check financing options {icon('external')}</a>
      <a class="btn btn--ghost" href="contact.html">Get an estimate first</a>
    </div>
    <p class="note" style="margin-top:1rem">Financing is provided by Acorn Finance and its lending partners. As You Like It Painting is not a lender. All loans subject to credit approval.</p>
  </div>
  {faq(q)}
</div></section>"""
    html += cta_band() + footer()
    write("financing.html", html)


def build_contact():
    pills = "".join(
        f'<label class="pill"><input type="checkbox" name="services" value="{s["slug"]}"><span style="--c:{s["color"]}">{s["name"]}</span></label>'
        for s in SERVICES)
    city_opts = "".join(f'<option>{c["name"]}</option>' for c in CITIES)
    html = head("Free Painting Estimate | Contact As You Like It Painting",
                f"Request a free written painting estimate in Palm Beach or Martin County. Call or text {BIZ['phone']} or send us the details online.",
                "contact.html")
    html += header("contact")
    html += page_hero("Free estimate", "Tell us about your project.",
                      "Fill this out and we'll call you back, usually within one business day. Prefer to talk? Call or text anytime.",
                      [("Home", "index.html"), ("Free estimate", None)], buttons=False)
    html += f"""<section class="section">
  <div class="wrap split split--top" style="grid-template-columns:1.4fr .9fr">
    <form class="form-card" id="estimate-form" novalidate>
      <h2 style="font-size:var(--step-2)">Request a free estimate</h2>
      <p class="muted">Fields marked <span class="req">*</span> are required.</p>
      <div class="form-grid">
        <div class="field">
          <label for="f-name">Full name <span class="req">*</span></label>
          <input id="f-name" name="name" type="text" autocomplete="name" required aria-describedby="e-name">
          <p class="field__error" id="e-name" role="alert"></p>
        </div>
        <div class="field">
          <label for="f-phone">Phone <span class="req">*</span></label>
          <input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required aria-describedby="e-phone">
          <p class="field__error" id="e-phone" role="alert"></p>
        </div>
        <div class="field">
          <label for="f-email">Email <span class="hint">(optional)</span></label>
          <input id="f-email" name="email" type="email" autocomplete="email" aria-describedby="e-email">
          <p class="field__error" id="e-email" role="alert"></p>
        </div>
        <div class="field">
          <label for="f-city">City <span class="req">*</span></label>
          <input id="f-city" name="city" list="city-list" autocomplete="address-level2" required aria-describedby="e-city">
          <datalist id="city-list">{city_opts}</datalist>
          <p class="field__error" id="e-city" role="alert"></p>
        </div>
        <fieldset class="field field--full">
          <legend>What do you need? <span class="hint">(pick any)</span></legend>
          <div class="pills">{pills}</div>
        </fieldset>
        <div class="field">
          <label for="f-type">Property type</label>
          <select id="f-type" name="property_type">
            <option>Single-family home</option><option>Condo / apartment</option><option>HOA community</option><option>Commercial property</option><option>Rental property</option>
          </select>
        </div>
        <div class="field">
          <label for="f-when">When do you want to start?</label>
          <select id="f-when" name="timeline">
            <option>As soon as possible</option><option>Within a month</option><option>1 to 3 months</option><option>Just pricing it out</option>
          </select>
        </div>
        <div class="field field--full">
          <label for="f-msg">Project details <span class="hint">(rooms, square footage, colors, anything helpful)</span></label>
          <textarea id="f-msg" name="message"></textarea>
        </div>
        <div class="field field--full">
          <label for="f-contact">Best way to reach you</label>
          <select id="f-contact" name="contact_pref"><option>Phone call</option><option>Text message</option><option>Email</option></select>
        </div>
        <label class="hp" aria-hidden="true">Company <input name="company" tabindex="-1" autocomplete="off"></label>
      </div>
      <div class="form-foot">
        <small>We only use your info to reply about your project. No spam, no sharing.</small>
        <button class="btn" type="submit"><span class="spinner" aria-hidden="true"></span>Send my request</button>
      </div>
      <div class="form-status" role="status" tabindex="-1"></div>
    </form>
    <div class="contact-cards">
      <a class="contact-card" href="tel:{BIZ['tel']}">{icon('phone')}<div><b>Call {BIZ['phone']}</b><span>Talk to us directly about your job</span></div></a>
      <a class="contact-card" href="sms:{BIZ['tel']}">{icon('message')}<div><b>Text us</b><span>Send photos of the job for a faster quote</span></div></a>
      <a class="contact-card" href="mailto:{BIZ['email']}">{icon('mail')}<div><b>Email</b><span>{BIZ['email']}</span></div></a>
      <div class="contact-card">{icon('pin')}<div><b>Based in Jupiter, FL</b><span>Serving Palm Beach &amp; Martin County<br>Mailing: {BIZ['street']}, West Palm Beach, FL 33407</span></div></div>
      <a class="contact-card" href="financing.html">{icon('card')}<div><b>Financing available</b><span>Check offers through Acorn Finance</span></div></a>
    </div>
  </div>
</section>
"""
    html += footer()
    write("contact.html", html)


def build_404():
    html = head("Page not found | As You Like It Painting", "That page moved or doesn't exist.", "404.html")
    html += header()
    html += f"""<section class="section"><div class="wrap center" style="max-width:640px">
  <p class="eyebrow" style="justify-content:center">404</p>
  <h1>This page needs a fresh coat.</h1>
  <p class="lede" style="margin-inline:auto">It moved or never existed. Try one of these instead.</p>
  <div class="btn-row" style="justify-content:center"><a class="btn" href="index.html">Go home</a><a class="btn btn--ghost" href="services.html">See services</a><a class="btn btn--ghost" href="contact.html">Free estimate</a></div>
</div></section>"""
    html += footer()
    write("404.html", html)


def build_brand():
    big = LOGO.replace('class="brand__mark"', 'class="brand-show__mark"')
    sw = [("Harbor Navy", "#064d6f", "House outline, headlines"), ("Pool Teal", "#2493aa", "Paint drips, accents"),
          ("Sunset Orange", "#f2a032", "Brushstroke highlight"), ("Coral Red", "#dc4a30", "Paint, calls to action"),
          ("Inlet Green", "#1f4a44", "Site backgrounds"), ("Gesso", "#f7f3ec", "Paper and backgrounds")]
    chips = "".join(f'<div class="brand-swatch"><span style="background:{c}"></span><b>{n}</b><code>{c}</code><small>{u}</small></div>' for n, c, u in sw)
    html = head("Our Logo | As You Like It Painting Company",
                "The As You Like It Painting logo: a house painted by a dripping brush, plus the animated brush lockup used across the site.",
                "brand.html")
    html += header()
    html += page_hero("Brand", "Our logo.",
                      "A house painted with a single dripping brush, in teal, orange and coral. On the site it sits beside our name, with a brush that paints a stroke underneath.",
                      [("Home", "index.html"), ("Brand", None)], buttons=False)
    html += f"""<section class="section"><div class="wrap">
  <div class="brand-show">
    <div class="brand-show__stage brand-show__stage--white"><img class="brand-show__full" src="img/logo-full.png" width="400" height="400" alt="As You Like It Painting logo"></div>
    <div class="brand-show__stage">{brand_lockup('b1')}</div>
    <div class="brand-show__stage brand-show__stage--dark footer-brand">{brand_lockup('b2', label=False)}</div>
  </div>
  <div class="brand-notes">
    <div><h3>The house</h3><p>Homes are most of what we paint. The navy outline keeps the mark readable at any size.</p></div>
    <div><h3>The brush</h3><p>The brush handle is the left wall of the house. Paint drips from it, so you can tell what we do at a glance.</p></div>
    <div><h3>The animated stroke</h3><p>In the site header a small brush paints a teal-to-coral stroke under the name, then fades and repeats. It stays still for visitors who turn off motion.</p></div>
  </div>
  <h2 class="brand-page-h2">Colors</h2>
  <div class="brand-swatches">{chips}</div>
  <h2 class="brand-page-h2">Download</h2>
  <div class="btn-row">
    <a class="btn" href="img/logo-full.png" download>Full logo (PNG)</a>
    <a class="btn btn--ghost" href="img/logo-icon.png" download>Icon only (PNG)</a>
  </div>
  <h2 class="brand-page-h2">Alternate mark (concept)</h2>
  <div class="brand-alt">
    <div class="brand-show__stage">{big}</div>
    <p>An alternate concept we drew: the Jupiter Lighthouse with a gold brushstroke beam over Intracoastal water. It isn't used on the site. It's here as an option for shirts, truck decals, or a local-pride mark.</p>
    <div class="btn-row"><a class="btn btn--ghost" href="img/logo-mark.svg" download>Lighthouse mark (SVG)</a><a class="btn btn--ghost" href="img/logo-mark-512.png" download>Lighthouse mark (PNG)</a></div>
  </div>
</div></section>"""
    html += cta_band()
    html += footer()
    write("brand.html", html)


def build_sitemap():
    pages = ["index.html", "services.html", "residential-painting.html", "service-areas.html", "about.html",
             "gallery.html", "reviews.html", "financing.html", "contact.html", "brand.html"]
    pages += [f"{s['slug']}.html" for s in SERVICES] + [f"{c['slug']}.html" for c in CITIES]
    pages = list(dict.fromkeys(pages))
    urls = "".join(f"<url><loc>{BIZ['url']}{'' if p == 'index.html' else p}</loc></url>" for p in pages)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BIZ['url']}sitemap.xml\n")
    print("built sitemap.xml, robots.txt")


if __name__ == "__main__":
    build_home()
    build_services()
    build_residential()
    for i, s in enumerate(SERVICES):
        build_service(s, i + 1)
    build_areas()
    for c in CITIES:
        build_city(c)
    build_about()
    build_gallery()
    build_reviews()
    build_financing()
    build_contact()
    build_404()
    build_brand()
    build_sitemap()
