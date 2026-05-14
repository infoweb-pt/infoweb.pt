#!/usr/bin/env python3
"""Patch EN free-tool index.html: hreflang + og:locale:alternate + header EN|PT switch."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FREE_TOOLS = ROOT / "free-tools"
BASE = "https://hc-sousa.github.io/infoweb/free-tools"
SKIP = {"pt", "qr-example"}

OG_LOCALE_RE = re.compile(
    r"<meta\s+property=\"og:locale\"\s+content=\"(?P<loc>[^\"]+)\"\s*/>",
    re.MULTILINE,
)


def href_block(slug: str, loc: str) -> str:
    en_url = f"{BASE}/{slug}/"
    pt_url = f"{BASE}/pt/{slug}/"
    if loc == "en_GB":
        return (
            '  <meta property="og:locale" content="en_GB" />\n'
            '  <meta property="og:locale:alternate" content="pt_PT" />\n'
            f'  <link rel="alternate" hreflang="en" href="{en_url}" />\n'
            f'  <link rel="alternate" hreflang="pt" href="{pt_url}" />\n'
            f'  <link rel="alternate" hreflang="x-default" href="{en_url}" />\n'
        )
    return (
        '  <meta property="og:locale" content="pt_PT" />\n'
        '  <meta property="og:locale:alternate" content="en_GB" />\n'
        f'  <link rel="alternate" hreflang="en" href="{en_url}" />\n'
        f'  <link rel="alternate" hreflang="pt" href="{pt_url}" />\n'
        f'  <link rel="alternate" hreflang="x-default" href="{en_url}" />\n'
    )


def patch_head(text: str, slug: str) -> str:
    if 'hreflang="pt"' in text:
        return text
    m = OG_LOCALE_RE.search(text)
    if not m:
        raise ValueError(f"no og:locale: {slug}")
    loc = m.group("loc")
    return text[: m.start()] + href_block(slug, loc) + text[m.end() :]


NAV_INNER = (
    '      <div class="flex items-center gap-2 shrink-0">\n'
    '        <nav class="flex items-center gap-1 text-[11px] font-semibold" aria-label="Language">\n'
    '          <span class="rounded-full px-2 py-1 bg-slate-800 border border-slate-500 text-white" title="English">EN</span>\n'
    '          <a href="pt/{slug}/" hreflang="pt" class="rounded-full px-2 py-1 text-slate-400 hover:text-white border border-transparent hover:border-slate-600 transition" data-track="language_switch" data-track-target="pt" title="Português">PT</a>\n'
    "        </nav>\n"
)

# Standard: logo </a> immediately followed by pricing <a
PLAN_AFTER_LOGO = re.compile(
    r"(</a>\n)([ \t]*<a href=\"https://infoweb\.sousadev\.com/\?utm_source=freetool&utm_medium=[^\"]+&utm_campaign=header_btn#pricing\")",
    re.MULTILINE,
)


def patch_header_tailwind(text: str, slug: str) -> str:
    if "language_switch" in text and 'data-track-target="pt"' in text:
        return text
    repl = r"\1" + NAV_INNER.format(slug=slug) + r"\2"
    new, n = PLAN_AFTER_LOGO.subn(repl, text, count=1)
    if n != 1:
        return text
    # Close wrapper after first header pricing </a> (before </div></header> for this header block)
    new2, n2 = re.subn(
        r'(<a href="https://infoweb\.sousadev\.com/\?utm_source=freetool&utm_medium=[^\"]+&utm_campaign=header_btn#pricing"[^>]*>\s*(?:See Website Plans|Ver planos)\s*</a>)(\n[ \t]*</div>\n[ \t]*</header>)',
        r"\1\n      </div>\2",
        new,
        count=1,
    )
    if n2 != 1:
        raise ValueError(f"close div not found tailwind {slug}")
    new2 = new2.replace(
        "flex items-center justify-between\">",
        "flex items-center justify-between gap-3\">",
        1,
    )
    return new2


def patch_header_inline_presence_lost(text: str, slug: str) -> str:
    if "language_switch" in text:
        return text
    nav = (
        "</a>\n"
        '      <div style="display:flex;align-items:center;gap:0.5rem;">\n'
        '        <nav style="display:flex;align-items:center;gap:0.25rem;font-size:11px;font-weight:700;" aria-label="Language">\n'
        '          <span style="border-radius:999px;padding:0.2rem 0.45rem;background:#1e293b;border:1px solid #64748b;color:#fff;">EN</span>\n'
        f'          <a href="pt/{slug}/" hreflang="pt" style="border-radius:999px;padding:0.2rem 0.45rem;color:#94a3b8;text-decoration:none;" data-track="language_switch" data-track-target="pt">PT</a>\n'
        "        </nav>\n"
    )
    new, n = PLAN_AFTER_LOGO.subn(r"\1" + nav + r"\2", text, count=1)
    if n != 1:
        return text
    new, n2 = re.subn(
        r"(See Website Plans\s*</a>)(\n[ \t]*</div>\s*\n[ \t]*</header>)",
        r"\1\n      </div>\2",
        new,
        count=1,
    )
    if n2 != 1:
        raise ValueError(f"close inline header {slug}")
    return new


def patch_qr_manage(text: str, slug: str) -> str:
    if "language_switch" in text:
        return text
    needle = (
        '        <img src="../../assets/images/infoweb-logo.png" alt="InfoWeb" class="h-9 w-auto" />\n'
        "      </a>\n"
        "    </div>"
    )
    rep = (
        '        <img src="../../assets/images/infoweb-logo.png" alt="InfoWeb" class="h-9 w-auto" />\n'
        "      </a>\n"
        '      <nav class="flex items-center gap-1 text-[11px] font-semibold shrink-0" aria-label="Language">\n'
        '        <span class="rounded-full px-2 py-1 bg-slate-800 border border-slate-500 text-white" title="English">EN</span>\n'
        '        <a href="pt/qr-manage/" hreflang="pt" class="rounded-full px-2 py-1 text-slate-400 hover:text-white border border-transparent hover:border-slate-600 transition" data-track="language_switch" data-track-target="pt" title="Português">PT</a>\n'
        "      </nav>\n"
        "    </div>"
    )
    if needle not in text:
        raise ValueError("qr-manage needle")
    return text.replace(needle, rep, 1).replace(
        '<div class="max-w-2xl mx-auto px-4 py-3 flex items-center justify-between">',
        '<div class="max-w-2xl mx-auto px-4 py-3 flex items-center justify-between gap-3">',
        1,
    )


def main() -> None:
    for p in sorted(FREE_TOOLS.glob("*/index.html")):
        slug = p.parent.name
        if slug in SKIP:
            continue
        raw = p.read_text(encoding="utf-8")
        try:
            out = patch_head(raw, slug)
        except ValueError as e:
            print("skip head", slug, e)
            continue

        if slug == "qr-manage":
            out = patch_qr_manage(out, slug)
        elif slug in ("presence-score", "lost-customers-calculator"):
            out2 = patch_header_inline_presence_lost(out, slug)
            if out2 == out:
                print("WARN inline header unchanged", slug)
            out = out2
        else:
            out2 = patch_header_tailwind(out, slug)
            if out2 == out and "language_switch" not in out:
                print("WARN tailwind header unchanged", slug)
            out = out2

        p.write_text(out, encoding="utf-8")
        print("ok", slug)


if __name__ == "__main__":
    main()
