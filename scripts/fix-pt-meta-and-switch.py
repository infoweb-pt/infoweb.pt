#!/usr/bin/env python3
"""Fix lang, canonical, og:url, JSON-LD url, og:locale order, header EN/PT switch on copied PT tool pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PT = ROOT / "free-tools" / "pt"
HOST = "https://hc-sousa.github.io/infoweb"


def swap_header_nav(html: str, slug: str) -> str:
    en_url = f"../../{slug}/"
    old = (
        '        <nav class="flex items-center gap-1 text-[11px] font-semibold" aria-label="Language">\n'
        '          <span class="rounded-full px-2 py-1 bg-slate-800 border border-slate-500 text-white" title="English">EN</span>\n'
        f'          <a href="pt/{slug}/" hreflang="pt" class="rounded-full px-2 py-1 text-slate-400 hover:text-white border border-transparent hover:border-slate-600 transition" data-track="language_switch" data-track-target="pt" title="Português">PT</a>\n'
        "        </nav>\n"
    )
    new = (
        '        <nav class="flex items-center gap-1 text-[11px] font-semibold" aria-label="Idioma">\n'
        f'          <a href="{en_url}" hreflang="en" class="rounded-full px-2 py-1 text-slate-400 hover:text-white border border-transparent hover:border-slate-600 transition" data-track="language_switch" data-track-target="en" title="English">EN</a>\n'
        '          <span class="rounded-full px-2 py-1 bg-slate-800 border border-slate-500 text-white" title="Português">PT</span>\n'
        "        </nav>\n"
    )
    if old not in html:
        return html
    return html.replace(old, new, 1)


def swap_og_locale(html: str) -> str:
    a = (
        '  <meta property="og:locale" content="en_GB" />\n'
        '  <meta property="og:locale:alternate" content="pt_PT" />\n'
    )
    b = (
        '  <meta property="og:locale" content="pt_PT" />\n'
        '  <meta property="og:locale:alternate" content="en_GB" />\n'
    )
    if a in html:
        return html.replace(a, b, 1)
    return html


def pt_tool_url(slug: str) -> str:
    return f"{HOST}/free-tools/pt/{slug}/"


def en_tool_url(slug: str) -> str:
    return f"{HOST}/free-tools/{slug}/"


def patch_urls(html: str, slug: str) -> str:
    """Point canonical, og:url, WebApplication url to /pt/slug/; restore hreflang en + x-default to EN URL."""
    en_u = en_tool_url(slug)
    pt_u = pt_tool_url(slug)
    html = html.replace(f'<link rel="canonical" href="{en_u}"', f'<link rel="canonical" href="{pt_u}"', 1)
    html = html.replace(f'<meta property="og:url" content="{en_u}"', f'<meta property="og:url" content="{pt_u}"', 1)
    html = html.replace(f'"url": "{en_u}"', f'"url": "{pt_u}"', 1)
    html = html.replace(f'"url": "{en_u}",', f'"url": "{pt_u}",', 1)
    # hreflang en + x-default must stay English
    html = html.replace(f'hreflang="en" href="{pt_u}"', f'hreflang="en" href="{en_u}"', 1)
    html = html.replace(f'hreflang="x-default" href="{pt_u}"', f'hreflang="x-default" href="{en_u}"', 1)
    return html


def patch_file(path: Path) -> None:
    slug = path.parent.name
    html = path.read_text(encoding="utf-8")
    html = html.replace('<html lang="en"', '<html lang="pt"', 1)
    html = patch_urls(html, slug)
    html = swap_og_locale(html)
    html = swap_header_nav(html, slug)
    path.write_text(html, encoding="utf-8")


def main() -> None:
    for p in sorted(PT.glob("*/index.html")):
        if p.parent.name == "vat-calculator-pt":
            continue
        patch_file(p)
        print("meta", p.parent.name)


if __name__ == "__main__":
    main()
