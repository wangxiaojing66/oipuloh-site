#!/usr/bin/env python3
"""Build the Oipuloh brand website from local product data.

Run from this directory:
    python3 build.py

The script only writes generated HTML, sitemap.xml and robots.txt inside this
folder. Product facts come from data/products.json, which was compiled from the
seller's Amazon catalog data.
"""

from __future__ import annotations

import html
import json
import os
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "site.config.json").read_text("utf-8"))["site"]
PRODUCTS = json.loads((ROOT / "data/products.json").read_text("utf-8"))

DOMAIN = os.environ.get("SITE_DOMAIN", CONFIG["domain"]).rstrip("/")
BRAND = CONFIG["brand"]
LEGAL = CONFIG["legalName"]
EMAIL = CONFIG["email"]
AMAZON_SEARCH = CONFIG["amazonSearch"]
BUILD_DATE = CONFIG.get("buildDate") or date.today().isoformat()

AMAZON_BASE = "https://www.amazon.com/dp/"


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def href(path: str, prefix: str = "") -> str:
    return f"{prefix}{path}"


def absolute(path: str) -> str:
    return f"{DOMAIN}/{path.lstrip('/')}"


def logo_mark(size: int = 34) -> str:
    petals = []
    for angle in range(0, 360, 45):
        petals.append(
            f'<ellipse cx="20" cy="9.4" rx="3.1" ry="6.2" '
            f'transform="rotate({angle} 20 20)"/>'
        )
    return (
        f'<svg class="logo-mark" width="{size}" height="{size}" viewBox="0 0 40 40" '
        'aria-hidden="true" focusable="false">'
        f'<g fill="currentColor" opacity=".92">{"".join(petals)}</g>'
        '<circle cx="20" cy="20" r="3.5" fill="var(--paper, #fbf7f0)"/>'
        '<circle cx="20" cy="20" r="1.8" fill="currentColor"/>'
        "</svg>"
    )


def picture(image_key: str, alt: str, prefix: str, class_name: str = "", eager: bool = True, sizes: str = "(max-width: 720px) 92vw, 46vw") -> str:
    base = f"{prefix}assets/img/{image_key}"
    loading = "eager" if eager else "lazy"
    cls = f' class="{class_name}"' if class_name else ""
    return (
        f'<img{cls} src="{base}-700.jpg" '
        f'srcset="{base}-700.jpg 700w, {base}-1400.jpg 1400w" '
        f'sizes="{sizes}" width="1400" height="1400" '
        f'alt="{esc(alt)}" loading="{loading}" decoding="async">'
    )


def site_header(prefix: str, active: str = "") -> str:
    def nav_link(path: str, label: str, key: str) -> str:
        current = ' aria-current="page"' if key == active else ""
        return f'<a href="{href(path, prefix)}"{current}>{label}</a>'

    return f"""
<div class="announcement">
  <span>Hand-crocheted</span><span class="dot" aria-hidden="true"></span>
  <span>Ready to gift</span><span class="dot" aria-hidden="true"></span>
  <span>Available on Amazon</span>
</div>
<header class="site-header" id="siteHeader">
  <div class="shell header-inner">
    <a class="brand" href="{href('index.html', prefix)}" aria-label="{esc(BRAND)} home">
      {logo_mark(36)}
      <span class="brand-type">
        <span class="brand-name">{esc(BRAND)}</span>
        <span class="brand-sub">crochet flowers</span>
      </span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primaryNav">
      <span class="sr-only">Menu</span>
      <span></span><span></span>
    </button>
    <nav class="nav" id="primaryNav" aria-label="Main">
      {nav_link('collection.html', 'Collection', 'collection')}
      {nav_link('about.html', 'Our story', 'about')}
      {nav_link('contact.html', 'Contact', 'contact')}
      <a class="nav-cta" href="{esc(AMAZON_SEARCH)}" target="_blank" rel="noopener">Shop on Amazon</a>
    </nav>
  </div>
</header>
"""


def site_footer(prefix: str) -> str:
    product_links_parts = []
    for product in PRODUCTS[:5]:
        product_url = href("product/{0}.html".format(product["slug"]), prefix)
        product_links_parts.append(
            '<li><a href="{0}">{1}</a></li>'.format(product_url, esc(product["name"]))
        )
    product_links = "".join(product_links_parts)
    return f"""
<footer class="site-footer">
  <div class="shell footer-grid">
    <div class="footer-brand">
      <a class="brand brand--footer" href="{href('index.html', prefix)}" aria-label="{esc(BRAND)} home">
        {logo_mark(42)}
        <span class="brand-type">
          <span class="brand-name">{esc(BRAND)}</span>
          <span class="brand-sub">crochet flowers</span>
        </span>
      </a>
      <p>Hand-crocheted flower bouquets made to outlast the moment. Soft cotton yarn, finished by hand, ready to give.</p>
    </div>
    <div>
      <h2 class="footer-title">Shop</h2>
      <ul class="footer-list">
        {product_links}
        <li><a href="{href('collection.html', prefix)}">All bouquets</a></li>
      </ul>
    </div>
    <div>
      <h2 class="footer-title">Information</h2>
      <ul class="footer-list">
        <li><a href="{href('about.html', prefix)}">Our story</a></li>
        <li><a href="{href('shipping.html', prefix)}">Shipping &amp; returns</a></li>
        <li><a href="{href('privacy.html', prefix)}">Privacy policy</a></li>
        <li><a href="{href('terms.html', prefix)}">Terms of use</a></li>
      </ul>
    </div>
    <div>
      <h2 class="footer-title">Contact</h2>
      <ul class="footer-list">
        <li><a href="mailto:{esc(EMAIL)}">{esc(EMAIL)}</a></li>
        <li><a href="{href('contact.html', prefix)}">Questions &amp; order help</a></li>
        <li><a href="{esc(AMAZON_SEARCH)}" target="_blank" rel="noopener">Oipuloh on Amazon</a></li>
      </ul>
    </div>
  </div>
  <div class="shell footer-bottom">
    <p>&copy; {date.today().year} {esc(LEGAL)}. All rights reserved.</p>
    <p class="fine">Amazon and the Amazon logo are trademarks of Amazon.com, Inc. or its affiliates. {esc(BRAND)} is a brand of {esc(LEGAL)}.</p>
  </div>
</footer>
"""


def page_shell(
    *,
    title: str,
    description: str,
    path: str,
    prefix: str,
    body: str,
    active: str = "",
    og_image: str = "assets/img/daisy-main-1400.jpg",
    og_type: str = "website",
    structured_data: dict | None = None,
    body_class: str = "",
) -> str:
    canonical = absolute(path)
    image_url = absolute(og_image)
    json_ld = ""
    if structured_data:
        json_ld = (
            '<script type="application/ld+json">'
            + json.dumps(structured_data, ensure_ascii=False, separators=(",", ":"))
            + "</script>"
        )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{esc(canonical)}">
  <meta property="og:type" content="{esc(og_type)}">
  <meta property="og:site_name" content="{esc(BRAND)}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(canonical)}">
  <meta property="og:image" content="{esc(image_url)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="{esc(CONFIG['themeColor'])}">
  <link rel="icon" href="{href('assets/img/favicon.svg', prefix)}" type="image/svg+xml">
  <link rel="stylesheet" href="{href('assets/css/styles.css', prefix)}">
  <script>
    if (!new URLSearchParams(location.search).has("static")) document.documentElement.classList.add("js");
  </script>
  {json_ld}
</head>
<body class="{body_class}">
  <a class="skip-link" href="#main">Skip to content</a>
  {site_header(prefix, active)}
  <main id="main">
{body}
  </main>
  {site_footer(prefix)}
  <script src="{href('assets/js/site.js', prefix)}" defer></script>
</body>
</html>
"""


def product_card(product: dict, prefix: str, eager: bool = True) -> str:
    return f"""
<article class="product-card reveal">
  <a class="product-media" href="{href(f'product/{product["slug"]}.html', prefix)}" aria-label="{esc(product['name'])} bouquet">
    {picture(product['image'] + '-main', product['alt'], prefix, eager=True, sizes='(max-width: 640px) 88vw, (max-width: 1100px) 44vw, 30vw')}
  </a>
  <div class="product-card-body">
    <p class="product-kicker">{esc(product['style'])}</p>
    <h3><a href="{href(f'product/{product["slug"]}.html', prefix)}">{esc(product['name'])}</a></h3>
    <p class="product-tagline">{esc(product['tagline'])}</p>
    <p class="product-meta">{esc(product['blooms'])} <span aria-hidden="true">·</span> Gift bag &amp; card</p>
  </div>
</article>
"""


def home_page() -> str:
    featured = ["pink-daisy", "pink-peony", "pink-rose-tulip"]
    cards = "".join(
        product_card(next(p for p in PRODUCTS if p["slug"] == slug), "")
        for slug in featured
    )
    occasion_items = [
        "Birthdays",
        "Anniversaries",
        "Mother's Day",
        "Weddings",
        "Housewarmings",
        "Just because",
    ]
    occasions = "".join(f"<li>{esc(o)}</li>" for o in occasion_items)
    description = (
        "Oipuloh makes hand-crocheted flower bouquets from soft cotton yarn. "
        "No water, no wilting — each arrives with a gift bag and greeting card."
    )
    structured = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": LEGAL,
        "url": DOMAIN + "/",
        "email": EMAIL,
        "brand": {"@type": "Brand", "name": BRAND},
        "logo": absolute("assets/img/favicon.svg"),
        "description": description,
    }
    body = f"""
<section class="hero">
  <div class="shell hero-grid">
    <div class="hero-copy">
      <p class="eyebrow"><span class="rule" aria-hidden="true"></span>Crochet flower bouquets</p>
      <h1>Flowers that <em>stay.</em></h1>
      <p class="lede">Soft cotton blooms, hand-crocheted one stitch at a time. No water, no wilting — just a gift that keeps its shape.</p>
      <div class="actions">
        <a class="button" href="{href('collection.html')}">Explore the collection</a>
        <a class="text-link" href="{href('about.html')}">Our story <span aria-hidden="true">→</span></a>
      </div>
      <ul class="hero-notes">
        <li>Hand-crocheted cotton yarn</li>
        <li>Gift bag + greeting card</li>
        <li>Zero upkeep</li>
      </ul>
    </div>
    <div class="hero-media">
      <div class="arch arch--hero">
        {picture('daisy-main', 'Oipuloh Pink Daisy crochet flower bouquet with gift bag and greeting card', '', eager=True, sizes='(max-width: 900px) 92vw, 44vw')}
      </div>
      <a class="floating-card" href="{href('product/pink-daisy.html')}">
        <span class="floating-card-label">The Pink Daisy</span>
        <span class="floating-card-meta">8 crochet blooms · Ready to gift</span>
        <span class="floating-card-link">View bouquet <span aria-hidden="true">→</span></span>
      </a>
      <span class="hero-stamp" aria-hidden="true">hand<br>made</span>
    </div>
  </div>
</section>

<div class="value-strip">
  <div class="shell value-strip-inner">
    <span>Hand-crocheted</span><span class="dot" aria-hidden="true"></span>
    <span>Soft cotton yarn</span><span class="dot" aria-hidden="true"></span>
    <span>No watering</span><span class="dot" aria-hidden="true"></span>
    <span>Gift-ready</span>
  </div>
</div>

<section class="section" id="collection">
  <div class="shell">
    <div class="section-head reveal">
      <div>
        <p class="eyebrow"><span class="rule" aria-hidden="true"></span>Seven bouquets</p>
        <h2>One quiet idea: flowers should last longer than the moment.</h2>
      </div>
      <a class="text-link" href="{href('collection.html')}">See all bouquets <span aria-hidden="true">→</span></a>
    </div>
    <div class="product-grid product-grid--three">
      {cards}
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="shell split">
    <div class="split-media reveal">
      <div class="arch arch--soft">
        {picture('peony-main', 'Oipuloh Pink Peony crochet bouquet with sage green wrapping', '', sizes='(max-width: 900px) 92vw, 44vw')}
      </div>
    </div>
    <div class="split-copy reveal">
      <p class="eyebrow"><span class="rule" aria-hidden="true"></span>Why Oipuloh</p>
      <h2>Made slowly. Kept for years.</h2>
      <p class="lede-sm">Fresh flowers are beautiful, but they fade, drop petals, and need constant care. A crochet bouquet is a different kind of gift: finished by hand, and ready to stay.</p>
      <dl class="value-list">
        <div>
          <dt>Hand-crocheted, not printed</dt>
          <dd>The blooms are crocheted from soft cotton yarn, so every bouquet has a real textile texture.</dd>
        </div>
        <div>
          <dt>Zero upkeep</dt>
          <dd>No watering, sunlight, pruning, or cleanup. Place it on a desk, shelf, or nightstand and leave it be.</dd>
        </div>
        <div>
          <dt>Ready to give</dt>
          <dd>Each bouquet arrives fully assembled with a gift bag and greeting card.</dd>
        </div>
      </dl>
      <a class="button button--ghost" href="{href('about.html')}">How they are made</a>
    </div>
  </div>
</section>

<section class="section" id="gift">
  <div class="shell gift-grid">
    <div class="gift-copy reveal">
      <p class="eyebrow"><span class="rule" aria-hidden="true"></span>Gift-ready by design</p>
      <h2>A gift you can hand over straight away.</h2>
      <p class="lede-sm">No wrapping, no vase, no last-minute stop at the florist. The bouquet arrives assembled, with a gift bag for the presentation and a greeting card for your own words.</p>
      <ol class="steps">
        <li><span>01</span><p><strong>Choose a bouquet.</strong> Seven flower styles, each with its own mood and color story.</p></li>
        <li><span>02</span><p><strong>It arrives assembled.</strong> The finished bouquet, gift bag, and greeting card come together.</p></li>
        <li><span>03</span><p><strong>Add your message.</strong> Write on the card and hand it over — no extra wrapping needed.</p></li>
      </ol>
    </div>
    <div class="gift-media reveal">
      <div class="gift-photo">
        {picture('daisy-alt', 'Pink Daisy bouquet with clear-window gift bag and heart greeting card', '', sizes='(max-width: 900px) 92vw, 40vw')}
      </div>
      <div class="gift-note">
        <span class="gift-note-title">In every box</span>
        <span>1 finished bouquet</span>
        <span>1 gift bag</span>
        <span>1 greeting card</span>
      </div>
    </div>
  </div>
</section>

<section class="section section--forest">
  <div class="shell occasions">
    <div class="reveal">
      <p class="eyebrow eyebrow--light"><span class="rule" aria-hidden="true"></span>For the moments that matter</p>
      <h2>A bouquet for the occasion — and the quiet days after.</h2>
    </div>
    <ul class="occasion-list reveal">
      {occasions}
    </ul>
    <div class="reveal">
      <a class="button button--light" href="{href('collection.html')}">Find your bouquet</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell faq-grid">
    <div class="faq-intro reveal">
      <p class="eyebrow"><span class="rule" aria-hidden="true"></span>Good to know</p>
      <h2>Questions, answered.</h2>
      <p class="lede-sm">Everything you might want to know before choosing a bouquet.</p>
      <a class="text-link" href="{href('contact.html')}">Ask us something else <span aria-hidden="true">→</span></a>
    </div>
    <div class="faq-list reveal">
      <details>
        <summary>Are the flowers real?</summary>
        <p>They are hand-crocheted from soft cotton yarn — not fresh, dried, or preserved flowers. The texture is textile, and the shape holds.</p>
      </details>
      <details>
        <summary>Do they need water or sunlight?</summary>
        <p>No. The bouquets need no watering, sunlight, pruning, or cleanup. Keep them wherever you would place a small vase.</p>
      </details>
      <details>
        <summary>What is included?</summary>
        <p>One finished bouquet, one gift bag, and one greeting card. The bouquet arrives assembled — it is not a DIY kit.</p>
      </details>
      <details>
        <summary>Will mine look exactly like the photo?</summary>
        <p>Because each bouquet is handmade, stitch detail, flower shape, and color may vary slightly from the photos. That variation is part of the handmade finish.</p>
      </details>
      <details>
        <summary>Where can I buy?</summary>
        <p>Our bouquets are sold on Amazon.com. Price, shipping speed, and availability are shown on each Amazon product page.</p>
      </details>
    </div>
  </div>
</section>

<section class="closing">
  <div class="shell closing-inner reveal">
    <p class="eyebrow eyebrow--light"><span class="rule" aria-hidden="true"></span>The collection</p>
    <h2>Flowers that stay. A gift that keeps.</h2>
    <div class="actions actions--center">
      <a class="button button--light" href="{href('collection.html')}">Shop all seven bouquets</a>
      <a class="text-link text-link--light" href="{esc(AMAZON_SEARCH)}" target="_blank" rel="noopener">Buy on Amazon <span aria-hidden="true">→</span></a>
    </div>
  </div>
</section>
"""
    return page_shell(
        title=f"{BRAND} — Hand-crocheted flower bouquets that stay",
        description=description,
        path="",
        prefix="",
        body=body,
        active="home",
        structured_data=structured,
    )


def collection_page() -> str:
    cards = "".join(product_card(p, "") for p in PRODUCTS)
    body = f"""
<section class="page-hero">
  <div class="shell page-hero-inner">
    <p class="eyebrow"><span class="rule" aria-hidden="true"></span>The collection</p>
    <h1>Seven ways to keep a flower.</h1>
    <p class="lede">Each bouquet is hand-crocheted from soft cotton yarn, finished with a gift bag and greeting card, and made to stay in bloom.</p>
  </div>
</section>
<section class="section section--top-tight">
  <div class="shell">
    <div class="collection-note reveal">
      <p>All bouquets are approximately 13.7 in H × 10.2 in W × 3.3 in D and weigh about 0.44 lb.</p>
      <a class="text-link" href="{esc(AMAZON_SEARCH)}" target="_blank" rel="noopener">See current availability on Amazon <span aria-hidden="true">→</span></a>
    </div>
    <div class="product-grid">
      {cards}
    </div>
  </div>
</section>
<section class="section section--tint">
  <div class="shell narrow center">
    <p class="eyebrow eyebrow--center">A note on handmade</p>
    <h2>Every bouquet is a little different.</h2>
    <p class="lede-sm">Because each piece is crocheted and assembled by hand, stitch detail, flower shape, and color may vary slightly. The photos show the style; your bouquet will have its own small variations.</p>
  </div>
</section>
"""
    return page_shell(
        title=f"The Collection — {BRAND} crochet flower bouquets",
        description="Explore seven hand-crocheted flower bouquets from Oipuloh. Cotton yarn, zero upkeep, gift bag and greeting card included.",
        path="collection.html",
        prefix="",
        body=body,
        active="collection",
    )


def product_page(product: dict) -> str:
    others = [p for p in PRODUCTS if p["slug"] != product["slug"]][:3]
    related = "".join(product_card(p, "../") for p in others)
    occasions = "".join(f"<li>{esc(o)}</li>" for o in product["occasions"])
    description_text = " ".join(product["description"])
    details = [
        ("Blooms", product["blooms"]),
        ("Materials", "Cotton yarn, crochet thread, paper wrap, ribbon"),
        ("Size", "Approx. 13.7 in H × 10.2 in W × 3.3 in D"),
        ("Weight", "Approx. 0.44 lb"),
        ("Included", "Finished bouquet, gift bag, greeting card"),
        ("Finish", "Hand-crocheted and fully assembled"),
    ]
    detail_rows = "".join(
        f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in details
    )
    structured = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product["fullName"],
        "image": [absolute(f"assets/img/{product['image']}-main-1400.jpg")],
        "description": description_text,
        "sku": product["asin"],
        "brand": {"@type": "Brand", "name": BRAND},
        "material": "Cotton yarn",
        "category": "Artificial Flowers",
    }
    body = f"""
<nav class="breadcrumb shell" aria-label="Breadcrumb">
  <a href="../index.html">Home</a><span aria-hidden="true">/</span>
  <a href="../collection.html">Collection</a><span aria-hidden="true">/</span>
  <span aria-current="page">{esc(product['name'])}</span>
</nav>

<section class="section section--top-tight">
  <div class="shell product-layout">
    <div class="product-gallery">
      <div class="gallery-main">
        <img id="galleryImage" src="../assets/img/{product['image']}-main-1400.jpg"
             srcset="../assets/img/{product['image']}-main-700.jpg 700w, ../assets/img/{product['image']}-main-1400.jpg 1400w"
             sizes="(max-width: 900px) 92vw, 52vw" width="1400" height="1400"
             alt="{esc(product['alt'])}" fetchpriority="high" decoding="async">
      </div>
      <div class="gallery-thumbs" role="group" aria-label="Product images">
        <button type="button" class="thumb is-active" data-src="../assets/img/{product['image']}-main-1400.jpg"
                data-srcset="../assets/img/{product['image']}-main-700.jpg 700w, ../assets/img/{product['image']}-main-1400.jpg 1400w"
                aria-label="View bouquet photo" aria-pressed="true">
          <img src="../assets/img/{product['image']}-main-700.jpg" width="700" height="700" alt="" loading="lazy">
        </button>
        <button type="button" class="thumb" data-src="../assets/img/{product['image']}-alt-1400.jpg"
                data-srcset="../assets/img/{product['image']}-alt-700.jpg 700w, ../assets/img/{product['image']}-alt-1400.jpg 1400w"
                aria-label="View gift bag and card photo" aria-pressed="false">
          <img src="../assets/img/{product['image']}-alt-700.jpg" width="700" height="700" alt="" loading="lazy">
        </button>
      </div>
    </div>

    <div class="product-info">
      <p class="eyebrow"><span class="rule" aria-hidden="true"></span>Crochet bouquet</p>
      <h1>{esc(product['name'])}</h1>
      <p class="product-tagline product-tagline--large">{esc(product['tagline'])}</p>
      <div class="product-description">
        {''.join(f'<p>{esc(x)}</p>' for x in product['description'])}
      </div>
      <a class="button button--wide" href="{AMAZON_BASE}{product['asin']}" target="_blank" rel="noopener">View on Amazon <span aria-hidden="true">↗</span></a>
      <p class="fine-print">Price, shipping, and availability are shown on Amazon. ASIN {esc(product['asin'])}.</p>

      <dl class="detail-list">
        {detail_rows}
      </dl>

      <div class="product-accordions">
        <details open>
          <summary>Care</summary>
          <p>Spot clean gently with a damp cloth and let it air dry. No watering, sunlight, pruning, or cleanup is needed.</p>
        </details>
        <details>
          <summary>Handmade note</summary>
          <p>Each bouquet is handmade. Stitch detail, flower shape, and color may vary slightly from the photos.</p>
        </details>
        <details>
          <summary>Shipping &amp; returns</summary>
          <p>Orders are completed on Amazon.com. Shipping options and returns are handled under Amazon's policies. <a href="../shipping.html">Read more</a>.</p>
        </details>
      </div>

      <div class="occasion-tags">
        <span class="occasion-tags-title">A good fit for</span>
        <ul>{occasions}</ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="shell product-story">
    <div class="reveal">
      <p class="eyebrow"><span class="rule" aria-hidden="true"></span>The idea</p>
      <h2>Fresh flowers fade. These are made to stay.</h2>
    </div>
    <div class="reveal">
      <p class="lede-sm">A bouquet should not ask for much. This one asks for nothing: no water, no trimming, no sunlight. It sits on a desk or shelf and keeps the shape it arrived in.</p>
      <p>Hand-crocheted from soft cotton yarn, then wrapped and finished by hand. The result is a small, lasting object — closer to a textile keepsake than a flower arrangement.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <div class="section-head reveal">
      <div>
        <p class="eyebrow"><span class="rule" aria-hidden="true"></span>More to keep</p>
        <h2>You may also like.</h2>
      </div>
      <a class="text-link" href="../collection.html">All bouquets <span aria-hidden="true">→</span></a>
    </div>
    <div class="product-grid product-grid--three">
      {related}
    </div>
  </div>
</section>
"""
    return page_shell(
        title=f"{product['fullName']} — {BRAND}",
        description=(
            f"{product['tagline']} {product['fullName']} — hand-crocheted cotton yarn, "
            "gift bag and greeting card included."
        ),
        path=f"product/{product['slug']}.html",
        prefix="../",
        body=body,
        og_image=f"assets/img/{product['image']}-main-1400.jpg",
        og_type="product",
        structured_data=structured,
    )


def about_page() -> str:
    body = f"""
<section class="page-hero page-hero--about">
  <div class="shell page-hero-inner">
    <p class="eyebrow"><span class="rule" aria-hidden="true"></span>Our story</p>
    <h1>Made by hand,<br>meant to keep.</h1>
    <p class="lede">Oipuloh makes hand-crocheted flower bouquets as a long-lasting alternative to fresh flowers.</p>
  </div>
</section>

<section class="section">
  <div class="shell split split--wide">
    <div class="split-media reveal">
      <div class="arch arch--soft">
        {picture('rose-main', 'Oipuloh Yellow Rose crochet bouquet', '', sizes='(max-width: 900px) 92vw, 42vw')}
      </div>
    </div>
    <div class="split-copy reveal">
      <p class="eyebrow"><span class="rule" aria-hidden="true"></span>The brand</p>
      <h2>A quieter kind of flower.</h2>
      <p>Fresh flowers are beautiful, but they fade, drop petals, and need constant care. Oipuloh was built around a simple alternative: a bouquet that is finished by hand and ready to stay.</p>
      <p>Each bouquet is crocheted from soft cotton yarn, assembled in full, and wrapped with paper and ribbon. No assembly is required when it arrives. There is no water to change and no petals to sweep up.</p>
      <p>The collection includes seven floral styles, from bright daisies to layered peonies. Each one is designed to sit on a desk, shelf, nightstand, dining table, or entryway — and to look the same next week as it does today.</p>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="shell">
    <div class="section-head reveal">
      <div>
        <p class="eyebrow"><span class="rule" aria-hidden="true"></span>The process</p>
        <h2>From yarn to a finished bouquet.</h2>
      </div>
    </div>
    <ol class="process-grid">
      <li class="reveal"><span>01</span><h3>Stitch</h3><p>Blooms are crocheted from soft cotton yarn, petal by petal.</p></li>
      <li class="reveal"><span>02</span><h3>Shape</h3><p>Each flower is shaped and assembled into a finished arrangement.</p></li>
      <li class="reveal"><span>03</span><h3>Wrap</h3><p>The bouquet is wrapped in paper and finished with a ribbon.</p></li>
      <li class="reveal"><span>04</span><h3>Gift</h3><p>A gift bag and greeting card are added, so it is ready to hand over.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="shell values-grid">
    <div class="reveal">
      <p class="eyebrow"><span class="rule" aria-hidden="true"></span>What we care about</p>
      <h2>Three simple things.</h2>
    </div>
    <dl class="value-list value-list--large reveal">
      <div><dt>Craft</dt><dd>Hand-crocheted blooms with a real textile texture — not printed or molded plastic.</dd></div>
      <div><dt>Longevity</dt><dd>A bouquet that needs no water and keeps its shape, season after season.</dd></div>
      <div><dt>Readiness</dt><dd>Gift bag and greeting card included, so the bouquet is complete when it arrives.</dd></div>
    </dl>
  </div>
</section>

<section class="closing closing--short">
  <div class="shell closing-inner reveal">
    <h2>Find the one that feels like yours.</h2>
    <div class="actions actions--center">
      <a class="button button--light" href="collection.html">Explore the collection</a>
    </div>
  </div>
</section>
"""
    return page_shell(
        title=f"Our Story — {BRAND}",
        description="Oipuloh makes hand-crocheted flower bouquets from soft cotton yarn — a long-lasting, zero-upkeep alternative to fresh flowers.",
        path="about.html",
        prefix="",
        body=body,
        active="about",
    )


def contact_page() -> str:
    body = f"""
<section class="page-hero">
  <div class="shell page-hero-inner">
    <p class="eyebrow"><span class="rule" aria-hidden="true"></span>Contact</p>
    <h1>Say hello.</h1>
    <p class="lede">Questions about a bouquet, a gift, or an order? Send us a note and we will point you in the right direction.</p>
  </div>
</section>

<section class="section section--top-tight">
  <div class="shell contact-grid">
    <div class="contact-card reveal">
      <p class="eyebrow"><span class="rule" aria-hidden="true"></span>Email</p>
      <h2><a href="mailto:{esc(EMAIL)}">{esc(EMAIL)}</a></h2>
      <p>We aim to reply within two business days. Include your order number if your question is about an existing order.</p>
      <a class="button" href="mailto:{esc(EMAIL)}?subject=Question%20about%20an%20Oipuloh%20bouquet">Write to us</a>
    </div>
    <div class="contact-side reveal">
      <div>
        <h3>Order help</h3>
        <p>Orders are placed and fulfilled through Amazon. For delivery status, changes, or returns, open your order in your Amazon account.</p>
        <a class="text-link" href="https://www.amazon.com/gp/help/customer/display.html?nodeId=GKM69DUUYKQWKWX7" target="_blank" rel="noopener">Amazon returns &amp; refunds <span aria-hidden="true">→</span></a>
      </div>
      <div>
        <h3>Before you write</h3>
        <p>Because each bouquet is handmade, stitch detail, flower shape, and color may vary slightly. This is expected, not a defect.</p>
      </div>
      <div>
        <h3>Where to buy</h3>
        <p>Our full collection is available on Amazon.com.</p>
        <a class="text-link" href="{esc(AMAZON_SEARCH)}" target="_blank" rel="noopener">Find Oipuloh on Amazon <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="shell narrow center">
    <p class="eyebrow eyebrow--center">Company information</p>
    <h2>{esc(LEGAL)}</h2>
    <p class="lede-sm">{esc(BRAND)} is a brand of {esc(LEGAL)}. For business and website enquiries, use the email address above.</p>
  </div>
</section>
"""
    return page_shell(
        title=f"Contact — {BRAND}",
        description="Contact Oipuloh about crochet flower bouquets, gifts, website questions, or an existing Amazon order.",
        path="contact.html",
        prefix="",
        body=body,
        active="contact",
    )


def prose_page(title: str, description: str, path: str, sections: list[tuple[str, str]]) -> str:
    content = "".join(f"<h2>{esc(h)}</h2>{body}" for h, body in sections)
    body = f"""
<section class="page-hero page-hero--small">
  <div class="shell page-hero-inner">
    <p class="eyebrow"><span class="rule" aria-hidden="true"></span>Information</p>
    <h1>{esc(title)}</h1>
    <p class="lede">Last updated: 18 October 2026</p>
  </div>
</section>
<section class="section section--top-tight">
  <div class="shell prose">
    {content}
  </div>
</section>
"""
    return page_shell(
        title=f"{title} — {BRAND}",
        description=description,
        path=path,
        prefix="",
        body=body,
    )


def privacy_page() -> str:
    sections = [
        (
            "Who we are",
            f"<p>This website is operated by {esc(LEGAL)}, the brand owner of {esc(BRAND)}. For privacy questions, contact <a href=\"mailto:{esc(EMAIL)}\">{esc(EMAIL)}</a>.</p>",
        ),
        (
            "What this site collects",
            "<p>This website does not use advertising cookies, analytics trackers, or third-party pixels. We do not ask you to create an account or enter payment details here.</p>"
            "<p>If you email us, we receive the information you choose to include in your message, such as your name, email address, and order details. We use it only to answer your enquiry and keep a record of the conversation.</p>"
            "<p>Our hosting provider may process standard server logs — such as IP address, browser type, and the page requested — to keep the site secure and reliable.</p>",
        ),
        (
            "How we use information",
            "<p>We use the information you send to respond to your question, provide customer support, and meet legal or accounting obligations. We do not sell personal information.</p>",
        ),
        (
            "Sharing",
            "<p>We share information only with service providers that help us run the site or respond to enquiries, or when required by law. Purchases made on Amazon are governed by Amazon's own privacy policy.</p>",
        ),
        (
            "Retention",
            "<p>We keep email correspondence only for as long as needed to handle the enquiry and meet legal obligations, then delete or anonymise it.</p>",
        ),
        (
            "Your rights",
            "<p>Depending on where you live, you may have the right to access, correct, or delete personal information we hold about you, or to object to certain processing. Email us to make a request. You may also have the right to complain to your local data protection authority.</p>",
        ),
        (
            "External links",
            "<p>This site links to Amazon.com. When you follow those links, Amazon's terms and privacy policy apply.</p>",
        ),
        (
            "Changes",
            "<p>We may update this policy from time to time. The date at the top of this page shows the latest revision.</p>",
        ),
    ]
    return prose_page(
        "Privacy Policy",
        "How Oipuloh handles information collected through this website and by email.",
        "privacy.html",
        sections,
    )


def terms_page() -> str:
    sections = [
        (
            "About these terms",
            f"<p>These terms apply to your use of this website, operated by {esc(LEGAL)}. By using the site, you agree to them. If you do not agree, please do not use the site.</p>",
        ),
        (
            "Informational site",
            "<p>This website introduces the Oipuloh collection. It does not process orders or payments. Product purchases are completed on Amazon.com and are subject to Amazon's terms, policies, and return process.</p>",
        ),
        (
            "Product information",
            "<p>We aim to describe products accurately. Because each bouquet is handmade, stitch detail, flower shape, and color may vary slightly. Images are illustrative of the style. Price, availability, and delivery estimates are shown on Amazon and may change.</p>",
        ),
        (
            "Intellectual property",
            f"<p>The {esc(BRAND)} name, logo, text, and product photography on this site are owned by {esc(LEGAL)} or used with permission. You may not copy or reuse them for commercial purposes without written permission.</p>",
        ),
        (
            "Acceptable use",
            "<p>Do not attempt to disrupt the site, gain unauthorised access, scrape it at scale, or use it in a way that infringes the rights of others.</p>",
        ),
        (
            "No warranties",
            "<p>The site is provided on an “as is” basis. We do not warrant that it will be uninterrupted or error-free. Nothing in these terms limits any rights you have under mandatory consumer law.</p>",
        ),
        (
            "Limitation of liability",
            "<p>To the extent permitted by law, we are not liable for indirect or consequential loss arising from use of this website. This does not affect liability for matters that cannot legally be excluded.</p>",
        ),
        (
            "Contact",
            f"<p>Questions about these terms: <a href=\"mailto:{esc(EMAIL)}\">{esc(EMAIL)}</a>.</p>",
        ),
    ]
    return prose_page(
        "Terms of Use",
        "Terms governing use of the Oipuloh brand website.",
        "terms.html",
        sections,
    )


def shipping_page() -> str:
    sections = [
        (
            "Where to buy",
            "<p>Oipuloh bouquets are sold on Amazon.com. Product pages on this site link to the corresponding Amazon listing, where you can see the current price and availability.</p>",
        ),
        (
            "Shipping",
            "<p>Shipping options, delivery estimates, and any delivery charges are shown at checkout on Amazon. Orders are fulfilled through Amazon, so the delivery method and carrier are determined by the option you choose there.</p>",
        ),
        (
            "Returns",
            "<p>Returns and refunds are handled under Amazon's return policy and the return window shown on your order. To start a return, open your Amazon order and choose Return or Replace Items.</p>"
            "<p><a href=\"https://www.amazon.com/gp/help/customer/display.html?nodeId=GKM69DUUYKQWKWX7\" target=\"_blank\" rel=\"noopener\">Amazon returns &amp; refunds help</a></p>",
        ),
        (
            "Damaged or incorrect item",
            "<p>If your bouquet arrives damaged or is not the item you ordered, contact us at <a href=\"mailto:"
            + esc(EMAIL)
            + "\">"
            + esc(EMAIL)
            + "</a> with your order number and a photo. We will help you resolve it through Amazon's support process.</p>",
        ),
        (
            "Handmade variation",
            "<p>Slight differences in stitch detail, flower shape, and color are part of the handmade finish and are not considered defects.</p>",
        ),
    ]
    return prose_page(
        "Shipping & Returns",
        "How shipping, delivery, and returns work for Oipuloh orders placed on Amazon.",
        "shipping.html",
        sections,
    )


def not_found_page() -> str:
    body = """
<section class="page-hero page-hero--small">
  <div class="shell page-hero-inner">
    <p class="eyebrow"><span class="rule" aria-hidden="true"></span>404</p>
    <h1>This page has wandered off.</h1>
    <p class="lede">The link may be old, or the page may have moved. The bouquets are still here.</p>
    <div class="actions">
      <a class="button" href="index.html">Back home</a>
      <a class="text-link" href="collection.html">See the collection <span aria-hidden="true">→</span></a>
    </div>
  </div>
</section>
"""
    return page_shell(
        title="Page not found — Oipuloh",
        description="This page could not be found.",
        path="404.html",
        prefix="",
        body=body,
    )


def favicon_svg() -> str:
    petals = []
    for angle in range(0, 360, 45):
        petals.append(
            f'<ellipse cx="32" cy="15" rx="5" ry="10" transform="rotate({angle} 32 32)"/>'
        )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        '<rect width="64" height="64" rx="14" fill="#24473A"/>'
        f'<g fill="#F6E7D8">{"".join(petals)}</g>'
        '<circle cx="32" cy="32" r="6" fill="#C26A4A"/>'
        "</svg>"
    )


def build() -> None:
    (ROOT / "product").mkdir(exist_ok=True)

    pages = {
        "index.html": home_page(),
        "collection.html": collection_page(),
        "about.html": about_page(),
        "contact.html": contact_page(),
        "privacy.html": privacy_page(),
        "terms.html": terms_page(),
        "shipping.html": shipping_page(),
        "404.html": not_found_page(),
    }
    for product in PRODUCTS:
        pages[f"product/{product['slug']}.html"] = product_page(product)

    for path, content in pages.items():
        (ROOT / path).write_text(content, "utf-8")

    (ROOT / "assets/img/favicon.svg").write_text(favicon_svg(), "utf-8")

    urls = [""] + [
        p for p in pages if p not in {"404.html", "index.html"}
    ]
    sitemap_entries = "".join(
        f"  <url><loc>{absolute(p)}</loc><lastmod>{BUILD_DATE}</lastmod></url>\n"
        for p in urls
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{sitemap_entries}</urlset>\n",
        "utf-8",
    )
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {absolute('sitemap.xml')}\n",
        "utf-8",
    )
    print(f"Built {len(pages)} pages in {ROOT}")


if __name__ == "__main__":
    build()
