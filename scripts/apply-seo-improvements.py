#!/usr/bin/env python3
"""Apply SEO improvements from docs/plans/2026-05-20-001-feat-comprehensive-seo-improvements-plan.md"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://infoweb.sousadev.com"
OLD_BASE = "https://hc-sousa.github.io/infoweb"

BLOG_PAIRS = {
    "choosing-perfect-domain": "como-escolher-dominio-perfeito",
    "como-escolher-dominio-perfeito": "choosing-perfect-domain",
    "small-business-website-cost": "quanto-custa-website-pequena-empresa",
    "quanto-custa-website-pequena-empresa": "small-business-website-cost",
    "need-website-if-have-instagram": "precisa-website-se-tem-instagram",
    "precisa-website-se-tem-instagram": "need-website-if-have-instagram",
    "local-seo-checklist-small-business": "checklist-seo-local-pequenos-negocios",
    "checklist-seo-local-pequenos-negocios": "local-seo-checklist-small-business",
}

TOOL_RELATED = {
    "whatsapp-qr-generator": ["menu-qr-generator", "google-review-generator", "business-card-qr"],
    "menu-qr-generator": ["whatsapp-qr-generator", "wifi-qr-generator", "google-review-generator"],
    "wifi-qr-generator": ["menu-qr-generator", "business-card-qr", "whatsapp-qr-generator"],
    "business-card-qr": ["whatsapp-qr-generator", "wifi-qr-generator", "google-review-generator"],
    "google-review-generator": ["presence-score", "whatsapp-qr-generator", "menu-qr-generator"],
    "presence-score": ["google-review-generator", "website-health-scorecard", "competitor-visibility-gap"],
    "website-health-scorecard": ["presence-score", "website-roi-calculator", "competitor-visibility-gap"],
    "competitor-visibility-gap": ["presence-score", "website-health-scorecard", "google-review-generator"],
    "website-roi-calculator": ["break-even-calculator", "customer-ltv-calculator", "cost-per-lead-calculator"],
    "break-even-calculator": ["website-roi-calculator", "markup-margin-calculator", "freelancer-rate-calculator"],
    "markup-margin-calculator": ["break-even-calculator", "vat-calculator-pt", "freelancer-rate-calculator"],
    "vat-calculator-pt": ["markup-margin-calculator", "break-even-calculator", "freelancer-rate-calculator"],
    "freelancer-rate-calculator": ["markup-margin-calculator", "break-even-calculator", "cost-per-lead-calculator"],
    "cost-per-lead-calculator": ["customer-ltv-calculator", "website-roi-calculator", "break-even-calculator"],
    "customer-ltv-calculator": ["cost-per-lead-calculator", "website-roi-calculator", "lost-customers-calculator"],
    "lost-customers-calculator": ["customer-ltv-calculator", "downtime-cost-calculator", "website-roi-calculator"],
    "downtime-cost-calculator": ["lost-customers-calculator", "website-roi-calculator", "break-even-calculator"],
    "utm-link-builder": ["website-roi-calculator", "cost-per-lead-calculator", "presence-score"],
    "discount-calculator": ["markup-margin-calculator", "vat-calculator-pt", "break-even-calculator"],
    "schema-local-business-generator": ["presence-score", "google-review-generator", "website-health-scorecard"],
    "tip-split-calculator": ["menu-qr-generator", "food-cost-calculator", "markup-margin-calculator"],
    "food-cost-calculator": ["menu-qr-generator", "markup-margin-calculator", "tip-split-calculator"],
}

TOOL_LABELS_EN = {
    "whatsapp-qr-generator": "WhatsApp QR Generator",
    "menu-qr-generator": "Menu QR Generator",
    "wifi-qr-generator": "Wi-Fi QR Generator",
    "business-card-qr": "Business Card QR",
    "google-review-generator": "Google Review Link Generator",
    "presence-score": "Online Presence Score",
    "website-health-scorecard": "Website Health Scorecard",
    "competitor-visibility-gap": "Competitor Visibility Gap",
    "website-roi-calculator": "Website ROI Calculator",
    "break-even-calculator": "Break-Even Calculator",
    "markup-margin-calculator": "Markup & Margin Calculator",
    "vat-calculator-pt": "Portuguese VAT Calculator",
    "freelancer-rate-calculator": "Freelancer Rate Calculator",
    "cost-per-lead-calculator": "Cost Per Lead Calculator",
    "customer-ltv-calculator": "Customer LTV Calculator",
    "lost-customers-calculator": "Lost Customers Calculator",
    "downtime-cost-calculator": "Downtime Cost Calculator",
    "utm-link-builder": "UTM Link Builder",
    "discount-calculator": "Discount Calculator",
    "schema-local-business-generator": "Local Business Schema Generator",
    "tip-split-calculator": "Tip Split Calculator",
    "food-cost-calculator": "Food Cost Calculator",
}

BLOG_RELATED = {
    "choosing-perfect-domain": [
        ("/blog/posts/small-business-website-cost/", "How much does a small business website cost?"),
        ("/blog/posts/local-seo-checklist-small-business/", "Local SEO checklist for small businesses"),
        ("/free-tools/website-health-scorecard/", "Free website health scorecard"),
    ],
    "como-escolher-dominio-perfeito": [
        ("/blog/posts/quanto-custa-website-pequena-empresa/", "Quanto custa um website para pequenas empresas?"),
        ("/blog/posts/checklist-seo-local-pequenos-negocios/", "Checklist de SEO local"),
        ("/free-tools/pt/website-health-scorecard/", "Scorecard gratuito de saúde do website"),
    ],
    "small-business-website-cost": [
        ("/blog/posts/choosing-perfect-domain/", "How to choose the perfect domain name"),
        ("/blog/posts/need-website-if-have-instagram/", "Do you need a website if you have Instagram?"),
        ("/free-tools/website-roi-calculator/", "Website ROI calculator"),
    ],
    "quanto-custa-website-pequena-empresa": [
        ("/blog/posts/como-escolher-dominio-perfeito/", "Como escolher o domínio perfeito"),
        ("/blog/posts/precisa-website-se-tem-instagram/", "Precisa de website se tem Instagram?"),
        ("/free-tools/pt/website-roi-calculator/", "Calculadora ROI de website"),
    ],
    "need-website-if-have-instagram": [
        ("/blog/posts/small-business-website-cost/", "Small business website cost guide"),
        ("/blog/posts/local-seo-checklist-small-business/", "Local SEO checklist"),
        ("/free-tools/presence-score/", "Online presence score tool"),
    ],
    "precisa-website-se-tem-instagram": [
        ("/blog/posts/quanto-custa-website-pequena-empresa/", "Quanto custa um website"),
        ("/blog/posts/checklist-seo-local-pequenos-negocios/", "Checklist SEO local"),
        ("/free-tools/pt/presence-score/", "Score de presença online"),
    ],
    "local-seo-checklist-small-business": [
        ("/blog/posts/choosing-perfect-domain/", "Domain name guide"),
        ("/blog/posts/need-website-if-have-instagram/", "Website vs Instagram"),
        ("/free-tools/google-review-generator/", "Google review link generator"),
    ],
    "checklist-seo-local-pequenos-negocios": [
        ("/blog/posts/como-escolher-dominio-perfeito/", "Guia de domínios"),
        ("/blog/posts/precisa-website-se-tem-instagram/", "Website vs Instagram"),
        ("/free-tools/pt/google-review-generator/", "Gerador de link Google Reviews"),
    ],
}


def normalize_domain(text: str) -> str:
    return text.replace(OLD_BASE, BASE_URL)


def breadcrumb_json(items: list[tuple[int, str, str]]) -> str:
    elements = []
    for pos, name, url in items:
        elements.append(
            {
                "@type": "ListItem",
                "position": pos,
                "name": name,
                "item": url,
            }
        )
    payload = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": elements,
    }
    return (
        "\n  <!-- Breadcrumb Structured Data -->\n"
        f'  <script type="application/ld+json">\n{json.dumps(payload, indent=2, ensure_ascii=False)}\n  </script>'
    )


def insert_before_closing_head(text: str, block: str) -> str:
    if block.strip() in text:
        return text
    return text.replace("</head>", f"{block}\n</head>", 1)


def related_tools_html(slug: str, lang: str) -> str:
    related = TOOL_RELATED.get(slug, ["website-roi-calculator", "whatsapp-qr-generator", "presence-score"])
    prefix = "../pt/" if lang == "pt" else ""
    hub = "../pt/" if lang == "pt" else "../"
    title = "Ferramentas relacionadas" if lang == "pt" else "Related tools"
    blog_href = f"{BASE_URL}/blog/"
    blog_label = "Blog InfoWeb" if lang == "pt" else "InfoWeb Blog"
    links = []
    for rel in related[:3]:
        label = TOOL_LABELS_EN.get(rel, rel.replace("-", " ").title())
        links.append(f'        <li><a href="{prefix}{rel}/" class="hover:text-signal transition">{label}</a></li>')
    links_html = "\n".join(links)
    return f"""
    <!-- Related internal links -->
    <section class="related-resources max-w-2xl mx-auto px-4 mb-8" aria-labelledby="related-tools-heading">
      <h2 id="related-tools-heading" class="text-sm font-bold uppercase tracking-wider text-slate-500 mb-3">{title}</h2>
      <ul class="flex flex-wrap gap-x-4 gap-y-2 text-sm text-slate-400">
{links_html}
        <li><a href="{hub}" class="hover:text-signal transition">{"Todas as ferramentas" if lang == "pt" else "All free tools"}</a></li>
        <li><a href="{blog_href}" class="hover:text-signal transition">{blog_label}</a></li>
      </ul>
    </section>
"""


def related_blog_html(slug: str, lang: str) -> str:
    links = BLOG_RELATED.get(slug, [])
    if not links:
        return ""
    title = "Leitura relacionada" if lang == "pt" else "Related reading"
    items = "\n".join(
        f'        <li><a href="{BASE_URL}{href}" class="hover:text-signal transition">{label}</a></li>'
        for href, label in links
    )
    tools_href = f"{BASE_URL}/free-tools/pt/" if lang == "pt" else f"{BASE_URL}/free-tools/"
    tools_label = "Ferramentas gratuitas" if lang == "pt" else "Free tools"
    return f"""
    <!-- Related internal links -->
    <section class="related-resources mt-10 pt-8 border-t border-slate-800" aria-labelledby="related-reading-heading">
      <h2 id="related-reading-heading" class="text-lg font-bold text-white mb-4">{title}</h2>
      <ul class="space-y-2 text-slate-300">
{items}
        <li><a href="{tools_href}" class="hover:text-signal transition">{tools_label}</a></li>
      </ul>
    </section>
"""


def process_free_tool(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    text = normalize_domain(text)

    rel = path.relative_to(ROOT)
    parts = rel.parts
    if "pt" in parts:
        lang = "pt"
        slug = path.parent.name
        tool_url = f"{BASE_URL}/free-tools/pt/{slug}/"
        hub_name = "Ferramentas Gratuitas"
        hub_url = f"{BASE_URL}/free-tools/pt/"
    else:
        lang = "en"
        slug = path.parent.name
        if slug in ("index", "qr-example", "qr-manage", "competitor-visibility-gap"):
            if slug == "index":
                crumbs = breadcrumb_json([(1, "Home", f"{BASE_URL}/"), (2, "Free Tools", f"{BASE_URL}/free-tools/")])
                text = insert_before_closing_head(text, crumbs)
            path.write_text(text, encoding="utf-8")
            return text != original
        tool_url = f"{BASE_URL}/free-tools/{slug}/"
        hub_name = "Free Tools"
        hub_url = f"{BASE_URL}/free-tools/"

    title_match = re.search(r"<title>([^<]+)</title>", text)
    tool_name = title_match.group(1).split("—")[0].strip() if title_match else slug.replace("-", " ").title()

    crumbs = breadcrumb_json(
        [
            (1, "Home", f"{BASE_URL}/"),
            (2, hub_name, hub_url),
            (3, tool_name, tool_url),
        ]
    )
    text = insert_before_closing_head(text, crumbs)

    if 'id="related-tools-heading"' not in text and slug not in ("qr-manage", "competitor-visibility-gap"):
        block = related_tools_html(slug, lang)
        if "<!-- FOOTER -->" in text:
            text = text.replace("<!-- FOOTER -->", block + "\n  <!-- FOOTER -->", 1)
        elif "<footer" in text:
            text = text.replace("<footer", block + "\n  <footer", 1)

    # Improve generic logo alt text
    text = text.replace(
        'alt="InfoWeb" class="h-9 w-auto"',
        'alt="InfoWeb — managed websites for small businesses" class="h-9 w-auto"',
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def process_blog_post(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    slug = path.parent.name
    meta_path = path.parent / "metadata.json"
    if not meta_path.exists():
        return False
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    title = meta["title"].replace("{{CURRENT_YEAR}}", "2026")
    lang = meta.get("language", "en")
    post_url = f"{BASE_URL}/blog/posts/{slug}/"
    blog_hub = "Blog" if lang == "en" else "Blog"

    crumbs = breadcrumb_json(
        [
            (1, "Home", f"{BASE_URL}/"),
            (2, blog_hub, f"{BASE_URL}/blog/"),
            (3, title, post_url),
        ]
    )
    text = insert_before_closing_head(text, crumbs)

    h1_block = (
        f'      <h1 class="text-3xl sm:text-4xl font-extrabold text-white mb-6 leading-tight" id="postTitle">{title}</h1>\n'
    )
    if 'id="postTitle"' not in text:
        text = text.replace(
            '    <article class="blog-content" id="postContent">\n      <!-- Content will be loaded here by JavaScript -->',
            f'    <article class="blog-content" id="postContent">\n{h1_block}      <!-- Content will be loaded here by JavaScript -->',
        )

    related = related_blog_html(slug, lang)
    if related and 'id="related-reading-heading"' not in text:
        text = text.replace(
            "    <!-- Tags -->\n    <div id=\"postTags\"",
            related + "\n    <!-- Tags -->\n    <div id=\"postTags\"",
        )

    text = text.replace(
        'alt="InfoWeb" class="h-9 w-auto"',
        'alt="InfoWeb — managed websites for small businesses" class="h-9 w-auto"',
    )
    text = text.replace(
        'alt="InfoWeb" class="w-16 h-16',
        'alt="InfoWeb logo — website as a service for small businesses" class="w-16 h-16',
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def add_hreflang_block(text: str, en_url: str, pt_url: str | None = None) -> str:
    if 'hreflang="en"' in text or 'hreflang="pt"' in text:
        return text
    block = f'  <link rel="alternate" hreflang="en" href="{en_url}" />\n'
    if pt_url:
        block += f'  <link rel="alternate" hreflang="pt" href="{pt_url}" />\n'
    block += f'  <link rel="alternate" hreflang="x-default" href="{en_url}" />\n'
    if 'rel="canonical"' in text:
        return re.sub(r'(<link rel="canonical"[^>]+>\n)', r"\1" + block, text, count=1)
    return insert_before_closing_head(text, block)


def process_index() -> bool:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    original = text

    text = add_hreflang_block(text, f"{BASE_URL}/", f"{BASE_URL}/")

    if '"LocalBusiness"' not in text and '"@type": "ProfessionalService"' in text:
        text = text.replace(
            '"@type": "ProfessionalService",',
            '"@type": ["ProfessionalService", "LocalBusiness"],',
        )
        if '"address"' not in text:
            text = text.replace(
                '"areaServed": { "@type": "Country", "name": "Portugal" },',
                '"areaServed": { "@type": "Country", "name": "Portugal" },\n        "address": {\n          "@type": "PostalAddress",\n          "addressCountry": "PT"\n        },',
            )

    text = text.replace(
        'alt="InfoWeb"\n            class="h-10',
        'alt="InfoWeb logo — website as a service for small businesses"\n            class="h-10',
    )
    text = text.replace(
        'alt="InfoWeb" class="h-9 w-auto opacity-95"',
        'alt="InfoWeb logo — managed websites for small businesses" class="h-9 w-auto opacity-95"',
    )
    text = text.replace(
        'alt="Henrique Sousa" class="developer-photo"',
        'alt="Henrique Sousa — InfoWeb founder and full-stack developer" class="developer-photo"',
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def process_affiliates() -> bool:
    path = ROOT / "affiliates" / "index.html"
    text = path.read_text(encoding="utf-8")
    original = text
    url = f"{BASE_URL}/affiliates/"
    text = add_hreflang_block(text, url, url)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def process_blog_index() -> bool:
    path = ROOT / "blog" / "index.html"
    text = path.read_text(encoding="utf-8")
    original = text
    url = f"{BASE_URL}/blog/"
    if 'hreflang="pt"' not in text:
        block = f'  <link rel="alternate" hreflang="pt" href="{url}" />\n  <link rel="alternate" hreflang="x-default" href="{url}" />\n'
        text = re.sub(r'(<link rel="canonical"[^>]+>\n)', r"\1" + block, text, count=1)
    crumbs = breadcrumb_json([(1, "Home", f"{BASE_URL}/"), (2, "Blog", url)])
    text = insert_before_closing_head(text, crumbs)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed: list[str] = []

    if process_index():
        changed.append("index.html")
    if process_affiliates():
        changed.append("affiliates/index.html")
    if process_blog_index():
        changed.append("blog/index.html")

    for path in sorted((ROOT / "blog" / "posts").glob("*/index.html")):
        if process_blog_post(path):
            changed.append(str(path.relative_to(ROOT)))

    skip_tools = {"qr-example", "TOOL_TEMPLATE.html"}
    for path in sorted((ROOT / "free-tools").rglob("index.html")):
        if path.parent.name in skip_tools or "TOOL_TEMPLATE" in str(path):
            continue
        if process_free_tool(path):
            changed.append(str(path.relative_to(ROOT)))

    print(f"Updated {len(changed)} files")
    for item in changed:
        print(" ", item)


if __name__ == "__main__":
    main()
