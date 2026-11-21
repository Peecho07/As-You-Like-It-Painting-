# As You Like It Painting: Site Audit and Rebuild Plan

Current site: https://www.asyoulikeitpainting.com/ (hand-coded static HTML)
Prepared by tsKaizen, Nov 2026

## What's working on the current site
- Strong local SEO bones: service pages and city pages already exist
- Phone number is clickable and repeated (good for calls)
- Clear "since 1983" and "licensed and insured" claims
- Financing (Acorn) and a photo gallery (SmugMug) already exist

## What needs to be fixed

| # | Problem | Why it costs jobs | Fix in the rebuild |
|---|---|---|---|
| 1 | Estimate form sends people to an outside 123FormBuilder page | Every extra click loses leads, and the off-brand page looks less trustworthy | Built-in estimate form with service checkboxes, validation, and success/error states |
| 2 | No project photos on the homepage (only the logo) | Painting is visual. Buyers want to see the work before they call | Photo slots on home, service, and gallery pages, plus a filterable gallery |
| 3 | Reviews are a generic Google search link | No on-page proof. Visitors leave to check reviews and may not come back | Review section on home, about, and a dedicated Reviews page |
| 4 | License numbers not shown | Two real county certifications are a trust edge competitors don't show | PBC #U-14533 and Martin #MCPTG02452 in footer, service sidebars, and city pages |
| 5 | Hobe Sound, Stuart, Palm City, Jensen Beach link to the generic areas page | Lost Martin County search traffic | Dedicated pages for all 13 cities |
| 6 | Popcorn ceiling removal listed with no page | Missed searches for a high-intent service | New popcorn ceiling removal page |
| 7 | Overlapping nav ("Commercial" vs "HOA & Commercial", duplicate Interior links) | Confusing navigation | One Services menu with all 9 services, plus Homeowners and HOA & Commercial paths |
| 8 | Generic hero, no visual identity | Looks like every other painter in Palm Beach County | Paint-chip design system, coastal palette, and a clear "since 1983" hero |
| 9 | No address, schema, or FAQ markup | Weaker Google Maps and rich-result visibility | LocalBusiness (HousePainter) and FAQ schema, sitemap.xml, robots.txt |
| 10 | No mobile quick-contact bar | Mobile users scroll to find the number | Sticky Call / Text / Free Estimate bar on phones |

## New sitemap (36 pages)
- Home, Services, Homeowners, About, Our Work (gallery), Reviews, Financing, Free Estimate (contact), 404
- 9 service pages: Interior, Exterior, Cabinet Refinishing, HOA & Commercial, Trim Carpentry, Faux Wood Graining, Epoxy Floors, Pressure Cleaning, Popcorn Ceiling Removal (new)
- Service Areas hub + 13 city pages

Existing service URLs were kept (interior-painting.html, exterior-painting.html, etc.) so Google rankings carry over.

## Needs from the client before launch
1. 10 to 20 real project photos (pull from SmugMug) for gallery and photo slots
2. Permission to feature 3 to 6 named reviews on the Reviews page
3. Confirm the About page timeline and whether to name Tim / crew leads
4. Where estimate requests should be emailed (form endpoint)
5. Old city page URLs, so we can match them or redirect
