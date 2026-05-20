#!/usr/bin/env python3
"""Fix Portuguese free-tool pages: translations, related links, and broken ../pt/ paths."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PT_DIR = ROOT / "free-tools" / "pt"

TOOL_LABELS_PT = {
    "whatsapp-qr-generator": "Gerador de link e QR WhatsApp",
    "menu-qr-generator": "Gerador de QR Code para ementa",
    "wifi-qr-generator": "Gerador de QR Code Wi‑Fi",
    "business-card-qr": "Cartão de visita digital em QR",
    "google-review-generator": "Gerador de link para avaliações Google",
    "presence-score": "Score de presença online",
    "website-health-scorecard": "Avaliação de saúde do site",
    "competitor-visibility-gap": "Gap de visibilidade vs concorrentes",
    "website-roi-calculator": "Calculadora de ROI do site",
    "break-even-calculator": "Calculadora de break-even",
    "markup-margin-calculator": "Calculadora margem vs markup",
    "vat-calculator-pt": "Calculadora de IVA (Portugal)",
    "freelancer-rate-calculator": "Calculadora de tarifa freelancer",
    "cost-per-lead-calculator": "Calculadora de custo por lead",
    "customer-ltv-calculator": "Calculadora de LTV do cliente",
    "lost-customers-calculator": "Calculadora de clientes perdidos",
    "downtime-cost-calculator": "Calculadora de custo de downtime",
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
}


def fix_related_links_in_pt_tools() -> None:
    """Fix ../pt/ paths and English labels in tool subpages under free-tools/pt/<slug>/."""
    for html in PT_DIR.glob("*/index.html"):
        text = html.read_text(encoding="utf-8")
        original = text

        # Sibling tools: ../pt/foo/ -> ../foo/
        text = text.replace('href="../pt/', 'href="../')

        for slug, en_label in TOOL_LABELS_EN.items():
            pt_label = TOOL_LABELS_PT[slug]
            if slug == "competitor-visibility-gap":
                # No PT page — link to EN tool from PT subpages
                text = text.replace(
                    f'href="../{slug}/"',
                    f'href="../../{slug}/"',
                )
            text = text.replace(
                f'class="hover:text-signal transition">{en_label}</a>',
                f'class="hover:text-signal transition">{pt_label}</a>',
            )

        if text != original:
            html.write_text(text, encoding="utf-8")
            print(f"updated related links: {html.relative_to(ROOT)}")


def fix_pt_hub_related_links() -> None:
    hub = PT_DIR / "index.html"
    text = hub.read_text(encoding="utf-8")
    for slug, en_label in TOOL_LABELS_EN.items():
        if slug not in ("website-roi-calculator", "whatsapp-qr-generator", "presence-score"):
            continue
        pt_label = TOOL_LABELS_PT[slug]
        text = text.replace(
            f'class="hover:text-signal transition">{en_label}</a>',
            f'class="hover:text-signal transition">{pt_label}</a>',
        )
    hub.write_text(text, encoding="utf-8")
    print("updated free-tools/pt/index.html related labels")


def write_website_roi_pt() -> None:
    path = PT_DIR / "website-roi-calculator" / "index.html"
    path.write_text(
        """<!DOCTYPE html>
<html lang="pt" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>Calculadora de ROI do Website — InfoWeb</title>
  <meta name="description" content="Calcule quanto rendimento um website profissional pode gerar para o seu negócio. Veja o retorno do investimento em segundos. Grátis, sem registo." />
  <meta name="keywords" content="calculadora roi website, calculadora investimento website, rendimento website, valor website, InfoWeb" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
  <meta name="author" content="InfoWeb by Sousa Dev" />
  <link rel="canonical" href="https://infoweb.sousadev.com/free-tools/pt/website-roi-calculator/" />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="InfoWeb" />
  <meta property="og:url" content="https://infoweb.sousadev.com/free-tools/pt/website-roi-calculator/" />
  <meta property="og:title" content="Calculadora de ROI do Website — InfoWeb" />
  <meta property="og:description" content="Calcule quanto rendimento um website profissional pode gerar para o seu negócio. Veja o ROI em segundos." />
  <meta property="og:image" content="https://infoweb.sousadev.com/assets/images/og-image.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:locale" content="pt_PT" />
  <meta property="og:locale:alternate" content="en_GB" />
  <link rel="alternate" hreflang="en" href="https://infoweb.sousadev.com/free-tools/website-roi-calculator/" />
  <link rel="alternate" hreflang="pt" href="https://infoweb.sousadev.com/free-tools/pt/website-roi-calculator/" />
  <link rel="alternate" hreflang="x-default" href="https://infoweb.sousadev.com/free-tools/website-roi-calculator/" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Calculadora de ROI do Website — InfoWeb" />
  <meta name="twitter:description" content="Calcule quanto rendimento um website profissional pode gerar para o seu negócio. Veja o ROI em segundos." />
  <meta name="twitter:image" content="https://infoweb.sousadev.com/assets/images/og-image.png" />

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "Calculadora de ROI do Website",
    "url": "https://infoweb.sousadev.com/free-tools/pt/website-roi-calculator/",
    "description": "Calcule quanto rendimento um website profissional pode gerar para o seu negócio. Veja o retorno do investimento em segundos.",
    "applicationCategory": "UtilityApplication",
    "operatingSystem": "Any",
    "offers": { "@type": "Offer", "price": "0", "priceCurrency": "EUR" },
    "author": { "@type": "Organization", "name": "InfoWeb", "url": "https://infoweb.sousadev.com" }
  }
  </script>

  <link rel="icon" type="image/png" href="../../../favicon_io/favicon-32x32.png" />
  <link rel="apple-touch-icon" href="../../../favicon_io/apple-touch-icon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet" />

  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    window.tailwind = window.tailwind || {};
    window.tailwind.config = {
      theme: {
        extend: {
          fontFamily: { sans: ['"Instrument Sans"', 'ui-sans-serif', 'system-ui'] },
          colors: { ink: '#020617', signal: '#d7b46a' }
        }
      }
    };
  </script>

  <link rel="stylesheet" href="../../../assets/css/free-tools-shared.css" />
  <link rel="stylesheet" href="../../website-roi-calculator/style.css" />

  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXQSMBERJM"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    gtag('js', new Date());
    gtag('config', 'G-XXQSMBERJM');
  </script>
  <script src="../../../assets/js/analytics.js" defer></script>

  <script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Início", "item": "https://infoweb.sousadev.com/" },
    { "@type": "ListItem", "position": 2, "name": "Ferramentas Gratuitas", "item": "https://infoweb.sousadev.com/free-tools/pt/" },
    { "@type": "ListItem", "position": 3, "name": "Calculadora de ROI do Website", "item": "https://infoweb.sousadev.com/free-tools/pt/website-roi-calculator/" }
  ]
}
  </script>
</head>
<body class="bg-slate-950 text-white font-sans antialiased">

  <header class="sticky top-0 z-50 bg-slate-950/90 backdrop-blur-xl border-b border-slate-800/60">
    <div class="max-w-2xl mx-auto px-4 py-3 flex items-center justify-between gap-3">
      <a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium=website_roi_calculator&utm_campaign=header"
         target="_blank" rel="noopener" aria-label="Início InfoWeb">
        <img src="../../../assets/images/infoweb-logo.png" alt="InfoWeb — websites geridos para pequenos negócios" class="h-9 w-auto" />
      </a>
      <div class="flex items-center gap-2 shrink-0">
        <nav class="flex items-center gap-1 text-[11px] font-semibold" aria-label="Idioma">
          <a href="../../website-roi-calculator/" hreflang="en" class="rounded-full px-2 py-1 text-slate-400 hover:text-white border border-transparent hover:border-slate-600 transition" data-track="language_switch" data-track-target="en" title="English">EN</a>
          <span class="rounded-full px-2 py-1 bg-slate-800 border border-slate-500 text-white" title="Português">PT</span>
        </nav>
        <a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium=website_roi_calculator&utm_campaign=header_btn#pricing"
           target="_blank" rel="noopener"
           class="text-sm font-semibold border border-slate-600 rounded-full px-4 py-1.5 hover:border-white hover:text-white text-slate-300 transition-all"
           data-track="header_cta_click">Ver planos</a>
      </div>
    </div>
  </header>

  <main class="max-w-2xl mx-auto px-4 py-12">

    <section class="text-center mb-10">
      <div class="inline-flex items-center gap-2 bg-green-500/10 border border-green-500/30 rounded-full px-4 py-1.5 text-sm font-semibold text-green-400 mb-5">
        <span class="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
        Grátis — sem registo
      </div>
      <h1 class="text-3xl sm:text-4xl font-bold leading-tight mb-4 text-white">
        Quanto Rendimento Pode um Website Trazer-lhe?
      </h1>
      <p class="text-slate-400 text-lg leading-relaxed">
        Calcule o potencial retorno do investimento de um website profissional. Veja quantos clientes novos pode atrair e quanto rendimento pode gerar.
      </p>
    </section>

    <section aria-labelledby="tool-input-heading" class="mb-6">
      <h2 id="tool-input-heading" class="sr-only">Entradas</h2>
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-5">

        <div>
          <label for="customer-value" class="block text-sm font-semibold text-slate-300 mb-2">
            Valor médio por cliente (€)
          </label>
          <input id="customer-value" type="number" min="1" placeholder="ex: 50"
            class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 transition-all" />
          <p class="text-xs text-slate-500 mt-1.5">Quanto gasta em média cada cliente?</p>
        </div>

        <div>
          <label for="monthly-visitors" class="block text-sm font-semibold text-slate-300 mb-2">
            Visitantes mensais esperados no website
          </label>
          <input id="monthly-visitors" type="number" min="1" placeholder="ex: 500"
            class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 transition-all" />
          <p class="text-xs text-slate-500 mt-1.5">Quantas pessoas podem visitar o site por mês?</p>
        </div>

        <div>
          <label for="conversion-rate" class="block text-sm font-semibold text-slate-300 mb-2">
            Taxa de conversão esperada (%)
          </label>
          <input id="conversion-rate" type="number" min="0.1" max="100" step="0.1" placeholder="ex: 2"
            class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 transition-all" />
          <p class="text-xs text-slate-500 mt-1.5">Que % de visitantes pode tornar-se cliente? (Média do setor: 1–3%)</p>
        </div>

        <div>
          <label for="website-cost" class="block text-sm font-semibold text-slate-300 mb-2">
            Investimento no website (€)
          </label>
          <input id="website-cost" type="number" min="1" placeholder="ex: 500"
            class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 transition-all" />
          <p class="text-xs text-slate-500 mt-1.5">Quanto investiria num website?</p>
        </div>

        <button id="btn-generate" type="button" onclick="runTool()"
          class="w-full bg-green-600 hover:bg-green-500 text-white font-bold rounded-xl px-6 py-4 transition-all focus:outline-none focus:ring-2 focus:ring-green-400 text-base">
          Calcular o meu ROI — É grátis
        </button>
      </div>
    </section>

    <section aria-labelledby="tool-output-heading" class="mb-10" id="output-section">
      <h2 id="tool-output-heading" class="sr-only">Resultado</h2>

      <div id="spinner" class="hidden flex-col items-center justify-center py-12 text-slate-400" aria-live="polite">
        <svg class="animate-spin h-8 w-8 mb-3 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
        </svg>
        <span>A calcular o seu ROI...</span>
      </div>

      <div id="error-box" class="hidden bg-red-900/30 border border-red-700/50 rounded-2xl p-5 text-center" role="alert">
        <p class="text-red-300 mb-3">Algo correu mal. Tente novamente dentro de momentos.</p>
        <button onclick="runTool()" class="text-sm underline text-red-400 hover:text-red-200">Tentar novamente</button>
      </div>

      <div id="result-box" class="hidden space-y-4">
        <div class="bg-slate-900 border border-green-500/30 rounded-2xl p-5">
          <div class="flex items-center gap-2 mb-3">
            <span class="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
            <p class="text-xs font-bold uppercase tracking-widest text-green-400">Os seus resultados</p>
          </div>

          <div class="grid grid-cols-2 gap-4 mb-4">
            <div class="bg-slate-800 rounded-xl p-4 text-center">
              <p class="text-2xl font-bold text-white mb-1" id="monthly-revenue">€0</p>
              <p class="text-xs text-slate-400">Rendimento mensal</p>
            </div>
            <div class="bg-slate-800 rounded-xl p-4 text-center">
              <p class="text-2xl font-bold text-white mb-1" id="annual-revenue">€0</p>
              <p class="text-xs text-slate-400">Rendimento anual</p>
            </div>
          </div>

          <div class="bg-slate-800 rounded-xl p-4 text-center mb-4">
            <p class="text-3xl font-bold text-green-400 mb-1" id="roi-percentage">0%</p>
            <p class="text-sm text-slate-400">Retorno do investimento</p>
          </div>

          <div class="bg-slate-800 rounded-xl p-4">
            <p class="text-sm text-slate-300 mb-2">Ponto de equilíbrio em: <span id="break-even" class="font-bold text-white">0 meses</span></p>
            <p class="text-sm text-slate-300">Novos clientes por mês: <span id="new-customers" class="font-bold text-white">0</span></p>
          </div>
        </div>

        <div class="bg-gradient-to-br from-slate-900 via-slate-900 to-ink border-2 border-signal/40 rounded-2xl p-6 text-center">
          <p class="text-signal mb-2 text-xs font-black uppercase tracking-[0.2em]">Pronto para começar?</p>
          <h3 class="text-xl font-bold text-white mb-3">Tenha um website profissional hoje</h3>
          <p class="text-slate-400 mb-4 text-sm">Junte-se a centenas de negócios que já crescem online com a InfoWeb.</p>
          <a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium=website_roi_calculator&utm_campaign=result_cta#pricing"
             target="_blank"
             class="inline-flex items-center gap-2 bg-green-600 hover:bg-green-500 text-white font-bold rounded-xl px-6 py-3 transition-all">
            Ver planos
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/>
            </svg>
          </a>
        </div>

        <p class="text-center">
          <button onclick="resetTool()" class="text-sm text-slate-500 hover:text-slate-300 underline transition-all">
            Calcular de novo
          </button>
        </p>
      </div>
    </section>

    <section class="mb-10">
      <h2 class="text-xl font-bold text-white mb-4">Perguntas frequentes</h2>
      <div class="space-y-3">
        <details class="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <summary class="font-semibold text-white cursor-pointer">Quão precisa é esta calculadora?</summary>
          <p class="text-slate-400 text-sm mt-2">Usa médias do setor. Os resultados reais variam consoante o tipo de negócio, localização e esforço de marketing.</p>
        </details>
        <details class="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <summary class="font-semibold text-white cursor-pointer">Qual é uma boa taxa de conversão?</summary>
          <p class="text-slate-400 text-sm mt-2">A média do setor é 1–3% na maioria dos negócios. E-commerce pode ver 2–5%; serviços B2B podem ver 5–10%.</p>
        </details>
        <details class="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <summary class="font-semibold text-white cursor-pointer">Como consigo mais visitantes no website?</summary>
          <p class="text-slate-400 text-sm mt-2">SEO, Google Ads, redes sociais e diretórios locais são formas eficazes de trazer tráfego ao seu site.</p>
        </details>
        <details class="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <summary class="font-semibold text-white cursor-pointer">Posso mesmo ganhar este valor?</summary>
          <p class="text-slate-400 text-sm mt-2">São estimativas com base nos seus dados. Muitos dos nossos clientes veem crescimento significativo nos primeiros 3–6 meses.</p>
        </details>
      </div>
    </section>

  </main>

  <section class="related-resources max-w-2xl mx-auto px-4 mb-8" aria-labelledby="related-tools-heading">
    <h2 id="related-tools-heading" class="text-sm font-bold uppercase tracking-wider text-slate-500 mb-3">Ferramentas relacionadas</h2>
    <ul class="flex flex-wrap gap-x-4 gap-y-2 text-sm text-slate-400">
      <li><a href="../break-even-calculator/" class="hover:text-signal transition">Calculadora de break-even</a></li>
      <li><a href="../customer-ltv-calculator/" class="hover:text-signal transition">Calculadora de LTV do cliente</a></li>
      <li><a href="../cost-per-lead-calculator/" class="hover:text-signal transition">Calculadora de custo por lead</a></li>
      <li><a href="../" class="hover:text-signal transition">Todas as ferramentas</a></li>
      <li><a href="https://infoweb.sousadev.com/blog/" class="hover:text-signal transition">Blog InfoWeb</a></li>
    </ul>
  </section>

  <footer class="border-t border-slate-800 py-6 text-center text-sm text-slate-500">
    <a href="../../../" class="text-slate-400 hover:text-white transition">← Início InfoWeb</a>
  </footer>

  <script src="../../../assets/js/free-tools-shared.js"></script>
  <script src="../../website-roi-calculator/script.js"></script>
</body>
</html>
""",
        encoding="utf-8",
    )
    print("wrote website-roi-calculator PT")


LOST_CUSTOMERS_REPLACEMENTS = [
    ("Lost Customers Cost Calculator — Free Tool by InfoWeb", "Calculadora de clientes perdidos — InfoWeb"),
    ('content="3 quick questions. Instant result. See exactly how much revenue you lose per week without a website — in euros."', 'content="3 perguntas rápidas. Resultado instantâneo. Veja quanto rendimento perde por semana sem website — em euros."'),
    ('"name": "Lost Customers Cost Calculator"', '"name": "Calculadora de clientes perdidos"'),
    ('"description": "Calcular how much revenue your small business loses per week and per month by not having a website. Free, instant, no sign-up required."', '"description": "Calcule quanto rendimento o seu negócio perde por semana e por mês por não ter website. Grátis, instantâneo, sem registo."'),
    ("Find Out How Much Your Business Loses Without a Website", "Saiba quanto o seu negócio perde sem website"),
    ("Answer 3 quick questions. Get an instant, honest estimate of the revenue slipping through your fingers every week.", "Responda a 3 perguntas rápidas. Obtenha uma estimativa honesta e instantânea do rendimento que perde todas as semanas."),
    ('class="sr-only" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);">Calculator</h2>', 'class="sr-only" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);">Calculadora</h2>'),
    ('aria-label="Calculator progress"', 'aria-label="Progresso da calculadora"'),
    (">Step 1 of 3</span>", ">Passo 1 de 3</span>"),
    (">Question 1 of 3</p>", ">Pergunta 1 de 3</p>"),
    ("What is the average spend per customer at your business?", "Qual é o gasto médio por cliente no seu negócio?"),
    ("E.g. €30 for a restaurant meal, €80 for a beauty treatment, €200 for a plumber call-out.", "Ex.: €30 por refeição num restaurante, €80 por tratamento de beleza, €200 por visita de canalizador."),
    ("Please enter a positive number.", "Introduza um número positivo."),
    ("Next →", "Seguinte →"),
    (">Question 2 of 3</p>", ">Pergunta 2 de 3</p>"),
    ("How many people contact you outside business hours or on weekends — and get no answer?", "Quantas pessoas o contactam fora do horário ou ao fim de semana — e não obtêm resposta?"),
    ("Per week. Include WhatsApp messages, missed calls, and emails you see the next morning.", "Por semana. Inclua mensagens WhatsApp, chamadas perdidas e emails que só vê na manhã seguinte."),
    ("Please enter 0 or more.", "Introduza 0 ou mais."),
    ("← Back", "← Voltar"),
    (">Question 3 of 3</p>", ">Pergunta 3 de 3</p>"),
    ("How many of those people give up and go to a competitor?", "Quantas dessas pessoas desistem e vão para um concorrente?"),
    ("Be honest — even 50% is common. If they don't hear back, they move on.", "Seja honesto — até 50% é comum. Se não obtêm resposta, seguem em frente."),
    ("Per week. Must be equal to or fewer than your answer in step 2.", "Por semana. Deve ser igual ou inferior à resposta do passo 2."),
    ("Calcular My Loss", "Calcular a minha perda"),
    (">Lost every week</p>", ">Perdido por semana</p>"),
    (">Lost every month</p>", ">Perdido por mês</p>"),
    ("Want the full breakdown?", "Quer o relatório completo?"),
    ("Get a detailed PDF sent to your email.", "Receba um PDF detalhado no seu email."),
    ("We'll include industry benchmarks, recovery strategies, and a website ROI estimate — all free.", "Incluímos benchmarks do setor, estratégias de recuperação e uma estimativa de ROI do website — tudo grátis."),
    ('placeholder="your@email.com"', 'placeholder="o.seu@email.pt"'),
    ('aria-label="Email address for full breakdown"', 'aria-label="Email para o relatório completo"'),
    ("Please enter a valid email address.", "Introduza um endereço de email válido."),
    ("Send me the full breakdown", "Enviar o relatório completo"),
    ("Check your inbox!", "Verifique a sua caixa de entrada!"),
    ("The full breakdown is on its way. Check your spam folder if you don't see it in a few minutes.", "O relatório completo está a caminho. Verifique o spam se não o vir em poucos minutos."),
    ("← Recalculate with different numbers", "← Calcular de novo com outros valores"),
    ("Stop losing money while you sleep", "Pare de perder dinheiro enquanto dorme"),
    ("Our website service fixes this for a fraction of that cost.", "O nosso serviço de websites resolve isto por uma fração desse custo."),
    ("InfoWeb builds, hosts, and maintains your site so customers can find you 24/7 — even while you sleep. Plans from €29 every 4 weeks.", "A InfoWeb cria, aloja e mantém o seu site para os clientes o encontrarem 24/7 — mesmo enquanto dorme. Planos desde €29 a cada 4 semanas."),
    ("Helping local businesses grow online since 2024.", "A ajudar negócios locais a crescer online desde 2024."),
    ("How much revenue does a small business lose without a website?", "Quanto rendimento perde um pequeno negócio sem website?"),
    ("It varies by industry, but research consistently shows that businesses without an online presence miss between 20% and 40% of potential customers — simply because they cannot be found or contacted outside business hours. For a business with an average transaction of €50 and just 5 missed customers per week, that is €250/week or €1,000/month in lost revenue. This calculator helps you put a real number on it.", "Varia por setor, mas estudos mostram que negócios sem presença online perdem entre 20% e 40% de clientes potenciais — simplesmente porque não são encontrados ou contactados fora do horário. Com transação média de €50 e 5 clientes perdidos por semana, são €250/semana ou €1.000/mês. Esta calculadora ajuda a quantificar."),
    ("Why do customers give up if I don't reply immediately?", "Porque é que os clientes desistem se não respondo de imediato?"),
    ("Studies show that 78% of customers buy from the business that responds first. When someone looks for a restaurant, clinic, or service provider and gets no answer, they simply move on to the next result on Google. A website with a contact form, booking system, or WhatsApp button means customers can act immediately — at 11 pm on a Sunday — without waiting for you to open.", "Estudos indicam que 78% dos clientes compram ao negócio que responde primeiro. Quem procura um restaurante, clínica ou serviço e não obtém resposta passa ao seguinte resultado no Google. Um website com formulário, marcações ou botão WhatsApp permite agir já — às 23h de domingo — sem esperar que abra."),
    ("Is a website really worth the cost for a small local business?", "Vale a pena um website para um pequeno negócio local?"),
    ("For most local businesses the maths is clear: if a managed website costs €29–€49 every 4 weeks and captures just one or two extra customers per month, it pays for itself many times over. Beyond direct revenue, a professional website builds trust, improves your Google visibility, and lets customers self-serve (booking, menus, prices) without calling you — saving you time too.", "Para a maioria dos negócios locais as contas são claras: se um website gerido custa €29–€49 a cada 4 semanas e traz um ou dois clientes extra por mês, paga-se muitas vezes. Além do rendimento direto, um site profissional gera confiança, melhora a visibilidade no Google e permite autoserviço (marcações, ementas, preços) sem telefonemas — poupando tempo."),
    ("How accurate is this calculator?", "Quão precisa é esta calculadora?"),
    ("The calculation is intentionally simple: weekly loss = average customer spend × number of customers who give up each week. It is a conservative floor estimate — it does not account for repeat customer lifetime value, referrals, or reviews lost. The real cost is likely higher. The purpose of this tool is to make the cost of inaction concrete and personal, not to be a precise financial forecast.", "O cálculo é propositadamente simples: perda semanal = gasto médio × clientes que desistem por semana. É uma estimativa conservadora — não inclui valor de vida do cliente, referências ou avaliações perdidas. O custo real é provavelmente maior. O objetivo é tornar o custo da inação concreto e pessoal, não uma previsão financeira exata."),
]


PRESENCE_SCORE_REPLACEMENTS = [
    ("Online Presence Score — Free Tool by InfoWeb", "Score de presença online — InfoWeb"),
    ('content="Answer 7 quick Yes/No questions and get your free online presence score out of 100. Instantly see your biggest gap and how to fix it — no sign-up required."', 'content="Responda a 7 perguntas Sim/Não e obtenha o seu score de presença online gratuito sobre 100. Veja o maior gap e como corrigir — sem registo."'),
    ('content="7 questions. 60 seconds. Get your free online presence score out of 100 and discover your #1 gap holding your business back."', 'content="7 perguntas. 60 segundos. Score gratuito sobre 100 e descubra o gap n.º 1 que limita o seu negócio."'),
    ('"name": "Online Presence Score Diagnostic"', '"name": "Diagnóstico de presença online"'),
    ('"description": "Answer 7 quick Yes/No questions and get your free online presence score out of 100. Instantly see your biggest gap and how to fix it."', '"description": "Responda a 7 perguntas Sim/Não e obtenha o score de presença online gratuito sobre 100. Veja o maior gap e como corrigir."'),
    ('"name": "Online Presence Score",\n      "item": "https://infoweb.sousadev.com/free-tools/pt/presence-score/"', '"name": "Score de presença online",\n      "item": "https://infoweb.sousadev.com/free-tools/pt/presence-score/"'),
    ("How Visible Is Your Business Online? Get Your Score in 60 Seconds", "Quão visível está o seu negócio online? Obtenha o score em 60 segundos"),
    ("7 Yes/No questions. Instant score out of 100. Find out your biggest weakness and what to fix first — completely free.", "7 perguntas Sim/Não. Score instantâneo sobre 100. Descubra a maior fraqueza e o que corrigir primeiro — totalmente grátis."),
    ('clip:rect(0,0,0,0);">Online Presence Quiz</h2>', 'clip:rect(0,0,0,0);">Questionário de presença online</h2>'),
    (">Question 1 of 7</span>", ">Pergunta 1 de 7</span>"),
    ('aria-label="Quiz progress"', 'aria-label="Progresso do questionário"'),
    ("<span aria-hidden=\"true\">✓</span> Yes", "<span aria-hidden=\"true\">✓</span> Sim"),
    ("<span aria-hidden=\"true\">✗</span> No", "<span aria-hidden=\"true\">✗</span> Não"),
    ("Tap an answer to advance — no wrong answers, just honesty helps.", "Toque numa resposta para avançar — não há respostas erradas, a honestidade ajuda."),
    ('clip:rect(0,0,0,0);">Your Presence Score</h2>', 'clip:rect(0,0,0,0);">O seu score de presença</h2>'),
    (">Your Online Presence Score</p>", ">O seu score de presença online</p>"),
    ('aria-label="Score ring"', 'aria-label="Anel de pontuação"'),
    (">Your primary opportunity</p>", ">A sua principal oportunidade</p>"),
    (">Full diagnostic breakdown</p>", ">Relatório diagnóstico completo</p>"),
    (">Unlock your full breakdown</p>", ">Desbloqueie o relatório completo</p>"),
    ("Enter your email below to see a question-by-question analysis sent straight to your inbox.", "Introduza o email abaixo para receber análise pergunta a pergunta na sua caixa de entrada."),
    (">Unlock your full report</p>", ">Desbloqueie o relatório completo</p>"),
    ("Get the question-by-question breakdown.", "Obtenha a análise pergunta a pergunta."),
    ("We'll also include tips to improve each weak area — all free, no spam.", "Incluímos dicas para melhorar cada área fraca — grátis, sem spam."),
    ('placeholder="your@email.com"', 'placeholder="o.seu@email.pt"'),
    ('aria-label="Email address for full diagnostic report"', 'aria-label="Email para o relatório diagnóstico completo"'),
    ("Please enter a valid email address.", "Introduza um endereço de email válido."),
    ("Something went wrong. Please try again.", "Algo correu mal. Tente novamente."),
    ("Unlock my full breakdown", "Desbloquear o relatório completo"),
    ("Check your inbox!", "Verifique a sua caixa de entrada!"),
    ("Your full diagnostic report is on its way. Check your spam folder if you don't see it.", "O relatório completo está a caminho. Verifique o spam se não o vir."),
    ("← Retake the quiz", "← Repetir o questionário"),
    ("Ready to score 100/100?", "Pronto para 100/100?"),
    ("We can take your score to 100/100 in less than a week — without the headaches.", "Podemos levar o seu score a 100/100 em menos de uma semana — sem dores de cabeça."),
    ("InfoWeb builds, hosts, and maintains your complete online presence for a flat subscription. No agencies, no surprises.", "A InfoWeb cria, aloja e mantém a sua presença online completa por subscrição fixa. Sem agências, sem surpresas."),
    ("Helping local businesses grow online since 2024.", "A ajudar negócios locais a crescer online desde 2024."),
    ("What is an online presence score for a small business?", "O que é um score de presença online para um pequeno negócio?"),
    ("An online presence score is a simple 0–100 rating that shows how visible and accessible your business is to customers online. It considers factors like Google ranking, having your own domain, your Google Business Profile, a service or menu page, online booking capability, website speed, and Google Maps listing. A low score means customers are struggling to find or contact you — and likely choosing a competitor instead.", "O score de presença online é uma classificação simples de 0 a 100 que mostra quão visível e acessível o seu negócio é online. Considera ranking no Google, domínio próprio, perfil Google Business, página de serviços ou ementa, marcações online, velocidade do site e listagem no Maps. Um score baixo significa que os clientes têm dificuldade em encontrá-lo — e provavelmente escolhem um concorrente."),
    ("How can I improve my Google ranking as a small business?", "Como posso melhorar o ranking no Google como pequeno negócio?"),
    ("The most effective steps for a local business are: complete your Google Business Profile with accurate hours, photos and categories; get a professional website on your own domain (.com or .pt); ensure your site loads quickly on mobile; and collect genuine customer reviews. Google favours businesses that look complete and trustworthy. A managed website from InfoWeb covers all of these in one subscription.", "Os passos mais eficazes: completar o perfil Google Business com horários, fotos e categorias corretas; ter um website profissional no seu domínio (.com ou .pt); garantir carregamento rápido no telemóvel; e recolher avaliações genuínas. O Google favorece negócios completos e credíveis. Um website gerido pela InfoWeb cobre tudo numa subscrição."),
    ("Is my business visible online if I only have a Facebook page?", "O meu negócio é visível online se só tiver página no Facebook?"),
    ("A Facebook page helps, but it is far from enough. Google does not give Facebook pages the same weight as a proper business website in search results. Customers who search for your service on Google will see competitors with websites ranked above you. You also have no control over your Facebook page — Meta can change the algorithm or restrict your reach at any time. A dedicated website on your own domain gives you full ownership of your online presence.", "Uma página Facebook ajuda, mas está longe de chegar. O Google não dá o mesmo peso a páginas Facebook que a um website profissional. Quem pesquisa no Google vê concorrentes com sites acima de si. Também não controla a página — a Meta pode alterar o algoritmo ou limitar o alcance. Um website no seu domínio dá-lhe controlo total da presença online."),
    ("How do I check if my business appears on Google Maps?", "Como verifico se o meu negócio aparece no Google Maps?"),
    ("Search Google Maps for your business name and location. If it does not appear, or if the information (address, phone, hours) is wrong, you need to claim and verify your Google Business Profile at business.google.com. Once verified, you can manage all your details directly. An incomplete or missing Maps listing means customers walking or driving nearby simply cannot find you — it is one of the fastest wins for any local business.", "Pesquise no Google Maps pelo nome e localização. Se não aparecer ou os dados estiverem errados, reivindique e verifique o perfil em business.google.com. Depois de verificado, gere tudo diretamente. Uma listagem incompleta no Maps significa que clientes perto não o encontram — é uma das vitórias mais rápidas para qualquer negócio local."),
]


def apply_replacements(path: Path, pairs: list[tuple[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        if old not in text:
            raise SystemExit(f"missing expected text in {path}: {old[:60]!r}...")
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    print(f"applied replacements: {path.relative_to(ROOT)}")


def fix_lost_customers_meta() -> None:
    path = PT_DIR / "lost-customers-calculator" / "index.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        'content="https://infoweb.sousadev.com/free-tools/lost-customers-calculator/"',
        'content="https://infoweb.sousadev.com/free-tools/pt/lost-customers-calculator/"',
    )
    text = text.replace(
        'href="https://infoweb.sousadev.com/free-tools/lost-customers-calculator/"',
        'href="https://infoweb.sousadev.com/free-tools/pt/lost-customers-calculator/"',
    )
    path.write_text(text, encoding="utf-8")


def fix_presence_score_meta() -> None:
    path = PT_DIR / "presence-score" / "index.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        'content="https://infoweb.sousadev.com/free-tools/presence-score/"',
        'content="https://infoweb.sousadev.com/free-tools/pt/presence-score/"',
    )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    import sys

    only = sys.argv[1:] if len(sys.argv) > 1 else []
    if not only or "roi" in only:
        write_website_roi_pt()
    if not only or "links" in only:
        fix_related_links_in_pt_tools()
        fix_pt_hub_related_links()
    if not only or "lost" in only:
        apply_replacements(PT_DIR / "lost-customers-calculator" / "index.html", LOST_CUSTOMERS_REPLACEMENTS)
        fix_lost_customers_meta()
    if not only or "presence" in only:
        apply_replacements(PT_DIR / "presence-score" / "index.html", PRESENCE_SCORE_REPLACEMENTS)
        fix_presence_score_meta()


if __name__ == "__main__":
    main()
