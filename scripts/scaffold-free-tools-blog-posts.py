#!/usr/bin/env python3
"""Scaffold bilingual blog posts that drive traffic to InfoWeb free tools."""

from __future__ import annotations

import importlib.util
import json
import textwrap
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
POSTS_DIR = REPO / "blog" / "posts"
DATE = "2026-05-27"

_scaffold_path = Path(__file__).resolve().parent / "scaffold-five-blog-posts.py"
_spec = importlib.util.spec_from_file_location("scaffold_five", _scaffold_path)
sf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sf)

BASE = sf.BASE_URL
TOOL_EN = f"{BASE}/free-tools"
TOOL_PT = f"{BASE}/free-tools/pt"


def t(en_path: str, pt_path: str | None = None) -> tuple[str, str]:
    pt_path = pt_path or en_path.replace("/free-tools/", "/free-tools/pt/")
    return (f"{BASE}{en_path}", f"{BASE}{pt_path}")


POSTS = [
    {
        "en_slug": "seo-title-meta-description-guide",
        "pt_slug": "guia-titulo-meta-description-seo",
        "category": "seo",
        "read_time": 9,
        "accent": "#34d399",
        "en": {
            "title": "SEO Title and Meta Description Guide for Small Business Websites",
            "description": "Write Google-friendly page titles and meta descriptions with the right length, keywords, and structure — plus free generators to draft them fast.",
            "keywords": "seo title tag, meta description, small business seo, page title length",
            "image_alt": "SEO title and meta description checklist on a laptop for a small business website",
            "image_scene": "search result snippet mockup with title and description highlighted in gold on dark navy",
            "related": [
                ("Local SEO checklist", "/blog/posts/local-seo-checklist-small-business/"),
                ("SEO meta generator (free tool)", "/free-tools/seo-meta-generator/"),
                ("Character counter for SEO", "/free-tools/character-counter/"),
            ],
            "content": textwrap.dedent(
                f"""
                # SEO Title and Meta Description Guide for Small Business Websites

                Your page title and meta description are the ad copy Google shows before anyone clicks. For a local shop, clinic, or freelancer, they decide whether searchers choose you or scroll past.

                ## What Google actually shows

                - **Title tag:** usually up to ~60 characters on desktop; keep the brand and main keyword early.
                - **Meta description:** often ~150–160 characters; not a direct ranking factor, but strongly affects click-through rate.

                If either is missing, Google writes its own — usually worse than what you would craft.

                {{CTA:tools}}

                ## Formula for a strong title

                1. Primary service or topic first
                2. Location if you serve a city (optional but powerful for local SEO)
                3. Brand at the end

                Examples:

                - `Emergency Plumber in Bristol | Fast Call-Out | Smith & Co`
                - `Brunch Menu & Specialty Coffee | Café Central`

                Avoid duplicate titles across pages. Every service page deserves its own title.

                ## Writing meta descriptions that earn clicks

                Answer three questions in one or two sentences:

                - What do you offer?
                - Who is it for?
                - What should they do next (call, book, view menu)?

                Use our [SEO character counter]({TOOL_EN}/character-counter/) while you draft so you stay inside the 160-character band.

                ## URL slugs matter too

                Clean paths help humans and search engines:

                - Good: `/services/boiler-repair`
                - Weak: `/page?id=384&type=svc`

                Turn headlines into slugs with the [URL slug generator]({TOOL_EN}/url-slug-generator/).

                ## Draft three options in seconds

                Stuck on wording? The [SEO title & meta generator]({TOOL_EN}/seo-meta-generator/) builds three title/description pairs from your business name and page topic — sized for Google, ready to copy.

                Pair that with [LocalBusiness schema]({TOOL_EN}/schema-local-business-generator/) so Google understands your name, address, and hours.

                {{CTA}}

                ## Common mistakes

                - Same title on every page
                - Keyword stuffing that reads like spam
                - Promising discounts you do not honor
                - Descriptions longer than 200 characters (gets truncated)

                ## Quick audit checklist

                1. Unique title + description on homepage and each service page
                2. Primary keyword in the first half of the title
                3. One clear CTA in the description
                4. Slug matches the page topic
                5. Schema markup on contact/location pages

                {{CTA:tools}}

                ## Bottom line

                Titles and meta tags are free leverage. Spend twenty minutes per important page, use the free tools to stay within limits, and measure clicks in Search Console monthly.
                """
            ).strip(),
        },
        "pt": {
            "title": "Guia de Título SEO e Meta Description para Websites de PME",
            "description": "Escreva títulos e meta descriptions amigáveis para o Google — comprimento certo, palavras-chave e estrutura, com geradores gratuitos InfoWeb.",
            "keywords": "titulo seo, meta description, seo pequenos negócios, comprimento titulo pagina",
            "image_alt": "Checklist de título SEO e meta description num portátil para website de PME",
            "image_scene": "snippet de resultado Google com título e descrição destacados a dourado em fundo navy",
            "related": [
                ("Checklist SEO local", "/blog/posts/checklist-seo-local-pequenos-negocios/"),
                ("Gerador meta SEO (ferramenta grátis)", "/free-tools/pt/seo-meta-generator/"),
                ("Contador de caracteres SEO", "/free-tools/pt/character-counter/"),
            ],
            "content": textwrap.dedent(
                f"""
                # Guia de Título SEO e Meta Description para Websites de PME

                O título da página e a meta description são o anúncio que o Google mostra antes de alguém clicar. Para uma loja, clínica ou freelancer em Portugal, decidem se o utilizador escolhe o seu negócio ou passa à frente.

                ## O que o Google mostra

                - **Title tag:** cerca de 60 caracteres no desktop; marca e palavra-chave no início.
                - **Meta description:** ~150–160 caracteres; influencia cliques, não é fator de ranking direto.

                Se faltar, o Google inventa — normalmente pior do que o que escreveria.

                {{CTA:tools}}

                ## Fórmula para um bom título

                1. Serviço ou tema principal primeiro
                2. Cidade ou região (`.pt` e pesquisa local em Portugal)
                3. Marca no final

                Exemplos:

                - `Canalizador de Urgência em Lisboa | Resposta Rápida | Silva & Filhos`
                - `Brunch e Café de Especialidade | Café Central`

                Cada página de serviço precisa de título único.

                ## Meta descriptions que geram cliques

                Responda em uma ou duas frases:

                - O que oferece?
                - Para quem é?
                - Próximo passo (ligar, marcar, ver ementa)?

                Use o [contador de caracteres SEO]({TOOL_PT}/character-counter/) para ficar dentro dos 160 caracteres.

                ## Slugs de URL limpos

                - Bom: `/servicos/reparacao-caldeiras`
                - Fraco: `/pagina?id=384`

                Gere slugs com o [gerador de slug URL]({TOOL_PT}/url-slug-generator/).

                ## Três opções em segundos

                O [gerador de título e meta SEO]({TOOL_PT}/seo-meta-generator/) cria três combinações a partir do nome do negócio e do tema da página.

                Complete com [schema LocalBusiness]({TOOL_PT}/schema-local-business-generator/) para horário e morada.

                {{CTA}}

                ## Erros comuns

                - Mesmo título em todas as páginas
                - Keyword stuffing ilegível
                - Descrições com mais de 200 caracteres (cortadas)

                {{CTA:tools}}

                ## Conclusão

                Títulos e meta tags são alavancagem gratuita. Vinte minutos por página importante, ferramentas grátis para respeitar limites, e revista cliques no Search Console todos os meses.
                """
            ).strip(),
        },
    },
    {
        "en_slug": "online-presence-score-guide",
        "pt_slug": "guia-score-presenca-online",
        "category": "seo",
        "read_time": 8,
        "accent": "#22d3ee",
        "en": {
            "title": "How to Check Your Business Online Presence Score",
            "description": "Score how findable your business is on Google, Maps, and your website — then compare against competitors with free InfoWeb tools.",
            "keywords": "online presence score, local business visibility, google maps listing, competitor comparison",
            "image_alt": "Online presence score gauge for a local business on a phone screen",
            "image_scene": "circular score meter and map pin icons on dark navy dashboard",
            "related": [
                ("Optimize Google Business Profile", "/blog/posts/optimize-google-business-profile/"),
                ("Local presence score (free tool)", "/free-tools/presence-score/"),
                ("Competitor visibility gap tool", "/free-tools/competitor-visibility-gap/"),
            ],
            "content": textwrap.dedent(
                f"""
                # How to Check Your Business Online Presence Score

                Being good at your trade is not the same as being easy to find online. Many strong local businesses lose calls because Google, Maps, or their website sends mixed signals.

                ## What “online presence” includes

                - Showing up for relevant searches
                - Accurate Google Business Profile / Maps listing
                - A website on your own domain
                - Fast mobile experience
                - Clear ways to book, call, or message

                ## Self-score in seven questions

                Our [local presence score tool]({TOOL_EN}/presence-score/) walks you through seven yes/no questions and returns a 0–100 score plus your biggest gap. No sign-up — takes about two minutes.

                Typical weak spots we see:

                1. No dedicated service pages
                2. Outdated hours on Google
                3. Slow mobile site
                4. Only social media, no owned website

                {{CTA:tools}}

                ## Compare against competitors

                Knowing your score is step one. Step two is context: are rivals stronger on reviews, website, or social proof?

                Use the [competitor visibility gap analyzer]({TOOL_EN}/competitor-visibility-gap/) to benchmark against up to two competitors and get an action list.

                {{CTA}}

                ## Fix the highest-impact gap first

                Do not try ten projects at once. Pick the single line item that unlocks calls:

                - **Not on Maps?** Claim and verify Google Business Profile.
                - **No website?** Launch a focused one-page site with phone, services, and proof.
                - **Slow site?** Run the [website health scorecard]({TOOL_EN}/website-health-scorecard/).

                ## Track monthly

                Re-run the presence quiz after changes. Scores should move within weeks when you fix fundamentals.

                {{CTA:tools}}

                ## Takeaway

                Treat online presence like inventory — measure it, compare it, improve the worst line first. The free tools give you a baseline without hiring an agency audit.
                """
            ).strip(),
        },
        "pt": {
            "title": "Como Avaliar o Score de Presença Online do Seu Negócio",
            "description": "Meça quão encontrável está o seu negócio no Google, Maps e website — e compare com concorrentes com ferramentas InfoWeb grátis.",
            "keywords": "presença online, score visibilidade, perfil empresa google, comparar concorrentes",
            "image_alt": "Medidor de presença online para negócio local no telemóvel",
            "image_scene": "medidor circular de score e ícones de mapa em dashboard navy",
            "related": [
                ("Otimizar Perfil da Empresa Google", "/blog/posts/otimizar-perfil-empresa-google/"),
                ("Score de presença local (ferramenta)", "/free-tools/pt/presence-score/"),
                ("Gap vs concorrentes", "/free-tools/pt/competitor-visibility-gap/"),
            ],
            "content": textwrap.dedent(
                f"""
                # Como Avaliar o Score de Presença Online do Seu Negócio

                Ser bom no ofício não é o mesmo que ser fácil de encontrar online. Muitas PME fortes em Portugal perdem contactos porque Google, Maps ou o site enviam sinais fracos.

                ## O que entra na “presença online”

                - Aparecer em pesquisas relevantes
                - Perfil Google Business / Maps correto
                - Website no domínio próprio (`.pt` ou `.com`)
                - Site rápido no telemóvel
                - Formas claras de marcar, ligar ou WhatsApp

                ## Autoavaliação em sete perguntas

                A ferramenta [pontuação de presença local]({TOOL_PT}/presence-score/) faz sete perguntas Sim/Não e devolve score 0–100 e o maior gap. Cerca de dois minutos, sem registo.

                {{CTA:tools}}

                ## Compare com concorrentes

                O [analizador de gap de visibilidade]({TOOL_PT}/competitor-visibility-gap/) compara até dois rivais em avaliações, web e redes.

                {{CTA}}

                ## Corrija o gap de maior impacto

                - **Maps incompleto?** Reivindique o perfil em business.google.com
                - **Sem site?** Lançe página com telefone, serviços e prova social
                - **Site lento?** Use a [avaliação de saúde do site]({TOOL_PT}/website-health-scorecard/)

                {{CTA:tools}}

                ## Conclusão

                Meça presença online como inventário: baseline grátis, um foco de melhoria de cada vez.
                """
            ).strip(),
        },
    },
    {
        "en_slug": "website-health-audit-small-business",
        "pt_slug": "auditoria-saude-website-pequeno-negocio",
        "category": "web-design",
        "read_time": 8,
        "accent": "#fb923c",
        "en": {
            "title": "Free Website Health Audit for Small Businesses",
            "description": "Run a five-point website health check — speed, mobile, SSL, meta tags, and Google Business — and estimate downtime cost if the site fails.",
            "keywords": "website health check, small business website audit, site speed test, ssl check",
            "image_alt": "Website health audit checklist with speed and mobile icons",
            "image_scene": "health score dashboard with green amber red indicators on dark background",
            "related": [
                ("Slow website guide", "/blog/posts/website-speed-small-business-guide/"),
                ("Website health scorecard (free)", "/free-tools/website-health-scorecard/"),
                ("Downtime cost calculator", "/free-tools/downtime-cost-calculator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # Free Website Health Audit for Small Businesses

                A website that looks fine on your laptop can still fail customers on mobile — slow, insecure, or invisible to Google.

                ## Five checks that matter

                1. **Mobile usability** — thumb-friendly layout and readable text
                2. **Load speed** — most visitors leave if the first screen takes more than a few seconds
                3. **HTTPS / SSL** — browsers warn on insecure sites; trust drops instantly
                4. **Title & meta tags** — each important page needs unique SEO labels
                5. **Google Business link** — site and profile should reinforce the same NAP data

                Run all five in the [website health scorecard]({TOOL_EN}/website-health-scorecard/). You get a 0–100 score and a prioritized fix list in the browser.

                {{CTA:tools}}

                ## What downtime actually costs

                Hosting outages and broken checkout forms are not abstract IT problems — they are lost revenue.

                Plug in your average daily sales and outage hours in the [downtime cost calculator]({TOOL_EN}/downtime-cost-calculator/) to see hourly, daily, and weekly bleed.

                {{CTA}}

                ## Fix order we recommend

                1. SSL and broken forms (blockers)
                2. Mobile layout on service pages
                3. Compress hero images
                4. Rewrite titles for top three pages — use the [SEO meta generator]({TOOL_EN}/seo-meta-generator/)
                5. Sync hours with Google Business Profile

                ## When to escalate

                If score stays below 60 after basics, consider managed hosting and maintenance so updates do not depend on you remembering plugins.

                {{CTA:tools}}

                ## Summary

                Audit quarterly. Small fixes compound into more calls and fewer “your site does not work” messages.
                """
            ).strip(),
        },
        "pt": {
            "title": "Auditoria Gratuita de Saúde do Website para PME",
            "description": "Checklist de cinco pontos — velocidade, mobile, SSL, meta tags e Google Business — e calculadora de custo de downtime.",
            "keywords": "auditoria website, saúde do site, velocidade site pme, verificar ssl",
            "image_alt": "Checklist de auditoria de saúde do website com ícones de velocidade",
            "image_scene": "painel de score de saúde com indicadores verde âmbar vermelho",
            "related": [
                ("Guia velocidade website", "/blog/posts/guia-velocidade-website-pequenos-negocios/"),
                ("Avaliação saúde do site", "/free-tools/pt/website-health-scorecard/"),
                ("Calculadora custo downtime", "/free-tools/pt/downtime-cost-calculator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # Auditoria Gratuita de Saúde do Website para PME

                Um site que parece bem no portátil pode falhar no telemóvel do cliente — lento, inseguro ou mal indexado no Google.pt.

                ## Cinco verificações essenciais

                1. **Mobile** — texto legível e botões clicáveis
                2. **Velocidade** — abandono rápido se a primeira ecrã demora
                3. **HTTPS** — avisos do browser destroem confiança
                4. **Title e meta** — páginas importantes com etiquetas únicas
                5. **Ligação ao Perfil Google** — NAP coerente

                Use a [avaliação de saúde do site]({TOOL_PT}/website-health-scorecard/) para score 0–100 e lista de correções.

                {{CTA:tools}}

                ## Custo real do downtime

                [Calculadora de custo de downtime]({TOOL_PT}/downtime-cost-calculator/) — receita perdida por horas offline.

                {{CTA}}

                ## Ordem de correção

                SSL e formulários → mobile → imagens → meta tags ([gerador SEO]({TOOL_PT}/seo-meta-generator/)) → horário no Google.

                {{CTA:tools}}

                ## Conclusão

                Audite trimestralmente. Pequenas correções reduzem chamadas perdidas e mensagens “o site não abre”.
                """
            ).strip(),
        },
    },
    {
        "en_slug": "website-roi-calculator-guide",
        "pt_slug": "guia-calculadora-roi-website",
        "category": "small-business",
        "read_time": 9,
        "accent": "#38bdf8",
        "en": {
            "title": "How to Calculate Website ROI for a Small Business",
            "description": "Estimate whether a website pays for itself using traffic, conversion rate, customer value, and payback period — with free calculators.",
            "keywords": "website roi calculator, small business website worth it, website payback period",
            "image_alt": "Website ROI calculation chart for small business revenue",
            "image_scene": "revenue curve and calculator icons on navy gold infographic",
            "related": [
                ("Website cost guide 2026", "/blog/posts/small-business-website-cost/"),
                ("Website ROI calculator", "/free-tools/website-roi-calculator/"),
                ("Customer LTV calculator", "/free-tools/customer-ltv-calculator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # How to Calculate Website ROI for a Small Business

                “Is a website worth it?” is really “Will enough qualified visitors convert often enough to cover the cost?”

                ## Inputs you need

                - Monthly website visitors (or realistic estimate after SEO)
                - Conversion rate (% who call, book, or buy)
                - Average revenue per sale or job
                - Monthly website cost (build + hosting + maintenance)

                ## Run the numbers

                The [website ROI calculator]({TOOL_EN}/website-roi-calculator/) models monthly and annual revenue from visitors × conversion × order value, then compares against cost.

                Rough example:

                - 800 visits/month
                - 3% convert → 24 leads
                - £120 average job → £2,880/month gross

                If the site costs £80/month all-in, payback is obvious. If conversion is 0.3%, fix the site before blaming the channel.

                {{CTA:tools}}

                ## Layer customer lifetime value

                One-off jobs understate ROI for repeat businesses (salons, clinics, B2B services). Use the [customer LTV calculator]({TOOL_EN}/customer-ltv-calculator/) to see what a loyal customer is worth over a year.

                ## Cost per lead sanity check

                Running ads? The [cost-per-lead calculator]({TOOL_EN}/cost-per-lead-calculator/) shows whether Google, Meta, or referrals deliver cheaper leads.

                {{CTA}}

                ## When ROI looks negative

                - No clear CTA above the fold
                - Slow mobile site
                - Thin service pages (bad for SEO)
                - Google Business Profile not linked

                Fix conversion before spending more on traffic.

                {{CTA:tools}}

                ## Decision rule

                If projected annual gross margin from web leads exceeds 3× annual site cost, invest in improvements. If not, diagnose with the health scorecard and presence score first.
                """
            ).strip(),
        },
        "pt": {
            "title": "Como Calcular o ROI de um Website para PME",
            "description": "Saiba se o website compensa com visitas, taxa de conversão, valor do cliente e período de retorno — calculadoras grátis InfoWeb.",
            "keywords": "roi website, calculadora roi site, website compensa pme, retorno investimento site",
            "image_alt": "Gráfico de cálculo ROI de website para receita de PME",
            "image_scene": "curva de receita e ícones de calculadora em infográfico navy dourado",
            "related": [
                ("Quanto custa um website", "/blog/posts/quanto-custa-website-pequena-empresa/"),
                ("Calculadora ROI do site", "/free-tools/pt/website-roi-calculator/"),
                ("Calculadora LTV", "/free-tools/pt/customer-ltv-calculator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # Como Calcular o ROI de um Website para PME

                “O website compensa?” resume-se a: visitantes qualificados convertem com frequência suficiente para cobrir o custo?

                ## Dados necessários

                - Visitas mensais (ou estimativa realista)
                - Taxa de conversão (% que liga, marca ou compra)
                - Valor médio por venda ou serviço
                - Custo mensal do site (hosting + manutenção)

                ## Simule

                A [calculadora de ROI do site]({TOOL_PT}/website-roi-calculator/) compara receita estimada com custo.

                Exemplo:

                - 600 visitas/mês
                - 3% conversão → 18 leads
                - 85€ valor médio → 1 530€/mês bruto

                Com site a 45€/mês, o retorno é claro. Com 0,3% conversão, corrija o site primeiro.

                {{CTA:tools}}

                ## Valor de vida do cliente

                [Calculadora LTV]({TOOL_PT}/customer-ltv-calculator/) para negócios com repetição (cabeleireiro, clínica, B2B).

                ## Custo por lead

                [Calculadora custo por lead]({TOOL_PT}/cost-per-lead-calculator/) para comparar canais de marketing.

                {{CTA}}

                {{CTA:tools}}

                ## Regra prática

                Se margem anual estimada de leads web > 3× custo anual do site, invista em melhorias. Caso contrário, use score de presença e auditoria de saúde.
                """
            ).strip(),
        },
    },
    {
        "en_slug": "smart-qr-codes-small-business",
        "pt_slug": "qr-codes-inteligentes-pequenos-negocios",
        "category": "digital-marketing",
        "read_time": 10,
        "accent": "#a78bfa",
        "en": {
            "title": "Smart QR Codes for Small Business Marketing",
            "description": "Use trackable QR codes for menus, WhatsApp, Wi-Fi, business cards, and any URL — with logos and editable destinations.",
            "keywords": "smart qr code generator, business qr code, qr code marketing, trackable qr",
            "image_alt": "Smart QR codes on menu tent, business card, and shop window",
            "image_scene": "multiple QR codes with scan analytics waves and logo center on cards",
            "related": [
                ("Restaurant menu QR guide", "/blog/posts/restaurant-menu-qr-code-guide/"),
                ("URL QR generator", "/free-tools/url-qr-generator/"),
                ("WhatsApp QR generator", "/free-tools/whatsapp-qr-generator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # Smart QR Codes for Small Business Marketing

                Static QR codes are fine for Wi-Fi passwords. For marketing links, you want **smart QR** — short URLs you can change later without reprinting.

                ## When to use smart QR

                - Menu PDF that updates seasonally
                - WhatsApp click-to-chat for orders
                - Google review collection
                - Campaign landing pages
                - Digital business cards

                ## Generic URL QR with analytics

                The [URL QR generator]({TOOL_EN}/url-qr-generator/) turns any link into a trackable code with optional centre logo. Change the destination after print if the campaign URL moves.

                {{CTA:tools}}

                ## WhatsApp and menu workflows

                Restaurants and retailers often pair:

                - [Menu QR generator]({TOOL_EN}/menu-qr-generator/) — upload PDF, brand colours, scan stats
                - [WhatsApp QR generator]({TOOL_EN}/whatsapp-qr-generator/) — pre-filled chat for orders

                See our [restaurant menu QR guide](/blog/posts/restaurant-menu-qr-code-guide/) for placement tips.

                ## Wi-Fi and business cards

                - **Guest Wi-Fi:** [Wi-Fi QR generator]({TOOL_EN}/wifi-qr-generator/) encodes join credentials (no typing passwords).
                - **Networking:** [Digital business card QR]({TOOL_EN}/business-card-qr/) saves your vCard in one scan.

                ## Placement ideas

                - Counter tent facing queue
                - Receipt footer
                - Vehicle magnet
                - Trade show badge

                Test scan distance and lighting before printing 500 stickers.

                {{CTA}}

                ## Measure what works

                Compare scan counts by location if your smart QR backend provides stats. Double down on placements that actually convert.

                {{CTA:tools}}

                ## Summary

                QR is not 2010 novelty — it is a bridge from offline to digital when the destination is mobile-friendly and trackable.
                """
            ).strip(),
        },
        "pt": {
            "title": "QR Codes Inteligentes para Marketing de PME",
            "description": "QR rastreáveis para ementa, WhatsApp, Wi-Fi, cartões de visita e URLs — com logótipo e destino editável.",
            "keywords": "gerador qr code, qr marketing, qr inteligente, qr whatsapp negócio",
            "image_alt": "QR codes inteligentes em ementa, cartão de visita e montra",
            "image_scene": "vários QR com ondas de analytics e logótipo ao centro",
            "related": [
                ("Guia QR ementa restaurante", "/blog/posts/guia-qr-code-menu-restaurante/"),
                ("Gerador QR URL", "/free-tools/pt/url-qr-generator/"),
                ("Gerador QR WhatsApp", "/free-tools/pt/whatsapp-qr-generator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # QR Codes Inteligentes para Marketing de PME

                QR estático serve para Wi-Fi. Para marketing, use **smart QR** — links curtos que pode alterar sem reimprimir.

                ## Quando usar smart QR

                - Ementa PDF sazonal
                - WhatsApp para encomendas
                - Pedido de avaliações Google
                - Landing pages de campanha
                - Cartão de visita digital

                ## QR para qualquer URL

                O [gerador de QR para URL]({TOOL_PT}/url-qr-generator/) cria código rastreável com logótipo opcional.

                {{CTA:tools}}

                ## Ementa e WhatsApp

                - [QR ementa]({TOOL_PT}/menu-qr-generator/)
                - [QR WhatsApp]({TOOL_PT}/whatsapp-qr-generator/)

                Guia completo: [QR code ementa](/blog/posts/guia-qr-code-menu-restaurante/).

                ## Wi-Fi e cartões

                - [QR Wi-Fi]({TOOL_PT}/wifi-qr-generator/)
                - [Cartão de visita QR]({TOOL_PT}/business-card-qr/)

                {{CTA}}

                {{CTA:tools}}

                ## Conclusão

                QR liga o físico ao digital quando o destino é rápido no telemóvel e mensurável.
                """
            ).strip(),
        },
    },
    {
        "en_slug": "restaurant-menu-pricing-guide",
        "pt_slug": "guia-precos-ementa-restaurante",
        "category": "small-business",
        "read_time": 9,
        "accent": "#f97316",
        "en": {
            "title": "Restaurant Menu Pricing: Food Cost, Margins, and Tips",
            "description": "Price dishes with food cost %, markup, and tip splitting — plus a digital menu QR customers actually use.",
            "keywords": "restaurant food cost, menu pricing calculator, plate margin, tip split calculator",
            "image_alt": "Restaurant owner calculating menu prices and food cost percentage",
            "image_scene": "menu clipboard, calculator, and plate cost percentage chart",
            "related": [
                ("Restaurant menu QR guide", "/blog/posts/restaurant-menu-qr-code-guide/"),
                ("Food cost calculator", "/free-tools/food-cost-calculator/"),
                ("Markup margin calculator", "/free-tools/markup-margin-calculator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # Restaurant Menu Pricing: Food Cost, Margins, and Tips

                Underpriced mains erase profit on drinks. Overpriced specials sit unsold. You need simple math before redesigning the menu.

                ## Target food cost %

                Many full-service restaurants aim for **28–35% food cost** (ingredient cost ÷ menu price). Fast casual may run lower; fine dining higher on premium ingredients.

                Use the [food cost calculator]({TOOL_EN}/food-cost-calculator/) per dish: enter ingredient total and menu price, see food cost % and a suggested price for a 30% target.

                {{CTA:tools}}

                ## Markup vs margin

                “50% markup” is not the same as “50% margin.” Confusing them wipes margin.

                The [markup vs margin calculator]({TOOL_EN}/markup-margin-calculator/) converts cost + desired margin into selling price.

                ## Splitting tips fairly

                Pool tips across front-of-house? The [tip & bill split calculator]({TOOL_EN}/tip-split-calculator/) divides bill + tip % by headcount for staff payouts or customer transparency.

                ## Publish the menu where guests look

                Paper costs add up. A [menu QR code]({TOOL_EN}/menu-qr-generator/) lets you update PDFs without reprinting — pair with the [menu QR guide](/blog/posts/restaurant-menu-qr-code-guide/).

                {{CTA}}

                ## Weekly routine

                1. Recalculate food cost on top 10 sellers when supplier prices move
                2. Flag any dish above 40% food cost
                3. Review discount promos with the [discount calculator]({TOOL_EN}/discount-calculator/) before campaigns

                {{CTA:tools}}

                ## Bottom line

                Price from data, not gut — then make the menu easy to scan on mobile.
                """
            ).strip(),
        },
        "pt": {
            "title": "Preços de Ementa: Custo Alimentar, Margens e Gorjetas",
            "description": "Defina preços com % custo alimentar, markup e divisão de gorjetas — e ementa digital em QR.",
            "keywords": "custo alimentar restaurante, preços ementa, margem prato, calculadora gorjeta",
            "image_alt": "Restaurador a calcular preços de ementa e percentagem custo alimentar",
            "image_scene": "ementa, calculadora e gráfico de custo alimentar",
            "related": [
                ("Guia QR ementa", "/blog/posts/guia-qr-code-menu-restaurante/"),
                ("Calculadora custo alimentar", "/free-tools/pt/food-cost-calculator/"),
                ("Calculadora margem markup", "/free-tools/pt/markup-margin-calculator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # Preços de Ementa: Custo Alimentar, Margens e Gorjetas

                Pratos baratos demais comem a margem das bebidas. Especiais caros encalham. Precisa de números simples antes de redesenhar a ementa.

                ## Percentagem alvo de custo alimentar

                Muitos restaurantes em Portugal visam **28–35%** (custo ingredientes ÷ preço menu).

                [Calculadora custo alimentar]({TOOL_PT}/food-cost-calculator/) por prato — vê % e preço sugerido para alvo 30%.

                {{CTA:tools}}

                ## Markup vs margem

                [Calculadora margem vs markup]({TOOL_PT}/markup-margin-calculator/) — não confunda os dois.

                ## Gorjetas

                [Gorjeta e divisão de conta]({TOOL_PT}/tip-split-calculator/) para equipa ou transparência ao cliente.

                ## Ementa digital

                [QR ementa]({TOOL_PT}/menu-qr-generator/) — atualize PDF sem reimprimir tudo.

                {{CTA}}

                ## Rotina semanal

                Recalcule os 10 pratos mais vendidos quando fornecedores sobem preços. Campanhas com [calculadora de desconto]({TOOL_PT}/discount-calculator/).

                {{CTA:tools}}

                ## Conclusão

                Preço com dados; depois torne a ementa fácil de ler no telemóvel.
                """
            ).strip(),
        },
    },
    {
        "en_slug": "iva-vat-portugal-small-business",
        "pt_slug": "iva-portugal-guia-pequenos-negocios",
        "category": "small-business",
        "read_time": 8,
        "accent": "#facc15",
        "en": {
            "title": "IVA (VAT) in Portugal: Quick Guide for Small Businesses",
            "description": "Add or remove IVA for Continente, Madeira, and Azores rates — and model discounts and break-even with free calculators.",
            "keywords": "iva portugal calculator, vat portugal, madeira azores iva, small business tax portugal",
            "image_alt": "IVA VAT calculation for Portugal small business invoice",
            "image_scene": "euro invoice with IVA percentage badges for mainland and islands",
            "related": [
                ("Website cost guide", "/blog/posts/small-business-website-cost/"),
                ("IVA calculator Portugal", "/free-tools/vat-calculator-pt/"),
                ("Break-even calculator", "/free-tools/break-even-calculator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # IVA (VAT) in Portugal: Quick Guide for Small Businesses

                Quoting the wrong IVA rate erodes margin or surprises customers at checkout. Portugal has different rates by region and category.

                ## Rates you will see most

                - **Standard (Continente):** commonly 23% on many goods/services
                - **Madeira / Azores:** reduced regional rates apply — always confirm current tables
                - **Intermediate / reduced:** food, books, and specific sectors (check official lists)

                This is not tax advice — verify with your accountant. For quick math, use the [IVA / VAT calculator]({TOOL_EN}/vat-calculator-pt/) to add or remove tax for each region.

                {{CTA:tools}}

                ## Show prices clearly on your website

                B2C sites should state whether displayed prices include IVA. Ambiguity creates support calls and cart abandonment.

                ## Promotions and net margin

                Before a sale, run the [discount calculator]({TOOL_EN}/discount-calculator/) to see net price and savings message for ads.

                ## Cover fixed costs

                IVA collected is not profit. Pair pricing work with the [break-even calculator]({TOOL_EN}/break-even-calculator/) to know how many sales cover rent, wages, and software.

                {{CTA}}

                ## Freelancers billing hourly

                If you invoice time, the [freelancer rate calculator]({TOOL_EN}/freelancer-rate-calculator/) backs into an hourly rate that includes tax, costs, and profit target.

                {{CTA:tools}}

                ## Summary

                Use calculators for speed, accountants for compliance — then publish transparent pricing online.
                """
            ).strip(),
        },
        "pt": {
            "title": "IVA em Portugal: Guia Rápido para Pequenos Negócios",
            "description": "Adicione ou retire IVA (Continente, Madeira, Açores) e simule descontos e break-even com calculadoras grátis.",
            "keywords": "calculadora iva, iva madeira açores, iva pme portugal, preços com iva",
            "image_alt": "Cálculo de IVA para fatura de PME em Portugal",
            "image_scene": "fatura em euros com badges de IVA continente e ilhas",
            "related": [
                ("Quanto custa um website", "/blog/posts/quanto-custa-website-pequena-empresa/"),
                ("Calculadora IVA Portugal", "/free-tools/pt/vat-calculator-pt/"),
                ("Calculadora break-even", "/free-tools/pt/break-even-calculator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # IVA em Portugal: Guia Rápido para Pequenos Negócios

                Orçamentos com IVA errado comem margem ou surpreendem o cliente. Em Portugal as taxas variam por região e setor.

                ## Taxas mais comuns

                - **Continente:** taxa normal (ex.: 23% em muitos bens/serviços — confirmar tabela em vigor)
                - **Madeira / Açores:** taxas regionais
                - **Reduzida / intermédia:** alimentação, livros, setores específicos

                Não é aconselhamento fiscal — confirme com o contabilista. Para contas rápidas: [calculadora de IVA]({TOOL_PT}/vat-calculator-pt/).

                {{CTA:tools}}

                ## Preços no website

                Indique se os preços mostrados incluem IVA. Evita chamadas e abandono de carrinho.

                ## Promoções

                [Calculadora de desconto]({TOOL_PT}/discount-calculator/) antes de campanhas.

                ## Custos fixos

                IVA cobrado não é lucro. [Calculadora break-even]({TOOL_PT}/break-even-calculator/) para saber quantas vendas cobrem renda e salários.

                {{CTA}}

                ## Freelancers

                [Calculadora tarifa horária]({TOOL_PT}/freelancer-rate-calculator/) com impostos e custos incluídos.

                {{CTA:tools}}

                ## Conclusão

                Calculadoras para velocidade, contabilista para conformidade, site com preços transparentes.
                """
            ).strip(),
        },
    },
    {
        "en_slug": "utm-campaign-tracking-guide",
        "pt_slug": "guia-rastrear-campanhas-utm",
        "category": "digital-marketing",
        "read_time": 7,
        "accent": "#0ea5e9",
        "en": {
            "title": "UTM Parameters: Track Marketing Campaigns That Actually Convert",
            "description": "Tag URLs with utm_source, utm_medium, and utm_campaign so Google Analytics shows which ads, emails, and posts drive leads.",
            "keywords": "utm builder, utm parameters guide, campaign tracking url, google analytics utm",
            "image_alt": "UTM campaign URL builder dashboard for marketing tracking",
            "image_scene": "browser address bar with utm parameters highlighted in gold",
            "related": [
                ("WhatsApp for business guide", "/blog/posts/whatsapp-for-business-complete-guide/"),
                ("UTM link builder (free)", "/free-tools/utm-link-builder/"),
                ("Cost per lead calculator", "/free-tools/cost-per-lead-calculator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # UTM Parameters: Track Marketing Campaigns That Actually Convert

                If every link in your bio, flyer, and email is identical, analytics cannot tell you what worked.

                ## The three required fields

                - `utm_source` — where traffic comes from (`facebook`, `newsletter`, `flyer`)
                - `utm_medium` — channel type (`social`, `email`, `cpc`)
                - `utm_campaign` — specific push (`spring-menu`, `black-friday`)

                Optional: `utm_content` for A/B variants, `utm_term` for paid keywords.

                Build clean URLs with the [UTM link builder]({TOOL_EN}/utm-link-builder/) — copies a full tagged link in one click.

                {{CTA:tools}}

                ## Naming conventions

                Use lowercase, hyphens, no spaces:

                - Good: `utm_campaign=summer-lunch-2026`
                - Bad: `utm_campaign=Post #3!!!`

                Document names in a spreadsheet so the team stays consistent.

                ## Tie to lead cost

                Once campaigns run, compare channel efficiency with the [cost-per-lead calculator]({TOOL_EN}/cost-per-lead-calculator/).

                {{CTA}}

                ## Common mistakes

                - Tagging only homepage while ads land on service pages (split data)
                - Changing campaign names mid-flight (breaks history)
                - Forgetting UTMs on QR destinations — add them to smart QR target URLs

                {{CTA:tools}}

                ## Summary

                UTMs take five minutes per campaign and save blind budget decisions later.
                """
            ).strip(),
        },
        "pt": {
            "title": "Parâmetros UTM: Rastrear Campanhas que Convertem",
            "description": "Etiquete URLs com utm_source, utm_medium e utm_campaign para o Analytics mostrar que anúncios e emails geram leads.",
            "keywords": "utm parametros, gerador utm, rastrear campanhas, google analytics utm",
            "image_alt": "Construtor de links UTM para rastrear campanhas de marketing",
            "image_scene": "barra de URL com parâmetros UTM destacados a dourado",
            "related": [
                ("Guia WhatsApp negócios", "/blog/posts/whatsapp-para-negocios-guia-completo/"),
                ("Gerador links UTM", "/free-tools/pt/utm-link-builder/"),
                ("Calculadora custo por lead", "/free-tools/pt/cost-per-lead-calculator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # Parâmetros UTM: Rastrear Campanhas que Convertem

                Se todos os links na bio, flyer e newsletter forem iguais, o Analytics não diz o que funcionou.

                ## Três campos obrigatórios

                - `utm_source` — origem (`facebook`, `newsletter`, `flyer`)
                - `utm_medium` — tipo (`social`, `email`, `cpc`)
                - `utm_campaign` — campanha (`ementa-verao`, `black-friday`)

                Opcional: `utm_content`, `utm_term`.

                [Gerador de links UTM]({TOOL_PT}/utm-link-builder/) — URL etiquetada pronta a copiar.

                {{CTA:tools}}

                ## Convenções

                Minúsculas, hífens, sem espaços. Registe nomes numa folha partilhada.

                ## Custo por lead

                [Calculadora custo por lead]({TOOL_PT}/cost-per-lead-calculator/) para comparar canais.

                {{CTA}}

                {{CTA:tools}}

                ## Conclusão

                Cinco minutos por campanha evitam orçamento às cegas.
                """
            ).strip(),
        },
    },
]


def update_posts_index(post_date: str) -> None:
    index_path = POSTS_DIR / "metadata.json"
    existing = json.loads(index_path.read_text(encoding="utf-8"))
    seen = {(e["slug"], e.get("language", "en")) for e in existing.get("posts", [])}
    posts = list(existing.get("posts", []))
    for spec in POSTS:
        for slug, lang in ((spec["en_slug"], "en"), (spec["pt_slug"], "pt")):
            key = (slug, lang)
            if key in seen:
                continue
            posts.append(
                {
                    "slug": slug,
                    "language": lang,
                    "dateCreated": post_date,
                    "dateUpdated": post_date,
                }
            )
            seen.add(key)
    posts.sort(key=lambda p: (p["dateCreated"], p["slug"]), reverse=True)
    payload = {
        "posts": posts,
        "lastUpdated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }
    index_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def append_sitemap() -> None:
    sitemap = REPO / "sitemap.xml"
    text = sitemap.read_text(encoding="utf-8")
    block: list[str] = []
    for spec in POSTS:
        for slug in (spec["en_slug"], spec["pt_slug"]):
            url = f"{BASE}/blog/posts/{slug}/"
            if url in text:
                continue
            block.extend(
                [
                    "  <url>",
                    f"    <loc>{url}</loc>",
                    "    <changefreq>monthly</changefreq>",
                    "    <priority>0.7</priority>",
                    "  </url>",
                ]
            )
    if block:
        text = text.replace("</urlset>", "\n".join(block) + "\n</urlset>")
        sitemap.write_text(text, encoding="utf-8")


def main() -> None:
    sf.DATE = DATE
    sf.DATE_DISPLAY_EN = "27 May 2026"
    sf.DATE_DISPLAY_PT = "27 maio 2026"

    for spec in POSTS:
        category = spec["category"]
        read_time = spec["read_time"]
        accent = spec["accent"]
        for lang, slug_key, alt_key in (
            ("en", "en_slug", "pt_slug"),
            ("pt", "pt_slug", "en_slug"),
        ):
            slug = spec[slug_key]
            alt_slug = spec[alt_key]
            data = spec[lang]
            post_dir = POSTS_DIR / slug
            assets = post_dir / "assets"
            assets.mkdir(parents=True, exist_ok=True)

            (post_dir / "content.md").write_text(data["content"] + "\n", encoding="utf-8")
            sf.write_metadata(slug, lang, data, alt_slug, category, read_time, DATE)
            sf.write_image_prompt(slug, lang, data)
            sf.write_index_html(slug, lang, data, alt_slug, category, read_time, DATE)
            sf.generate_featured_image(
                assets / "featured.png",
                data["title"],
                accent=accent,
                category=category,
                slug=slug,
            )
            print(f"  {slug}")

    update_posts_index(DATE)
    append_sitemap()
    print("Done — index and sitemap updated.")


if __name__ == "__main__":
    main()
