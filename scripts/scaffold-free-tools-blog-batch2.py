#!/usr/bin/env python3
"""Batch 2: five bilingual blog posts for remaining free tools."""

from __future__ import annotations

import importlib.util
import json
import textwrap
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
POSTS_DIR = REPO / "blog" / "posts"
DATE = "2026-06-05"

_scaffold_path = Path(__file__).resolve().parent / "scaffold-five-blog-posts.py"
_spec = importlib.util.spec_from_file_location("scaffold_five", _scaffold_path)
sf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sf)

BASE = sf.BASE_URL
TOOL_EN = f"{BASE}/free-tools"
TOOL_PT = f"{BASE}/free-tools/pt"

POSTS = [
    {
        "en_slug": "lost-revenue-small-business-guide",
        "pt_slug": "guia-receita-perdida-pequenos-negocios",
        "category": "small-business",
        "read_time": 8,
        "accent": "#f87171",
        "en": {
            "title": "How Much Revenue Are You Losing Without a Proper Website?",
            "description": "Estimate lost customers from missed calls, slow replies, and downtime — free calculators for small businesses.",
            "keywords": "lost customers calculator, missed calls revenue, website downtime cost, small business leaks",
            "image_alt": "Small business owner reviewing lost revenue from missed calls and website downtime",
            "image_scene": "red downward chart and phone missed-call icons on dark navy dashboard",
            "related": [
                ("Website ROI guide", "/blog/posts/website-roi-calculator-guide/"),
                ("Lost customers calculator", "/free-tools/lost-customers-calculator/"),
                ("Downtime cost calculator", "/free-tools/downtime-cost-calculator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # How Much Revenue Are You Losing Without a Proper Website?

                Leaks are rarely dramatic — they are missed calls, a site that will not load on 4G, and forms nobody answers until Monday.

                ## The three silent leaks

                1. **Missed phone calls** during service hours
                2. **No credible website** when people Google you after seeing social posts
                3. **Website downtime** during campaigns or busy weekends

                Each has a number attached if you are willing to estimate honestly.

                {{CTA:tools}}

                ## Model missed-call loss

                If you miss five calls a week and one in three would have bought a £80 job, that is roughly £650/month gone — before word of mouth.

                Use the [lost customers calculator]({TOOL_EN}/lost-customers-calculator/) with your real call volume, close rate, and average ticket.

                ## Price website outages

                Hosting failures during a promo weekend hurt more than the hosting bill. The [downtime cost calculator]({TOOL_EN}/downtime-cost-calculator/) turns hours offline into revenue at risk.

                Pair both numbers with the [website ROI calculator]({TOOL_EN}/website-roi-calculator/) to see if fixes pay back in weeks.

                {{CTA}}

                ## Fixes that stop the bleed

                - Click-to-call in the header on mobile
                - WhatsApp auto-reply with hours (see our [WhatsApp guide](/blog/posts/whatsapp-for-business-complete-guide/))
                - Uptime monitoring + managed hosting
                - [Website health scorecard]({TOOL_EN}/website-health-scorecard/) pass on mobile and SSL

                {{CTA:tools}}

                ## Takeaway

                Measure leaks quarterly. Fixing the biggest euro line beats chasing ten small marketing hacks.
                """
            ).strip(),
        },
        "pt": {
            "title": "Quanta Receita Está a Perder Sem um Website à Altura?",
            "description": "Estime clientes perdidos por chamadas perdidas, respostas lentas e downtime — calculadoras grátis para PME.",
            "keywords": "calculadora clientes perdidos, chamadas perdidas receita, custo downtime website, fugas receita pme",
            "image_alt": "Dono de PME a analisar receita perdida por chamadas e downtime do site",
            "image_scene": "gráfico vermelho descendente e ícones de chamada perdida em dashboard navy",
            "related": [
                ("Guia ROI do site", "/blog/posts/guia-calculadora-roi-website/"),
                ("Calculadora clientes perdidos", "/free-tools/pt/lost-customers-calculator/"),
                ("Calculadora custo downtime", "/free-tools/pt/downtime-cost-calculator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # Quanta Receita Está a Perder Sem um Website à Altura?

                As fugas são silenciosas: chamadas não atendidas, site que não abre no 4G e formulários sem resposta até segunda-feira.

                ## Três fugas comuns

                1. **Chamadas perdidas** em horário de serviço
                2. **Sem website credível** quando pesquisam no Google.pt
                3. **Site em baixo** em campanhas ou fins de semana movimentados

                {{CTA:tools}}

                ## Simule chamadas perdidas

                [Calculadora de clientes perdidos]({TOOL_PT}/lost-customers-calculator/) com volume real de chamadas, taxa de fecho e valor médio.

                ## Custo do downtime

                [Calculadora de custo de downtime]({TOOL_PT}/downtime-cost-calculator/) — horas offline em euros de receita em risco.

                Cruze com a [calculadora de ROI do site]({TOOL_PT}/website-roi-calculator/).

                {{CTA}}

                ## Correções rápidas

                - Clique-para-ligar no telemóvel
                - WhatsApp com horário ([guia WhatsApp](/blog/posts/whatsapp-para-negocios-guia-completo/))
                - [Avaliação de saúde do site]({TOOL_PT}/website-health-scorecard/)

                {{CTA:tools}}

                ## Conclusão

                Meça fugas trimestralmente. Corrigir a maior linha em euros compensa dezenas de micro-otimizações.
                """
            ).strip(),
        },
    },
    {
        "en_slug": "break-even-guide-small-business",
        "pt_slug": "guia-break-even-pequeno-negocio",
        "category": "small-business",
        "read_time": 8,
        "accent": "#4ade80",
        "en": {
            "title": "Break-Even Analysis for Small Businesses (Simple Guide)",
            "description": "Find how many sales you need to cover fixed costs and start making profit — free break-even calculator included.",
            "keywords": "break even calculator, break even analysis small business, fixed costs profit",
            "image_alt": "Break-even chart showing fixed costs and unit contribution for a small business",
            "image_scene": "break-even intersection chart in green and gold on dark background",
            "related": [
                ("Restaurant menu pricing", "/blog/posts/restaurant-menu-pricing-guide/"),
                ("Break-even calculator", "/free-tools/break-even-calculator/"),
                ("Markup vs margin calculator", "/free-tools/markup-margin-calculator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # Break-Even Analysis for Small Businesses (Simple Guide)

                Break-even is the sales volume where you stop losing money on operations — not where you get rich, but where survival turns into profit.

                ## What you need

                - **Fixed costs** per month (rent, salaries, software, insurance)
                - **Average selling price** per unit or job
                - **Variable cost** per sale (materials, commissions, payment fees)

                Contribution per sale = price − variable cost.  
                Break-even units = fixed costs ÷ contribution.

                {{CTA:tools}}

                ## Run the math instantly

                The [break-even calculator]({TOOL_EN}/break-even-calculator/) does the division and shows how many sales you need per month and per week.

                Example: €4,000 fixed costs, €120 price, €45 variable cost → €75 contribution → ~54 sales/month to break even.

                ## Connect to pricing

                If break-even units feel unrealistic, your margin is too thin. Use the [markup vs margin calculator]({TOOL_EN}/markup-margin-calculator/) to reset prices before cutting costs blindly.

                For Portugal-specific tax display on quotes, pair with the [IVA calculator]({TOOL_EN}/vat-calculator-pt/).

                {{CTA}}

                ## After break-even

                Target profit = break-even sales + extra units × contribution. Track monthly actuals vs the number — not just bank balance.

                {{CTA:tools}}

                ## Summary

                Break-even turns “are we okay?” into a countable answer. Update inputs when rent, wages, or supplier prices move.
                """
            ).strip(),
        },
        "pt": {
            "title": "Análise de Break-Even para Pequenos Negócios (Guia Simples)",
            "description": "Descubra quantas vendas precisa para cobrir custos fixos e lucrar — calculadora break-even grátis.",
            "keywords": "calculadora break even, ponto equilibrio pme, custos fixos lucro",
            "image_alt": "Gráfico break-even com custos fixos e contribuição unitária",
            "image_scene": "gráfico de interseção break-even verde e dourado",
            "related": [
                ("Preços de ementa", "/blog/posts/guia-precos-ementa-restaurante/"),
                ("Calculadora break-even", "/free-tools/pt/break-even-calculator/"),
                ("Calculadora margem markup", "/free-tools/pt/markup-margin-calculator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # Análise de Break-Even para Pequenos Negócios (Guia Simples)

                Break-even é o volume de vendas em que deixa de perder dinheiro na operação — sobrevivência antes de lucro confortável.

                ## Dados necessários

                - **Custos fixos** mensais (renda, salários, software)
                - **Preço médio** de venda
                - **Custo variável** por venda

                Contribuição = preço − variável.  
                Unidades break-even = fixos ÷ contribuição.

                {{CTA:tools}}

                ## Calcule já

                [Calculadora break-even]({TOOL_PT}/break-even-calculator/) — vendas por mês e por semana para equilibrar.

                ## Preços e margem

                [Calculadora margem vs markup]({TOOL_PT}/markup-margin-calculator/) se o número de vendas necessário for irrealista.

                [Calculadora IVA]({TOOL_PT}/vat-calculator-pt/) para orçamentos em Portugal.

                {{CTA}}

                {{CTA:tools}}

                ## Conclusão

                Atualize os inputs quando a renda ou fornecedores mudarem.
                """
            ).strip(),
        },
    },
    {
        "en_slug": "freelancer-hourly-rate-guide",
        "pt_slug": "guia-tarifa-horaria-freelancer",
        "category": "small-business",
        "read_time": 9,
        "accent": "#fbbf24",
        "en": {
            "title": "How to Set Your Freelancer Hourly Rate (Without Undercharging)",
            "description": "Calculate an hourly rate that covers costs, taxes, non-billable time, and profit — free freelancer rate calculator.",
            "keywords": "freelancer hourly rate calculator, how to price freelance work, freelance rate portugal",
            "image_alt": "Freelancer calculating hourly rate on laptop with invoice and time tracker",
            "image_scene": "clock, euro symbol and invoice stack on navy gold illustration",
            "related": [
                ("Break-even guide", "/blog/posts/break-even-guide-small-business/"),
                ("Freelancer rate calculator", "/free-tools/freelancer-rate-calculator/"),
                ("IVA Portugal guide", "/blog/posts/iva-vat-portugal-small-business/"),
            ],
            "content": textwrap.dedent(
                f"""
                # How to Set Your Freelancer Hourly Rate (Without Undercharging)

                Picking a rate from what competitors charge on LinkedIn is how skilled freelancers end up earning less than employed roles.

                ## Billable vs real hours

                You might sell 25 hours a week but work 40 when you include proposals, admin, and learning. Your rate must spread fixed costs across **billable** hours only.

                ## What the rate must cover

                1. Living and business costs (annual → monthly)
                2. Taxes and social contributions (reserve % — confirm with your accountant)
                3. Tools, insurance, hardware
                4. Profit buffer for slow months
                5. Non-billable time

                {{CTA:tools}}

                ## Use the calculator

                The [freelancer rate calculator]({TOOL_EN}/freelancer-rate-calculator/) backs into an hourly figure from desired take-home, costs, tax %, and billable hours per week.

                Sanity-check with the [break-even calculator]({TOOL_EN}/break-even-calculator/) if you also have studio rent or subcontractors.

                {{CTA}}

                ## Present prices confidently

                - Quote projects as fixed packages derived from hours × rate
                - Show IVA separately for PT clients with the [IVA calculator]({TOOL_EN}/vat-calculator-pt/)
                - Publish a simple services page — freelancers with websites close better deals ([see essentials in our cost guide](/blog/posts/small-business-website-cost/))

                {{CTA:tools}}

                ## Red flags you are too cheap

                - Every client accepts instantly
                - You skip contracts “to be nice”
                - No savings after a full year

                Raise in steps; existing clients on legacy rates can stay until renewal.

                ## Bottom line

                Your rate is a business model number, not a personality test. Calculate it, write it down, defend it with outcomes.
                """
            ).strip(),
        },
        "pt": {
            "title": "Como Definir a Sua Tarifa Horária de Freelancer (Sem Se Vender Barato)",
            "description": "Calcule uma tarifa horária que cubra custos, impostos, tempo não faturável e lucro — calculadora grátis.",
            "keywords": "calculadora tarifa freelancer, preço hora freelancer, freelance portugal",
            "image_alt": "Freelancer a calcular tarifa horária com fatura e registo de tempo",
            "image_scene": "relógio, euro e pilha de faturas em ilustração navy dourado",
            "related": [
                ("Guia break-even", "/blog/posts/guia-break-even-pequeno-negocio/"),
                ("Calculadora tarifa freelancer", "/free-tools/pt/freelancer-rate-calculator/"),
                ("Guia IVA Portugal", "/blog/posts/iva-portugal-guia-pequenos-negocios/"),
            ],
            "content": textwrap.dedent(
                f"""
                # Como Definir a Sua Tarifa Horária de Freelancer (Sem Se Vender Barato)

                Copiar valores do LinkedIn é como freelancers experientes ganham menos do que em emprego.

                ## Horas faturáveis vs reais

                Pode vender 25 horas/semana e trabalhar 40 com propostas e administração. A tarifa tem de cobrir só horas **faturáveis**.

                ## O que a tarifa deve incluir

                1. Custos de vida e negócio
                2. Impostos e contribuições (confirmar com contabilista)
                3. Ferramentas e seguros
                4. Margem para meses fracos
                5. Tempo não faturável

                {{CTA:tools}}

                ## Calculadora

                [Calculadora de tarifa freelancer]({TOOL_PT}/freelancer-rate-calculator/) — tarifa horária a partir do rendimento desejado, custos e % de impostos.

                Valide com [break-even]({TOOL_PT}/break-even-calculator/) se tiver renda de estúdio.

                {{CTA}}

                ## Apresente preços com IVA

                [Calculadora IVA]({TOOL_PT}/vat-calculator-pt/) em orçamentos a clientes em Portugal.

                {{CTA:tools}}

                ## Conclusão

                A tarifa é um número de modelo de negócio — calcule, documente, defenda com resultados.
                """
            ).strip(),
        },
    },
    {
        "en_slug": "markup-vs-margin-pricing-guide",
        "pt_slug": "guia-markup-vs-margem-precos",
        "category": "small-business",
        "read_time": 8,
        "accent": "#a78bfa",
        "en": {
            "title": "Markup vs Margin: Price Products Without Guessing",
            "description": "Learn the difference between markup and margin, avoid pricing mistakes, and use free calculators for retail and services.",
            "keywords": "markup vs margin, pricing calculator, profit margin small business",
            "image_alt": "Markup versus margin comparison chart for product pricing",
            "image_scene": "two bar charts labeled markup and margin with percent badges",
            "related": [
                ("Restaurant menu pricing", "/blog/posts/restaurant-menu-pricing-guide/"),
                ("Markup margin calculator", "/free-tools/markup-margin-calculator/"),
                ("Discount calculator", "/free-tools/discount-calculator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # Markup vs Margin: Price Products Without Guessing

                “50% markup” sounds great until you realize it is only 33% margin — and your rent still expects 40% margin to survive.

                ## Definitions in one minute

                - **Markup** = (price − cost) ÷ cost  
                - **Margin** = (price − cost) ÷ price  

                Same euro difference, different denominator — completely different story.

                {{CTA:tools}}

                ## Calculate selling price from target margin

                The [markup vs margin calculator]({TOOL_EN}/markup-margin-calculator/) takes cost + desired margin (or markup) and outputs price, profit per unit, and both percentages.

                Restaurants should also check plate economics with the [food cost calculator]({TOOL_EN}/food-cost-calculator/).

                ## Promotions without panic

                Before a sale, run the [discount calculator]({TOOL_EN}/discount-calculator/) to see net price and whether you still cover variable cost.

                {{CTA}}

                ## Rules of thumb by business type

                - **Retail shops:** track margin % per category, not store average only
                - **Trades:** quote labour + materials with margin on both
                - **SaaS/services:** high margin, low COGS — focus on LTV instead ([customer LTV calculator]({TOOL_EN}/customer-ltv-calculator/))

                {{CTA:tools}}

                ## Summary

                Pick margin targets, let calculators convert to price, document assumptions quarterly.
                """
            ).strip(),
        },
        "pt": {
            "title": "Markup vs Margem: Defina Preços Sem Adivinhar",
            "description": "Diferença entre markup e margem, erros comuns e calculadoras grátis para retalho e serviços.",
            "keywords": "markup vs margem, calculadora preços, margem lucro pme",
            "image_alt": "Comparação markup versus margem para preços de produtos",
            "image_scene": "dois gráficos de barras markup e margem com percentagens",
            "related": [
                ("Preços ementa restaurante", "/blog/posts/guia-precos-ementa-restaurante/"),
                ("Calculadora margem markup", "/free-tools/pt/markup-margin-calculator/"),
                ("Calculadora desconto", "/free-tools/pt/discount-calculator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # Markup vs Margem: Defina Preços Sem Adivinhar

                “50% de markup” parece ótimo até perceber que é só 33% de margem — e a renda ainda exige 40%.

                ## Definições

                - **Markup** = (preço − custo) ÷ custo  
                - **Margem** = (preço − custo) ÷ preço  

                {{CTA:tools}}

                ## Calculadora

                [Calculadora margem vs markup]({TOOL_PT}/markup-margin-calculator/) — preço de venda a partir do custo e margem alvo.

                Restauração: [custo alimentar]({TOOL_PT}/food-cost-calculator/).

                ## Promoções

                [Calculadora de desconto]({TOOL_PT}/discount-calculator/) antes de campanhas.

                {{CTA}}

                Serviços com margem alta: veja [LTV do cliente]({TOOL_PT}/customer-ltv-calculator/).

                {{CTA:tools}}

                ## Conclusão

                Defina margem alvo, use calculadoras para preço, reveja trimestralmente.
                """
            ).strip(),
        },
    },
    {
        "en_slug": "customer-lifetime-value-guide",
        "pt_slug": "guia-valor-vida-cliente-ltv",
        "category": "digital-marketing",
        "read_time": 9,
        "accent": "#38bdf8",
        "en": {
            "title": "Customer Lifetime Value (LTV) for Small Businesses",
            "description": "Calculate how much a repeat customer is worth and how much you can spend to acquire them — free LTV and CPL tools.",
            "keywords": "customer lifetime value, LTV calculator, cost per lead, small business marketing budget",
            "image_alt": "Customer lifetime value funnel diagram for small business marketing",
            "image_scene": "repeat customer loop arrows and euro LTV badge on dark dashboard",
            "related": [
                ("Website ROI guide", "/blog/posts/website-roi-calculator-guide/"),
                ("Customer LTV calculator", "/free-tools/customer-ltv-calculator/"),
                ("Cost per lead calculator", "/free-tools/cost-per-lead-calculator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # Customer Lifetime Value (LTV) for Small Businesses

                LTV answers: “How much is a loyal customer worth over a year?” That number sets your marketing budget, referral rewards, and how hard you fight churn.

                ## Simple LTV formula

                LTV ≈ average order value × purchase frequency per year × average customer lifespan (years)

                A café customer at €4 × 80 visits × 3 years ≈ €960 LTV — very different from a one-off €4 ticket.

                {{CTA:tools}}

                ## Calculate yours

                The [customer LTV calculator]({TOOL_EN}/customer-ltv-calculator/) models annual value and suggests a max acquisition cost (often ⅓ of LTV as a starting rule).

                Compare channels with the [cost-per-lead calculator]({TOOL_EN}/cost-per-lead-calculator/) — if cost per lead × close rate exceeds what LTV allows, that channel is underwater.

                {{CTA}}

                ## Improve LTV before buying more ads

                - Faster rebooking (email/WhatsApp reminders)
                - Loyalty perks that cost little margin
                - Service pages that sell the **next** visit
                - Track campaigns with the [UTM link builder]({TOOL_EN}/utm-link-builder/)

                Tie strategy back to [website ROI]({TOOL_EN}/website-roi-calculator/) — traffic without LTV thinking buys vanity clicks.

                {{CTA:tools}}

                ## Summary

                LTV turns retention into a number. Calculate it once per segment, revisit when prices or frequency shift.
                """
            ).strip(),
        },
        "pt": {
            "title": "Valor de Vida do Cliente (LTV) para Pequenos Negócios",
            "description": "Calcule quanto vale um cliente repetido e quanto pode gastar para o adquirir — ferramentas LTV e CPL grátis.",
            "keywords": "ltv cliente, valor vida cliente, calculadora ltv, custo por lead",
            "image_alt": "Diagrama de valor de vida do cliente para marketing de PME",
            "image_scene": "setas de cliente repetido e badge LTV em euros",
            "related": [
                ("Guia ROI website", "/blog/posts/guia-calculadora-roi-website/"),
                ("Calculadora LTV", "/free-tools/pt/customer-ltv-calculator/"),
                ("Calculadora custo por lead", "/free-tools/pt/cost-per-lead-calculator/"),
            ],
            "content": textwrap.dedent(
                f"""
                # Valor de Vida do Cliente (LTV) para Pequenos Negócios

                O LTV responde: “Quanto vale um cliente fiel num ano?” Define orçamento de marketing, referências e esforço de retenção.

                ## Fórmula simples

                LTV ≈ valor médio × frequência anual × anos como cliente

                Cliente de café a 4€ × 80 visitas × 3 anos ≈ 960€ de LTV.

                {{CTA:tools}}

                ## Calcule

                [Calculadora LTV]({TOOL_PT}/customer-ltv-calculator/) — valor anual e custo máximo de aquisição sugerido.

                Compare canais com [custo por lead]({TOOL_PT}/cost-per-lead-calculator/).

                {{CTA}}

                ## Melhore LTV antes de mais anúncios

                - Re-marcações rápidas
                - Benefícios de fidelização
                - Páginas de serviço que vendem a **próxima** visita
                - [Gerador UTM]({TOOL_PT}/utm-link-builder/)

                [ROI do site]({TOOL_PT}/website-roi-calculator/) — tráfego sem LTV compra cliques vazios.

                {{CTA:tools}}

                ## Conclusão

                Calcule LTV por segmento e reveja quando preços ou frequência mudarem.
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
    sf.DATE_DISPLAY_EN = "5 June 2026"
    sf.DATE_DISPLAY_PT = "5 junho 2026"

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
    print("Batch 2 done.")


if __name__ == "__main__":
    main()
