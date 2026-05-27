#!/usr/bin/env python3
"""Scaffold three SEO discovery free tools (EN + PT) + competitor PT page."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FT = ROOT / "free-tools"
OG = "https://infoweb.sousadev.com/assets/images/og-image.png"

STYLE = """#spinner.flex, #spinner.show-flex { display: flex !important; }
.copy-row { display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: stretch; margin-top: 0.75rem; }
.copy-row input, .copy-row textarea {
  flex: 1; min-width: 0; width: 100%;
  background: #1e293b; border: 1px solid #334155; border-radius: 0.75rem;
  color: #f1f5f9; font-family: ui-monospace, monospace; font-size: 0.8rem;
  padding: 0.65rem 1rem;
}
.copy-row textarea { min-height: 5rem; resize: vertical; }
.char-ok { color: #4ade80; }
.char-warn { color: #fbbf24; }
.char-bad { color: #f87171; }
"""


def head(lang: str, slug: str, m: dict) -> str:
    en = lang == "en"
    canon = f"https://infoweb.sousadev.com/free-tools/{'pt/' if not en else ''}{slug}/"
    en_url = f"https://infoweb.sousadev.com/free-tools/{slug}/"
    pt_url = f"https://infoweb.sousadev.com/free-tools/pt/{slug}/"
    rel = "../../" if en else "../../../"
    css = "style.css" if en else f"../../{slug}/style.css"
    return f"""<!DOCTYPE html>
<html lang="{lang}" class="scroll-smooth">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{m['title']}</title>
<meta name="description" content="{m['description']}"/>
<meta name="keywords" content="{m['keywords']}"/>
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1"/>
<link rel="canonical" href="{canon}"/>
<meta property="og:url" content="{canon}"/><meta property="og:title" content="{m['title']}"/>
<meta property="og:description" content="{m['og']}"/><meta property="og:image" content="{OG}"/>
<link rel="alternate" hreflang="en" href="{en_url}"/><link rel="alternate" hreflang="pt" href="{pt_url}"/>
<link rel="icon" href="{rel}favicon_io/favicon-32x32.png"/>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
<script src="https://cdn.tailwindcss.com"></script>
<link rel="stylesheet" href="{css}"/>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXQSMBERJM"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-XXQSMBERJM");</script>
<script src="{rel}assets/js/analytics.js" defer></script>
</head>"""


def shell(lang: str, slug: str, medium: str, accent: str, m: dict, body: str, related: str) -> str:
    en = lang == "en"
    a = accent
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
        head(lang, slug, m)
        + f"""
<body class="bg-slate-950 text-white font-sans antialiased">
<header class="sticky top-0 z-50 bg-slate-950/90 backdrop-blur border-b border-slate-800/60">
<div class="max-w-2xl mx-auto px-4 py-3 flex justify-between items-center gap-3">
<a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium={medium}&utm_campaign=header" target="_blank" rel="noopener"><img src="{rel_root}assets/images/infoweb-logo.png" alt="InfoWeb" class="h-9"/></a>
<div class="flex gap-2 items-center"><nav class="flex gap-1 text-[11px] font-semibold">{lang_nav}</nav>
<a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium={medium}&utm_campaign=header_btn#pricing" target="_blank" class="text-sm border border-slate-600 rounded-full px-4 py-1.5 text-slate-300">{m['cta']}</a></div></div></header>
<main class="max-w-2xl mx-auto px-4 py-12">
<section class="text-center mb-10"><div class="inline-flex gap-2 bg-{a}-500/10 border border-{a}-500/30 rounded-full px-4 py-1.5 text-sm text-{a}-400 mb-5"><span class="w-2 h-2 rounded-full bg-{a}-400 animate-pulse"></span>{m['badge']}</div>
<h1 class="text-3xl sm:text-4xl font-bold mb-4">{m['h1']}</h1><p class="text-slate-400 text-lg">{m['sub']}</p></section>
{body}
<section class="mb-10" id="output-section">
<div id="spinner" class="hidden flex-col items-center py-12 text-slate-400"><svg class="animate-spin h-8 w-8 mb-3 text-{a}-500" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path fill="currentColor" d="M4 12a8 8 0 018-8v8z"/></svg><span>{m['spin']}</span></div>
<div id="error-box" class="hidden bg-red-900/30 border border-red-700/50 rounded-2xl p-5 text-center text-red-300">{m['err']}</div>
<div id="result-box" class="hidden space-y-4"></div></section>
<section class="mb-10"><h2 class="text-xl font-bold mb-4">{m['faq']}</h2>
<details class="bg-slate-900 border border-slate-800 rounded-xl p-4"><summary class="font-semibold cursor-pointer">{m['fq1']}</summary><p class="text-slate-400 text-sm mt-2">{m['fa1']}</p></details></section>
</main>
<section class="max-w-2xl mx-auto px-4 mb-8"><h2 class="text-sm font-bold uppercase text-slate-500 mb-3">{m['rel']}</h2><ul class="flex flex-wrap gap-x-4 gap-y-2 text-sm text-slate-400">
{related}<li><a href="{rel_hub}" class="hover:text-signal">{m['all']}</a></li></ul></section>
<footer class="border-t border-slate-800 py-6 text-center text-sm"><a href="{rel_root}" class="text-slate-400">{m['foot']}</a></footer>
<script src="{script}" defer></script></body></html>"""
    )


def write_tool(spec: dict) -> None:
    slug = spec["slug"]
    d = FT / slug
    pt = FT / "pt" / slug
    d.mkdir(parents=True, exist_ok=True)
    pt.mkdir(parents=True, exist_ok=True)
    (d / "style.css").write_text(STYLE, encoding="utf-8")
    (d / "script.js").write_text(spec["script"], encoding="utf-8")
    (d / "index.html").write_text(shell("en", slug, spec["medium"], spec["accent"], spec["en"], spec["body_en"], spec["rel_en"]), encoding="utf-8")
    (pt / "index.html").write_text(shell("pt", slug, spec["medium"], spec["accent"], spec["pt"], spec["body_pt"], spec["rel_pt"]), encoding="utf-8")
    print(f"  tool {slug}")


SEO_META_SCRIPT = r"""'use strict';
const PT=(document.documentElement.lang||'').toLowerCase().startsWith('pt');
const L=(e,p)=>PT?p:e;
function show(id){document.getElementById(id).classList.remove('hidden')}
function hide(id){document.getElementById(id).classList.add('hidden')}
function showFlex(id){const el=document.getElementById(id);el.classList.remove('hidden');el.classList.add('flex')}
function hideFlex(id){const el=document.getElementById(id);el.classList.add('hidden');el.classList.remove('flex')}
function lenClass(n,max){if(n<=max)return 'char-ok';if(n<=max+15)return 'char-warn';return 'char-bad'}
async function copyText(t,id){try{await navigator.clipboard.writeText(t);const b=document.getElementById(id);if(b){const o=b.textContent;b.textContent=L('Copied!','Copiado!');setTimeout(()=>b.textContent=o,2000)}}catch(e){alert(L('Copy failed.','Falha ao copiar.'))}}
function titles(biz,topic,loc){
  const locBit=loc?` ${loc.trim()}`:'';
  const base=[`${topic.trim()} | ${biz.trim()}`,`${biz.trim()} — ${topic.trim()}`,`${topic.trim()} — ${biz.trim()}${locBit}`];
  return base.map(t=>t.slice(0,60));
}
function descriptions(biz,topic,loc){
  const locBit=loc?` ${loc.trim()}.`:'';
  const lines=[
    `${biz.trim()} — ${topic.trim()}.${locBit} Book online, see services & contact us in seconds.`,
    `Looking for ${topic.trim().toLowerCase()}? ${biz.trim()} helps local customers${locBit} Fast site, clear offers & easy contact.`,
    `${topic.trim()} at ${biz.trim()}${locBit} Trusted local business — prices, hours & how to reach us on one page.`
  ];
  return lines.map(d=>d.slice(0,160));
}
async function runTool(){
  const biz=document.getElementById('biz').value.trim();
  const topic=document.getElementById('topic').value.trim();
  const loc=document.getElementById('loc').value.trim();
  if(!biz||!topic){alert(L('Enter business name and page topic.','Introduza nome do negócio e tema da página.'));return}
  if(typeof window.trackEvent==='function')window.trackEvent('tool_used');
  showFlex('spinner');hide('result-box');
  try{
    const ts=titles(biz,topic,loc);const ds=descriptions(biz,topic,loc);
    let html='';
    ts.forEach((t,i)=>{
      const n=t.length;
      html+=`<div class="bg-slate-900 border border-emerald-500/30 rounded-2xl p-5 mb-4"><p class="text-xs font-bold uppercase text-emerald-400 mb-2">${L('Title option','Opção de título')} ${i+1} <span class="${lenClass(n,60)}">(${n}/60)</span></p><div class="copy-row"><input readonly id="t${i}" value="${t.replace(/"/g,'&quot;')}"/><button type="button" id="bt${i}" onclick="copyText(document.getElementById('t${i}').value,'bt${i}')" class="shrink-0 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-xl px-4 py-2 text-sm">${L('Copy','Copiar')}</button></div></div>`;
    });
    ds.forEach((d,i)=>{
      const n=d.length;
      html+=`<div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 mb-4"><p class="text-xs font-bold uppercase text-slate-400 mb-2">${L('Meta description','Meta description')} ${i+1} <span class="${lenClass(n,160)}">(${n}/160)</span></p><div class="copy-row"><textarea readonly id="d${i}">${d}</textarea><button type="button" id="bd${i}" onclick="copyText(document.getElementById('d${i}').value,'bd${i}')" class="shrink-0 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-xl px-4 py-2 text-sm">${L('Copy','Copiar')}</button></div></div>`;
    });
    html+=`<div class="bg-gradient-to-br from-slate-900 to-ink border-2 border-signal/40 rounded-2xl p-6 text-center"><h3 class="text-xl font-bold mb-2">${L('Put these on a fast website','Publique num site rápido')}</h3><p class="text-slate-400 text-sm mb-4">${L('Titles and meta tags only work if Google can crawl a real page.','Títulos e meta só funcionam se o Google conseguir indexar uma página real.')}</p><a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium=seo_meta_generator&utm_campaign=result_cta#pricing" target="_blank" class="inline-flex bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl px-6 py-3">${L('See Website Plans','Ver planos')}</a></div>`;
    document.getElementById('result-box').innerHTML=html;show('result-box');
    if(typeof window.trackEvent==='function')window.trackEvent('tool_result_shown');
  }finally{hideFlex('spinner')}
}
"""

SLUG_SCRIPT = r"""'use strict';
const PT=(document.documentElement.lang||'').toLowerCase().startsWith('pt');
const L=(e,p)=>PT?p:e;
function show(id){document.getElementById(id).classList.remove('hidden')}
function hide(id){document.getElementById(id).classList.add('hidden')}
function showFlex(id){const el=document.getElementById(id);el.classList.remove('hidden');el.classList.add('flex')}
function hideFlex(id){const el=document.getElementById(id);el.classList.add('hidden');el.classList.remove('flex')}
function toSlug(raw){
  return raw.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase()
    .replace(/[^a-z0-9\s-]/g,'').trim().replace(/\s+/g,'-').replace(/-+/g,'-').replace(/^-|-$/g,'');
}
async function copyText(t,id){try{await navigator.clipboard.writeText(t);const b=document.getElementById(id);if(b){const o=b.textContent;b.textContent=L('Copied!','Copiado!');setTimeout(()=>b.textContent=o,2000)}}catch(e){alert(L('Copy failed.','Falha ao copiar.'))}}
async function runTool(){
  const text=document.getElementById('text-in').value;
  const slug=toSlug(text);
  if(!slug){alert(L('Enter some text first.','Escreva algum texto primeiro.'));return}
  if(typeof window.trackEvent==='function')window.trackEvent('tool_used');
  showFlex('spinner');hide('result-box');
  try{
    document.getElementById('result-box').innerHTML=`<div class="bg-slate-900 border border-violet-500/30 rounded-2xl p-5"><p class="text-xs font-bold uppercase text-violet-400 mb-2">${L('SEO-friendly slug','Slug amigável para SEO')}</p><div class="copy-row"><input readonly id="out-slug" value="${slug}"/><button type="button" id="btn-slug" onclick="copyText(document.getElementById('out-slug').value,'btn-slug')" class="shrink-0 bg-violet-600 hover:bg-violet-500 text-white font-semibold rounded-xl px-4 py-2 text-sm">${L('Copy','Copiar')}</button></div><p class="text-xs text-slate-500 mt-3">${L('Use in URLs like: /services/'+slug,'Use em URLs como: /servicos/'+slug)}</p></div>
    <div class="bg-gradient-to-br from-slate-900 to-ink border-2 border-signal/40 rounded-2xl p-6 text-center mt-4"><h3 class="text-xl font-bold mb-2">${L('Clean URLs on a managed site','URLs limpas num site gerido')}</h3><a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium=url_slug_generator&utm_campaign=result_cta#pricing" target="_blank" class="inline-flex bg-violet-600 hover:bg-violet-500 text-white font-bold rounded-xl px-6 py-3">${L('See Website Plans','Ver planos')}</a></div>`;
    show('result-box');
    if(typeof window.trackEvent==='function')window.trackEvent('tool_result_shown');
  }finally{hideFlex('spinner')}
}
"""

CHAR_SCRIPT = r"""'use strict';
const PT=(document.documentElement.lang||'').toLowerCase().startsWith('pt');
const L=(e,p)=>PT?p:e;
function count(){
  const t=document.getElementById('text-in').value;
  const chars=t.length;const words=(t.trim()?t.trim().split(/\s+/).length:0);const lines=(t?t.split(/\n/).length:0);
  const el=document.getElementById('live-stats');
  if(!el)return;
  const titleOk=chars<=60?'char-ok':chars<=70?'char-warn':'char-bad';
  const metaOk=chars<=160?'char-ok':chars<=180?'char-warn':'char-bad';
  el.innerHTML=`<div class="grid grid-cols-3 gap-3 text-center mb-4"><div class="bg-slate-800 rounded-xl p-3"><p class="text-2xl font-bold">${chars}</p><p class="text-xs text-slate-400">${L('Characters','Caracteres')}</p></div><div class="bg-slate-800 rounded-xl p-3"><p class="text-2xl font-bold">${words}</p><p class="text-xs text-slate-400">${L('Words','Palavras')}</p></div><div class="bg-slate-800 rounded-xl p-3"><p class="text-2xl font-bold">${lines}</p><p class="text-xs text-slate-400">${L('Lines','Linhas')}</p></div></div>
  <p class="text-sm text-slate-400">${L('Google title target','Alvo título Google')}: <span class="${titleOk}">${chars}/60</span> · ${L('Meta description target','Alvo meta description')}: <span class="${metaOk}">${chars}/160</span></p>`;
}
document.addEventListener('DOMContentLoaded',()=>{
  const ta=document.getElementById('text-in');
  if(ta){ta.addEventListener('input',count);count();}
  if(typeof window.trackEvent==='function')window.trackEvent('tool_used');
});
"""


def competitor_pt_page() -> str:
    return """<!DOCTYPE html>
<html lang="pt" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Gap de visibilidade vs concorrentes — InfoWeb</title>
  <meta name="description" content="Compare o seu negócio com até 2 concorrentes em avaliações Google, site e redes sociais. Score de visibilidade gratuito e plano de ação." />
  <meta name="keywords" content="análise concorrentes, ferramenta visibilidade negócio, comparar avaliações Google, SEO local Portugal, InfoWeb" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
  <link rel="canonical" href="https://infoweb.sousadev.com/free-tools/pt/competitor-visibility-gap/" />
  <meta property="og:url" content="https://infoweb.sousadev.com/free-tools/pt/competitor-visibility-gap/" />
  <meta property="og:title" content="Gap de visibilidade vs concorrentes — InfoWeb" />
  <meta property="og:description" content="Compare o seu negócio com concorrentes e receba um plano de ação gratuito." />
  <meta property="og:image" content="https://infoweb.sousadev.com/free-tools/competitor-visibility-gap/og-image.png" />
  <meta property="og:locale" content="pt_PT" />
  <link rel="alternate" hreflang="en" href="https://infoweb.sousadev.com/free-tools/competitor-visibility-gap/" />
  <link rel="alternate" hreflang="pt" href="https://infoweb.sousadev.com/free-tools/pt/competitor-visibility-gap/" />
  <link rel="icon" type="image/png" href="../../../favicon_io/favicon-32x32.png" />
  <link rel="stylesheet" href="../../competitor-visibility-gap/style.css" />
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXQSMBERJM"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-XXQSMBERJM');</script>
  <script src="../../../assets/js/analytics.js" defer></script>
</head>
<body>
  <header style="position:sticky;top:0;z-index:50;background:rgba(2,6,23,0.88);border-bottom:1px solid #1e293b;">
    <div style="max-width:640px;margin:0 auto;padding:0.75rem 1rem;display:flex;align-items:center;justify-content:space-between;">
      <a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium=competitor_visibility_gap_header" target="_blank" rel="noopener"><img src="../../../assets/images/infoweb-logo.png" alt="InfoWeb" style="height:2rem;width:auto;" /></a>
      <div style="display:flex;align-items:center;gap:0.5rem;">
        <nav style="display:flex;gap:0.25rem;font-size:11px;font-weight:700;" aria-label="Idioma">
          <a href="../../competitor-visibility-gap/" hreflang="en" style="border-radius:999px;padding:0.2rem 0.45rem;color:#94a3b8;text-decoration:none;">EN</a>
          <span style="border-radius:999px;padding:0.2rem 0.45rem;background:#1e293b;border:1px solid #64748b;color:#fff;">PT</span>
        </nav>
        <a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium=competitor_visibility_gap_header_btn#pricing" target="_blank" rel="noopener" class="header-cta-btn">Ver planos de website</a>
      </div>
    </div>
  </header>
  <main style="max-width:640px;margin:0 auto;padding:2.5rem 1rem 4rem;">
    <section style="text-align:center;margin-bottom:2.5rem;">
      <span class="free-badge" style="margin-bottom:1.25rem;"><span class="free-badge-dot"></span>Grátis — Sem registo</span>
      <h1 style="font-size:clamp(1.9rem,6vw,2.75rem);font-weight:900;line-height:1.1;margin:0.75rem 0;color:#f1f5f9;">Compare-se com os seus concorrentes</h1>
      <p style="color:#94a3b8;font-size:1.05rem;line-height:1.65;max-width:480px;margin:0 auto;">Veja como o seu negócio se posiciona face a até 2 rivais em avaliações, site e redes. Score de visibilidade e plano de ação gratuito.</p>
    </section>
    <section id="quiz-section" style="margin-bottom:2.5rem;">
      <div style="margin-bottom:1.25rem;">
        <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
          <span id="q-counter" style="font-size:0.78rem;font-weight:700;color:#64748b;text-transform:uppercase;">Pergunta 1 de 7</span>
          <span id="quiz-pct" style="font-size:0.78rem;font-weight:700;color:#64748b;">0%</span>
        </div>
        <div class="progress-track" id="quiz-progress-bar" role="progressbar" aria-valuemin="1" aria-valuemax="7" aria-valuenow="1"><div class="progress-fill" id="quiz-progress-fill"></div></div>
      </div>
      <div id="question-card" class="question-card">
        <p id="q-text" style="font-size:1.15rem;font-weight:700;color:#f1f5f9;line-height:1.45;margin:0 0 1.75rem;min-height:3.5rem;"></p>
        <div style="display:flex;gap:0.75rem;">
          <button type="button" class="answer-btn yes-btn" onclick="answerQuestion('yes')"><span aria-hidden="true">✓</span> Sim</button>
          <button type="button" class="answer-btn no-btn" onclick="answerQuestion('no')"><span aria-hidden="true">✗</span> Não</button>
        </div>
        <p style="font-size:0.78rem;color:#475569;text-align:center;margin:1rem 0 0;">Toque numa resposta — a honestidade ajuda a obter um diagnóstico útil.</p>
      </div>
    </section>
    <section id="result-section" class="hidden" style="margin-bottom:2.5rem;">
      <div style="background:#0f172a;border:1px solid #1e293b;border-radius:1.25rem;padding:2rem 1.5rem;text-align:center;margin-bottom:1rem;">
        <p style="font-size:0.7rem;font-weight:800;text-transform:uppercase;letter-spacing:0.14em;color:#64748b;margin:0 0 1.25rem;">O seu score de visibilidade</p>
        <div class="ring-container">
          <svg class="ring-svg" width="220" height="220" viewBox="0 0 220 220"><circle class="ring-track" cx="110" cy="110" r="90" /><circle id="score-ring" cx="110" cy="110" r="90" style="stroke-dasharray:565.5;stroke-dashoffset:565.5;" /></svg>
          <div class="ring-label"><span class="ring-number" id="ring-count" style="color:#f1f5f9;">0</span><span class="ring-total" id="score-total">/ 100</span></div>
        </div>
        <span id="score-band" class="score-band" style="margin-bottom:1rem;display:inline-block;"></span>
        <div style="background:#020617;border:1px solid #1e293b;border-radius:0.875rem;padding:1rem 1.25rem;margin-top:1.25rem;text-align:left;">
          <p style="font-size:0.7rem;font-weight:800;text-transform:uppercase;color:#64748b;margin:0 0 0.35rem;">A sua principal oportunidade</p>
          <p id="weakness-msg" style="color:#cbd5e1;font-size:0.9rem;line-height:1.65;margin:0;"></p>
        </div>
      </div>
      <div style="background:#0f172a;border:1px solid #1e293b;border-radius:1.25rem;padding:1.5rem;margin-bottom:1rem;">
        <p style="font-size:0.7rem;font-weight:800;text-transform:uppercase;color:#64748b;margin:0 0 1rem;">Diagnóstico completo</p>
        <div class="breakdown-wrapper breakdown-locked" id="breakdown-wrapper">
          <ul class="breakdown-list" id="breakdown-list"></ul>
          <div id="breakdown-overlay" class="breakdown-overlay">
            <p style="font-weight:700;color:#f1f5f9;margin:0;">Desbloqueie o relatório completo</p>
            <p style="color:#94a3b8;font-size:0.85rem;margin:0;">Indique o email para ver a análise pergunta a pergunta na caixa de entrada.</p>
          </div>
        </div>
      </div>
      <div id="email-gate" style="background:#0f172a;border:1px solid #1e293b;border-radius:1.25rem;padding:1.5rem;margin-bottom:1rem;">
        <p style="font-weight:700;color:#f1f5f9;margin:0 0 0.35rem;">Receba o relatório completo</p>
        <p style="color:#64748b;font-size:0.85rem;margin:0 0 1rem;">Sem spam — só o diagnóstico e dicas práticas.</p>
        <input id="gate-email" type="email" placeholder="o.seu@email.pt" autocomplete="email" style="width:100%;background:#1e293b;border:1.5px solid #334155;border-radius:0.625rem;color:#f1f5f9;padding:0.7rem 1rem;margin-bottom:0.5rem;box-sizing:border-box;" oninput="clearEmailError()" />
        <p id="gate-email-error" class="hidden" style="font-size:0.8rem;color:#f87171;">Introduza um email válido.</p>
        <div id="email-api-error" class="hidden"><p style="font-size:0.8rem;color:#f87171;">Algo correu mal. Tente novamente.</p></div>
        <div id="email-spinner" class="hidden" aria-live="polite"><span style="color:#94a3b8;">A enviar…</span></div>
        <button id="email-submit-btn" type="button" onclick="submitEmail()" class="btn-primary">Desbloquear relatório</button>
      </div>
      <div id="email-success" class="hidden" style="background:rgba(52,211,153,0.08);border:1px solid rgba(52,211,153,0.3);border-radius:1rem;padding:1.25rem;text-align:center;">
        <p style="font-weight:700;color:#34d399;">Verifique a caixa de entrada!</p>
        <p style="font-size:0.875rem;color:#64748b;margin:0;">O relatório está a caminho. Veja também o spam.</p>
      </div>
      <p style="text-align:center;"><button type="button" onclick="retakeQuiz()" style="background:none;border:none;color:#64748b;cursor:pointer;text-decoration:underline;">← Repetir o questionário</button></p>
    </section>
    <section class="conversion-cta">
      <p class="conversion-cta-eyebrow">Pronto para chegar aos 100/100?</p>
      <h2 class="conversion-cta-title">Podemos levar o seu score a 100/100 em menos de uma semana.</h2>
      <p class="conversion-cta-body">A InfoWeb cria, aloja e mantém a sua presença online por subscrição fixa.</p>
      <a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium=competitor_visibility_gap&utm_campaign=cta#pricing" target="_blank" class="conversion-cta-btn">Ver planos de website →</a>
    </section>
  </main>
  <footer style="border-top:1px solid #1e293b;padding:1.5rem 0;text-align:center;">
    <a href="../" data-track="back_to_tools_click" style="color:#475569;font-size:0.75rem;">← Todas as ferramentas</a>
  </footer>
  <script src="../../competitor-visibility-gap/script.js"></script>
</body>
</html>
"""


def main() -> None:
    pt_dir = FT / "pt" / "competitor-visibility-gap"
    pt_dir.mkdir(parents=True, exist_ok=True)
    (pt_dir / "index.html").write_text(competitor_pt_page(), encoding="utf-8")
    print("  competitor PT page")

    form = '<section class="mb-6"><div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-5">{fields}<button type="button" onclick="runTool()" class="w-full bg-{a}-600 hover:bg-{a}-500 text-white font-bold rounded-xl px-6 py-4">{btn}</button></div></section>'

    write_tool({
        "slug": "seo-meta-generator",
        "medium": "seo_meta_generator",
        "accent": "emerald",
        "script": SEO_META_SCRIPT,
        "en": {"title": "Free SEO Title & Meta Description Generator — InfoWeb", "description": "Generate Google-ready page titles (60 chars) and meta descriptions (160 chars) for your local business. Copy-paste in seconds.", "keywords": "meta title generator, meta description generator, seo title tool, free seo meta tags", "og": "SEO titles and meta descriptions for local businesses.", "cta": "See Website Plans", "badge": "Free — No sign-up", "h1": "SEO title & meta description generator", "sub": "Three title and description combos sized for Google — ready to paste into your site.", "spin": "Generating…", "err": "Something went wrong.", "faq": "FAQ", "fq1": "Why 60 and 160 characters?", "fa1": "Google typically shows ~60 characters for titles and ~160 for meta descriptions. Staying inside these limits avoids truncation in search results.", "rel": "Related tools", "all": "All free tools", "foot": "← InfoWeb home"},
        "pt": {"title": "Gerador de título SEO e meta description — InfoWeb", "description": "Gere títulos (60 car.) e meta descriptions (160 car.) para o seu negócio local. Copiar e colar em segundos.", "keywords": "gerador meta title, meta description, ferramenta seo gratuita, tags seo", "og": "Títulos e meta descriptions SEO para PME.", "cta": "Ver planos de website", "badge": "Grátis — Sem registo", "h1": "Gerador de título SEO e meta description", "sub": "Três combinações com limites Google — prontas para o seu site.", "spin": "A gerar…", "err": "Algo correu mal.", "faq": "Perguntas frequentes", "fq1": "Porquê 60 e 160 caracteres?", "fa1": "O Google mostra cerca de 60 caracteres no título e 160 na meta description. Respeitar estes limites evita cortes nos resultados.", "rel": "Ferramentas relacionadas", "all": "Todas as ferramentas", "foot": "← Início InfoWeb"},
        "body_en": form.format(a="emerald", btn="Generate SEO tags", fields='<div><label for="biz" class="block text-sm font-semibold text-slate-300 mb-2">Business name</label><input id="biz" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white" placeholder="Café Central"/></div><div><label for="topic" class="block text-sm font-semibold text-slate-300 mb-2">Page topic / service</label><input id="topic" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white" placeholder="Breakfast menu & brunch"/></div><div><label for="loc" class="block text-sm font-semibold text-slate-300 mb-2">City (optional)</label><input id="loc" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white" placeholder="Lisbon"/></div>'),
        "body_pt": form.format(a="emerald", btn="Gerar tags SEO", fields='<div><label for="biz" class="block text-sm font-semibold text-slate-300 mb-2">Nome do negócio</label><input id="biz" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white" placeholder="Café Central"/></div><div><label for="topic" class="block text-sm font-semibold text-slate-300 mb-2">Tema / serviço da página</label><input id="topic" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white" placeholder="Pequeno-almoço e brunch"/></div><div><label for="loc" class="block text-sm font-semibold text-slate-300 mb-2">Cidade (opcional)</label><input id="loc" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white" placeholder="Lisboa"/></div>'),
        "rel_en": '      <li><a href="schema-local-business-generator/" class="hover:text-signal">Schema Generator</a></li>\n      <li><a href="url-slug-generator/" class="hover:text-signal">URL Slug Generator</a></li>\n',
        "rel_pt": '      <li><a href="schema-local-business-generator/" class="hover:text-signal">Gerador Schema</a></li>\n      <li><a href="url-slug-generator/" class="hover:text-signal">Gerador de slug</a></li>\n',
    })

    write_tool({
        "slug": "url-slug-generator",
        "medium": "url_slug_generator",
        "accent": "violet",
        "script": SLUG_SCRIPT,
        "en": {"title": "Free URL Slug Generator — InfoWeb", "description": "Turn any headline or page name into a clean, SEO-friendly URL slug. Lowercase, hyphens, no special characters.", "keywords": "url slug generator, seo slug tool, permalink generator, friendly url", "og": "SEO-friendly URL slugs in one click.", "cta": "See Website Plans", "badge": "Free — No sign-up", "h1": "URL slug generator", "sub": "Paste a title → get a clean path like /services/breakfast-menu", "spin": "Building slug…", "err": "Something went wrong.", "faq": "FAQ", "fq1": "What makes a good slug?", "fa1": "Short, readable, lowercase words separated by hyphens. Avoid dates and random IDs in URLs you want to rank.", "rel": "Related tools", "all": "All free tools", "foot": "← InfoWeb home"},
        "pt": {"title": "Gerador de slug para URL — InfoWeb", "description": "Transforme títulos em slugs limpos para SEO. Minúsculas, hífens, sem caracteres especiais.", "keywords": "gerador slug url, slug seo, permalink, url amigável", "og": "Slugs SEO num clique.", "cta": "Ver planos de website", "badge": "Grátis — Sem registo", "h1": "Gerador de slug para URL", "sub": "Cole um título → obtenha um caminho como /servicos/ementa-pequeno-almoco", "spin": "A gerar…", "err": "Algo correu mal.", "faq": "Perguntas frequentes", "fq1": "O que é um bom slug?", "fa1": "Curto, legível, palavras em minúsculas separadas por hífens. Evite datas e IDs aleatórios em URLs que quer posicionar.", "rel": "Ferramentas relacionadas", "all": "Todas as ferramentas", "foot": "← Início InfoWeb"},
        "body_en": form.format(a="violet", btn="Generate slug", fields='<div><label for="text-in" class="block text-sm font-semibold text-slate-300 mb-2">Page title or phrase</label><input id="text-in" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white" placeholder="Best Hair Salon in Porto"/></div>'),
        "body_pt": form.format(a="violet", btn="Gerar slug", fields='<div><label for="text-in" class="block text-sm font-semibold text-slate-300 mb-2">Título ou frase</label><input id="text-in" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white" placeholder="Melhor cabeleireiro no Porto"/></div>'),
        "rel_en": '      <li><a href="seo-meta-generator/" class="hover:text-signal">SEO Meta Generator</a></li>\n      <li><a href="character-counter/" class="hover:text-signal">Character Counter</a></li>\n',
        "rel_pt": '      <li><a href="seo-meta-generator/" class="hover:text-signal">Gerador meta SEO</a></li>\n      <li><a href="character-counter/" class="hover:text-signal">Contador de caracteres</a></li>\n',
    })

    char_body = '<section class="mb-6"><div class="bg-slate-900 border border-slate-800 rounded-2xl p-6"><label for="text-in" class="block text-sm font-semibold text-slate-300 mb-2">{label}</label><textarea id="text-in" rows="6" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white" placeholder="{ph}"></textarea><div id="live-stats" class="mt-4"></div></div></section>'
    write_tool({
        "slug": "character-counter",
        "medium": "character_counter",
        "accent": "cyan",
        "script": CHAR_SCRIPT,
        "en": {"title": "Free Character Counter for SEO — InfoWeb", "description": "Count characters and words for Google titles, meta descriptions, and social posts. Live 60/160 char guides.", "keywords": "character counter, meta description length, title length checker, word counter seo", "og": "Live character count for SEO copy.", "cta": "See Website Plans", "badge": "Free — No sign-up", "h1": "SEO character & word counter", "sub": "Type or paste copy — see length vs Google title (60) and meta description (160) limits.", "spin": "…", "err": "…", "faq": "FAQ", "fq1": "What length for meta descriptions?", "fa1": "Aim for 150–160 characters so Google shows your full message without cutting off mid-sentence.", "rel": "Related tools", "all": "All free tools", "foot": "← InfoWeb home"},
        "pt": {"title": "Contador de caracteres para SEO — InfoWeb", "description": "Conte caracteres e palavras para títulos Google, meta descriptions e redes. Limites 60/160 em tempo real.", "keywords": "contador caracteres, tamanho meta description, contador palavras seo", "og": "Contagem em tempo real para copy SEO.", "cta": "Ver planos de website", "badge": "Grátis — Sem registo", "h1": "Contador de caracteres e palavras SEO", "sub": "Escreva ou cole texto — veja o comprimento vs limites Google (60 e 160).", "spin": "…", "err": "…", "faq": "Perguntas frequentes", "fq1": "Que comprimento para meta descriptions?", "fa1": "Aponte a 150–160 caracteres para o Google mostrar a mensagem completa.", "rel": "Ferramentas relacionadas", "all": "Todas as ferramentas", "foot": "← Início InfoWeb"},
        "body_en": char_body.format(label="Your text", ph="Paste a draft meta description or page title…"),
        "body_pt": char_body.format(label="O seu texto", ph="Cole um rascunho de meta description ou título…"),
        "rel_en": '      <li><a href="seo-meta-generator/" class="hover:text-signal">SEO Meta Generator</a></li>\n      <li><a href="website-health-scorecard/" class="hover:text-signal">Website Health Scorecard</a></li>\n',
        "rel_pt": '      <li><a href="seo-meta-generator/" class="hover:text-signal">Gerador meta SEO</a></li>\n      <li><a href="website-health-scorecard/" class="hover:text-signal">Saúde do site</a></li>\n',
    })
    print("Done.")


if __name__ == "__main__":
    main()
