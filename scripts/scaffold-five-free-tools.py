#!/usr/bin/env python3
"""Scaffold five client-side free tools (EN + PT)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FT = ROOT / "free-tools"
OG = "https://infoweb.sousadev.com/assets/images/og-image.png"

STYLE = """/* Tool overrides */
#spinner.flex, #spinner.show-flex { display: flex !important; }
#result-box.show-flex { display: flex !important; }
.copy-row { display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: stretch; margin-top: 0.75rem; }
.copy-row input, .copy-row textarea {
  flex: 1; min-width: 0; width: 100%;
  background: #1e293b; border: 1px solid #334155; border-radius: 0.75rem;
  color: #f1f5f9; font-family: ui-monospace, monospace; font-size: 0.8rem;
  padding: 0.65rem 1rem;
}
.copy-row textarea { min-height: 12rem; resize: vertical; }
"""

ACCENTS = {
    "sky": "sky",
    "rose": "rose",
    "indigo": "indigo",
    "teal": "teal",
    "orange": "orange",
}


def related_li(slugs: list[tuple[str, str, str]]) -> str:
    lines = []
    for href, en_label, pt_label in slugs:
        lines.append(
            f'      <li><a href="{href}" class="hover:text-signal transition">{{{{en}}}}'
            .replace("{{en}}", en_label)
        )
    return "\n".join(lines)


def head_block(lang: str, m: dict, slug: str) -> str:
    en = lang == "en"
    canon = f"https://infoweb.sousadev.com/free-tools/{'pt/' if not en else ''}{slug}/"
    en_url = f"https://infoweb.sousadev.com/free-tools/{slug}/"
    pt_url = f"https://infoweb.sousadev.com/free-tools/pt/{slug}/"
    rel = "../../" if en else "../../../"
    css = "style.css" if en else f"../../{slug}/style.css"
    return f"""<!DOCTYPE html>
<html lang="{lang}" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{m['title']}</title>
  <meta name="description" content="{m['description']}" />
  <meta name="keywords" content="{m['keywords']}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
  <meta name="author" content="InfoWeb by Sousa Dev" />
  <link rel="canonical" href="{canon}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="InfoWeb" />
  <meta property="og:url" content="{canon}" />
  <meta property="og:title" content="{m['title']}" />
  <meta property="og:description" content="{m['og_description']}" />
  <meta property="og:image" content="{OG}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:locale" content="{'en_GB' if en else 'pt_PT'}" />
  <meta property="og:locale:alternate" content="{'pt_PT' if en else 'en_GB'}" />
  <link rel="alternate" hreflang="en" href="{en_url}" />
  <link rel="alternate" hreflang="pt" href="{pt_url}" />
  <link rel="alternate" hreflang="x-default" href="{en_url}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{m['title']}" />
  <meta name="twitter:description" content="{m['og_description']}" />
  <meta name="twitter:image" content="{OG}" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "{m['app_name']}",
    "url": "{canon}",
    "description": "{m['description']}",
    "applicationCategory": "UtilityApplication",
    "operatingSystem": "Any",
    "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "EUR" }},
    "author": {{ "@type": "Organization", "name": "InfoWeb", "url": "https://infoweb.sousadev.com" }}
  }}
  </script>
  <link rel="icon" type="image/png" href="{rel}favicon_io/favicon-32x32.png" />
  <link rel="apple-touch-icon" href="{rel}favicon_io/apple-touch-icon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    window.tailwind = window.tailwind || {{}};
    window.tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{ sans: ['"Instrument Sans"', 'ui-sans-serif', 'system-ui'] }},
          colors: {{ ink: '#020617', signal: '#d7b46a' }}
        }}
      }}
    }};
  </script>
  <link rel="stylesheet" href="{css}" />
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXQSMBERJM"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag() {{ dataLayer.push(arguments); }}
    gtag('js', new Date());
    gtag('config', 'G-XXQSMBERJM');
  </script>
  <script src="{rel}assets/js/analytics.js" defer></script>
</head>
"""


def page(lang: str, slug: str, medium: str, accent: str, m: dict, body: str, related: str) -> str:
    en = lang == "en"
    a = ACCENTS[accent]
    rel_hub = "../" if en else "../../"
    rel_pt = f"../pt/{slug}/" if en else "#"
    rel_en = "#" if en else f"../../{slug}/"
    rel_root = "../../" if en else "../../../"
    script = "script.js" if en else f"../../{slug}/script.js"
    lang_nav = (
        '<span class="rounded-full px-2 py-1 bg-slate-800 border border-slate-500 text-white">EN</span>'
        f'<a href="{rel_pt}" hreflang="pt" class="rounded-full px-2 py-1 text-slate-400 hover:text-white border border-transparent hover:border-slate-600 transition" data-track="language_switch" data-track-target="pt">PT</a>'
        if en
        else f'<a href="{rel_en}" hreflang="en" class="rounded-full px-2 py-1 text-slate-400 hover:text-white border border-transparent hover:border-slate-600 transition" data-track="language_switch" data-track-target="en">EN</a>'
        '<span class="rounded-full px-2 py-1 bg-slate-800 border border-slate-500 text-white">PT</span>'
    )
    return (
        head_block(lang, m, slug)
        + f"""<body class="bg-slate-950 text-white font-sans antialiased">
  <header class="sticky top-0 z-50 bg-slate-950/90 backdrop-blur-xl border-b border-slate-800/60">
    <div class="max-w-2xl mx-auto px-4 py-3 flex items-center justify-between gap-3">
      <a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium={medium}&utm_campaign=header"
         target="_blank" rel="noopener" aria-label="InfoWeb">
        <img src="{rel_root}assets/images/infoweb-logo.png" alt="InfoWeb" class="h-9 w-auto" />
      </a>
      <div class="flex items-center gap-2 shrink-0">
        <nav class="flex items-center gap-1 text-[11px] font-semibold" aria-label="{m['aria_lang']}">
          {lang_nav}
        </nav>
        <a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium={medium}&utm_campaign=header_btn#pricing"
           target="_blank" rel="noopener" class="text-sm font-semibold border border-slate-600 rounded-full px-4 py-1.5 hover:border-white text-slate-300 transition-all"
           data-track="header_cta_click">{m['header_cta']}</a>
      </div>
    </div>
  </header>
  <main class="max-w-2xl mx-auto px-4 py-12">
    <section class="text-center mb-10">
      <div class="inline-flex items-center gap-2 bg-{a}-500/10 border border-{a}-500/30 rounded-full px-4 py-1.5 text-sm font-semibold text-{a}-400 mb-5">
        <span class="w-2 h-2 rounded-full bg-{a}-400 animate-pulse"></span>
        {m['badge']}
      </div>
      <h1 class="text-3xl sm:text-4xl font-bold leading-tight mb-4 text-white">{m['h1']}</h1>
      <p class="text-slate-400 text-lg leading-relaxed">{m['subtitle']}</p>
    </section>
{body}
  </main>
  <section class="related-resources max-w-2xl mx-auto px-4 mb-8" aria-labelledby="related-tools-heading">
    <h2 id="related-tools-heading" class="text-sm font-bold uppercase tracking-wider text-slate-500 mb-3">{m['related_title']}</h2>
    <ul class="flex flex-wrap gap-x-4 gap-y-2 text-sm text-slate-400">
{related}
      <li><a href="{rel_hub}" class="hover:text-signal transition">{m['all_tools']}</a></li>
      <li><a href="https://infoweb.sousadev.com/blog/" class="hover:text-signal transition">Blog InfoWeb</a></li>
    </ul>
  </section>
  <footer class="border-t border-slate-800 py-6 text-center text-sm text-slate-500">
    <a href="{rel_root}" class="text-slate-400 hover:text-white transition">{m['footer']}</a>
  </footer>
  <script src="{script}" defer></script>
</body>
</html>
"""
    )


def output_section(accent: str, m: dict) -> str:
    a = ACCENTS[accent]
    return f"""
    <section aria-labelledby="tool-output-heading" class="mb-10" id="output-section">
      <h2 id="tool-output-heading" class="sr-only">{m['output_sr']}</h2>
      <div id="spinner" class="hidden flex-col items-center justify-center py-12 text-slate-400" aria-live="polite">
        <svg class="animate-spin h-8 w-8 mb-3 text-{a}-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
        </svg>
        <span id="spinner-text">{m['spinner']}</span>
      </div>
      <div id="error-box" class="hidden bg-red-900/30 border border-red-700/50 rounded-2xl p-5 text-center" role="alert">
        <p class="text-red-300 mb-3">{m['error']}</p>
        <button type="button" onclick="runTool()" class="text-sm underline text-red-400 hover:text-red-200">{m['retry']}</button>
      </div>
      <div id="result-box" class="hidden space-y-4"></div>
    </section>
"""


def faq_section(m: dict, items: list[tuple[str, str]]) -> str:
    blocks = []
    for q, a in items:
        blocks.append(f"""        <details class="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <summary class="font-semibold text-white cursor-pointer">{q}</summary>
          <p class="text-slate-400 text-sm mt-2">{a}</p>
        </details>""")
    return f"""
    <section class="mb-10">
      <h2 class="text-xl font-bold text-white mb-4">{m['faq_title']}</h2>
      <div class="space-y-3">
{chr(10).join(blocks)}
      </div>
    </section>
"""


TOOLS = [
    {
        "slug": "utm-link-builder",
        "medium": "utm_link_builder",
        "accent": "sky",
        "related_en": [
            ("website-roi-calculator/", "Website ROI Calculator"),
            ("cost-per-lead-calculator/", "Cost Per Lead Calculator"),
            ("presence-score/", "Online Presence Score"),
        ],
        "related_pt": [
            ("website-roi-calculator/", "Calculadora ROI do site"),
            ("cost-per-lead-calculator/", "Calculadora custo por lead"),
            ("presence-score/", "Score de presença online"),
        ],
        "script": r'''/**
 * UTM Link Builder
 */
'use strict';

const PT = (document.documentElement.getAttribute('lang') || '').toLowerCase().startsWith('pt');
function L(en, pt) { return PT ? pt : en; }

let toolRunStartedAt = 0;

function show(id) { document.getElementById(id).classList.remove('hidden'); }
function hide(id) { document.getElementById(id).classList.add('hidden'); }
function showFlex(id) {
  const el = document.getElementById(id);
  el.classList.remove('hidden');
  el.classList.add('flex');
}
function hideFlex(id) {
  const el = document.getElementById(id);
  el.classList.add('hidden');
  el.classList.remove('flex');
}

function normalizeUrl(raw) {
  const s = String(raw).trim();
  if (!s) return '';
  if (/^https?:\/\//i.test(s)) return s;
  return 'https://' + s.replace(/^\/+/, '');
}

function buildUtmUrl(base, source, medium, campaign, term, content) {
  const u = new URL(base);
  if (source) u.searchParams.set('utm_source', source);
  if (medium) u.searchParams.set('utm_medium', medium);
  if (campaign) u.searchParams.set('utm_campaign', campaign);
  if (term) u.searchParams.set('utm_term', term);
  if (content) u.searchParams.set('utm_content', content);
  return u.toString();
}

async function copyText(text, btnId) {
  try {
    await navigator.clipboard.writeText(text);
    const btn = document.getElementById(btnId);
    if (btn) {
      const orig = btn.textContent;
      btn.textContent = L('Copied!', 'Copiado!');
      setTimeout(() => { btn.textContent = orig; }, 2000);
    }
    if (typeof window.trackEvent === 'function') window.trackEvent('tool_copy', { field: btnId });
  } catch (e) {
    alert(L('Copy failed — select the text manually.', 'Falha ao copiar — selecione o texto manualmente.'));
  }
}

async function runTool() {
  const baseRaw = document.getElementById('base-url').value;
  const source = document.getElementById('utm-source').value.trim();
  const medium = document.getElementById('utm-medium').value.trim();
  const campaign = document.getElementById('utm-campaign').value.trim();
  const term = document.getElementById('utm-term').value.trim();
  const content = document.getElementById('utm-content').value.trim();

  const base = normalizeUrl(baseRaw);
  if (!base || !source || !medium || !campaign) {
    alert(L('Enter a valid URL plus utm_source, utm_medium, and utm_campaign.', 'Introduza um URL válido e utm_source, utm_medium e utm_campaign.'));
    return;
  }

  toolRunStartedAt = performance.now();
  if (typeof window.trackEvent === 'function') window.trackEvent('tool_used');

  showFlex('spinner');
  hide('result-box');
  hide('error-box');

  try {
    const full = buildUtmUrl(base, source, medium, campaign, term, content);
    const box = document.getElementById('result-box');
    box.innerHTML = `
      <div class="bg-slate-900 border border-sky-500/30 rounded-2xl p-5">
        <p class="text-xs font-bold uppercase tracking-widest text-sky-400 mb-3">${L('Your tagged URL', 'O seu URL com UTM')}</p>
        <div class="copy-row">
          <input type="text" id="out-full" readonly value="${full.replace(/"/g, '&quot;')}" />
          <button type="button" id="btn-copy-full" onclick="copyText(document.getElementById('out-full').value,'btn-copy-full')"
            class="shrink-0 bg-sky-600 hover:bg-sky-500 text-white font-semibold rounded-xl px-4 py-2 text-sm">${L('Copy', 'Copiar')}</button>
        </div>
        <p class="text-xs text-slate-500 mt-3">${L('Tip: use the same utm_medium on all InfoWeb free tools for clean analytics.', 'Dica: use o mesmo utm_medium em todas as ferramentas InfoWeb para analytics limpos.')}</p>
      </div>
      <div class="bg-gradient-to-br from-slate-900 via-slate-900 to-ink border-2 border-signal/40 rounded-2xl p-6 text-center">
        <p class="text-signal mb-2 text-xs font-black uppercase tracking-[0.2em]">${L('Track what works', 'Meça o que funciona')}</p>
        <h3 class="text-xl font-bold text-white mb-3">${L('A website built to convert', 'Um site feito para converter')}</h3>
        <p class="text-slate-400 mb-4 text-sm">${L('Pair UTMs with landing pages that load fast and capture leads.', 'Combine UTMs com páginas rápidas que captam leads.')}</p>
        <a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium=utm_link_builder&utm_campaign=result_cta#pricing" target="_blank"
           class="inline-flex items-center gap-2 bg-sky-600 hover:bg-sky-500 text-white font-bold rounded-xl px-6 py-3 transition-all">${L('See Website Plans', 'Ver planos de website')}</a>
      </div>
      <p class="text-center"><button type="button" onclick="resetTool()" class="text-sm text-slate-500 hover:text-slate-300 underline">${L('Build another link', 'Criar outro link')}</button></p>`;
    show('result-box');
    document.getElementById('output-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
    if (typeof window.trackEvent === 'function') {
      window.trackEvent('tool_result_shown', { duration_ms: Math.round(performance.now() - toolRunStartedAt) });
    }
  } catch (err) {
    console.error(err);
    show('error-box');
  } finally {
    hideFlex('spinner');
  }
}

function resetTool() {
  hide('result-box');
  hide('error-box');
  ['base-url','utm-source','utm-medium','utm-campaign','utm-term','utm-content'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = el.id === 'utm-source' ? 'freetool' : el.id === 'utm-medium' ? 'utm_link_builder' : '';
  });
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

document.addEventListener('DOMContentLoaded', () => {
  const src = document.getElementById('utm-source');
  const med = document.getElementById('utm-medium');
  if (src && !src.value) src.value = 'freetool';
  if (med && !med.value) med.value = 'utm_link_builder';
});
''',
    },
    # ... more tools defined in generate functions below
]


def write_tool(spec: dict) -> None:
    slug = spec["slug"]
    en_dir = FT / slug
    pt_dir = FT / "pt" / slug
    en_dir.mkdir(parents=True, exist_ok=True)
    pt_dir.mkdir(parents=True, exist_ok=True)

    (en_dir / "style.css").write_text(STYLE, encoding="utf-8")
    (en_dir / "script.js").write_text(spec["script"], encoding="utf-8")

    rel_en = "\n".join(
        f'      <li><a href="{h}" class="hover:text-signal transition">{l}</a></li>'
        for h, l in spec["related_en"]
    )
    rel_pt = "\n".join(
        f'      <li><a href="{h}" class="hover:text-signal transition">{l}</a></li>'
        for h, l in spec["related_pt"]
    )

    (en_dir / "index.html").write_text(
        page("en", slug, spec["medium"], spec["accent"], spec["meta_en"], spec["body_en"], rel_en),
        encoding="utf-8",
    )
    (pt_dir / "index.html").write_text(
        page("pt", slug, spec["medium"], spec["accent"], spec["meta_pt"], spec["body_pt"], rel_pt),
        encoding="utf-8",
    )
    print(f"  ✓ {slug}")


def main() -> None:
    specs = build_all_specs()
    print("Scaffolding 5 free tools...")
    for spec in specs:
        write_tool(spec)
    print("Done.")


if __name__ == "__main__":
    main()
