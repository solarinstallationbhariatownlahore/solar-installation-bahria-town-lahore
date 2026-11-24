# Solar Installation Bahria Town Lahore — Website

A complete, premium, luxury, multi-page static website for **Solar Installation Bahria Town Lahore**, a solar energy company based in Bahria Town Lahore, Pakistan.

- **Live URL (after GitHub Pages deploy):** https://solarinstallationbhariatownlahore.github.io/solar-installation-bahria-town-lahore
- **Business:** Solar Installation Bahria Town Lahore — Solar Energy Company
- **Address:** C, Plaza 210, 1st Floor, Sector C, Sector Tulip Commercial B, Sector C, Bahria Town, Lahore, 54000, Pakistan
- **Phone / WhatsApp:** 03200147783
- **Google Business Profile:** https://www.google.com/maps?cid=17411783398733912742

## What is in this project

- **27 HTML pages** — Home, About, Services overview, 8 service pages (Residential, Commercial, Hybrid, On-Grid, Off-Grid, Panel Installation, Inverter Installation, Battery Solutions), 2 location pages (Bahria Town Lahore, Lahore), Projects portfolio, Blog index, **8 full blog articles**, Contact, Privacy Policy, Terms & Conditions, and a custom 404 page.
- **Design** — deep navy `#071426`, charcoal `#101820`, metallic gold `#D4AF37`, electric blue `#1677D2`, dark slate `#142338`. Inter / Manrope / Poppins via Google Fonts. Sticky header (transparent → solid on scroll), mobile drawer menu, floating WhatsApp button, back-to-top button, mobile call/WhatsApp bar, FAQ accordion, project gallery with lightbox + category filters, blog search + category filters.
- **SEO** — unique title + meta description on every page, one H1 per page, OG + Twitter card meta, canonical URLs, `robots.txt`, `sitemap.xml` (26 pages), BreadcrumbList JSON-LD, Organization + LocalBusiness JSON-LD, Service JSON-LD on service pages, FAQPage JSON-LD on Home + both location pages, Article JSON-LD on blog posts, WebSite JSON-LD on Home.
- **Images** — 20 royalty-free solar photographs in `assets/images/` (hero, residential, commercial, installer, inverter, battery, mounting, panels close-up, solar fields). All JPEG, compressed to ≤ ~330 KB except two detailed photos (~380–550 KB).
- **Contact form** — validates name, phone, property type, system and message (plus a honeypot spam field). **There is no backend**: on valid submit the enquiry is composed as a WhatsApp message and opened at `https://wa.me/923200147783?text=…` — the visitor presses Send in WhatsApp. The site never shows a fake "submitted successfully" message.

## Project structure

```
.
├── build.py                  # Generator — builds all pages from one template + content
├── README.md                 # This file
├── favicon.svg               # Logo mark (inline SVG sun + panel)
├── index.html                # Home (generated)
├── about.html                # (generated)
├── services.html             # (generated)
├── residential-solar-installation.html
├── commercial-solar-installation.html
├── hybrid-solar-systems.html
├── on-grid-solar-systems.html
├── off-grid-solar-systems.html
├── solar-panel-installation.html
├── solar-inverter-installation.html
├── solar-battery-solutions.html
├── solar-installation-bahria-town-lahore.html
├── solar-installation-lahore.html
├── projects.html
├── blog.html
├── blog/                     # 8 article pages (generated)
├── contact.html
├── privacy-policy.html
├── terms-and-conditions.html
├── 404.html
├── sitemap.xml               # (generated)
├── robots.txt                # (generated)
├── assets/
│   ├── css/style.css         # All styles (single file)
│   ├── js/main.js            # All interactions (single file)
│   └── images/               # 20 JPEG photographs
└── download_images.py        # Image download script (provenance only)
```

## How to build

Requires Python 3 (no extra packages):

```bash
python3 build.py
```

This regenerates every HTML page, `sitemap.xml` and `robots.txt` from the shared template in `build.py`. Edit content in `build.py` and re-run — never edit the generated HTML by hand, or your changes will be lost on the next build.

To preview locally:

```bash
python3 -m http.server 8000
# open http://localhost:8000/
```

## How to deploy free on GitHub Pages

1. Create a new public repository on GitHub named **`solar-installation-bahria-town-lahore`** (account: `solarinstallationbhariatownlahore`).
2. Upload / push the contents of this folder to the repository (root of the repo, `main` branch).
3. In the repository: **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main`, folder: `/ (root)` → Save.**
4. Wait a few minutes. The site will be live at:
   `https://solarinstallationbhariatownlahore.github.io/solar-installation-bahria-town-lahore`
5. The custom 404 page (`404.html`) is picked up automatically by GitHub Pages.

## Changing the site URL

The public URL is configured once, at the top of `build.py`:

```python
SITE_URL = "https://solarinstallationbhariatownlahore.github.io/solar-installation-bahria-town-lahore"
```

If the repository name or username ever changes, update `SITE_URL` and re-run `python3 build.py` so canonical tags, Open Graph URLs and `sitemap.xml` use the new address. While `SITE_URL` is empty, links are relative and canonical/OG URLs are omitted.

## How the contact form works

GitHub Pages has no backend, so the form cannot send email by itself. On valid submit it:

1. Validates the fields in the browser (name, phone, property type, system, message).
2. Composes the enquiry as a WhatsApp message.
3. Opens `https://wa.me/923200147783?text=…` in a new tab and tells the visitor to press **Send** in WhatsApp.
4. If the pop-up is blocked, it shows a tap-to-open WhatsApp link instead.

No enquiry is ever sent anywhere else, and no fake success state is shown. If a real email backend is wanted later, connect a third-party form service (e.g. Formspree) and point the form at it — that is a separate setup, not included here.

## Honest limits

- **No backend / no email form.** The contact form works through WhatsApp only (see above).
- **No prices, savings or performance claims anywhere on the site.** Prices depend on system size, components and the property, and are discussed during a free consultation. No customer counts, installation figures, ratings, awards or certifications are claimed.
- **No fabricated testimonials.** The testimonials section is a neutral invitation for customers to share feedback. Only genuine, verified reviews should ever be published there.
- **Portfolio images are illustrative.** Every gallery image is labelled "Illustrative image". Only verified photographs of the company's own completed work should be published as company projects — replace the gallery images when real project photos are available.
- **Blog articles are general guides.** They are original, informative content, not technical specifications for any specific product. System recommendations always come from an assessment of the actual property.
- **Google Maps embed** on the contact page uses the business address (Plaza 210, Sector C, Tulip Commercial, Bahria Town, Lahore); the "Open in Google Maps" link goes to the official Google Business Profile.
