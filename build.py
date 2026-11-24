#!/usr/bin/env python3
"""
Solar Installation Bahria Town Lahore — static website generator.

Builds every page from one shared layout template + content data, so the
header, footer, navigation and SEO blocks stay consistent across the site.

Usage:
    python3 build.py

Output: HTML pages in this directory (project root), plus sitemap.xml and
robots.txt. The site is pure static HTML/CSS/JS — ready for free hosting on
GitHub Pages (no backend, no server code, no build step beyond this script).

Configuration:
    SITE_URL — set this to the real public URL once the GitHub Pages site
    exists, e.g. SITE_URL = "https://username.github.io/repo-name"
    then re-run `python3 build.py`. While empty, all links are relative and
    canonical / Open Graph URLs are omitted (relative links still work
    everywhere on the site).
"""

import json
import os
import re
from datetime import date

# ---------------------------------------------------------------- config ---
SITE_URL = "https://solarinstallationbhariatownlahore.github.io/solar-installation-bahria-town-lahore"  # e.g. "https://username.github.io/solar-bahria-town-lahore"
ROOT = os.path.dirname(os.path.abspath(__file__))
TODAY = date(2026, 11, 24).isoformat()

# ------------------------------------------------------------- business ---
BUSINESS = "Solar Installation Bahria Town Lahore"
SHORT = "Solar Installation Bahria Town Lahore"
CATEGORY = "Solar Energy Company"
PHONE_DISPLAY = "03200147783"
PHONE_TEL = "tel:+923200147783"
PHONE_INTL = "+92 320 0147783"
WA_LINK = "https://wa.me/923200147783"
ADDRESS = ("C, Plaza 210, 1st Floor, Sector C, Sector Tulip Commercial B, "
           "Sector C, Bahria Town, Lahore, 54000, Pakistan")
ADDRESS_SHORT = "Plaza 210, 1st Floor, Sector C, Tulip Commercial, Bahria Town, Lahore"
GMB = "https://www.google.com/maps?cid=17411783398733912742"
MAP_EMBED = ("https://maps.google.com/maps?q=Plaza%20210%2C%20Sector%20C%2C%20"
             "Tulip%20Commercial%2C%20Bahria%20Town%2C%20Lahore&z=15&output=embed")
OG_IMAGE = "assets/images/modern-house-flat-roof-solar.jpg"

SOCIAL = [
    ("Facebook", "https://web.facebook.com/solarinstallationbhariatownlahore1/",
     '<path d="M13.5 21.5v-7.2h2.4l.4-2.9h-2.8V9.5c0-.8.3-1.4 1.5-1.4h1.4V5.5c-.3 0-1.2-.1-2.2-.1-2.2 0-3.7 1.3-3.7 3.8v2.2H8v2.9h2.5v7.2h3z"/>'),
    ("X", "https://x.com/SolarInstam3f9",
     '<path d="M17.7 3H21l-7.3 8.3L22.2 21h-6.7l-5.2-6.3L4.3 21H1l7.8-8.9L1.5 3h6.9l4.7 5.7 4.6-5.7zm-1.2 16h1.9L7 4.9H5L16.5 19z"/>'),
    ("Pinterest", "https://www.pinterest.com/solarinstallationbharyiatown/",
     '<path d="M12 2C6.5 2 2 6.5 2 12c0 4.2 2.6 7.8 6.3 9.3-.1-.8-.2-2 0-2.9l1.2-4.9s-.3-.6-.3-1.5c0-1.4.8-2.4 1.8-2.4.9 0 1.3.6 1.3 1.4 0 .9-.6 2.2-.9 3.4-.2 1 .5 1.9 1.5 1.9 1.9 0 3.3-2 3.3-4.8 0-2.5-1.8-4.3-4.4-4.3-3 0-4.7 2.2-4.7 4.5 0 .9.3 1.9.8 2.4.1.1.1.2.1.3l-.3 1.1c0 .2-.2.2-.4.1-1.2-.6-2-2.4-2-3.9 0-3.2 2.3-6.1 6.7-6.1 3.5 0 6.2 2.5 6.2 5.8 0 3.5-2.2 6.3-5.2 6.3-1 0-2-.5-2.3-1.1l-.6 2.4c-.2.9-.8 2-1.2 2.6.9.3 1.9.4 2.9.4 5.5 0 10-4.5 10-10S17.5 2 12 2z"/>'),
    ("Instagram", "https://www.instagram.com/solarinstallactionbharyiatown1/",
     '<rect x="2.8" y="2.8" width="18.4" height="18.4" rx="5.2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.3" cy="6.7" r="1.4"/>'),
    ("Threads", "https://www.threads.com/@solarinstallationbharyiatown1",
     '<text x="12" y="17.5" text-anchor="middle" font-size="14" font-weight="700" fill="currentColor" font-family="Inter, sans-serif">@</text>'),
    ("Medium", "https://medium.com/@solarinstallationbharyiatownl",
     '<text x="12" y="17.5" text-anchor="middle" font-size="13" font-weight="700" fill="currentColor" font-family="Georgia, serif">M</text>'),
    ("YouTube", "https://www.youtube.com/@solarinstallactionbharyiatown5",
     '<rect x="2" y="5" width="20" height="14" rx="4.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M10.2 9.3v5.4l4.8-2.7-4.8-2.7z"/>'),
    ("TikTok", "https://www.tiktok.com/@solarinstallactionbharyi",
     '<path d="M16.6 3c.4 2 1.8 3.6 3.9 3.9v3c-1.5 0-2.9-.5-3.9-1.3v6.1c0 3.4-2.6 5.8-5.8 5.8A5.6 5.6 0 0 1 5 14.7c0-3.2 2.6-5.7 5.9-5.7.3 0 .7 0 1 .1v3.1c-.3-.1-.6-.2-1-.2-1.5 0-2.7 1.2-2.7 2.7 0 1.5 1.2 2.7 2.7 2.7 1.6 0 2.8-1.2 2.8-2.8V3h2.9z"/>'),
]

LOGO_SVG = """<svg class="logo-mark" viewBox="0 0 64 64" aria-hidden="true">
  <rect width="64" height="64" rx="14" fill="#0a1d33"/>
  <circle cx="32" cy="26" r="11" fill="#D4AF37"/>
  <g stroke="#D4AF37" stroke-width="3" stroke-linecap="round">
    <line x1="32" y1="8" x2="32" y2="12"/><line x1="32" y1="36" x2="32" y2="40"/>
    <line x1="14" y1="26" x2="18" y2="26"/><line x1="46" y1="26" x2="50" y2="26"/>
    <line x1="19" y1="13" x2="22" y2="16"/><line x1="42" y1="36" x2="45" y2="39"/>
    <line x1="45" y1="13" x2="42" y2="16"/><line x1="22" y1="36" x2="19" y2="39"/>
  </g>
  <g fill="#1677D2">
    <rect x="14" y="46" width="10" height="7" rx="1"/><rect x="27" y="46" width="10" height="7" rx="1"/><rect x="40" y="46" width="10" height="7" rx="1"/>
  </g>
</svg>"""

# -------------------------------------------------------------- helpers ---
def abs_url(path):
    """Absolute URL when SITE_URL is set, otherwise the relative path."""
    if SITE_URL:
        return SITE_URL.rstrip("/") + "/" + path.lstrip("/")
    return path

def social_icons():
    out = []
    for name, url, svg in SOCIAL:
        out.append(
            '<a class="social-ico" href="{url}" target="_blank" rel="noopener" '
            'aria-label="{name} — Solar Installation Bahria Town Lahore">'
            '<svg viewBox="0 0 24 24" aria-hidden="true">{svg}</svg></a>'
            .format(url=url, name=name, svg=svg))
    return "\n".join(out)

def org_ld():
    d = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": BUSINESS,
        "description": ("Solar Installation Bahria Town Lahore is a solar energy "
                        "company providing residential and commercial solar "
                        "installation services in Bahria Town Lahore, Pakistan."),
        "sameAs": [url for _, url, _ in SOCIAL],
    }
    if SITE_URL:
        d["url"] = SITE_URL
        d["logo"] = abs_url("favicon.svg")
    return d

def local_ld():
    d = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": BUSINESS,
        "description": ("Solar energy company offering residential and commercial "
                        "solar installation, hybrid, on-grid and off-grid solar "
                        "systems in Bahria Town Lahore."),
        "telephone": "+92-320-0147783",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": ("C, Plaza 210, 1st Floor, Sector C, "
                              "Sector Tulip Commercial B, Sector C, Bahria Town"),
            "addressLocality": "Lahore",
            "postalCode": "54000",
            "addressCountry": "PK",
        },
        "sameAs": [url for _, url, _ in SOCIAL],
    }
    if SITE_URL:
        d["url"] = SITE_URL
    return d

def breadcrumb_ld(items):
    """items: list of (name, path-or-None)."""
    els = []
    for i, (name, path) in enumerate(items, start=1):
        item = {"@type": "ListItem", "position": i, "name": name}
        if path:
            item["item"] = abs_url(path)
        els.append(item)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": els}

def service_ld(name, desc, path):
    d = {"@context": "https://schema.org", "@type": "Service",
         "name": name, "description": desc,
         "provider": {"@type": "LocalBusiness", "name": BUSINESS}}
    if SITE_URL:
        d["url"] = abs_url(path)
    return d

def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
                for q, a in faqs]}

def article_ld(title, desc, path, image, date_pub):
    d = {"@context": "https://schema.org", "@type": "Article",
         "headline": title, "description": desc,
         "image": abs_url(image), "datePublished": date_pub,
         "dateModified": date_pub,
         "author": {"@type": "Organization", "name": BUSINESS},
         "publisher": {"@type": "Organization", "name": BUSINESS}}
    if SITE_URL:
        d["mainEntityOfPage"] = abs_url(path)
    return d

def website_ld():
    d = {"@context": "https://schema.org", "@type": "WebSite", "name": BUSINESS,
         "description": "Solar Installation Bahria Town Lahore — premium solar "
                        "energy solutions for homes and businesses in Bahria Town Lahore."}
    if SITE_URL:
        d["url"] = SITE_URL
    return d

# -------------------------------------------------------------- template ---
NAV_SERVICES = [
    ("Residential Solar Installation", "residential-solar-installation.html"),
    ("Commercial Solar Installation", "commercial-solar-installation.html"),
    ("Hybrid Solar Systems", "hybrid-solar-systems.html"),
    ("On-Grid Solar Systems", "on-grid-solar-systems.html"),
    ("Off-Grid Solar Systems", "off-grid-solar-systems.html"),
    ("Solar Panel Installation", "solar-panel-installation.html"),
    ("Solar Inverter Installation", "solar-inverter-installation.html"),
    ("Solar Battery Solutions", "solar-battery-solutions.html"),
    ("All Solar Services", "services.html"),
]
NAV_LOCATIONS = [
    ("Solar Installation in Bahria Town Lahore", "solar-installation-bahria-town-lahore.html"),
    ("Solar Installation in Lahore", "solar-installation-lahore.html"),
]

def header_html(rel, active):
    def cls(page):
        return ' class="active"' if page == active else ""
    svc_items = "\n".join(
        '<li><a href="{rel}{p}">{n}</a></li>'.format(rel=rel, p=p, n=n)
        for n, p in NAV_SERVICES)
    loc_items = "\n".join(
        '<li><a href="{rel}{p}">{n}</a></li>'.format(rel=rel, p=p, n=n)
        for n, p in NAV_LOCATIONS)
    return """<header class="site-header">
  <div class="container header-inner">
    <a class="logo" href="{rel}index.html" aria-label="Solar Installation Bahria Town Lahore — home">
      {logo}
      <span class="logo-text"><span class="name">Solar Installation</span>
      <span class="tag">Bahria Town Lahore</span></span>
    </a>
    <nav class="main-nav" aria-label="Main navigation">
      <ul>
        <li><a href="{rel}index.html"{home}>Home</a></li>
        <li><a href="{rel}about.html"{about}>About Us</a></li>
        <li class="has-sub"><a href="{rel}services.html"{services}>Services</a>
          <ul class="submenu">{svc}</ul>
        </li>
        <li class="has-sub"><a href="{rel}solar-installation-bahria-town-lahore.html"{loc}>Locations</a>
          <ul class="submenu">{locs}</ul>
        </li>
        <li><a href="{rel}projects.html"{projects}>Projects</a></li>
        <li><a href="{rel}blog.html"{blog}>Blog</a></li>
        <li><a href="{rel}contact.html"{contact}>Contact Us</a></li>
      </ul>
    </nav>
    <div class="header-cta">
      <a class="header-phone" href="{tel}">{phone}</a>
      <a class="btn btn-gold btn-sm" href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
      <button class="menu-toggle" id="menuToggle" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="drawer-overlay" id="drawerOverlay"></div>
<aside class="mobile-drawer" id="mobileDrawer" aria-label="Mobile navigation">
  <a href="{rel}index.html">Home</a>
  <a href="{rel}about.html">About Us</a>
  <div class="drawer-group">Services</div>
  {drawer_svc}
  <div class="drawer-group">Locations</div>
  {drawer_loc}
  <a href="{rel}projects.html">Projects</a>
  <a href="{rel}blog.html">Blog</a>
  <a href="{rel}contact.html">Contact Us</a>
  <div class="drawer-group">Get in touch</div>
  <a href="{tel}">Call {phone}</a>
  <a href="{wa}" target="_blank" rel="noopener">Chat on WhatsApp</a>
</aside>""".format(
        rel=rel, logo=LOGO_SVG, tel=PHONE_TEL, phone=PHONE_DISPLAY, wa=WA_LINK,
        home=cls("home"), about=cls("about"), services=cls("services"),
        loc=cls("locations"), projects=cls("projects"), blog=cls("blog"),
        contact=cls("contact"), svc=svc_items, locs=loc_items,
        drawer_svc="\n  ".join(
            '<a href="{rel}{p}">{n}</a>'.format(rel=rel, p=p, n=n) for n, p in NAV_SERVICES),
        drawer_loc="\n  ".join(
            '<a href="{rel}{p}">{n}</a>'.format(rel=rel, p=p, n=n) for n, p in NAV_LOCATIONS))

def footer_html(rel):
    svc_links = "\n".join(
        '          <li><a href="{rel}{p}">{n}</a></li>'.format(rel=rel, p=p, n=n)
        for n, p in NAV_SERVICES[:8])
    return """<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="logo" href="{rel}index.html" aria-label="Solar Installation Bahria Town Lahore — home">
          {logo}
          <span class="logo-text"><span class="name">Solar Installation</span>
          <span class="tag">Bahria Town Lahore</span></span>
        </a>
        <p style="margin-top:16px">A solar energy company providing residential and commercial solar installation services in Bahria Town Lahore — hybrid, on-grid and off-grid solar systems, planned and installed with a professional, customer-focused approach.</p>
        <div class="social-row">
{social}
        </div>
      </div>
      <div>
        <h4>Quick Links</h4>
        <ul class="footer-links">
          <li><a href="{rel}index.html">Home</a></li>
          <li><a href="{rel}about.html">About Us</a></li>
          <li><a href="{rel}projects.html">Our Projects</a></li>
          <li><a href="{rel}blog.html">Blog &amp; Solar Guides</a></li>
          <li><a href="{rel}contact.html">Contact Us</a></li>
          <li><a href="{rel}privacy-policy.html">Privacy Policy</a></li>
          <li><a href="{rel}terms-and-conditions.html">Terms and Conditions</a></li>
        </ul>
      </div>
      <div>
        <h4>Our Services</h4>
        <ul class="footer-links">
{svc_links}
        </ul>
      </div>
      <div>
        <h4>Contact Information</h4>
        <ul class="footer-contact">
          <li><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg><span>{addr}</span></li>
          <li><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.13.96.36 1.9.7 2.8a2 2 0 0 1-.45 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.45c.9.34 1.84.57 2.8.7A2 2 0 0 1 22 16.9z"/></svg><span><a href="{tel}">{phone}</a></span></li>
          <li><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.5 8.5 0 0 1-8.5 8.5c-1.5 0-3-.4-4.2-1.1L3 20l1.1-5.3A8.5 8.5 0 1 1 21 11.5z"/></svg><span><a href="{wa}" target="_blank" rel="noopener">WhatsApp: {phone}</a></span></li>
          <li><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg><span><a href="{gmb}" target="_blank" rel="noopener">View on Google Maps</a></span></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span id="year">2026</span> {biz}. All rights reserved.</span>
      <span><a href="{rel}privacy-policy.html">Privacy Policy</a> &nbsp;·&nbsp; <a href="{rel}terms-and-conditions.html">Terms and Conditions</a></span>
    </div>
  </div>
</footer>
<a class="float-wa" href="{wa}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5.1-1.3A10 10 0 1 0 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.6-6.1c-.3-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1-.2.3-.6.8-.8 1-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-2-1.2 7.5 7.5 0 0 1-1.4-1.7c-.1-.3 0-.4.1-.5l.4-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1.1 2.7c.1.2 1.9 2.9 4.5 4 .6.3 1.1.4 1.5.6.6.2 1.2.2 1.6.1.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.2-.2-.5-.3z"/></svg>
</a>
<button class="back-top" id="backTop" aria-label="Back to top">↑</button>
<div class="mobile-cta">
  <a class="btn btn-gold btn-sm" href="{tel}">Call Now</a>
  <a class="btn btn-blue btn-sm" href="{wa}" target="_blank" rel="noopener">WhatsApp Us</a>
</div>""".format(rel=rel, logo=LOGO_SVG, addr=ADDRESS, tel=PHONE_TEL,
                 phone=PHONE_DISPLAY, wa=WA_LINK, gmb=GMB, biz=BUSINESS,
                 social=social_icons(), svc_links=svc_links)

def cta_band(rel, heading, text):
    return """<section class="section"><div class="container"><div class="cta-band reveal">
  <h2>{h}</h2>
  <p>{t}</p>
  <div class="hero-ctas">
    <a class="btn btn-gold" href="{tel}">Call Now</a>
    <a class="btn btn-outline" href="{wa}" target="_blank" rel="noopener">WhatsApp Us</a>
    <a class="btn btn-blue" href="{rel}contact.html">Get a Consultation</a>
  </div>
</div></div></section>""".format(h=heading, t=text, tel=PHONE_TEL, wa=WA_LINK, rel=rel)

def page(rel, path, title, desc, h1, body, schemas, active, og_image=None,
         crumbs=None, hero_img=None, hero_sub=None, is_home=False):
    """Render one complete HTML page. `rel` is '' for root pages, '../' for blog/."""
    canon = '<link rel="canonical" href="{u}">'.format(u=abs_url(path)) if SITE_URL else ""
    ogurl = '<meta property="og:url" content="{u}">'.format(u=abs_url(path)) if SITE_URL else ""
    ogimg = abs_url(og_image or OG_IMAGE) if SITE_URL else "/" + (og_image or OG_IMAGE)
    schema_tags = "\n".join(
        '  <script type="application/ld+json">\n{js}\n  </script>'.format(
            js=json.dumps(s, indent=2, ensure_ascii=False)) for s in schemas)
    crumb_html = ""
    if crumbs:
        parts = []
        for i, (name, p) in enumerate(crumbs):
            if p and i < len(crumbs) - 1:
                parts.append('<a href="{rel}{p}">{n}</a>'.format(rel=rel, p=p, n=name))
            else:
                parts.append('<span aria-current="page">{n}</span>'.format(n=name))
        crumb_html = ('<nav class="breadcrumbs" aria-label="Breadcrumb">' +
                      '<span class="sep">›</span> '.join(parts) + '</nav>')
    if is_home:
        hero = body  # home page supplies its own hero section
        main_open = '<main>'
    else:
        hero_img_tag = ""
        if hero_img:
            hero_img_tag = ('<div class="hero-bg"><img src="{rel}{img}" alt="{alt}" '
                            'loading="lazy"></div>'.format(rel=rel, img=hero_img, alt=h1))
        hero = """<section class="page-hero">
  {img}
  <div class="container" style="position:relative;z-index:1">
    {crumbs}
    <h1>{h1}</h1>
    {sub}
  </div>
</section>
<main>""".format(img=hero_img_tag, crumbs=crumb_html, h1=h1,
                 sub=('<p>{}</p>'.format(hero_sub) if hero_sub else ""))
        body = hero + body
        main_open = ""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow">
  {canon}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{biz}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  {ogurl}
  <meta property="og:image" content="{ogimg}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{ogimg}">
  <link rel="icon" type="image/svg+xml" href="{rel}favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@500;600;700&family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{rel}assets/css/style.css">
{schema}
</head>
<body>
{header}
{main_open}
{body}
</main>
{footer}
<script src="{rel}assets/js/main.js" defer></script>
</body>
</html>""".format(title=title, desc=desc, canon=canon, biz=BUSINESS, ogurl=ogurl,
                  ogimg=ogimg, rel=rel, schema=schema_tags, header=header_html(rel, active),
                  main_open=main_open, body=body, footer=footer_html(rel))
    return html

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return path

# ============================================================ FAQ data ===
FAQS = [
    ("What is the cost of solar installation in Bahria Town Lahore?",
     "The cost depends on the size of the system, the type of system (hybrid, on-grid or off-grid), "
     "the panels, inverter and batteries selected, and the condition of the property and roof. "
     "Because every home and business is different, there is no single fixed price. Contact us for a "
     "free consultation and we will discuss your requirements and prepare a plan for your property."),
    ("Which solar system is suitable for a 5 Marla house?",
     "There is no one-size-fits-all answer for a 5 Marla house. The right system depends on your "
     "electricity usage, the appliances you run, your roof space and whether you want battery backup. "
     "During a consultation we review your load and usage pattern and then suggest a system size that "
     "fits your home. Contact us on WhatsApp or by phone to discuss your 5 Marla home."),
    ("Which solar system is suitable for a 10 Marla house?",
     "A 10 Marla house usually has more rooms and appliances, so the system is planned around your "
     "actual load — air conditioning, water motors, kitchen appliances and lighting all matter. "
     "We assess your property and energy needs first, then recommend a hybrid, on-grid or off-grid "
     "configuration that suits your home. A consultation is the right starting point."),
    ("What is the difference between hybrid and on-grid solar?",
     "An on-grid solar system is connected to the electricity grid. It generates solar power during "
     "the day and can export extra energy to the grid where net metering is available. It does not "
     "store energy, so it does not provide power during a grid outage on its own. A hybrid system "
     "combines solar panels with an inverter and battery storage, so it can store energy and keep "
     "essential loads running during outages, depending on the battery capacity and the loads connected."),
    ("How many solar panels are needed for a home?",
     "The number of panels depends on your daily electricity consumption, the capacity of the panels "
     "chosen, and the usable roof space available. A small home with modest usage needs fewer panels "
     "than a larger home with heavy appliances. We calculate this from your load and roof assessment "
     "rather than guessing a number in advance."),
    ("What is the purpose of solar batteries?",
     "Solar batteries store the energy your panels generate during the day so it can be used in the "
     "evening or during a power outage. They are a core part of hybrid and off-grid systems. Battery "
     "size and type are chosen according to how much backup you need and which appliances you want to "
     "run from stored energy."),
    ("How can I contact a solar installation company in Bahria Town Lahore?",
     "You can call or WhatsApp us on 03200147783, visit our office at C, Plaza 210, 1st Floor, "
     "Sector C, Sector Tulip Commercial B, Sector C, Bahria Town, Lahore, or use the contact form "
     "on this website — your enquiry opens in WhatsApp so you can send it directly to us."),
    ("How do I request a solar installation consultation?",
     "Simply call 03200147783, send us a WhatsApp message, or fill in the contact form with your "
     "name, phone number, property type and the solar system you are interested in. We will then "
     "discuss your requirements and arrange the next step, starting with a property and energy assessment."),
]

def faq_html(faqs):
    items = []
    for q, a in faqs:
        items.append(
            '<div class="faq-item"><button class="faq-q" aria-expanded="false">'
            '<span>{q}</span><span class="chev">+</span></button>'
            '<div class="faq-a"><p>{a}</p></div></div>'.format(q=q, a=a))
    return '<div class="faq">\n' + "\n".join(items) + "\n</div>"

# ====================================================== shared snippets ===
def service_card(rel, title, img, alt, desc, link):
    return """<article class="card service-card reveal">
  <div class="thumb"><img src="{rel}{img}" alt="{alt}" loading="lazy"></div>
  <div class="body"><h3>{t}</h3><p>{d}</p>
  <a class="card-link" href="{rel}{link}">Learn More →</a></div>
</article>""".format(rel=rel, img=img, alt=alt, t=title, d=desc, link=link)

def trust_cards():
    return """<div class="grid grid-4">
  <div class="card reveal"><div class="icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M9 20v-6h6v6"/></svg></div><h3>Residential Solar Solutions</h3><p>Solar systems planned around your home, your roof and the way your family uses electricity.</p></div>
  <div class="card reveal"><div class="icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="7" width="18" height="13" rx="1"/><path d="M7 7V4h10v3M7 11h2m3 0h2m3 0h2M7 15h2m3 0h2m3 0h2"/></svg></div><h3>Commercial Solar Solutions</h3><p>Solar planning for shops, offices and commercial properties in Bahria Town Lahore.</p></div>
  <div class="card reveal"><div class="icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M13 2L4.5 13.5H11L9.5 22 19 10h-6.5L13 2z"/></svg></div><h3>Hybrid Solar Systems</h3><p>Solar generation combined with grid connection and battery storage, configured to your needs.</p></div>
  <div class="card reveal"><div class="icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1"/></svg></div><h3>Professional Solar Installation</h3><p>Careful installation and configuration by a team that treats your property with respect.</p></div>
</div>"""

GALLERY = [
    ("modern-house-flat-roof-solar.jpg", "Modern home with rooftop solar panels", "Residential", "residential"),
    ("residential-rooftop-solar-panels.jpg", "Residential rooftop solar panel array", "Residential", "residential"),
    ("aerial-home-solar-panels.jpg", "Aerial view of a home with rooftop solar", "Residential", "residential"),
    ("rooftop-solar-panels-house.jpg", "Large rooftop solar array at sunset", "Commercial", "commercial"),
    ("commercial-rooftop-solar-panels.jpg", "Commercial rooftop solar installation", "Commercial", "commercial"),
    ("solar-installer-rooftop-work.jpg", "Installer working on a rooftop solar array", "Installation", "installation"),
    ("hybrid-inverter-battery-system.jpg", "Hybrid inverter with battery storage", "Hybrid Systems", "hybrid"),
    ("solar-inverter-battery-wall.jpg", "Wall-mounted solar inverter and battery", "Hybrid Systems", "hybrid"),
    ("solar-panel-mounting-structure.jpg", "Solar panel mounting structure", "Installation", "installation"),
]

def gallery_html(rel):
    figs = []
    for img, cap, cat, code in GALLERY:
        figs.append(
            '<figure data-cat="{code}"><img src="{rel}assets/images/{img}" alt="{cap} — illustrative image" '
            'loading="lazy" data-full="{rel}assets/images/{img}">'
            '<figcaption>{cap}<small>Illustrative image</small></figcaption></figure>'
            .format(rel=rel, img=img, cap=cap, code=code))
    return """<div class="gallery-filters" role="group" aria-label="Filter projects">
  <button class="filter-btn active" data-filter="all">All</button>
  <button class="filter-btn" data-filter="residential">Residential</button>
  <button class="filter-btn" data-filter="commercial">Commercial</button>
  <button class="filter-btn" data-filter="hybrid">Hybrid Systems</button>
  <button class="filter-btn" data-filter="installation">Installation</button>
</div>
<div class="gallery">
{figs}
</div>
<p class="illustrative-note">The images in this gallery are illustrative examples of solar installations. Only photographs of our own completed work, once verified, will be published as company projects.</p>
<div class="lightbox" id="lightbox" role="dialog" aria-label="Image viewer">
  <button class="lb-close" id="lbClose" aria-label="Close image viewer">×</button>
  <img id="lbImg" src="" alt="">
  <div class="lb-cap" id="lbCap"></div>
</div>""".format(figs="\n".join(figs))

# ============================================================== HOME ======
def build_home():
    rel = ""
    svc = [
        ("Residential Solar Installation", "assets/images/residential-rooftop-solar-panels.jpg",
         "Residential rooftop solar panel array", "Solar systems for houses in Bahria Town — planned around your load, roof and daily usage.", "residential-solar-installation.html"),
        ("Commercial Solar Installation", "assets/images/commercial-rooftop-solar-panels.jpg",
         "Commercial rooftop solar installation", "Solar planning for shops, offices and commercial buildings across Bahria Town Lahore.", "commercial-solar-installation.html"),
        ("Hybrid Solar Systems", "assets/images/hybrid-inverter-battery-system.jpg",
         "Hybrid inverter with battery storage", "Solar panels, inverter and battery storage working together for day and night use.", "hybrid-solar-systems.html"),
        ("On-Grid Solar Systems", "assets/images/solar-panels-field-sunset.jpg",
         "Solar panels in a field at sunset", "Grid-connected solar systems that generate power during the day and work with the grid.", "on-grid-solar-systems.html"),
        ("Off-Grid Solar Systems", "assets/images/solar-array-field.jpg",
         "Solar panel array in an open field", "Independent solar systems with battery storage for properties without a reliable grid connection.", "off-grid-solar-systems.html"),
        ("Solar Panel Installation", "assets/images/solar-panel-installation-worker.jpg",
         "Installer fitting a solar panel on a roof", "Professional panel mounting and installation, positioned for your roof and sun exposure.", "solar-panel-installation.html"),
        ("Solar Inverter Installation", "assets/images/solar-inverter-battery-wall.jpg",
         "Wall-mounted solar inverter and battery", "Inverter selection, installation and configuration for your system type and load.", "solar-inverter-installation.html"),
        ("Solar Battery Storage Solutions", "assets/images/solar-inverter-battery-wall.jpg",
         "Solar battery storage with inverters", "Battery storage that keeps essential power available when the sun goes down or the grid is off.", "solar-battery-solutions.html"),
    ]
    cards = "\n".join(service_card(rel, t, i, a, d, l) for t, i, a, d, l in svc)
    body = """<section class="hero">
  <div class="hero-bg"><img src="assets/images/modern-house-flat-roof-solar.jpg" alt="Modern luxury house in Bahria Town Lahore with premium rooftop solar panels" fetchpriority="high"></div>
  <div class="container hero-inner">
    <span class="eyebrow">Solar Energy Company · Bahria Town Lahore</span>
    <h1>Solar Installation in <span>Bahria Town Lahore</span></h1>
    <p class="sub">Premium Solar Energy Solutions for Homes and Businesses</p>
    <p class="desc">Discover reliable solar energy solutions with professional solar installation services in Bahria Town Lahore. Explore hybrid, on-grid and off-grid solar systems designed to help residential and commercial properties make better use of solar energy.</p>
    <div class="hero-ctas">
      <a class="btn btn-gold" href="contact.html">Get a Free Consultation</a>
      <a class="btn btn-outline" href="{wa}" target="_blank" rel="noopener">Chat on WhatsApp</a>
    </div>
    <ul class="hero-points">
      <li><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M20 6L9 17l-5-5"/></svg> Residential &amp; commercial solar</li>
      <li><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M20 6L9 17l-5-5"/></svg> Hybrid, on-grid &amp; off-grid systems</li>
      <li><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M20 6L9 17l-5-5"/></svg> Local team in Bahria Town Lahore</li>
    </ul>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">What We Do</span>
      <h2>Solar Solutions for Every Property</h2>
      <p>From a family home to a commercial building, we plan solar around your property — not the other way round.</p>
    </div>
    {trust}
  </div>
</section>
<section class="section alt">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">About Our Business</span>
      <h2>Your Local Solar Installation Partner in Bahria Town Lahore</h2>
      <hr class="gold-rule">
      <p>Solar energy is one of the most practical ways for a home or business in Lahore to take control of its electricity. With long sunny days for much of the year, a well-planned rooftop system can turn unused roof space into a working source of power.</p>
      <p>We are a solar energy company based in Bahria Town Lahore. We work with homeowners and businesses across the community — from Sector A to Sector F — helping them understand their options, plan a system that fits their property, and install it properly.</p>
      <p>Our work covers residential solar systems, commercial solar solutions, careful system planning and professional installation. Every project starts with a conversation about how you actually use electricity, because a system planned around real usage performs better than one chosen from a catalogue.</p>
      <p>Visit us at Plaza 210, 1st Floor, Sector C, Tulip Commercial, Bahria Town, Lahore, or call / WhatsApp <a href="{tel}">{phone}</a> to start with a free consultation.</p>
      <a class="btn btn-gold" href="about.html">More About Us</a>
    </div>
    <div class="img-frame reveal"><img src="assets/images/modern-villa-solar-panels-pool.jpg" alt="Modern villa with rooftop solar panels" loading="lazy"></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Our Solar Services</span>
      <h2>Complete Solar Installation Services</h2>
      <p>Panels, inverters, batteries and full system planning — everything your property needs, in one place.</p>
    </div>
    <div class="grid grid-3">
{cards}
    </div>
  </div>
</section>
<section class="section alt">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Choose Your System</span>
      <h2>Hybrid, On-Grid or Off-Grid — <span>Which Fits You?</span></h2>
      <p>Each system type works differently. Here is an honest comparison to help you understand your options before you decide.</p>
    </div>
    <div class="grid grid-3">
      <div class="card compare-card reveal">
        <span class="tag">Most Flexible</span>
        <h3>Hybrid Solar System</h3>
        <p>Solar generation combined with a grid connection and battery storage, depending on the system configuration.</p>
        <ul>
          <li class="pro">Stores daytime energy in batteries for evening use</li>
          <li class="pro">Can keep essential loads running during outages</li>
          <li class="pro">Works with the grid when solar is not enough</li>
          <li class="con">Higher upfront cost than on-grid alone</li>
          <li class="con">Battery capacity limits how much backup you get</li>
        </ul>
        <p class="lim">Best for: homes and businesses that want backup power as well as daytime solar generation.</p>
        <a class="card-link" href="hybrid-solar-systems.html">Learn More →</a>
      </div>
      <div class="card compare-card reveal">
        <span class="tag">Grid Connected</span>
        <h3>On-Grid Solar System</h3>
        <p>A grid-connected solar system that generates electricity during the day and works together with the electricity grid.</p>
        <ul>
          <li class="pro">Straightforward design with fewer components</li>
          <li class="pro">Can export extra daytime energy where net metering applies</li>
          <li class="pro">Lower upfront cost than a hybrid system</li>
          <li class="con">No stored energy for use at night</li>
          <li class="con">Does not power your home during a grid outage on its own</li>
        </ul>
        <p class="lim">Best for: properties with a stable grid connection that mainly want daytime solar generation.</p>
        <a class="card-link" href="on-grid-solar-systems.html">Learn More →</a>
      </div>
      <div class="card compare-card reveal">
        <span class="tag">Fully Independent</span>
        <h3>Off-Grid Solar System</h3>
        <p>An independent solar system with battery storage, designed to operate without a grid connection.</p>
        <ul>
          <li class="pro">Works where there is no grid connection at all</li>
          <li class="pro">Full control over your own power supply</li>
          <li class="pro">Battery storage covers night-time use</li>
          <li class="con">Needs careful sizing — the system is your only source</li>
          <li class="con">Larger battery banks are needed for cloudy stretches</li>
        </ul>
        <p class="lim">Best for: properties without a reliable grid connection, or where full independence is the goal.</p>
        <a class="card-link" href="off-grid-solar-systems.html">Learn More →</a>
      </div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Why Choose Us</span>
      <h2>Why Choose Solar Installation Bahria Town Lahore?</h2>
    </div>
    <div class="grid grid-4">
      <div class="card reveal"><h3>Location-Focused Solar</h3><p>We work in Bahria Town Lahore every day, so we understand its houses, roofs and neighbourhoods.</p></div>
      <div class="card reveal"><h3>Residential &amp; Commercial</h3><p>From family homes to shops and offices — systems planned for each property type.</p></div>
      <div class="card reveal"><h3>Customised System Planning</h3><p>Your system is sized from your actual load and usage, not from a standard package.</p></div>
      <div class="card reveal"><h3>Professional Installation</h3><p>Careful mounting, wiring and configuration, finished with a proper handover.</p></div>
      <div class="card reveal"><h3>Modern Solar Technologies</h3><p>Current panels, inverters and battery options, explained in plain language.</p></div>
      <div class="card reveal"><h3>Customer-Focused Consultation</h3><p>We listen first, then recommend — and we explain the trade-offs honestly.</p></div>
      <div class="card reveal"><h3>Solar System Guidance</h3><p>Clear guidance on system types, net metering and what to expect after installation.</p></div>
      <div class="card reveal"><h3>Convenient Local Contact</h3><p>An office in Sector C, Tulip Commercial — call, WhatsApp or walk in.</p></div>
    </div>
  </div>
</section>
<section class="section alt">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Our Projects</span>
      <h2>Solar Installations, Up Close</h2>
      <p>A look at the kinds of installations we work on — residential rooftops, commercial roofs, hybrid systems and battery storage.</p>
    </div>
{gallery}
    <div style="text-align:center;margin-top:34px"><a class="btn btn-outline" href="projects.html">View Full Portfolio</a></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">How We Work</span>
      <h2>Our Work Process</h2>
      <p>Five clear steps from your first message to a working solar system.</p>
    </div>
    <div class="grid grid-3 steps">
      <div class="card step reveal"><div class="num">01</div><h3>Initial Consultation</h3><p>We talk about your property, your electricity usage and what you want from solar — by phone, WhatsApp or in person.</p></div>
      <div class="card step reveal"><div class="num">02</div><h3>Property &amp; Energy Assessment</h3><p>We look at your roof, your load and your daily usage pattern to understand what your property really needs.</p></div>
      <div class="card step reveal"><div class="num">03</div><h3>Solar System Planning</h3><p>We plan the system — panels, inverter, batteries and layout — matched to your property and your priorities.</p></div>
      <div class="card step reveal"><div class="num">04</div><h3>Installation &amp; Configuration</h3><p>Our team installs the system carefully and configures it so it runs the way it was planned.</p></div>
      <div class="card step reveal"><div class="num">05</div><h3>System Handover &amp; Guidance</h3><p>We walk you through your system, explain how it works and how to look after it, and answer your questions.</p></div>
      <div class="card step reveal"><div class="num">✦</div><h3>After Installation</h3><p>Need help later? Contact us on <a href="{tel}">{phone}</a> — we are a local business and we stay reachable.</p></div>
    </div>
  </div>
</section>
<section class="section alt">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Service Areas</span>
      <h2>Solar Installation Services in Bahria Town Lahore</h2>
      <hr class="gold-rule">
      <p>We provide solar installation services across Bahria Town Lahore, including residential and commercial properties in every sector of the community. Our office in Sector C, Tulip Commercial, keeps us close to the homes and businesses we serve.</p>
      <ul class="chips">
        <li>Solar Installation in Bahria Town Lahore</li>
        <li>Solar Company in Bahria Town Lahore</li>
        <li>Solar Panels in Bahria Town Lahore</li>
        <li>Solar Installation in Sector A Bahria Town</li>
        <li>Solar Installation in Sector B Bahria Town</li>
        <li>Solar Installation in Sector C Bahria Town</li>
        <li>Solar Installation in Sector D Bahria Town</li>
        <li>Solar Installation in Sector E Bahria Town</li>
        <li>Solar Installation in Sector F Bahria Town</li>
      </ul>
      <p>These are service areas, not separate offices — one local team, one office, serving the whole of Bahria Town Lahore and the wider Lahore area.</p>
      <a class="btn btn-gold" href="solar-installation-bahria-town-lahore.html">Bahria Town Solar Services</a>
    </div>
    <div class="img-frame reveal"><img src="assets/images/solar-panels-field-sunset.jpg" alt="Solar panels at sunset in a field" loading="lazy"></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Solar Education</span>
      <h2>Learn Before You Decide</h2>
      <p>Short, honest guides that explain how solar works and how to choose the right system for your home.</p>
    </div>
    <div class="grid grid-4">
      <div class="card reveal"><h3>How Solar Energy Works</h3><p>Panels, inverters and the journey from sunlight to the sockets in your home.</p><a class="card-link" href="blog/how-solar-energy-works.html">Read the Guide →</a></div>
      <div class="card reveal"><h3>Hybrid vs On-Grid Solar</h3><p>The real differences between the two most common system types — and who each suits.</p><a class="card-link" href="blog/hybrid-vs-on-grid-solar-systems.html">Read the Guide →</a></div>
      <div class="card reveal"><h3>How to Choose Solar Panels</h3><p>What actually matters when comparing panels — beyond the brochure.</p><a class="card-link" href="blog/how-to-choose-solar-panels.html">Read the Guide →</a></div>
      <div class="card reveal"><h3>Solar Battery Storage Explained</h3><p>What batteries do, what they cannot do, and how to think about backup.</p><a class="card-link" href="blog/solar-battery-storage-explained.html">Read the Guide →</a></div>
    </div>
    <div style="text-align:center;margin-top:34px"><a class="btn btn-outline" href="blog.html">Visit the Blog</a></div>
  </div>
</section>
<section class="section alt">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Customer Feedback</span>
      <h2>What Our Customers Say</h2>
    </div>
    <div class="testi-invite reveal">
      <div class="stars" aria-hidden="true">★★★★★</div>
      <h3 style="margin-bottom:10px">Share Your Experience With Us</h3>
      <p>We are building our collection of customer feedback. If you have had solar installed with us, we would love to hear how it is working for you. Your honest feedback helps other homeowners in Bahria Town Lahore make confident decisions.</p>
      <p style="margin-bottom:22px">Only genuine, verified customer reviews are published here — never invented testimonials.</p>
      <a class="btn btn-gold" href="{wa}" target="_blank" rel="noopener">Share Your Feedback on WhatsApp</a>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Good to Know</span>
      <h2>Frequently Asked Questions</h2>
      <p>Straight answers to the questions we hear most often in Bahria Town Lahore.</p>
    </div>
    {faq}
  </div>
</section>
""".format(wa=WA_LINK, tel=PHONE_TEL, phone=PHONE_DISPLAY, trust=trust_cards(),
            cards=cards, gallery=gallery_html(rel), faq=faq_html(FAQS))
    body += cta_band(rel, "Ready to Explore Solar Energy for Your Property?",
                     "Contact Solar Installation Bahria Town Lahore to discuss your residential or commercial solar requirements.")
    schemas = [org_ld(), local_ld(), website_ld(), faq_ld(FAQS),
               breadcrumb_ld([("Home", None)])]
    return page(rel, "index.html",
                "Solar Installation in Bahria Town Lahore | Solar Installation Bahria Town Lahore",
                "Premium solar installation services in Bahria Town Lahore — residential & commercial solar, hybrid, on-grid and off-grid systems. Free consultation: 03200147783.",
                "Solar Installation in Bahria Town Lahore", body, schemas, "home", is_home=True)

# ============================================================== ABOUT =====
def build_about():
    rel = ""
    body = """<section class="section">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">About Us</span>
      <h2>A Local Solar Company With a Simple Goal</h2>
      <hr class="gold-rule">
      <p>Solar Installation Bahria Town Lahore is a solar energy company based in Bahria Town Lahore. Our goal is simple: help the homes and businesses around us make good use of the sun that shines on their roofs every day.</p>
      <p>We believe solar works best when it is planned properly. A system should match the property it serves — its roof, its wiring, and the way the people inside use electricity. That is why every project we take on starts with listening and assessment, not with a pre-made package.</p>
      <p>We work with homeowners, shop owners and commercial property owners across Bahria Town Lahore, and we take pride in doing careful, honest work. If a system type does not suit your situation, we will say so and explain why.</p>
    </div>
    <div class="img-frame reveal"><img src="assets/images/aerial-home-solar-panels.jpg" alt="Aerial view of a home with rooftop solar panels" loading="lazy"></div>
  </div>
</section>
<section class="section alt">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Why Solar Matters</span>
      <h2>Why Solar Energy Makes Sense in Lahore</h2>
      <p>Lahore receives strong sunlight for most of the year. For a home with a usable roof, that sunlight is a resource that is otherwise wasted. A solar system turns it into electricity for daily use — lights, fans, cooling, water motors and the appliances a modern household depends on.</p>
    </div>
    <div class="grid grid-3">
      <div class="card reveal"><h3>Use Your Own Roof</h3><p>Most homes in Bahria Town have flat or sloped roofs with good sun exposure. A rooftop system uses space that is already there.</p></div>
      <div class="card reveal"><h3>Daytime Generation</h3><p>Solar panels generate electricity during the day, when many homes and businesses use power the most.</p></div>
      <div class="card reveal"><h3>Backup With Batteries</h3><p>With a hybrid system and battery storage, stored energy can keep essential loads running when the grid is down.</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container split">
    <div class="img-frame reveal"><img src="assets/images/solar-installer-rooftop-work.jpg" alt="Solar installer working on a rooftop array" loading="lazy"></div>
    <div class="reveal">
      <span class="eyebrow">How We Work</span>
      <h2>Residential, Commercial — Planned, Not Packaged</h2>
      <hr class="gold-rule">
      <p><strong>Residential solar systems.</strong> We plan systems for houses of every size in Bahria Town, from smaller homes to large residences. The plan starts with your load — what you run, and when — and your roof.</p>
      <p><strong>Commercial solar solutions.</strong> For shops, offices and commercial buildings, we look at daytime usage patterns and roof space, and plan a system that fits the way the business operates.</p>
      <p><strong>System planning.</strong> Panels, inverters and batteries are chosen together, as one system. A panel is only as useful as the inverter behind it, and a battery is only as useful as the loads it is sized to carry.</p>
      <p><strong>Professional installation.</strong> Mounting, wiring and configuration are done carefully, and every system is handed over with a clear explanation of how it works and how to look after it.</p>
    </div>
  </div>
</section>
<section class="section alt">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Visit Us</span>
      <h2>Our Office in Bahria Town Lahore</h2>
      <p>We are easy to reach — in person, by phone or on WhatsApp.</p>
    </div>
    <div class="grid grid-3">
      <div class="card reveal"><h3>Our Address</h3><p>{addr}</p></div>
      <div class="card reveal"><h3>Call or WhatsApp</h3><p><a href="{tel}">{phone}</a><br>Call or message us for a free consultation.</p></div>
      <div class="card reveal"><h3>Google Business Profile</h3><p><a href="{gmb}" target="_blank" rel="noopener">View our profile on Google Maps</a><br>Find directions and our business details.</p></div>
    </div>
  </div>
</section>
""".format(addr=ADDRESS, tel=PHONE_TEL, phone=PHONE_DISPLAY, gmb=GMB)
    body += cta_band(rel, "Ready to Explore Solar Energy for Your Property?",
                     "Contact Solar Installation Bahria Town Lahore to discuss your residential or commercial solar requirements.")
    schemas = [org_ld(), local_ld(),
               breadcrumb_ld([("Home", "index.html"), ("About Us", None)])]
    return page(rel, "about.html",
                "About Us | Solar Installation Bahria Town Lahore",
                "About Solar Installation Bahria Town Lahore — a local solar energy company providing residential and commercial solar installation, system planning and professional installation.",
                "About Us", body, schemas, "about",
                hero_img="assets/images/aerial-home-solar-panels.jpg",
                hero_sub="A local solar energy company in Bahria Town Lahore, helping homes and businesses make better use of solar energy.",
                crumbs=[("Home", "index.html"), ("About Us", None)])

# =========================================================== SERVICES =====
def build_services():
    rel = ""
    cards = [
        ("Residential Solar Installation", "assets/images/residential-rooftop-solar-panels.jpg",
         "Residential rooftop solar panel array", "Solar systems for houses — planned around your load, roof and daily usage.", "residential-solar-installation.html"),
        ("Commercial Solar Installation", "assets/images/commercial-rooftop-solar-panels.jpg",
         "Commercial rooftop solar installation", "Solar planning for shops, offices and commercial buildings.", "commercial-solar-installation.html"),
        ("Hybrid Solar Systems", "assets/images/hybrid-inverter-battery-system.jpg",
         "Hybrid inverter with battery storage", "Solar, grid and battery storage working together.", "hybrid-solar-systems.html"),
        ("On-Grid Solar Systems", "assets/images/solar-panels-field-sunset.jpg",
         "Solar panels in a field at sunset", "Grid-connected systems for daytime solar generation.", "on-grid-solar-systems.html"),
        ("Off-Grid Solar Systems", "assets/images/solar-array-field.jpg",
         "Solar panel array in an open field", "Independent systems with battery storage.", "off-grid-solar-systems.html"),
        ("Solar Panel Installation", "assets/images/solar-panel-installation-worker.jpg",
         "Installer fitting a solar panel on a roof", "Professional panel mounting and installation.", "solar-panel-installation.html"),
        ("Solar Inverter Installation", "assets/images/solar-inverter-battery-wall.jpg",
         "Wall-mounted solar inverter and battery", "Inverter selection, installation and configuration.", "solar-inverter-installation.html"),
        ("Solar Battery Storage Solutions", "assets/images/solar-inverter-battery-wall.jpg",
         "Solar battery storage with inverters", "Battery storage for evenings and outages.", "solar-battery-solutions.html"),
    ]
    body = """<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">What We Offer</span>
      <h2>Solar Installation Services in Bahria Town Lahore</h2>
      <p>Every service below is planned around your property and delivered by our local team. Choose a service to learn more, or contact us and we will help you decide.</p>
    </div>
    <div class="grid grid-3">
{cards}
    </div>
  </div>
</section>
<section class="section alt">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">How a Project Works</span>
      <h2>From First Call to Handover</h2>
      <hr class="gold-rule">
      <p>Every service follows the same careful process: consultation, property and energy assessment, system planning, installation and configuration, then handover with guidance. You always know what is happening and why.</p>
      <p>If you are unsure which service fits your property, start with a free consultation — we will ask the right questions and point you to the right option, even if that option is to wait.</p>
      <a class="btn btn-gold" href="contact.html">Get a Free Consultation</a>
    </div>
    <div class="img-frame reveal"><img src="assets/images/solar-panel-installation-worker.jpg" alt="Solar installer fitting panels on a roof" loading="lazy"></div>
  </div>
</section>
""".format(cards="\n".join(service_card(rel, t, i, a, d, l) for t, i, a, d, l in cards))
    body += cta_band(rel, "Not Sure Which Service You Need?",
                     "Tell us about your property and how you use electricity — we will help you choose the right solar solution.")
    schemas = [org_ld(), breadcrumb_ld([("Home", "index.html"), ("Services", None)])]
    return page(rel, "services.html",
                "Solar Installation Services | Solar Installation Bahria Town Lahore",
                "Solar installation services in Bahria Town Lahore — residential & commercial solar, hybrid, on-grid and off-grid systems, panel, inverter and battery installation.",
                "Solar Installation Services", body, schemas, "services",
                hero_img="assets/images/solar-panel-installation-worker.jpg",
                hero_sub="Residential and commercial solar services, planned around your property and installed by a local professional team.",
                crumbs=[("Home", "index.html"), ("Services", None)])

# ------------------------------------------------- service page factory ---
def service_page(rel, slug, title, desc, h1, hero_img, hero_sub, intro_html,
                 bullets, extra_html, related):
    bullets_html = "\n".join("<li>{}</li>".format(b) for b in bullets)
    rel_links = "\n".join(
        '<a class="card-link" href="{rel}{p}">{n} →</a><br>'.format(rel=rel, p=p, n=n)
        for n, p in related)
    body = """<section class="section">
  <div class="container split">
    <div class="reveal">
      {intro}
      <ul class="check-list">
{bullets}
      </ul>
    </div>
    <div class="img-frame reveal"><img src="{rel}{img}" alt="{h1}" loading="lazy"></div>
  </div>
</section>
{extra}
<section class="section alt">
  <div class="container">
    <div class="section-head left reveal">
      <span class="eyebrow">Related Services</span>
      <h2>Explore More Solar Solutions</h2>
    </div>
    <p class="reveal">{links}</p>
  </div>
</section>
""".format(intro=intro_html, bullets=bullets_html, rel=rel, img=hero_img, h1=h1,
           extra=extra_html, links=rel_links)
    body += cta_band(rel, "Ready to Explore Solar Energy for Your Property?",
                     "Contact Solar Installation Bahria Town Lahore to discuss your residential or commercial solar requirements.")
    schemas = [org_ld(), service_ld(title.split(" | ")[0], desc, slug),
               breadcrumb_ld([("Home", "index.html"), ("Services", "services.html"), (h1, None)])]
    return page(rel, slug, title, desc, h1, body, schemas, "services",
                hero_img=hero_img, hero_sub=hero_sub,
                crumbs=[("Home", "index.html"), ("Services", "services.html"), (h1, None)])

def build_service_pages():
    rel = ""
    pages = {}
    pages["residential-solar-installation.html"] = service_page(
        rel, "residential-solar-installation.html",
        "Residential Solar Installation Bahria Town Lahore | Solar Installation Bahria Town Lahore",
        "Residential solar installation in Bahria Town Lahore — solar systems for houses planned around your load, roof and daily usage. Free consultation: 03200147783.",
        "Residential Solar Installation",
        "assets/images/residential-rooftop-solar-panels.jpg",
        "Solar for your home in Bahria Town Lahore — planned around your family, your roof and the way you use electricity.",
        """<span class="eyebrow">For Homeowners</span>
      <h2>Solar That Fits Your Home, Not a Catalogue</h2>
      <hr class="gold-rule">
      <p>Every house in Bahria Town is different — different roof, different rooms, different appliances, different daily routine. A residential solar system should be planned around all of that, not bought off a shelf.</p>
      <p>We start by understanding how your household uses electricity: cooling in summer, heating in winter, water motors, kitchen appliances, lighting and the devices your family relies on. Then we look at your roof — its size, orientation and shading — and plan a system that fits.</p>
      <p>Whether you are considering a hybrid system with battery backup, a straightforward on-grid system, or a fully off-grid setup, we explain the options in plain language and help you choose what suits your home.</p>""",
        ["System sized from your actual household load",
         "Panels positioned for your roof and sun exposure",
         "Hybrid, on-grid or off-grid options explained clearly",
         "Battery storage available where backup matters to you",
         "Professional installation with a proper handover"],
        """<section class="section alt"><div class="container"><div class="section-head left reveal">
      <span class="eyebrow">Good to Know</span>
      <h2>What We Look At Before Recommending a System</h2></div>
      <div class="grid grid-3">
        <div class="card reveal"><h3>Your Daily Usage</h3><p>When you use power matters as much as how much you use. Daytime-heavy usage suits solar generation directly; evening-heavy usage points towards battery storage.</p></div>
        <div class="card reveal"><h3>Your Roof</h3><p>Roof size, direction and shading decide how many panels fit and how well they will perform. We assess this during the property visit.</p></div>
        <div class="card reveal"><h3>Your Priorities</h3><p>Some homeowners want backup during outages; others want the simplest daytime system. Your priorities shape the recommendation.</p></div>
      </div></div></section>""",
        [("Hybrid Solar Systems", "hybrid-solar-systems.html"),
         ("Solar Panel Installation", "solar-panel-installation.html"),
         ("Solar Battery Solutions", "solar-battery-solutions.html"),
         ("All Solar Services", "services.html")])
    pages["commercial-solar-installation.html"] = service_page(
        rel, "commercial-solar-installation.html",
        "Commercial Solar Installation Bahria Town Lahore | Solar Installation Bahria Town Lahore",
        "Commercial solar installation in Bahria Town Lahore — solar planning for shops, offices and commercial buildings. Free consultation: 03200147783.",
        "Commercial Solar Installation",
        "assets/images/commercial-rooftop-solar-panels.jpg",
        "Solar for shops, offices and commercial properties in Bahria Town Lahore — planned around how your business actually uses power.",
        """<span class="eyebrow">For Businesses</span>
      <h2>Solar That Works the Way Your Business Works</h2>
      <hr class="gold-rule">
      <p>Commercial properties use electricity differently from homes. Shops and offices run their heaviest loads during the day — lighting, cooling, computers, machinery — which is exactly when solar panels generate.</p>
      <p>We plan commercial systems around your business hours, your daytime load and your roof space. A shop in Tulip Commercial and an office in Sector C have different needs, and the system should reflect that.</p>
      <p>We work with commercial property owners across Bahria Town Lahore, from single shops to larger buildings, and we keep the process straightforward: assessment, planning, installation and handover.</p>""",
        ["Daytime load analysis for your business hours",
         "Roof and structure assessment for commercial buildings",
         "Hybrid and on-grid options for commercial use",
         "Battery storage where backup is important",
         "Clear planning and a professional installation"],
        """<section class="section alt"><div class="container"><div class="section-head left reveal">
      <span class="eyebrow">For Your Business</span>
      <h2>What a Commercial Assessment Covers</h2></div>
      <div class="grid grid-3">
        <div class="card reveal"><h3>Business Hours &amp; Load</h3><p>We look at when your business uses power and which equipment draws the most, so the system is sized to your working day.</p></div>
        <div class="card reveal"><h3>Roof Space</h3><p>Commercial roofs vary widely. We measure the usable area and check orientation and shading before recommending a layout.</p></div>
        <div class="card reveal"><h3>Future Growth</h3><p>If your business may expand, we discuss how the system could grow with it — planning ahead is cheaper than rebuilding later.</p></div>
      </div></div></section>""",
        [("Hybrid Solar Systems", "hybrid-solar-systems.html"),
         ("On-Grid Solar Systems", "on-grid-solar-systems.html"),
         ("Solar Panel Installation", "solar-panel-installation.html"),
         ("All Solar Services", "services.html")])
    pages["hybrid-solar-systems.html"] = service_page(
        rel, "hybrid-solar-systems.html",
        "Hybrid Solar Systems in Bahria Town Lahore | Solar Installation Bahria Town Lahore",
        "Hybrid solar systems in Bahria Town Lahore — solar panels, inverter and battery storage working together. Free consultation: 03200147783.",
        "Hybrid Solar Systems",
        "assets/images/hybrid-inverter-battery-system.jpg",
        "Solar panels, an inverter and battery storage in one system — daytime generation plus stored energy for evenings and outages.",
        """<span class="eyebrow">Solar + Storage</span>
      <h2>What Is a Hybrid Solar System?</h2>
      <hr class="gold-rule">
      <p>A hybrid solar system combines three things: solar panels that generate electricity, an inverter that manages the power, and batteries that store energy for later. The system can use solar power directly during the day, store extra energy in the batteries, and draw from the grid when needed — depending on the configuration.</p>
      <p>For many homes in Bahria Town Lahore, the hybrid approach is popular because it covers both daytime generation and backup. When the sun is shining, your panels power your home. In the evening, or during a grid outage, stored energy can keep essential loads running — how much, and for how long, depends on the battery capacity and the loads connected.</p>
      <p>Hybrid systems cost more upfront than a simple on-grid system, because of the batteries and the hybrid inverter. We explain that trade-off honestly during the consultation so you can decide with clear eyes.</p>""",
        ["Daytime solar generation for direct use",
         "Battery storage for evenings and outages",
         "Grid connection as a backup source",
         "Essential-load backup, sized to your needs",
         "Inverter and battery selection matched to your load"],
        """<section class="section alt"><div class="container"><div class="section-head left reveal">
      <span class="eyebrow">Honest Comparison</span>
      <h2>Hybrid — Advantages and Limitations</h2></div>
      <div class="grid grid-2">
        <div class="card reveal"><h3>Advantages</h3><p>Stored energy for evenings and outages. Flexibility — the system can use solar, battery or grid power as needed. A good fit for homes where backup matters.</p></div>
        <div class="card reveal"><h3>Limitations</h3><p>Batteries add cost and need space and care. Backup is limited by battery capacity — it covers essential loads, not unlimited consumption. Batteries will need replacement after their service life.</p></div>
      </div></div></section>""",
        [("Solar Battery Solutions", "solar-battery-solutions.html"),
         ("Solar Inverter Installation", "solar-inverter-installation.html"),
         ("Hybrid vs On-Grid Solar Systems", "blog/hybrid-vs-on-grid-solar-systems.html"),
         ("On-Grid Solar Systems", "on-grid-solar-systems.html")])
    pages["on-grid-solar-systems.html"] = service_page(
        rel, "on-grid-solar-systems.html",
        "On-Grid Solar Systems in Bahria Town Lahore | Solar Installation Bahria Town Lahore",
        "On-grid solar systems in Bahria Town Lahore — grid-connected solar for daytime generation. Free consultation: 03200147783.",
        "On-Grid Solar Systems",
        "assets/images/solar-panels-field-sunset.jpg",
        "A grid-connected solar system that generates power during the day and works together with the electricity grid.",
        """<span class="eyebrow">Grid Connected</span>
      <h2>What Is an On-Grid Solar System?</h2>
      <hr class="gold-rule">
      <p>An on-grid solar system is connected to the electricity grid. During the day, your solar panels generate electricity and your home or business uses it directly. When your panels produce more than you are using, the extra energy can be exported to the grid where net metering is available — subject to the rules and approvals of your electricity provider.</p>
      <p>On-grid systems are simpler than hybrid systems: no batteries, fewer components, and a lower upfront cost. They are a good fit for properties with a stable grid connection that mainly want to make better use of daytime sunlight.</p>
      <p>One honest limitation: an on-grid system on its own does not provide power during a grid outage. Without batteries, there is nothing to draw from when the grid is down. If backup during outages matters to you, a hybrid system is the option to discuss.</p>""",
        ["Daytime solar generation for direct use",
         "Works with the grid — no batteries required",
         "Net metering guidance where it applies",
         "Simpler design, lower upfront cost",
         "Suitable for properties with a stable grid connection"],
        """<section class="section alt"><div class="container"><div class="section-head left reveal">
      <span class="eyebrow">Honest Comparison</span>
      <h2>On-Grid — Advantages and Limitations</h2></div>
      <div class="grid grid-2">
        <div class="card reveal"><h3>Advantages</h3><p>Straightforward and reliable design. Lower cost than hybrid or off-grid systems. Can export surplus daytime energy where net metering applies.</p></div>
        <div class="card reveal"><h3>Limitations</h3><p>No stored energy for night-time use. No power during grid outages on its own. Savings depend on how much of your usage happens during daylight hours.</p></div>
      </div></div></section>""",
        [("Hybrid Solar Systems", "hybrid-solar-systems.html"),
         ("Net Metering &amp; Solar Guidance", "solar-installation-bahria-town-lahore.html"),
         ("Solar Panel Installation", "solar-panel-installation.html"),
         ("Hybrid vs On-Grid Solar Systems", "blog/hybrid-vs-on-grid-solar-systems.html")])
    pages["off-grid-solar-systems.html"] = service_page(
        rel, "off-grid-solar-systems.html",
        "Off-Grid Solar Systems in Bahria Town Lahore | Solar Installation Bahria Town Lahore",
        "Off-grid solar systems in Bahria Town Lahore — independent solar with battery storage for properties without a reliable grid connection. Free consultation: 03200147783.",
        "Off-Grid Solar Systems",
        "assets/images/solar-array-field.jpg",
        "An independent solar system with battery storage, designed to operate without a grid connection.",
        """<span class="eyebrow">Fully Independent</span>
      <h2>What Is an Off-Grid Solar System?</h2>
      <hr class="gold-rule">
      <p>An off-grid solar system operates independently of the electricity grid. Solar panels generate electricity during the day, batteries store it, and an inverter supplies power to your property day and night — the system is your only source of electricity.</p>
      <p>Off-grid systems suit properties where there is no grid connection, or where the grid is so unreliable that independence is the goal. Because the system is your only source, sizing matters more than with any other system type: panels, batteries and inverter must be matched carefully to your real load.</p>
      <p>We plan off-grid systems conservatively and honestly. Cloudy stretches, seasonal changes and battery limits are all part of the conversation before anything is installed.</p>""",
        ["Complete independence from the grid",
         "Battery storage sized for day and night use",
         "Careful load assessment — the system is your only source",
         "Suitable for properties without a grid connection",
         "Professional installation and clear handover guidance"],
        """<section class="section alt"><div class="container"><div class="section-head left reveal">
      <span class="eyebrow">Honest Comparison</span>
      <h2>Off-Grid — Advantages and Limitations</h2></div>
      <div class="grid grid-2">
        <div class="card reveal"><h3>Advantages</h3><p>Works anywhere with sunlight, no grid needed. Full control over your own power supply. No dependence on grid outages or tariffs.</p></div>
        <div class="card reveal"><h3>Limitations</h3><p>Needs careful sizing and larger battery banks. Cloudy periods reduce generation, so storage must cover them. Higher upfront cost than grid-connected options.</p></div>
      </div></div></section>""",
        [("Solar Battery Solutions", "solar-battery-solutions.html"),
         ("Hybrid Solar Systems", "hybrid-solar-systems.html"),
         ("Solar Panel Installation", "solar-panel-installation.html"),
         ("All Solar Services", "services.html")])
    pages["solar-panel-installation.html"] = service_page(
        rel, "solar-panel-installation.html",
        "Solar Panel Installation Bahria Town Lahore | Solar Installation Bahria Town Lahore",
        "Solar panel installation in Bahria Town Lahore — professional panel mounting and installation for homes and businesses. Free consultation: 03200147783.",
        "Solar Panel Installation",
        "assets/images/solar-panel-installation-worker.jpg",
        "Professional solar panel installation — panels mounted securely, positioned for your roof and sun exposure, and wired into your system.",
        """<span class="eyebrow">Panels Done Properly</span>
      <h2>Solar Panel Installation in Bahria Town Lahore</h2>
      <hr class="gold-rule">
      <p>Panels are the visible part of your solar system — and the part that has to survive Lahore's summers, monsoon rain and winter dust. Good installation matters as much as the panels themselves.</p>
      <p>We assess your roof before anything is mounted: its structure, its direction, and any shading from neighbouring buildings or trees. Panels are then positioned to make the best use of the available sun, mounted on proper structures, and wired neatly into the rest of the system.</p>
      <p>We also explain how to look after your panels — simple cleaning and occasional checks keep them performing as they should. Our blog has a full guide on <a href="blog/solar-panel-maintenance.html">solar panel maintenance</a>.</p>""",
        ["Roof assessment before installation",
         "Secure mounting structures suited to your roof type",
         "Panels positioned for sun exposure and shading",
         "Neat, safe wiring into inverter and system",
         "Guidance on cleaning and looking after your panels"],
        """<section class="section alt"><div class="container"><div class="section-head left reveal">
      <span class="eyebrow">Choosing Panels</span>
      <h2>What Matters When Choosing Solar Panels</h2></div>
      <p class="reveal">Panel choice involves more than the headline wattage. Efficiency, build quality, warranty terms and how the panel performs in Lahore's heat all matter. Our guide on <a href="blog/how-to-choose-solar-panels.html">how to choose solar panels</a> explains what to look for — and during a consultation we walk through the options for your property specifically.</p></div></section>""",
        [("Solar Inverter Installation", "solar-inverter-installation.html"),
         ("Solar Battery Solutions", "solar-battery-solutions.html"),
         ("Residential Solar Installation", "residential-solar-installation.html"),
         ("How to Choose Solar Panels", "blog/how-to-choose-solar-panels.html")])
    pages["solar-inverter-installation.html"] = service_page(
        rel, "solar-inverter-installation.html",
        "Solar Inverter Installation Bahria Town Lahore | Solar Installation Bahria Town Lahore",
        "Solar inverter installation in Bahria Town Lahore — inverter selection, installation and configuration for your system. Free consultation: 03200147783.",
        "Solar Inverter Installation",
        "assets/images/solar-inverter-battery-wall.jpg",
        "Inverter selection, installation and configuration — the heart of your solar system, matched to your panels, batteries and load.",
        """<span class="eyebrow">The Heart of the System</span>
      <h2>Solar Inverter Installation in Bahria Town Lahore</h2>
      <hr class="gold-rule">
      <p>The inverter converts the direct current (DC) from your solar panels into the alternating current (AC) your home uses. It also manages how power flows between panels, batteries and the grid in hybrid systems. A good inverter, correctly sized and configured, is what makes the whole system work well.</p>
      <p>We help you choose the right inverter type for your system — on-grid, hybrid or off-grid — and size it to your panels and your load. Installation includes proper placement, ventilation, wiring and configuration, followed by a walkthrough so you understand what your inverter is doing.</p>
      <p>If you already have a system and are considering an inverter change, talk to us first. Inverter compatibility depends on your existing panels and batteries, and we will give you an honest assessment.</p>""",
        ["Inverter type matched to your system — hybrid, on-grid or off-grid",
         "Correct sizing for your panels and load",
         "Safe installation with proper ventilation and wiring",
         "Configuration and testing before handover",
         "Clear explanation of how your inverter works"],
        """<section class="section alt"><div class="container"><div class="section-head left reveal">
      <span class="eyebrow">Buying Guide</span>
      <h2>Choosing an Inverter</h2></div>
      <p class="reveal">Inverter choice is one of the most technical parts of going solar. Our <a href="blog/solar-inverter-buying-guide.html">solar inverter buying guide</a> explains the main types, what sizing means, and the features worth paying attention to — in plain language.</p></div></section>""",
        [("Hybrid Solar Systems", "hybrid-solar-systems.html"),
         ("Solar Battery Solutions", "solar-battery-solutions.html"),
         ("Solar Inverter Buying Guide", "blog/solar-inverter-buying-guide.html"),
         ("Solar Panel Installation", "solar-panel-installation.html")])
    pages["solar-battery-solutions.html"] = service_page(
        rel, "solar-battery-solutions.html",
        "Solar Battery Solutions in Bahria Town Lahore | Solar Installation Bahria Town Lahore",
        "Solar battery solutions in Bahria Town Lahore — battery storage for evenings and outages, sized to your needs. Free consultation: 03200147783.",
        "Solar Battery Solutions",
        "assets/images/hybrid-inverter-battery-system.jpg",
        "Battery storage that keeps essential power available when the sun goes down or the grid is off — sized honestly to your needs.",
        """<span class="eyebrow">Stored Energy</span>
      <h2>Solar Battery Storage in Bahria Town Lahore</h2>
      <hr class="gold-rule">
      <p>Solar panels generate electricity while the sun shines. Batteries store that energy so you can use it in the evening — or during a power outage. Without storage, the energy your panels make after your daytime needs are met is either exported or unused, depending on your system.</p>
      <p>Battery sizing is the key decision. A battery sized for a few essential loads — lights, fans, a fridge, phone charging — costs far less than one sized to run an entire home through the night. We work through what you actually want to keep running, and size the storage to that, honestly.</p>
      <p>Batteries are a core part of hybrid and off-grid systems. They also have a service life and will eventually need replacement — something we discuss upfront, not after installation.</p>""",
        ["Battery sizing based on your essential loads",
         "Lithium and other battery options explained clearly",
         "Integration with hybrid and off-grid systems",
         "Safe installation with proper wiring and ventilation",
         "Honest guidance on battery life and replacement"],
        """<section class="section alt"><div class="container"><div class="section-head left reveal">
      <span class="eyebrow">Learn More</span>
      <h2>Batteries, Explained Simply</h2></div>
      <p class="reveal">Our guide <a href="blog/solar-battery-storage-explained.html">Solar Battery Storage Explained</a> covers how batteries work, what capacity really means, and how to think about backup — without the jargon.</p></div></section>""",
        [("Hybrid Solar Systems", "hybrid-solar-systems.html"),
         ("Off-Grid Solar Systems", "off-grid-solar-systems.html"),
         ("Solar Inverter Installation", "solar-inverter-installation.html"),
         ("Solar Battery Storage Explained", "blog/solar-battery-storage-explained.html")])
    return pages

# =========================================================== LOCATIONS ====
def build_bahria_location():
    rel = ""
    body = """<section class="section">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Our Home Ground</span>
      <h2>Solar Installation Across Bahria Town Lahore</h2>
      <hr class="gold-rule">
      <p>Our office sits in Sector C, Tulip Commercial, Bahria Town Lahore — right in the middle of the community we serve. That matters, because solar is a local business: roofs, sun exposure and house styles differ from sector to sector, and we see them every day.</p>
      <p>We provide solar installation services for residential and commercial properties throughout Bahria Town Lahore, including homes in every sector and the Overseas enclave. Whether your house is a compact family home or a large residence, we plan the system around your property.</p>
      <p>Being local also means we stay reachable after installation. If you have a question about your system months later, you know where to find us.</p>
    </div>
    <div class="img-frame reveal"><img src="assets/images/modern-house-flat-roof-solar.jpg" alt="Modern luxury house with rooftop solar panels in Bahria Town Lahore" loading="lazy"></div>
  </div>
</section>
<section class="section alt">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Service Areas</span>
      <h2>Sectors We Serve in Bahria Town Lahore</h2>
      <p>One local team, one office — serving every sector of Bahria Town Lahore.</p>
    </div>
    <div class="grid grid-3">
      <div class="card reveal"><h3>Sector A</h3><p>Solar installation for homes and commercial properties in Sector A Bahria Town Lahore, planned around each property's roof and load.</p></div>
      <div class="card reveal"><h3>Sector B</h3><p>Solar installation in Sector B Bahria Town Lahore — residential systems and commercial planning for properties across the sector.</p></div>
      <div class="card reveal"><h3>Sector C</h3><p>Our home sector. Solar installation in Sector C Bahria Town Lahore, with our office at Plaza 210, Tulip Commercial.</p></div>
      <div class="card reveal"><h3>Sector D</h3><p>Solar installation in Sector D Bahria Town Lahore for homes and businesses, with local assessment and planning.</p></div>
      <div class="card reveal"><h3>Sector E</h3><p>Solar installation in Sector E Bahria Town Lahore — hybrid, on-grid and off-grid systems for residential and commercial properties.</p></div>
      <div class="card reveal"><h3>Sector F</h3><p>Solar installation in Sector F Bahria Town Lahore, planned around your property and your daily electricity use.</p></div>
    </div>
    <p style="text-align:center;margin-top:26px;color:var(--gray)">We also serve the Overseas enclave and other areas of Bahria Town Lahore. If your property is in Bahria Town, we can help — contact us to discuss it.</p>
  </div>
</section>
<section class="section">
  <div class="container split">
    <div class="img-frame reveal"><img src="assets/images/solar-panels-field-sunset.jpg" alt="Solar panels at sunset" loading="lazy"></div>
    <div class="reveal">
      <span class="eyebrow">Before You Decide</span>
      <h2>Planning, Permissions and Net Metering</h2>
      <hr class="gold-rule">
      <p><strong>System planning.</strong> Every installation starts with an assessment of your property and your electricity use. We plan panels, inverter and batteries as one system — not as separate purchases.</p>
      <p><strong>Community rules.</strong> Bahria Town has its own community guidelines for properties. We discuss any relevant considerations for your home during the consultation, and we plan installations that respect the community's standards.</p>
      <p><strong>Net metering.</strong> Where net metering is available, an on-grid or hybrid system can export surplus daytime energy to the grid. Approval and metering arrangements depend on your electricity provider and the applicable rules — we explain the process and what it involves, and we do not promise approvals or timelines we cannot control.</p>
      <p><strong>Getting started.</strong> The simplest first step is a free consultation: call <a href="{tel}">{phone}</a> or message us on WhatsApp, and we will talk through your property and your options.</p>
    </div>
  </div>
</section>
<section class="section alt">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Good to Know</span>
      <h2>Frequently Asked Questions — Bahria Town Lahore</h2>
    </div>
    {faq}
  </div>
</section>
""".format(tel=PHONE_TEL, phone=PHONE_DISPLAY, faq=faq_html(FAQS))
    body += cta_band(rel, "Ready to Explore Solar Energy for Your Property?",
                     "Contact Solar Installation Bahria Town Lahore to discuss your residential or commercial solar requirements.")
    schemas = [org_ld(), local_ld(), faq_ld(FAQS),
               breadcrumb_ld([("Home", "index.html"), ("Locations", None),
                              ("Solar Installation in Bahria Town Lahore", None)])]
    return page(rel, "solar-installation-bahria-town-lahore.html",
                "Solar Installation in Bahria Town Lahore | Sectors A–F | Solar Installation Bahria Town Lahore",
                "Solar installation in Bahria Town Lahore — residential & commercial solar across Sectors A–F and the Overseas enclave. Local office in Sector C, Tulip Commercial. Free consultation: 03200147783.",
                "Solar Installation in Bahria Town Lahore", body, schemas, "locations",
                hero_img="assets/images/modern-house-flat-roof-solar.jpg",
                hero_sub="Residential and commercial solar installation across Sectors A to F and the Overseas enclave — from our office in Sector C, Tulip Commercial.",
                crumbs=[("Home", "index.html"), ("Solar Installation in Bahria Town Lahore", None)])

def build_lahore_location():
    rel = ""
    body = """<section class="section">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Serving Lahore</span>
      <h2>Solar Installation in Lahore</h2>
      <hr class="gold-rule">
      <p>Bahria Town Lahore is our home, and Lahore is the city we serve. We provide solar installation services for homes and businesses across Lahore, with a particular focus on Bahria Town and its surrounding areas.</p>
      <p>Lahore's climate makes solar a practical choice: strong sunlight for much of the year, and homes with roofs that are often well suited to panels. Whether you live in Bahria Town, DHA, Johar Town, Model Town, Gulberg or elsewhere in the city, we can discuss a system for your property.</p>
      <p>Every project follows the same process — consultation, property and energy assessment, system planning, professional installation and handover with guidance.</p>
    </div>
    <div class="img-frame reveal"><img src="assets/images/aerial-home-solar-panels.jpg" alt="Aerial view of a home with rooftop solar panels" loading="lazy"></div>
  </div>
</section>
<section class="section alt">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Across the City</span>
      <h2>Areas We Serve in Lahore</h2>
      <p>Our main service area is Bahria Town Lahore, and we also work with customers across the wider city.</p>
    </div>
    <div class="grid grid-3">
      <div class="card reveal"><h3>Bahria Town Lahore</h3><p>Our home ground — Sectors A to F and the Overseas enclave. <a href="solar-installation-bahria-town-lahore.html">Bahria Town solar services →</a></p></div>
      <div class="card reveal"><h3>DHA Lahore</h3><p>Residential and commercial solar installation for properties in DHA Lahore, planned around your home and usage.</p></div>
      <div class="card reveal"><h3>Johar Town &amp; Model Town</h3><p>Solar systems for homes and businesses in Johar Town, Model Town and nearby areas of Lahore.</p></div>
      <div class="card reveal"><h3>Gulberg &amp; Cantonment</h3><p>Solar installation for properties in Gulberg, Lahore Cantonment and surrounding neighbourhoods.</p></div>
      <div class="card reveal"><h3>Other Areas of Lahore</h3><p>If your property is elsewhere in Lahore, contact us — we will tell you honestly whether we can serve your area.</p></div>
      <div class="card reveal"><h3>Not Sure?</h3><p>Call <a href="{tel}">{phone}</a> or message us on WhatsApp and tell us where your property is. We will give you a straight answer.</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Why Lahore Homes Choose Solar</span>
      <h2>Solar Energy for Pakistani Homes</h2>
      <hr class="gold-rule">
      <p>Pakistani homes face two realities: long sunny days and an electricity grid that does not always deliver when it is needed. Solar addresses the first — and, with battery storage, helps with the second.</p>
      <p>A hybrid system is the most common choice for Lahore homes because it combines daytime generation with stored energy for evenings and outages. An on-grid system suits homes with a stable connection that mainly want daytime generation. Our guide on <a href="blog/solar-energy-for-pakistani-homes.html">solar energy for Pakistani homes</a> explains this in more detail.</p>
      <p>Whatever your situation, the right starting point is the same: a conversation about your home and how you use electricity.</p>
    </div>
    <div class="img-frame reveal"><img src="assets/images/solar-panels-roof-sunset.jpg" alt="Rooftop solar panels at sunset" loading="lazy"></div>
  </div>
</section>
<section class="section alt">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Good to Know</span>
      <h2>Frequently Asked Questions — Lahore</h2>
    </div>
    {faq}
  </div>
</section>
""".format(tel=PHONE_TEL, phone=PHONE_DISPLAY, faq=faq_html(FAQS))
    body += cta_band(rel, "Ready to Explore Solar Energy for Your Property?",
                     "Contact Solar Installation Bahria Town Lahore to discuss your residential or commercial solar requirements.")
    schemas = [org_ld(), local_ld(), faq_ld(FAQS),
               breadcrumb_ld([("Home", "index.html"), ("Locations", None),
                              ("Solar Installation in Lahore", None)])]
    return page(rel, "solar-installation-lahore.html",
                "Solar Installation in Lahore | Solar Installation Bahria Town Lahore",
                "Solar installation in Lahore — residential & commercial solar, hybrid, on-grid and off-grid systems, from our Bahria Town Lahore office. Free consultation: 03200147783.",
                "Solar Installation in Lahore", body, schemas, "locations",
                hero_img="assets/images/aerial-home-solar-panels.jpg",
                hero_sub="Solar installation services across Lahore — from our office in Bahria Town Lahore, serving homes and businesses throughout the city.",
                crumbs=[("Home", "index.html"), ("Solar Installation in Lahore", None)])

# =========================================================== PROJECTS =====
def build_projects():
    rel = ""
    body = """<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Portfolio</span>
      <h2>Our Projects &amp; Installations</h2>
      <p>Examples of the kinds of solar installations we work on — residential rooftops, commercial roofs, hybrid systems, battery storage and panel mounting. Use the filters to explore by category, or tap any image to view it larger.</p>
    </div>
{gallery}
  </div>
</section>
<section class="section alt">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">What a Project Looks Like</span>
      <h2>From First Visit to Handover</h2>
    </div>
    <div class="grid grid-3 steps">
      <div class="card step reveal"><div class="num">01</div><h3>Consultation &amp; Assessment</h3><p>We visit your property, review your load and roof, and talk through your options.</p></div>
      <div class="card step reveal"><div class="num">02</div><h3>Planning</h3><p>Panels, inverter and batteries are planned as one system, matched to your property.</p></div>
      <div class="card step reveal"><div class="num">03</div><h3>Installation</h3><p>Mounting, wiring and configuration — done carefully and checked before handover.</p></div>
      <div class="card step reveal"><div class="num">04</div><h3>Handover &amp; Guidance</h3><p>We explain your system, how to look after it, and how to reach us afterwards.</p></div>
      <div class="card step reveal"><div class="num">05</div><h3>Your Project, Your Photos</h3><p>With your permission, verified photographs of completed work are added to this portfolio.</p></div>
      <div class="card step reveal"><div class="num">✦</div><h3>Start Your Project</h3><p><a href="contact.html">Get a free consultation</a> — or call <a href="{tel}">{phone}</a>.</p></div>
    </div>
  </div>
</section>
""".format(gallery=gallery_html(rel), tel=PHONE_TEL, phone=PHONE_DISPLAY)
    body += cta_band(rel, "Want Your Home in Our Portfolio?",
                     "Start with a free consultation — we will plan a system for your property and install it professionally.")
    schemas = [org_ld(), breadcrumb_ld([("Home", "index.html"), ("Projects", None)])]
    return page(rel, "projects.html",
                "Our Projects | Solar Installation Bahria Town Lahore",
                "Solar installation portfolio — residential rooftops, commercial roofs, hybrid systems and battery storage. Illustrative images; verified project photos added as work is completed.",
                "Our Projects", body, schemas, "projects",
                hero_img="assets/images/rooftop-solar-panels-house.jpg",
                hero_sub="Residential rooftops, commercial roofs, hybrid systems and battery storage — the kinds of installations we work on.",
                crumbs=[("Home", "index.html"), ("Projects", None)])

# ============================================================== BLOG ======
BLOG_CATS = ["Solar Installation", "Solar Energy", "Solar Panels", "Solar Inverters",
             "Hybrid Solar Systems", "Solar Batteries", "Solar Maintenance",
             "Solar Installation Lahore", "Bahria Town Solar Guides"]

# slug, title, category, excerpt, image, alt
BLOG_INDEX = [
    ("how-solar-energy-works", "How Solar Energy Works",
     "Solar Energy", "Sunlight becomes electricity in your home through panels, an inverter and your wiring. Here is the journey, step by step, in plain language.",
     "assets/images/solar-panel-cells-closeup.jpg", "Close-up of solar panel cells"),
    ("hybrid-vs-on-grid-solar-systems", "Hybrid vs On-Grid Solar Systems",
     "Hybrid Solar Systems", "The two most common system types in Lahore, compared honestly — what each does, what each cannot do, and who each one suits.",
     "assets/images/hybrid-inverter-battery-system.jpg", "Hybrid inverter with battery storage"),
    ("how-to-choose-solar-panels", "How to Choose Solar Panels",
     "Solar Panels", "Wattage is only part of the story. Efficiency, build quality, heat performance and warranty terms all matter — here is what to look for.",
     "assets/images/solar-panel-cells-closeup.jpg", "Solar panel cells close-up"),
    ("solar-inverter-buying-guide", "Solar Inverter Buying Guide",
     "Solar Inverters", "The inverter is the heart of your system. This guide explains the main types, sizing and the features worth paying attention to.",
     "assets/images/solar-inverter-battery-wall.jpg", "Wall-mounted solar inverter and battery"),
    ("solar-battery-storage-explained", "Solar Battery Storage Explained",
     "Solar Batteries", "What batteries actually do, what capacity means in real life, and how to think about backup without overspending.",
     "assets/images/solar-inverter-battery-wall.jpg", "Solar battery storage with inverters"),
    ("solar-panel-maintenance", "Solar Panel Maintenance",
     "Solar Maintenance", "Cleaning, checks and the simple habits that keep your panels performing well in Lahore's dust and heat.",
     "assets/images/solar-panel-installation-worker.jpg", "Installer working on rooftop solar panels"),
    ("solar-energy-for-pakistani-homes", "Solar Energy for Pakistani Homes",
     "Solar Energy", "Long sunny days, an unreliable grid and rising bills — why solar fits Pakistani homes, and which system type suits which household.",
     "assets/images/solar-panels-roof-sunset.jpg", "Rooftop solar panels at sunset"),
    ("solar-installation-planning-in-lahore", "Solar Installation Planning in Lahore",
     "Solar Installation Lahore", "Before you buy anything: load, roof, system type, installer and the questions to ask — a planning checklist for Lahore homeowners.",
     "assets/images/modern-house-flat-roof-solar.jpg", "Modern house with rooftop solar panels"),
]

def build_blog_index():
    rel = ""
    cat_btns = "\n".join(
        '<button class="filter-btn cat-filter" data-filter="{c}">{c}</button>'.format(c=c)
        for c in BLOG_CATS)
    cards = []
    for slug, title, cat, excerpt, img, alt in BLOG_INDEX:
        cards.append(
            """<article class="card post-card reveal" data-cat="{cat}">
  <div class="thumb"><img src="{rel}{img}" alt="{alt}" loading="lazy"></div>
  <div class="body">
    <div class="meta"><span class="cat">{cat}</span> · 24 November 2026</div>
    <h3><a href="{rel}blog/{slug}.html">{title}</a></h3>
    <p>{ex}</p>
    <a class="card-link" href="{rel}blog/{slug}.html">Read Article →</a>
  </div>
</article>""".format(rel=rel, cat=cat, img=img, alt=alt, slug=slug, title=title, ex=excerpt))
    body = """<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Blog &amp; Solar Energy Guides</span>
      <h2>Learn About Solar, in Plain Language</h2>
      <p>Honest, practical guides about solar energy, systems and maintenance — written for homeowners in Bahria Town Lahore and across Pakistan.</p>
    </div>
    <div class="blog-search reveal">
      <span class="s-ico">⌕</span>
      <input type="search" id="blogSearch" placeholder="Search articles…" aria-label="Search articles">
    </div>
    <div class="cat-list reveal">
      <button class="filter-btn cat-filter active" data-filter="all">All Topics</button>
{cat_btns}
    </div>
    <p id="noResults" style="display:none;text-align:center;color:var(--gray)">No articles match your search. Try a different word.</p>
    <div class="grid grid-3" id="postGrid">
{cards}
    </div>
  </div>
</section>
""".format(cat_btns=cat_btns, cards="\n".join(cards))
    body += cta_band(rel, "Have a Question About Solar?",
                     "Our guides cover the basics — but your home is specific. Contact us for a free consultation tailored to your property.")
    schemas = [org_ld(), breadcrumb_ld([("Home", "index.html"), ("Blog", None)])]
    html = page(rel, "blog.html",
                "Blog & Solar Energy Guides | Solar Installation Bahria Town Lahore",
                "Solar energy guides for homeowners in Bahria Town Lahore — how solar works, hybrid vs on-grid systems, choosing panels, inverters, batteries and maintenance.",
                "Blog & Solar Energy Guides", body, schemas, "blog",
                hero_img="assets/images/solar-panels-sunset-field.jpg",
                hero_sub="Practical guides about solar energy, written in plain language for homeowners in Bahria Town Lahore and across Pakistan.",
                crumbs=[("Home", "index.html"), ("Blog", None)])
    # Category filter buttons reuse the gallery filter logic: they set data-filter
    # on post cards too. Add a small inline bridge so both filters work.
    html = html.replace(
        '</body>',
        """<script>
document.querySelectorAll('.cat-filter').forEach(function (btn) {
  btn.addEventListener('click', function () {
    document.querySelectorAll('.cat-filter').forEach(function (b) { b.classList.remove('active'); });
    btn.classList.add('active');
    var cat = btn.getAttribute('data-filter');
    document.querySelectorAll('.post-card').forEach(function (card) {
      card.style.display = (cat === 'all' || card.getAttribute('data-cat') === cat) ? '' : 'none';
    });
    var no = document.getElementById('noResults');
    if (no) no.style.display = 'none';
  });
});
</script>
</body>""")
    return html

# ============================================================ CONTACT =====
def build_contact():
    rel = ""
    social_list = "\n".join(
        '<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>'.format(u=u, n=n)
        for n, u, _ in SOCIAL)
    body = """<section class="section">
  <div class="container contact-grid">
    <div class="reveal">
      <div class="contact-card">
        <h3>Contact Details</h3>
        <div class="contact-line"><span class="ic">⌖</span><div><div class="lbl">Business Name</div><div class="val">{biz}</div></div></div>
        <div class="contact-line"><span class="ic">☎</span><div><div class="lbl">Phone</div><div class="val"><a href="{tel}">{phone}</a></div></div></div>
        <div class="contact-line"><span class="ic">✆</span><div><div class="lbl">WhatsApp</div><div class="val"><a href="{wa}" target="_blank" rel="noopener">{phone}</a></div></div></div>
        <div class="contact-line"><span class="ic">⌂</span><div><div class="lbl">Address</div><div class="val">{addr}</div></div></div>
        <div class="contact-line"><span class="ic">◎</span><div><div class="lbl">Google Business Profile</div><div class="val"><a href="{gmb}" target="_blank" rel="noopener">View on Google Maps</a></div></div></div>
      </div>
      <div class="contact-card">
        <h3>Follow Us</h3>
        <p>Find us on social media for updates, guides and solar tips.</p>
        <div class="social-row">
{social}
        </div>
        <ul class="footer-links" style="margin-top:18px">
{social_list}
        </ul>
      </div>
      <div class="map-frame">
        <iframe src="{map}" title="Map — Solar Installation Bahria Town Lahore, Plaza 210, Sector C, Tulip Commercial, Bahria Town, Lahore" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>
      <p style="text-align:center"><a href="{gmb}" target="_blank" rel="noopener">Open in Google Maps →</a></p>
    </div>
    <div class="form-wrap reveal">
      <h2 style="font-size:1.5rem;margin-bottom:8px">Request a Free Consultation</h2>
      <p>Tell us about your property and what you need. When you submit, your enquiry opens in WhatsApp so you can send it directly to us — nothing is sent anywhere else.</p>
      <form id="contactForm" novalidate>
        <div class="hp-field" aria-hidden="true">
          <label for="hpWebsite">Website (leave blank)</label>
          <input type="text" id="hpWebsite" name="website" tabindex="-1" autocomplete="off">
        </div>
        <div class="form-row">
          <div class="field">
            <label for="fName">Full Name <span class="req">*</span></label>
            <input type="text" id="fName" name="name" autocomplete="name" placeholder="Your full name">
            <div class="err">Please enter your full name.</div>
          </div>
          <div class="field">
            <label for="fPhone">Phone Number <span class="req">*</span></label>
            <input type="tel" id="fPhone" name="phone" autocomplete="tel" placeholder="Your mobile number">
            <div class="err">Please enter a valid phone number.</div>
          </div>
        </div>
        <div class="field">
          <label for="fEmail">Email Address</label>
          <input type="email" id="fEmail" name="email" autocomplete="email" placeholder="you@example.com (optional)">
          <div class="err">Please enter a valid email address, or leave it blank.</div>
        </div>
        <div class="form-row">
          <div class="field">
            <label for="fProperty">Property Type <span class="req">*</span></label>
            <select id="fProperty" name="property">
              <option value="">Select property type</option>
              <option>House — 5 Marla</option>
              <option>House — 10 Marla</option>
              <option>House — 1 Kanal</option>
              <option>House — larger than 1 Kanal</option>
              <option>Apartment / Flat</option>
              <option>Shop</option>
              <option>Office</option>
              <option>Commercial building</option>
              <option>Other</option>
            </select>
            <div class="err">Please choose a property type.</div>
          </div>
          <div class="field">
            <label for="fSystem">Required Solar System <span class="req">*</span></label>
            <select id="fSystem" name="system">
              <option value="">Select a system</option>
              <option>Hybrid solar system</option>
              <option>On-grid solar system</option>
              <option>Off-grid solar system</option>
              <option>Not sure — need advice</option>
            </select>
            <div class="err">Please choose a solar system (or "Not sure").</div>
          </div>
        </div>
        <div class="field">
          <label for="fMessage">Message <span class="req">*</span></label>
          <textarea id="fMessage" name="message" rows="5" placeholder="Tell us about your home or business and what you need from solar…"></textarea>
          <div class="err">Please write a short message.</div>
        </div>
        <button class="btn btn-gold" type="submit" style="width:100%">Send Enquiry via WhatsApp</button>
        <div class="form-status" id="formStatus" role="status"></div>
        <p class="form-note">This website has no email backend. Your enquiry is composed as a WhatsApp message and opened in WhatsApp — you press Send in WhatsApp to deliver it to {biz} on {phone}. We never show a fake "submitted successfully" message.</p>
      </form>
    </div>
  </div>
</section>
""".format(biz=BUSINESS, tel=PHONE_TEL, phone=PHONE_DISPLAY, wa=WA_LINK,
           addr=ADDRESS, gmb=GMB, social=social_icons(), social_list=social_list,
           map=MAP_EMBED)
    schemas = [org_ld(), local_ld(),
               breadcrumb_ld([("Home", "index.html"), ("Contact Us", None)])]
    return page(rel, "contact.html",
                "Contact Us | Solar Installation Bahria Town Lahore",
                "Contact Solar Installation Bahria Town Lahore — call or WhatsApp 03200147783, visit our office at Plaza 210, Sector C, Tulip Commercial, Bahria Town, Lahore, or send an enquiry via WhatsApp.",
                "Contact Us", body, schemas, "contact",
                hero_img="assets/images/modern-villa-solar-panels-pool.jpg",
                hero_sub="Call, WhatsApp, visit our office in Sector C, Tulip Commercial — or send an enquiry through the form.",
                crumbs=[("Home", "index.html"), ("Contact Us", None)])

# ============================================================== LEGAL =====
def build_privacy():
    rel = ""
    body = """<section class="section"><div class="container legal">
  <p class="updated">Last updated: 24 November 2026</p>
  <h2>1. Information We Collect</h2>
  <p>Solar Installation Bahria Town Lahore ("we", "us", "our") operates this website. When you use the contact form on this website, you provide your name, phone number, email address (optional), property type, solar system preference and message. This information is used only to respond to your enquiry.</p>
  <h2>2. How Your Enquiry Is Sent</h2>
  <p>This website has no server, database or email backend. When you submit the contact form, your enquiry is composed as a WhatsApp message and opened in WhatsApp on your own device. You choose whether to press Send in WhatsApp. We do not receive, store or transmit your enquiry through this website in any other way.</p>
  <h2>3. Information We Do Not Collect</h2>
  <p>We do not run analytics, advertising trackers or user accounts on this website. We do not collect payment information, and we do not sell or share personal information with third parties.</p>
  <h2>4. Links to Other Websites</h2>
  <p>This website links to our social media profiles (Facebook, X, Pinterest, Instagram, Threads, Medium, YouTube and TikTok), to Google Maps and to WhatsApp. Those services have their own privacy policies, and we are not responsible for their practices.</p>
  <h2>5. Cookies</h2>
  <p>This website does not set its own cookies. Embedded content (such as the Google Maps frame on the contact page) and the fonts loaded from Google Fonts may be subject to those providers' own cookie and privacy practices.</p>
  <h2>6. Your Rights</h2>
  <p>If you have shared information with us through WhatsApp or by phone and would like it corrected or deleted from our records, contact us on 03200147783 and we will deal with your request.</p>
  <h2>7. Contact</h2>
  <p>For any privacy question, contact Solar Installation Bahria Town Lahore — {addr} — phone / WhatsApp {phone}.</p>
</div></section>
""".format(addr=ADDRESS, phone=PHONE_DISPLAY)
    body += cta_band(rel, "Questions About Solar?",
                     "Contact us for a free consultation — we are happy to explain anything about your solar options.")
    schemas = [org_ld(), breadcrumb_ld([("Home", "index.html"), ("Privacy Policy", None)])]
    return page(rel, "privacy-policy.html",
                "Privacy Policy | Solar Installation Bahria Town Lahore",
                "Privacy policy for Solar Installation Bahria Town Lahore — what information the contact form collects and how enquiries are sent via WhatsApp.",
                "Privacy Policy", body, schemas, "contact",
                crumbs=[("Home", "index.html"), ("Privacy Policy", None)])

def build_terms():
    rel = ""
    body = """<section class="section"><div class="container legal">
  <p class="updated">Last updated: 24 November 2026</p>
  <h2>1. About This Website</h2>
  <p>This website is operated by Solar Installation Bahria Town Lahore, a solar energy company based at {addr}. The website provides information about our services and a way to contact us.</p>
  <h2>2. Information on This Website</h2>
  <p>We aim to keep the information on this website accurate and up to date. Solar system performance depends on many factors — your property, roof, usage, weather and the components chosen — so nothing on this website should be read as a guarantee of specific savings, generation or performance. Any figures discussed for your property will be based on an assessment of your home or business.</p>
  <h2>3. Consultations and Quotations</h2>
  <p>A consultation is free and does not commit you to anything. Any quotation or plan we provide is based on the information available at the time and the assessment of your property. Prices, availability and timelines (where given) are confirmed in writing at the time of agreement.</p>
  <h2>4. Contact Form</h2>
  <p>The contact form composes your enquiry as a WhatsApp message and opens WhatsApp on your device. Submitting the form does not send anything by itself — you press Send in WhatsApp to deliver the message to us.</p>
  <h2>5. Photography</h2>
  <p>Photographs on this website that are labelled "Illustrative image" are examples of solar installations and do not depict our own completed projects. Verified photographs of our own completed work are labelled as company projects when published.</p>
  <h2>6. Intellectual Property</h2>
  <p>The content of this website — including text, design and logo — belongs to Solar Installation Bahria Town Lahore unless stated otherwise. You may share links to our pages, but please do not copy our content without permission.</p>
  <h2>7. External Links</h2>
  <p>Links to social media, Google Maps and WhatsApp lead to third-party services. We are not responsible for the content or availability of those services.</p>
  <h2>8. Changes to These Terms</h2>
  <p>We may update these terms from time to time. The version on this page is the current one.</p>
  <h2>9. Contact</h2>
  <p>Solar Installation Bahria Town Lahore — {addr} — phone / WhatsApp {phone}.</p>
</div></section>
""".format(addr=ADDRESS, phone=PHONE_DISPLAY)
    body += cta_band(rel, "Questions About Solar?",
                     "Contact us for a free consultation — we are happy to explain anything about your solar options.")
    schemas = [org_ld(), breadcrumb_ld([("Home", "index.html"), ("Terms and Conditions", None)])]
    return page(rel, "terms-and-conditions.html",
                "Terms and Conditions | Solar Installation Bahria Town Lahore",
                "Terms and conditions for Solar Installation Bahria Town Lahore — information accuracy, consultations, the WhatsApp contact form and photography.",
                "Terms and Conditions", body, schemas, "contact",
                crumbs=[("Home", "index.html"), ("Terms and Conditions", None)])

# ================================================================ 404 =====
def build_404():
    rel = ""
    body = """<section class="notfound">
  <div class="container">
    <div class="code">404</div>
    <h2 style="font-size:1.6rem;margin-bottom:14px">This Page Could Not Be Found</h2>
    <p style="max-width:560px;margin:0 auto 30px">The page you were looking for may have moved, or the link may be out of date. You can return to the homepage or explore our solar services below.</p>
    <div class="hero-ctas" style="justify-content:center">
      <a class="btn btn-gold" href="index.html">Back to Home</a>
      <a class="btn btn-outline" href="services.html">Our Services</a>
      <a class="btn btn-blue" href="contact.html">Contact Us</a>
    </div>
  </div>
</section>
"""
    schemas = [org_ld()]
    return page(rel, "404.html",
                "Page Not Found (404) | Solar Installation Bahria Town Lahore",
                "The page you were looking for could not be found. Return to the Solar Installation Bahria Town Lahore homepage or explore our solar services.",
                "Page Not Found", body, schemas, "home",
                crumbs=[("Home", "index.html"), ("Page Not Found", None)])

# ======================================================= BLOG ARTICLES ====
def article_page(slug, title, cat, excerpt, image, alt, toc, body_html, related):
    rel = "../"
    toc_items = "\n".join(
        '<li><a href="#{a}">{t}</a></li>'.format(a=a, t=t) for a, t in toc)
    rel_cards = []
    by_slug = {s: (t, c, e, i, al) for s, t, c, e, i, al in BLOG_INDEX}
    for rs in related:
        rt, rc, rex, rimg, ralt = by_slug[rs]
        rel_cards.append(
            """<article class="card post-card">
  <div class="thumb"><img src="{rel}{img}" alt="{alt}" loading="lazy"></div>
  <div class="body">
    <div class="meta"><span class="cat">{cat}</span> · 24 November 2026</div>
    <h3><a href="{rel}blog/{slug}.html">{title}</a></h3>
    <p>{ex}</p>
    <a class="card-link" href="{rel}blog/{slug}.html">Read Article →</a>
  </div>
</article>""".format(rel=rel, img=rimg, alt=ralt, cat=rc, slug=rs, title=rt, ex=rex))
    share_url = abs_url("blog/{}.html".format(slug))
    body = """<section class="section">
  <div class="container">
    <article class="article">
      <div class="article-meta"><span class="cat" style="color:var(--gold);font-weight:600;text-transform:uppercase;letter-spacing:0.08em;font-size:0.78rem">{cat}</span> · Published 24 November 2026 · {biz}</div>
      <div class="toc"><h2>On This Page</h2><ol>
{toc}
      </ol></div>
      <img class="inline" src="{rel}{img}" alt="{alt}" loading="lazy">
{content}
      <div class="share-row">
        <span>Share this guide:</span>
        <a class="share-btn" href="https://www.facebook.com/sharer/sharer.php?u={share}" target="_blank" rel="noopener">Facebook</a>
        <a class="share-btn" href="https://twitter.com/intent/tweet?text={title_enc}&url={share}" target="_blank" rel="noopener">X</a>
        <a class="share-btn" href="https://wa.me/?text={title_enc}%20{share}" target="_blank" rel="noopener">WhatsApp</a>
        <a class="share-btn" href="https://www.linkedin.com/sharing/share-offsite/?url={share}" target="_blank" rel="noopener">LinkedIn</a>
      </div>
      <div class="related">
        <h2>Related Articles</h2>
        <div class="grid grid-2">
{rel_cards}
        </div>
      </div>
    </article>
  </div>
</section>
""".format(cat=cat, biz=BUSINESS, toc=toc_items, rel=rel, img=image, alt=alt,
           content=body_html, share=share_url,
           title_enc=title.replace(" ", "%20"),
           rel_cards="\n".join(rel_cards))
    body += cta_band(rel, "Questions About Your Own Home?",
                     "Every home is different. Contact us for a free consultation and we will talk through the right solar options for your property.")
    schemas = [org_ld(), article_ld(title, excerpt, "blog/{}.html".format(slug), image, TODAY),
               breadcrumb_ld([("Home", "index.html"), ("Blog", "blog.html"), (title, None)])]
    return page(rel, "blog/{}.html".format(slug), "{} | Solar Installation Bahria Town Lahore".format(title),
                excerpt, title, body, schemas, "blog",
                og_image=image, hero_img=image,
                hero_sub=excerpt,
                crumbs=[("Home", "index.html"), ("Blog", "blog.html"), (title, None)])

def build_articles():
    articles = {}

    articles["how-solar-energy-works.html"] = article_page(
        "how-solar-energy-works", "How Solar Energy Works", "Solar Energy",
        "Sunlight becomes electricity in your home through panels, an inverter and your wiring. Here is the journey, step by step, in plain language.",
        "assets/images/solar-panel-cells-closeup.jpg", "Close-up of solar panel cells",
        [("sunlight", "From Sunlight to Electricity"), ("inverter", "The Inverter: The Heart of the System"),
         ("home", "How Your Home Uses Solar Power"), ("batteries-grid", "Batteries and the Grid"),
         ("performance", "What Affects Performance"), ("cloudy", "What Happens on a Cloudy Day")],
        """<h2 id="sunlight">From Sunlight to Electricity</h2>
<p>A solar panel is made of photovoltaic cells — usually silicon — that produce direct current (DC) electricity when sunlight hits them. The brighter the sunlight, the more electricity the cells produce. This happens silently, with no moving parts, which is why panels are so reliable: there is very little to wear out.</p>
<p>Panels are mounted on your roof in an array. Each panel contributes to the total output, and the panels are wired together so their combined power flows to the next part of the system. The angle and direction of the panels matter: in Lahore, panels are generally positioned to face the sun for as much of the day as possible, with shading avoided wherever it can be.</p>
<h2 id="inverter">The Inverter: The Heart of the System</h2>
<p>Your home runs on alternating current (AC), but panels produce direct current (DC). The inverter converts DC into AC so your lights, fans, fridge and other appliances can use it. The inverter also manages the flow of power — deciding, in a hybrid system, when to send energy to your home, when to charge the batteries, and when to draw from or export to the grid.</p>
<p>Choosing the right inverter matters as much as choosing the panels. It must be sized to your panel array and your load, and matched to your system type — on-grid, hybrid or off-grid. Our <a href="../blog/solar-inverter-buying-guide.html">solar inverter buying guide</a> explains the options in more detail.</p>
<h2 id="home">How Your Home Uses Solar Power</h2>
<p>During the day, the electricity your panels generate flows first to whatever is running in your home — lights, fans, air conditioning, the water motor, kitchen appliances. If your panels are producing more than you are using, the surplus goes to charge your batteries (in a hybrid or off-grid system) or is exported to the grid (where net metering applies).</p>
<p>This is why daytime usage matters so much. A home that uses most of its power during the day gets the most direct benefit from its panels. A home whose heavy usage is in the evening benefits more from battery storage, which saves daytime energy for later.</p>
<h2 id="batteries-grid">Batteries and the Grid</h2>
<p>In an on-grid system there are no batteries: the grid is effectively your backup, and the system stops producing during a grid outage. In a hybrid system, batteries store energy for evenings and outages. In an off-grid system, batteries are essential — they are your only source of power after sunset.</p>
<p>Net metering, where available, lets a grid-connected system export surplus energy and receive credit for it under your electricity provider's rules. The process and the rules depend on your provider, and we explain them during a consultation rather than promising anything in advance.</p>
<h2 id="performance">What Affects Performance</h2>
<p>Several things affect how much electricity a solar system produces: the amount of sunlight, the angle and direction of the panels, shading from nearby buildings or trees, dust on the panels, and temperature — panels actually perform slightly less efficiently in extreme heat, which is worth knowing in Lahore's summers. Regular <a href="../blog/solar-panel-maintenance.html">solar panel maintenance</a>, especially cleaning, helps keep output where it should be.</p>
<p>The honest summary: solar is a straightforward technology. Sunlight hits panels, the inverter converts the power, and your home uses it. The skill is in planning the system properly for your property — which is where a good installer earns their keep. If you would like to talk through a system for your home, <a href="../contact.html">contact us for a free consultation</a>.</p>
<h2 id="cloudy">What Happens on a Cloudy Day</h2>
<p>Solar panels still generate electricity on cloudy days — just less of it. Diffuse sunlight still reaches the cells, so a system keeps working through overcast weather and the monsoon season, at reduced output. This is one reason installers in Lahore plan systems with some margin: a system sized only for perfect sunny days would disappoint for part of the year. Batteries and the grid cover the gaps, which is exactly what hybrid systems are designed to do.</p>
<p>Winter is the other seasonal change worth knowing about. Days are shorter, so total daily generation falls, even though cooler temperatures actually help panels run more efficiently. A well-planned system accounts for both seasons rather than assuming summer conditions all year round.</p>""",
        ["hybrid-vs-on-grid-solar-systems", "solar-battery-storage-explained"])

    articles["hybrid-vs-on-grid-solar-systems.html"] = article_page(
        "hybrid-vs-on-grid-solar-systems", "Hybrid vs On-Grid Solar Systems", "Hybrid Solar Systems",
        "The two most common system types in Lahore, compared honestly — what each does, what each cannot do, and who each one suits.",
        "assets/images/hybrid-inverter-battery-system.jpg", "Hybrid inverter with battery storage",
        [("on-grid", "How an On-Grid System Works"), ("hybrid", "How a Hybrid System Works"),
         ("compare", "Side-by-Side Comparison"), ("who", "Which One Suits You?"),
         ("cost", "Cost and Honest Trade-Offs"), ("net-metering", "What About Net Metering?")],
        """<h2 id="on-grid">How an On-Grid System Works</h2>
<p>An on-grid solar system connects your panels to the electricity grid through an inverter. During the day, your panels generate electricity and your home uses it directly. If the panels produce more than you need, the surplus can be exported to the grid where net metering is available.</p>
<p>On-grid systems are the simplest type of solar installation. There are no batteries to buy, maintain or replace, and fewer components overall. That simplicity is also their main limitation: without batteries, there is no stored energy. When the grid goes down, an on-grid system stops supplying power on its own.</p>
<h2 id="hybrid">How a Hybrid System Works</h2>
<p>A hybrid system adds batteries and a hybrid inverter to the same idea. The panels generate electricity during the day; the inverter sends power to your home first, charges the batteries with the surplus, and can draw from the grid when solar is not enough. In the evening, or during an outage, the batteries supply your essential loads — how much, and for how long, depends on the battery capacity and what is connected.</p>
<p>This flexibility is why hybrid systems are the most common choice for homes in Bahria Town Lahore. They cover daytime generation and give you something to fall back on when the grid is off. Read more on our <a href="../hybrid-solar-systems.html">hybrid solar systems</a> page.</p>
<h2 id="compare">Side-by-Side Comparison</h2>
<p><strong>Components:</strong> on-grid needs panels and an inverter. Hybrid adds batteries and a hybrid inverter.</p>
<p><strong>During an outage:</strong> on-grid stops on its own. Hybrid can keep essential loads running from stored energy.</p>
<p><strong>At night:</strong> on-grid has nothing stored. Hybrid draws from its batteries until they run down.</p>
<p><strong>Upfront cost:</strong> on-grid is cheaper to install. Hybrid costs more, mostly because of the batteries.</p>
<p><strong>Complexity:</strong> on-grid is simpler. Hybrid needs careful battery sizing and configuration.</p>
<h2 id="who">Which One Suits You?</h2>
<p>Choose on-grid if your grid connection is stable, your heavy usage happens during the day, and you mainly want to make better use of sunlight without paying for batteries.</p>
<p>Choose hybrid if outages are a regular problem for you, if your important loads run in the evening, or if you want the reassurance of stored energy. Most families in Bahria Town who ask us about backup end up choosing hybrid — but it is not the right answer for everyone, and we will say so if your situation points the other way.</p>
<h2 id="cost">Cost and Honest Trade-Offs</h2>
<p>There is no single price for either system: it depends on size, components and your property. What is certain is that hybrid costs more upfront, because batteries are a significant part of the system. Batteries also have a service life and will need replacement one day — a cost that should be part of the decision, not a surprise later.</p>
<p>Neither system is "better" in the abstract. The right question is which one fits your home, your usage and your priorities. If you are unsure, <a href="../contact.html">talk to us</a> — we will ask the right questions and give you an honest recommendation, even if that recommendation is to start with the simpler system.</p>
<h2 id="net-metering">What About Net Metering?</h2>
<p>Net metering is often part of the hybrid versus on-grid decision, so it is worth understanding. Where it is available, a grid-connected system can export surplus daytime energy and receive credit under your electricity provider's rules. Both hybrid and on-grid systems can use it, since both connect to the grid.</p>
<p>The details — application, a bidirectional meter, approval — depend on your provider, and the process takes time. It is not something an installer can promise on your behalf. What we can do is explain the process, help with the paperwork we are responsible for, and set honest expectations about what net metering does and does not do for your bills.</p>""",
        ["how-solar-energy-works", "solar-battery-storage-explained"])

    articles["how-to-choose-solar-panels.html"] = article_page(
        "how-to-choose-solar-panels", "How to Choose Solar Panels", "Solar Panels",
        "Wattage is only part of the story. Efficiency, build quality, heat performance and warranty terms all matter — here is what to look for.",
        "assets/images/solar-panel-cells-closeup.jpg", "Solar panel cells close-up",
        [("wattage", "Wattage Is Not the Whole Story"), ("types", "Panel Types"),
         ("heat", "Heat, Dust and Lahore's Climate"), ("warranty", "Warranties Worth Reading"),
         ("installer", "The Installer's Role"), ("roof", "Matching Panels to Your Roof")],
        """<h2 id="wattage">Wattage Is Not the Whole Story</h2>
<p>When people compare solar panels, the first number they look at is usually the wattage — how much power a panel is rated to produce. Wattage matters, but it is only one part of the picture. A panel's real value is how much energy it produces over years on your roof, in your climate, and that depends on several other factors too.</p>
<p>Efficiency is one of them. A more efficient panel produces more power from the same roof area. If your roof is large, efficiency matters less; if roof space is tight, it matters a lot. Either way, efficiency should be weighed against price — the most efficient panel is not automatically the best value for your home.</p>
<h2 id="types">Panel Types</h2>
<p>Most residential panels today are monocrystalline — made from a single silicon crystal — which generally offers higher efficiency and a sleeker look. Polycrystalline panels, made from multiple silicon fragments, are usually cheaper but slightly less efficient. Both types work well; the choice depends on your roof space, your budget and what is available.</p>
<p>Beyond the cell type, look at the build: the frame, the glass, the junction box and the overall finish. A well-built panel survives Lahore's summers, monsoon rain and winter dust far better than a cheaply made one.</p>
<h2 id="heat">Heat, Dust and Lahore's Climate</h2>
<p>Solar panels are tested at 25°C, but Lahore's rooftops get far hotter in summer — and panels lose a little efficiency as they heat up. The temperature coefficient on a panel's datasheet tells you how much output drops per degree above the test temperature. A lower (better) coefficient is worth having in our climate.</p>
<p>Dust is the other local factor. A layer of dust blocks sunlight and reduces output, which is why <a href="../blog/solar-panel-maintenance.html">regular cleaning</a> matters. Panels with good build quality and a sensible tilt shed dust and rain better than flat-mounted, poorly finished ones.</p>
<h2 id="warranty">Warranties Worth Reading</h2>
<p>Panels usually carry two warranties: a product warranty (against manufacturing defects) and a performance warranty (guaranteeing a percentage of output after a number of years). Read both. A long performance warranty means little if the manufacturer is unlikely to be around to honour it, so the reputation of the brand behind the panel matters too.</p>
<h2 id="installer">The Installer's Role</h2>
<p>Here is the part brochures skip: even the best panel performs badly if it is installed badly — wrong angle, poor mounting, shading that was never checked, or wiring that loses power before it reaches your inverter. Panel choice and installation quality go together.</p>
<p>When we plan a system, we recommend panels that suit your roof, your budget and the local climate — and we explain why. If you want to talk through the options for your home, <a href="../contact.html">contact us for a free consultation</a>. You can also read our guide to <a href="../solar-panel-installation.html">solar panel installation</a> to see how the work is done.</p>
<h2 id="roof">Matching Panels to Your Roof</h2>
<p>The best panel on paper is not the best panel for your roof if it does not fit well. Roof size decides how many panels you can place; roof direction and shading decide how much each panel will produce. A large, unshaded roof gives you freedom to choose on value. A small or partly shaded roof pushes you towards higher-efficiency panels, because every square metre has to work harder.</p>
<p>Mounting matters too. Panels need a secure structure that holds them at a sensible angle, lets air flow underneath to keep them cooler, and survives Lahore's summer heat and monsoon winds. During our assessment we measure the roof, check the structure and look at shading through the day — then recommend panels that fit the roof you actually have, not the roof in a brochure.</p>""",
        ["solar-panel-maintenance", "solar-inverter-buying-guide"])

    articles["solar-inverter-buying-guide.html"] = article_page(
        "solar-inverter-buying-guide", "Solar Inverter Buying Guide", "Solar Inverters",
        "The inverter is the heart of your system. This guide explains the main types, sizing and the features worth paying attention to.",
        "assets/images/solar-inverter-battery-wall.jpg", "Wall-mounted solar inverter and battery",
        [("job", "What an Inverter Actually Does"), ("types", "The Main Types"),
         ("sizing", "Sizing: Getting It Right"), ("features", "Features Worth Having"),
         ("choosing", "Choosing With Your Installer"), ("placement", "Installation and Placement")],
        """<h2 id="job">What an Inverter Actually Does</h2>
<p>Your solar panels produce direct current (DC). Your home runs on alternating current (AC). The inverter converts one to the other — and that is only the start of its job. In a hybrid system it also manages the flow of power between panels, batteries and the grid, deciding moment by moment where energy should go.</p>
<p>Because the inverter works constantly, it is the component most likely to need attention over the life of your system. Panels can last decades with little care; inverters work harder and are usually replaced at least once during a system's lifetime. That is normal, and it is worth knowing before you buy.</p>
<h2 id="types">The Main Types</h2>
<p><strong>On-grid (string) inverters</strong> connect your panel array to the grid. They are simple, reliable and the standard choice for grid-connected systems without batteries.</p>
<p><strong>Hybrid inverters</strong> do the same job and also manage batteries — charging them from solar or the grid, and supplying your home from stored energy when needed. They are the right choice for hybrid systems.</p>
<p><strong>Off-grid inverters</strong> work in systems with no grid connection at all, managing panels and batteries as your only power source.</p>
<p>There are also microinverters and optimisers, which work at the level of individual panels. They can help where shading is a problem, but they add cost and complexity. Whether they suit your roof is a question for your installer, not a catalogue.</p>
<h2 id="sizing">Sizing: Getting It Right</h2>
<p>An inverter must be sized to your panel array and your load. Too small, and it limits what your panels can deliver. Too large, and you have paid for capacity you never use. Sizing also depends on your system type — a hybrid inverter must handle both solar input and battery charging, which changes the calculation.</p>
<p>This is one of the places where a good installer earns their fee. Sizing is not a guess; it comes from your load assessment and your panel plan.</p>
<h2 id="features">Features Worth Having</h2>
<p>Look for clear monitoring — the ability to see what your system is producing and how it is performing, ideally from your phone. Look at the warranty and the service support behind it: a long warranty is only useful if someone will honour it. And check the operating temperature range — inverters in Lahore need to cope with real summer heat, so placement and ventilation matter as much as the unit itself.</p>
<h2 id="choosing">Choosing With Your Installer</h2>
<p>The inverter should be chosen together with your panels and batteries, as one system. A panel is only as useful as the inverter behind it, and a battery is only as useful as the inverter managing it.</p>
<p>If you are planning a system, talk to us about inverters as part of the consultation — not as an afterthought. You can also read about our <a href="../solar-inverter-installation.html">solar inverter installation</a> service to see how the work is done, and our <a href="../blog/hybrid-vs-on-grid-solar-systems.html">hybrid vs on-grid guide</a> to understand which system type fits your home.</p>
<h2 id="placement">Installation and Placement</h2>
<p>Where an inverter is installed matters. Inverters generate heat, so they need ventilation and shade — a cool, sheltered spot indoors or under cover, not a sun-baked wall. They also need to be accessible, because you will want to see the display and reach the unit if anything needs checking.</p>
<p>Wiring between the panels, inverter and batteries should be neat, protected and correctly sized. Undersized cabling wastes energy as heat and can become a safety issue; oversized cabling wastes money. These are details a professional installer gets right as a matter of routine, and they are part of what you are paying for when you choose a proper installation rather than the cheapest quote.</p>""",
        ["how-to-choose-solar-panels", "solar-battery-storage-explained"])

    articles["solar-battery-storage-explained.html"] = article_page(
        "solar-battery-storage-explained", "Solar Battery Storage Explained", "Solar Batteries",
        "What batteries actually do, what capacity means in real life, and how to think about backup without overspending.",
        "assets/images/solar-inverter-battery-wall.jpg", "Solar battery storage with inverters",
        [("what", "What a Solar Battery Does"), ("capacity", "Capacity: What the Numbers Mean"),
         ("types", "Battery Types"), ("sizing", "Sizing for Your Home"),
         ("life", "Lifespan and Replacement"), ("shedding", "Batteries and Load Shedding")],
        """<h2 id="what">What a Solar Battery Does</h2>
<p>A solar battery stores the electricity your panels generate during the day so you can use it later — in the evening, at night, or during a power outage. Without a battery, daytime surplus is either exported to the grid (where net metering applies) or simply not used.</p>
<p>Batteries are a core part of hybrid and off-grid systems. They are not part of a basic on-grid system. Whether you need one depends on when you use power and how much backup matters to you.</p>
<h2 id="capacity">Capacity: What the Numbers Mean</h2>
<p>Battery capacity is measured in kilowatt-hours (kWh). One kWh is roughly enough to run a 100-watt light for ten hours — or, more usefully, to keep a few fans, lights and a fridge going for an evening. The number on the box is the total capacity; the usable capacity is usually less, because batteries should not be fully drained every time.</p>
<p>Depth of discharge is the term for how much of a battery's capacity you can safely use. Lithium batteries can typically be discharged much further than older lead-acid types, which is one reason they have become the standard for home solar storage.</p>
<h2 id="types">Battery Types</h2>
<p><strong>Lithium batteries</strong> are the common choice for home solar today: they store more energy in less space, can be discharged further, last longer and need less maintenance. They cost more upfront.</p>
<p><strong>Lead-acid batteries</strong> are cheaper to buy but bulkier, heavier, less efficient and shorter-lived, and they need more care. They still have a place in some off-grid setups, but for most homes in Bahria Town, lithium is the practical choice.</p>
<h2 id="sizing">Sizing for Your Home</h2>
<p>This is the decision that matters most — and the one where overspending is easiest. A battery sized to run your whole house through the night costs far more than one sized for essential loads: lights, fans, a fridge, phone charging and a few sockets.</p>
<p>We size batteries by asking what you actually want to keep running during an outage or in the evening, and for how long. Air conditioning, water heaters and other heavy loads change the answer completely, and we discuss that honestly rather than selling you the biggest battery available.</p>
<h2 id="life">Lifespan and Replacement</h2>
<p>Batteries do not last forever. Their lifespan depends on the type, how deeply they are discharged, and how hot they get. A lithium battery in a well-planned system can serve for many years, but it will eventually need replacement — a real cost that should be part of your decision from the start, not a surprise years later.</p>
<p>If you want to talk through battery options for your home, <a href="../contact.html">contact us for a free consultation</a>. You can also read about our <a href="../solar-battery-solutions.html">solar battery solutions</a> and our <a href="../blog/hybrid-vs-on-grid-solar-systems.html">hybrid vs on-grid guide</a>.</p>
<h2 id="shedding">Batteries and Load Shedding</h2>
<p>For many families in Lahore, the real reason for buying batteries is load shedding. The question to ask is not "how big a battery can I buy" but "what do I need to keep running when the power goes out, and for how long?"</p>
<p>Make a list: lights in the rooms you use, ceiling fans, the fridge, phone charging, perhaps a television or a laptop. Add up what those draw, multiply by the hours you want them covered, and you have a realistic picture of the storage you need. Air conditioning changes the picture completely — a single air conditioner can use more in an hour than all your lights and fans combined — so be honest with yourself and your installer about whether cooling is part of your backup plan.</p>
<p>A battery sized to your real essential loads costs far less than one sized to run everything, and it will serve you better because it is used properly instead of being drained flat every night.</p>""",
        ["hybrid-vs-on-grid-solar-systems", "solar-inverter-buying-guide"])

    articles["solar-panel-maintenance.html"] = article_page(
        "solar-panel-maintenance", "Solar Panel Maintenance", "Solar Maintenance",
        "Cleaning, checks and the simple habits that keep your panels performing well in Lahore's dust and heat.",
        "assets/images/solar-panel-installation-worker.jpg", "Installer working on rooftop solar panels",
        [("why", "Why Maintenance Matters"), ("cleaning", "Cleaning Your Panels"),
         ("checks", "What to Check Regularly"), ("professional", "When to Call a Professional"),
         ("safety", "Safety First"), ("records", "Keeping Simple Records")],
        """<h2 id="why">Why Maintenance Matters</h2>
<p>Solar panels have no moving parts, so they need very little maintenance compared with most things in a home. But "very little" is not "none". Dust, bird droppings and pollution build up on the glass, and even a thin layer blocks sunlight and reduces output. In Lahore, where dust is a fact of life for much of the year, cleaning makes a real difference.</p>
<p>The good news is that basic maintenance is simple, cheap and quick. A few habits, done regularly, keep your system performing as it should.</p>
<h2 id="cleaning">Cleaning Your Panels</h2>
<p>Clean your panels with plain water and a soft cloth or sponge — early in the morning or in the evening, when the panels are cool. Never use harsh chemicals, abrasive pads or a high-pressure washer, all of which can damage the glass or the seals.</p>
<p>How often? It depends on your location and the season. In dusty periods, every few weeks is sensible; after rain, nature often does the job for you. If you notice output dropping and the panels look dirty, that is your cue. Some homeowners clean their own panels; others prefer to have it done professionally — either is fine, as long as it gets done.</p>
<h2 id="checks">What to Check Regularly</h2>
<p>Every month or so, take a look at your system: are all the panels intact, with no cracks or visible damage? Is the mounting secure? Is there anything shading the panels that was not there before — a growing tree, a new structure next door? Check your inverter display or monitoring app too: is the system producing roughly what you expect for the season? A sudden, unexplained drop is worth investigating.</p>
<p>Also keep the area around your inverter and batteries clear and ventilated. Inverters generate heat and need airflow; batteries need the same.</p>
<h2 id="professional">When to Call a Professional</h2>
<p>Call a professional if you see cracked panels, loose mounting, damaged wiring, water where it should not be, or an inverter showing a fault. Do not try to repair electrical components yourself — solar systems carry live DC voltage even when the grid is off, and that is dangerous without the right knowledge and tools.</p>
<p>An annual professional check is a sensible habit: mounting, wiring, inverter health and battery condition, all reviewed by someone who knows what to look for. If your system was installed by us, <a href="../contact.html">contact us</a> and we will arrange it.</p>
<h2 id="safety">Safety First</h2>
<p>Never climb onto a roof that is wet, steep or unstable to clean panels, and never work on a solar system while it is live. If your panels are hard to reach safely, hire someone with the right equipment. A clean panel is not worth a fall.</p>
<p>Maintenance is the unglamorous part of owning solar — but it is also the part that protects your investment. A little attention, a few times a year, is all it takes.</p>
<h2 id="records">Keeping Simple Records</h2>
<p>You do not need a spreadsheet to look after a solar system, but a few notes go a long way. Once a month, jot down what your system produced — from the inverter display or the monitoring app — and the date you last cleaned the panels. Over a few months you will learn what normal looks like for your home in each season.</p>
<p>That baseline is what lets you spot a problem early. If output drops sharply and the panels are clean, something has changed — shading, a connection, or the inverter — and it is worth a professional look. Without records, a slow decline can go unnoticed for a year. With them, you catch it in a month.</p>
<p>Keep your installer's number handy too. If your system was installed by us, <a href="../contact.html">contact us</a> — a quick call about something that looks wrong is always better than waiting.</p>""",
        ["how-to-choose-solar-panels", "how-solar-energy-works"])

    articles["solar-energy-for-pakistani-homes.html"] = article_page(
        "solar-energy-for-pakistani-homes", "Solar Energy for Pakistani Homes", "Solar Energy",
        "Long sunny days, an unreliable grid and rising bills — why solar fits Pakistani homes, and which system type suits which household.",
        "assets/images/solar-panels-roof-sunset.jpg", "Rooftop solar panels at sunset",
        [("why", "Why Solar Fits Pakistan"), ("types", "Which System Type?"),
         ("loads", "Planning Around Your Load"), ("net-metering", "Net Metering"),
         ("honest", "Honest Limits"), ("small", "Starting Small Is Fine")],
        """<h2 id="why">Why Solar Fits Pakistan</h2>
<p>Pakistan has two things that make solar unusually practical: abundant sunlight for most of the year, and an electricity grid that many households cannot rely on. Add rising electricity costs, and it is easy to see why so many homeowners in Lahore are looking at their roofs differently.</p>
<p>A solar system turns an unused roof into a source of power. During the day, your panels generate electricity for your home. With battery storage, that energy can also cover your evenings and the hours when the grid is down. For a family that has lived through load shedding, that is not a luxury — it is peace of mind.</p>
<h2 id="types">Which System Type?</h2>
<p>For most Pakistani homes, the choice is between hybrid and on-grid. An on-grid system is simpler and cheaper, and suits homes with a stable grid connection that mainly want daytime generation. A hybrid system adds batteries, so it keeps essential loads running during outages — which is why it is the most common choice for families in Bahria Town Lahore.</p>
<p>Off-grid systems are for properties without a grid connection at all. Our <a href="../blog/hybrid-vs-on-grid-solar-systems.html">hybrid vs on-grid guide</a> compares the two main options in detail.</p>
<h2 id="loads">Planning Around Your Load</h2>
<p>Pakistani homes have distinctive loads: ceiling fans and air conditioning in summer, water motors, irons, washing machines, fridges and the ever-growing collection of chargers. A system planned around your real load — not a generic package — performs far better.</p>
<p>That is why we always start with a conversation about how your household actually uses electricity, and when. A family that runs air conditioning all afternoon needs a different system from one whose heavy usage is in the evening.</p>
<h2 id="net-metering">Net Metering</h2>
<p>Where net metering is available, a grid-connected system can export surplus daytime energy and receive credit under your electricity provider's rules. The process involves an application, a bidirectional meter and approval — and the details depend on your provider. We explain the process during a consultation and do not promise approvals or timelines we cannot control.</p>
<h2 id="honest">Honest Limits</h2>
<p>Solar is not magic. It does not eliminate your electricity bill on its own, it does not power your home at night without batteries, and it does not fix a roof that cannot carry panels. What it does, when planned properly, is give your household a reliable source of daytime power and — with storage — a buffer against outages.</p>
<p>If you are considering solar for your home in Lahore, start with a conversation, not a purchase. <a href="../contact.html">Contact us for a free consultation</a> and we will talk through your home, your usage and your options — honestly.</p>
<h2 id="small">Starting Small Is Fine</h2>
<p>You do not have to solar-power your entire home on day one. Many families start with a system that covers their daytime essentials and a few key backup loads, then expand later as their needs or budget allow. A system planned with growth in mind — an inverter with room to add panels, space for another battery — makes that easy.</p>
<p>What matters is starting with a proper plan. A small, well-planned system that works reliably is worth far more than a large one that was never sized to your home. Talk to an installer who asks about your load and your roof before talking about price, and be wary of anyone who pushes a single package for every home.</p>
<p>Solar is a long-term decision. The panels on your roof will be there for years, so the few hours you spend planning now will pay off for a long time. And if you would like a hand with that planning, we are here in Bahria Town Lahore — <a href="../contact.html">contact us for a free consultation</a>.</p>""",
        ["hybrid-vs-on-grid-solar-systems", "solar-installation-planning-in-lahore"])

    articles["solar-installation-planning-in-lahore.html"] = article_page(
        "solar-installation-planning-in-lahore", "Solar Installation Planning in Lahore", "Solar Installation Lahore",
        "Before you buy anything: load, roof, system type, installer and the questions to ask — a planning checklist for Lahore homeowners.",
        "assets/images/modern-house-flat-roof-solar.jpg", "Modern house with rooftop solar panels",
        [("start", "Start With Your Load"), ("roof", "Check Your Roof"),
         ("system", "Choose the System Type"), ("installer", "Choose the Installer"),
         ("rules", "Rules, Net Metering and Paperwork"), ("checklist", "Your Planning Checklist"),
         ("after", "After Installation")],
        """<h2 id="start">Start With Your Load</h2>
<p>Before you buy a single panel, understand how your home uses electricity. Which appliances run, and when? How much do you use during the day versus the evening? Do you want backup during outages, and if so, for which loads?</p>
<p>These questions decide everything else — system size, battery needs, even whether solar is the right step for you right now. A good installer asks them before quoting anything. If someone quotes you a system without asking about your load, that is a warning sign.</p>
<h2 id="roof">Check Your Roof</h2>
<p>Your roof needs to carry the panels, face the sun reasonably well, and stay free of shading for most of the day. Flat roofs are common in Bahria Town and usually work well with the right mounting structure. Check for shading from neighbouring buildings and trees, and think about whether anything will be built nearby that could shade your panels in future.</p>
<p>Roof condition matters too. If your roof needs repair, do that before the panels go on — moving a whole array later is expensive and disruptive.</p>
<h2 id="system">Choose the System Type</h2>
<p>Hybrid, on-grid or off-grid? For most Lahore homes the real choice is hybrid versus on-grid. Hybrid gives you battery backup; on-grid is simpler and cheaper. Our <a href="../blog/hybrid-vs-on-grid-solar-systems.html">hybrid vs on-grid guide</a> walks through the trade-offs. Decide based on your outage experience and your evening usage, not on what is fashionable.</p>
<h2 id="installer">Choose the Installer</h2>
<p>The installer matters as much as the equipment. Ask how long they have worked in your area, whether they assess your property before quoting, and what their handover includes. Ask what happens if something goes wrong after installation — a local installer you can reach is worth more than a distant one with a glossy brochure.</p>
<p>We are based in Bahria Town Lahore, at Plaza 210, Sector C, Tulip Commercial — and we stay reachable after the work is done. You can read about <a href="../about.html">how we work</a> and our <a href="../services.html">services</a> before you decide anything.</p>
<h2 id="rules">Rules, Net Metering and Paperwork</h2>
<p>Community guidelines in Bahria Town, building considerations, and — for grid-connected systems — net metering applications all need attention. None of this is difficult, but it should be discussed upfront, not discovered afterwards. Ask your installer what is involved for your property specifically.</p>
<h2 id="checklist">Your Planning Checklist</h2>
<p>Before you commit: know your load and when you use power. Check your roof's condition, direction and shading. Decide whether you need battery backup. Choose an installer who assesses your property first. Understand the net metering process for your provider. And get everything — system size, components, price and what is included — in writing.</p>
<p>Planning well is the difference between a system that serves you for years and one that disappoints. If you would like help planning for your home, <a href="../contact.html">contact us for a free consultation</a> — the conversation costs nothing, and it is the right place to start.</p>
<h2 id="after">After Installation</h2>
<p>Planning does not stop when the panels go up. Ask your installer what the handover includes: a walkthrough of the system, an explanation of the inverter display, guidance on cleaning and basic checks, and a clear point of contact if anything goes wrong. You should leave the handover knowing how your system works and how to look after it — not just holding a remote control you were never shown how to use.</p>
<p>Keep the documentation too: warranties, the system plan, and the installer's contact details. If you sell the house one day, the next owner will want to know what is on the roof. And if you ever want to expand the system, the original plan makes that straightforward instead of a fresh investigation.</p>
<p>A good installation ends with a confident homeowner, not a confused one. That is the standard we hold ourselves to — and it is the standard you should expect from any installer you choose.</p>""",
        ["solar-energy-for-pakistani-homes", "how-solar-energy-works"])

    return articles

# ============================================================ SITEMAP =====
SITEMAP_PAGES = [
    "index.html", "about.html", "services.html",
    "residential-solar-installation.html", "commercial-solar-installation.html",
    "hybrid-solar-systems.html", "on-grid-solar-systems.html", "off-grid-solar-systems.html",
    "solar-panel-installation.html", "solar-inverter-installation.html",
    "solar-battery-solutions.html", "solar-installation-bahria-town-lahore.html",
    "solar-installation-lahore.html", "projects.html", "blog.html",
    "blog/how-solar-energy-works.html", "blog/hybrid-vs-on-grid-solar-systems.html",
    "blog/how-to-choose-solar-panels.html", "blog/solar-inverter-buying-guide.html",
    "blog/solar-battery-storage-explained.html", "blog/solar-panel-maintenance.html",
    "blog/solar-energy-for-pakistani-homes.html", "blog/solar-installation-planning-in-lahore.html",
    "contact.html", "privacy-policy.html", "terms-and-conditions.html",
]

def build_sitemap():
    if SITE_URL:
        urls = "\n".join(
            "  <url>\n    <loc>{u}</loc>\n    <lastmod>{d}</lastmod>\n    <changefreq>monthly</changefreq>\n  </url>".format(
                u=abs_url(p), d=TODAY) for p in SITEMAP_PAGES)
    else:
        urls = "\n".join(
            "  <!-- Set SITE_URL in build.py and rebuild to add absolute URLs -->\n"
            "  <url>\n    <loc>{p}</loc>\n    <lastmod>{d}</lastmod>\n  </url>".format(
                p=p, d=TODAY) for p in SITEMAP_PAGES)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + urls + '\n</urlset>\n')

def build_robots():
    sitemap_line = "Sitemap: {}/sitemap.xml".format(SITE_URL.rstrip("/")) if SITE_URL else "# Set SITE_URL in build.py and rebuild to enable the absolute sitemap URL"
    return ("User-agent: *\nAllow: /\n\n" + sitemap_line + "\n")

# ================================================================ MAIN =====
def main():
    built = []
    built.append(write("index.html", build_home()))
    built.append(write("about.html", build_about()))
    built.append(write("services.html", build_services()))
    for name, html in build_service_pages().items():
        built.append(write(name, html))
    built.append(write("solar-installation-bahria-town-lahore.html", build_bahria_location()))
    built.append(write("solar-installation-lahore.html", build_lahore_location()))
    built.append(write("projects.html", build_projects()))
    built.append(write("blog.html", build_blog_index()))
    for name, html in build_articles().items():
        built.append(write("blog/" + name, html))
    built.append(write("contact.html", build_contact()))
    built.append(write("privacy-policy.html", build_privacy()))
    built.append(write("terms-and-conditions.html", build_terms()))
    built.append(write("404.html", build_404()))
    built.append(write("sitemap.xml", build_sitemap()))
    built.append(write("robots.txt", build_robots()))
    print("Built {} files:".format(len(built)))
    for b in built:
        print("  " + b)
    if not SITE_URL:
        print("\nNOTE: SITE_URL is empty — canonical/OG URLs omitted, links are relative.")
        print("Set SITE_URL in build.py to the GitHub Pages URL and re-run to enable them.")

if __name__ == "__main__":
    main()
