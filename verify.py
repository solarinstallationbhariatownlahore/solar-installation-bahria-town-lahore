#!/usr/bin/env python3
"""Verify the built site: HTTP 200s, internal links, JSON-LD, social links,
forbidden text, images, and form JS. Serves the site locally and curls it."""
import json, os, re, subprocess, sys, time, urllib.request, urllib.error
from html.parser import HTMLParser

ROOT = os.path.expanduser("~/workspace/solar-bahria-website")
PORT = 8123
BASE = f"http://127.0.0.1:{PORT}"

failures, notes = [], []

def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(name + " " + detail)

# ---- start server -------------------------------------------------------
srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT)],
                       cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)

def get(path):
    try:
        with urllib.request.urlopen(BASE + path, timeout=10) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return None, str(e)

try:
    pages = []
    for dp, _, fns in os.walk(ROOT):
        for fn in fns:
            if fn.endswith(".html"):
                pages.append(os.path.relpath(os.path.join(dp, fn), ROOT))
    pages.sort()
    print(f"{len(pages)} HTML pages found")

    # 1. every page returns 200
    bodies = {}
    bad = []
    for p in pages:
        st, body = get("/" + p)
        if st != 200:
            bad.append((p, st))
        else:
            bodies[p] = body
    check("all pages return HTTP 200", not bad, str(bad) if bad else f"{len(pages)} pages")

    # 2. every internal link resolves
    class LinkParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.links = set()
        def handle_starttag(self, tag, attrs):
            d = dict(attrs)
            for a in ("href", "src"):
                if a in d:
                    self.links.add(d[a])

    def resolve(page, link):
        if not link or link.startswith(("#", "mailto:", "tel:", "javascript:")):
            return None
        if link.startswith("http"):
            return ("external", link)
        link = link.split("#")[0].split("?")[0]
        if not link:
            return None
        if link.startswith("/"):
            return ("local", link.lstrip("/"))
        base = os.path.dirname(page)
        return ("local", os.path.normpath(os.path.join(base, link)))

    missing, external = set(), set()
    for p, body in bodies.items():
        lp = LinkParser(); lp.feed(body)
        for link in lp.links:
            r = resolve(p, link)
            if not r:
                continue
            kind, target = r
            if kind == "external":
                external.add(target)
            else:
                full = os.path.join(ROOT, target)
                if not os.path.isfile(full):
                    missing.add((p, link, target))
    check("all internal links resolve to files", not missing,
          str(sorted(missing)[:10]) if missing else f"{sum(len(bodies[p]) for p in bodies)} bytes scanned")
    # also HTTP-check the local targets that are html/css/js/images
    http_bad = []
    for p, body in bodies.items():
        lp = LinkParser(); lp.feed(body)
        for link in lp.links:
            r = resolve(p, link)
            if r and r[0] == "local":
                st, _ = get("/" + r[1])
                if st != 200:
                    http_bad.append((p, link, st))
    check("all internal links return HTTP 200", not http_bad,
          str(http_bad[:10]) if http_bad else "checked via server")

    # 3. all 8 social URLs in footer of every page
    socials = [
        "web.facebook.com/solarinstallationbhariatownlahore1",
        "x.com/SolarInstam3f9",
        "pinterest.com/solarinstallationbharyiatown",
        "instagram.com/solarinstallactionbharyiatown1",
        "threads.com/@solarinstallationbharyiatown1",
        "medium.com/@solarinstallationbharyiatownl",
        "youtube.com/@solarinstallactionbharyiatown5",
        "tiktok.com/@solarinstallactionbharyi",
    ]
    bad_pages = {}
    for p, body in bodies.items():
        absent = [s for s in socials if s not in body]
        if absent:
            bad_pages[p] = absent
    check("all 8 social URLs present on every page", not bad_pages,
          str(bad_pages) if bad_pages else f"{len(pages)} pages x 8 links")

    # 4. JSON-LD parses as valid JSON on each page
    bad_json = {}
    ld_count = 0
    for p, body in bodies.items():
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.S)
        ld_count += len(blocks)
        for b in blocks:
            try:
                json.loads(b)
            except Exception as e:
                bad_json.setdefault(p, []).append(str(e))
    check("JSON-LD parses as valid JSON", not bad_json,
          str(bad_json) if bad_json else f"{ld_count} blocks across {len(pages)} pages")

    # 5. one H1 per page; title + meta description present
    h1_bad, meta_bad = [], []
    for p, body in bodies.items():
        h1s = re.findall(r"<h1[^>]*>", body)
        if len(h1s) != 1:
            h1_bad.append((p, len(h1s)))
        if not re.search(r"<title>[^<]{10,}</title>", body):
            meta_bad.append((p, "title"))
        if not re.search(r'<meta name="description" content="[^"]{20,}">', body):
            meta_bad.append((p, "description"))
    check("exactly one H1 per page", not h1_bad, str(h1_bad) if h1_bad else "")
    check("title + meta description on every page", not meta_bad, str(meta_bad) if meta_bad else "")

    # 6. forbidden text
    bad_text = {}
    for p in pages:
        with open(os.path.join(ROOT, p), encoding="utf-8") as f:
            txt = f.read()
        hits = []
        if re.search(r"lorem", txt, re.I): hits.append("lorem")
        if re.search(r"TODO|FIXME|XXX", txt): hits.append("TODO/FIXME")
        # 'placeholder' as visible content, not the form attribute
        stripped = re.sub(r'placeholder="[^"]*"', "", txt)
        if re.search(r"placeholder", stripped, re.I): hits.append("placeholder")
        if hits:
            bad_text[p] = hits
    for extra in ["assets/css/style.css", "assets/js/main.js", "README.md"]:
        with open(os.path.join(ROOT, extra), encoding="utf-8") as f:
            txt = f.read()
        if re.search(r"lorem|TODO", txt, re.I):
            bad_text[extra] = ["lorem/TODO"]
    check("no lorem / TODO / placeholder content", not bad_text, str(bad_text) if bad_text else "")

    # 7. business facts consistent
    fact_bad = []
    for p, body in bodies.items():
        if "03200147783" not in body: fact_bad.append((p, "phone"))
        if "Bahria Town" not in body: fact_bad.append((p, "Bahria Town"))
        if "wa.me/923200147783" not in body: fact_bad.append((p, "wa link"))
    check("phone + WhatsApp link on every page", not fact_bad, str(fact_bad) if fact_bad else "")
    addr_bad = [p for p, b in bodies.items() if "Plaza 210" not in b and p not in ("404.html",)]
    check("address present (except 404)", not addr_bad, str(addr_bad) if addr_bad else "")

    # 8. images: exist + valid JPEG
    from PIL import Image
    imgdir = os.path.join(ROOT, "assets/images")
    imgs = sorted(os.listdir(imgdir))
    bad_img = []
    total_kb = 0
    for im in imgs:
        full = os.path.join(imgdir, im)
        total_kb += os.path.getsize(full)
        try:
            with Image.open(full) as pic:
                pic.verify()
                if pic.format != "JPEG":
                    bad_img.append((im, pic.format))
        except Exception as e:
            bad_img.append((im, str(e)))
    check("all images are valid JPEGs", not bad_img,
          f"{len(imgs)} images, {total_kb//1024} KB total" + (f" — {bad_img}" if bad_img else ""))
    # every <img> src in pages exists
    missing_img = set()
    for p, body in bodies.items():
        for src in re.findall(r'<img[^>]+src="([^"]+)"', body):
            r = resolve(p, src)
            if r and r[0] == "local" and not os.path.isfile(os.path.join(ROOT, r[1])):
                missing_img.add((p, src))
    check("every <img> src exists", not missing_img, str(missing_img) if missing_img else "")

    # 9. sitemap + robots
    st, sm = get("/sitemap.xml")
    locs = re.findall(r"<loc>([^<]+)</loc>", sm) if st == 200 else []
    check("sitemap.xml 200 + absolute URLs", st == 200 and len(locs) == 26 and all(l.startswith("https://solarinstallationbhariatownlahore.github.io/") for l in locs),
          f"{len(locs)} URLs")
    st, rb = get("/robots.txt")
    check("robots.txt 200 + sitemap line", st == 200 and "sitemap.xml" in rb, rb.strip().splitlines()[-1] if rb else "")

    # 10. canonical + OG on every page
    canon_bad = [p for p, b in bodies.items()
                 if "solarinstallationbhariatownlahore.github.io/solar-installation-bahria-town-lahore" not in b]
    check("canonical/OG use real GitHub Pages URL", not canon_bad, str(canon_bad) if canon_bad else f"{len(pages)} pages")

    # 11. form JS: node syntax check + WhatsApp logic present
    rc = subprocess.run(["node", "--check", os.path.join(ROOT, "assets/js/main.js")],
                        capture_output=True, text=True)
    check("main.js passes node --check", rc.returncode == 0, rc.stderr.strip()[:200])
    with open(os.path.join(ROOT, "assets/js/main.js"), encoding="utf-8") as f:
        js = f.read()
    js_ok = all(s in js for s in ["wa.me/", "923200147783", "encodeURIComponent",
                                   "hpWebsite", "validPhone", "formStatus"])
    check("form JS has WhatsApp compose + validation + honeypot", js_ok, "")

    # 12. no fake claims
    claim_bad = {}
    for p, body in bodies.items():
        txt = re.sub(r"<[^>]+>", " ", body)
        for pat in [r"\d+\s*%\s*(saving|guarantee)", r"guaranteed savings",
                    r"\d+\s*installations completed", r"★\s*5\.0", r"award-winning"]:
            if re.search(pat, txt, re.I):
                claim_bad.setdefault(p, []).append(pat)
    check("no invented savings/ratings/awards claims", not claim_bad, str(claim_bad) if claim_bad else "")
    # testimonials invite present, no fake names
    check("testimonials = neutral invite, no fabricated reviews",
          "Share Your Experience With Us" in bodies["index.html"]
          and "never invented testimonials" in bodies["index.html"], "")
    # illustrative labelling on gallery
    gal = bodies["index.html"] + bodies["projects.html"]
    check("gallery images labelled Illustrative image",
          gal.count("Illustrative image") >= 9, f"{gal.count('Illustrative image')} labels")

    # 13. external links present (social + GMB + wa) — spot check reachability of GMB cid link format
    check("GMB cid link present on contact page",
          "maps?cid=17411783398733912742" in bodies["contact.html"], "")

    # 14. word counts for blog articles (600-900 words of body text)
    wc = {}
    for p in pages:
        if p.startswith("blog/"):
            body = bodies[p]
            m = re.search(r'<article class="article">(.*?)<div class="share-row">', body, re.S)
            if m:
                text = re.sub(r"<[^>]+>", " ", m.group(1))
                wc[p] = len(text.split())
    wc_bad = {p: n for p, n in wc.items() if not (600 <= n <= 900)}
    check("blog articles ~600-900 words", not wc_bad,
          str(wc) if wc_bad else str(wc))
finally:
    srv.terminate()

print()
print("FAILURES:" if failures else "ALL CHECKS PASSED")
for f in failures:
    print(" -", f)
sys.exit(1 if failures else 0)
