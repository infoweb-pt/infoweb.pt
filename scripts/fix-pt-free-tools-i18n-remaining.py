#!/usr/bin/env python3
"""Additional PT translations for free tools not covered by fix-pt-free-tools-i18n.py."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PT = ROOT / "free-tools" / "pt"


def apply(path: Path, pairs: list[tuple[str, str]], *, strict: bool = True) -> None:
    text = path.read_text(encoding="utf-8")
    missing = []
    for old, new in pairs:
        if old not in text:
            missing.append(old[:80])
            continue
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    print(f"ok: {path.relative_to(ROOT)}" + (f" ({len(missing)} skipped)" if missing else ""))
    if strict and missing:
        raise SystemExit(f"missing in {path}: {missing[0]!r}...")


LOST_FAQ_JSON = [
    (
        '"text": "It varies by industry, but businesses without an online presence miss between 20% and 40% of potential customers. For a business with an average transaction of €50 and just 5 missed customers per week, that is €250/week or €1,000/month in lost revenue."',
        '"text": "Varia por setor, mas negócios sem presença online perdem entre 20% e 40% de clientes potenciais. Com transação média de €50 e 5 clientes perdidos por semana, são €250/semana ou €1.000/mês."',
    ),
    (
        '"text": "Studies show that 78% of customers buy from the business that responds first. When someone gets no answer, they move on to the next result on Google. A website with a booking system or contact form means customers can act immediately — even at 11 pm on a Sunday."',
        '"text": "Estudos indicam que 78% dos clientes compram ao negócio que responde primeiro. Quem não obtém resposta passa ao seguinte resultado no Google. Um website com marcações ou formulário permite agir de imediato — mesmo às 23h de domingo."',
    ),
    (
        '"text": "For most local businesses the maths is clear: if a managed website costs €29–€49 every 4 weeks and captures just one or two extra customers per month, it pays for itself many times over. Beyond direct revenue, a professional website builds trust and improves Google visibility."',
        '"text": "Para a maioria dos negócios locais as contas são claras: um website gerido a €29–€49 a cada 4 semanas que traga um ou dois clientes extra por mês paga-se muitas vezes. Além do rendimento, um site profissional gera confiança e melhora a visibilidade no Google."',
    ),
    (
        '"text": "The calculation is simple: weekly loss = average customer spend × number of customers who give up each week. It is a conservative floor estimate — the real cost including lifetime value and referrals is likely higher."',
        '"text": "O cálculo é simples: perda semanal = gasto médio × clientes que desistem por semana. É uma estimativa conservadora — o custo real, incluindo valor de vida e referências, é provavelmente maior."',
    ),
]

PRESENCE_FAQ_JSON = [
    (
        '"text": "An online presence score is a simple 0–100 rating that shows how visible and accessible your business is to customers online. It considers Google ranking, domain ownership, Google Business Profile completeness, a service page, online booking, website speed, and Google Maps listing."',
        '"text": "O score de presença online é uma classificação de 0 a 100 que mostra quão visível e acessível o negócio é online. Considera ranking no Google, domínio, perfil Google Business, página de serviços, marcações, velocidade do site e Maps."',
    ),
    (
        '"text": "The most effective steps are: complete your Google Business Profile; get a professional website on your own domain; ensure your site loads quickly on mobile; and collect genuine customer reviews. Google favours businesses that look complete and trustworthy."',
        '"text": "Os passos mais eficazes: completar o perfil Google Business; ter website profissional no seu domínio; carregamento rápido no telemóvel; e recolher avaliações genuínas. O Google favorece negócios completos e credíveis."',
    ),
    (
        '"text": "A Facebook page helps, but is far from enough. Google does not give Facebook pages the same weight as a proper business website in search results. A dedicated website on your own domain gives you full ownership and better search visibility."',
        '"text": "Uma página Facebook ajuda, mas não chega. O Google não dá o mesmo peso a páginas Facebook que a um website profissional. Um site no seu domínio dá controlo total e melhor visibilidade na pesquisa."',
    ),
    (
        '"text": "Search Google Maps for your business name and location. If it doesn\'t appear, claim and verify your Google Business Profile at business.google.com. An incomplete or missing Maps listing means local customers simply cannot find you."',
        '"text": "Pesquise no Google Maps pelo nome e localização. Se não aparecer, reivindique o perfil em business.google.com. Uma listagem incompleta no Maps significa que clientes perto não o encontram."',
    ),
]

GOOGLE_REVIEW = [
    ("Free Google Review Link Generator — InfoWeb", "Gerador gratuito de link para avaliações Google — InfoWeb"),
    (
        'content="Create a direct Google review link for your business in seconds. Get more 5-star reviews with one click. No sign-up needed."',
        'content="Crie um link direto para avaliações Google do seu negócio em segundos. Mais avaliações 5 estrelas com um clique. Sem registo."',
    ),
    ('content="https://infoweb.sousadev.com/free-tools/google-review-generator/"', 'content="https://infoweb.sousadev.com/free-tools/pt/google-review-generator/"'),
    ('href="https://infoweb.sousadev.com/free-tools/google-review-generator/"', 'href="https://infoweb.sousadev.com/free-tools/pt/google-review-generator/"'),
    ('"name": "Free Google Review Link Generator"', '"name": "Gerador de link para avaliações Google"'),
    (
        '"description": "Create a direct Google review link for your business in seconds. Get more 5-star reviews with one click."',
        '"description": "Crie um link direto para avaliações Google em segundos. Mais avaliações 5 estrelas com um clique."',
    ),
    ("Get More Google Reviews — Instantly", "Mais avaliações Google — de imediato"),
    (
        "Create a direct link that takes customers straight to your Google review page. No searching, no friction — just more 5-star reviews.",
        "Crie um link direto que leva os clientes à página de avaliação Google. Sem pesquisas, sem fricção — mais avaliações 5 estrelas.",
    ),
    ("Business Name", "Nome do negócio"),
    ("Google Place ID", "Google Place ID"),
    ("(optional — for direct link)", "(opcional — para link direto)"),
    ("Find your Place ID", "Encontrar o Place ID"),
    ("or leave blank for a Google Maps search link", "ou deixe em branco para um link de pesquisa no Google Maps"),
    ("Suggested review text", "Texto de avaliação sugerido"),
    ("(optional — copy yourself; not added to the link)", "(opcional — copie manualmente; não entra no link)"),
    ('placeholder="Great service! Highly recommended."', 'placeholder="Excelente serviço! Recomendo."'),
    (
        "Google does not support prefilled review text in URLs. After the review page opens, paste this text (or use Copiar suggested text in your results).",
        "O Google não permite texto pré-preenchido nos URLs. Depois de abrir a página de avaliação, cole este texto (ou use «Copiar texto sugerido» nos resultados).",
    ),
    ("Live QR preview", "Pré-visualização do QR"),
    ("PREVIEW", "PRÉ-VIS."),
    ("Encodes your review link after you generate", "Codifica o link de avaliação depois de gerar"),
    ("Customize your QR", "Personalizar o QR"),
    ("QR color", "Cor do QR"),
    ('placeholder="e.g., Leave a review"', 'placeholder="ex.: Deixe uma avaliação"'),
    ("Generate Review Link — It's Free", "Gerar link de avaliação — Grátis"),
    ("Generating your review link…", "A gerar o link de avaliação…"),
    ("Your Review Link", "O seu link de avaliação"),
    ("Test link", "Testar link"),
    ("Suggested review (paste after the page opens)", "Avaliação sugerida (cole depois de abrir a página)"),
    ("Copiar suggested text", "Copiar texto sugerido"),
    ("QR Code for Reviews", "QR Code para avaliações"),
    (
        '<p class="text-xs text-slate-500 mb-4 text-center">Your QR is in <strong class="text-slate-400">Live QR preview</strong> above — customize there, then download.</p>',
        '<p class="text-xs text-slate-500 mb-4 text-center">O QR está na <strong class="text-slate-400">pré-visualização</strong> acima — personalize aí e descarregue.</p>',
    ),
    ("Download QR Code", "Descarregar QR Code"),
    ("Generate a new one", "Gerar outro"),
    ("Is this really free?", "É mesmo grátis?"),
    ("Yes! Generate as many review links as you need. No credit card required.", "Sim! Gere quantos links precisar. Sem cartão de crédito."),
    ("What is a Google Place ID?", "O que é um Google Place ID?"),
    (
        "It's a unique identifier for your business on Google Maps. You can find it using Google's Place ID finder.",
        "É o identificador único do negócio no Google Maps. Pode encontrá-lo na ferramenta Place ID do Google.",
    ),
    ("Can I use this without a Place ID?", "Posso usar sem Place ID?"),
    (
        "Without a Place ID we use a Google Maps search link (<code class=\"text-slate-500\">maps/search/?api=1</code>) so customers can pick your listing.",
        "Sem Place ID usamos um link de pesquisa no Google Maps (<code class=\"text-slate-500\">maps/search/?api=1</code>) para o cliente escolher a ficha.",
    ),
    ("How do I get more reviews?", "Como obter mais avaliações?"),
    (
        "Share your link via WhatsApp, email, or print the QR code on receipts and business cards.",
        "Partilhe o link por WhatsApp, email ou imprima o QR em recibos e cartões de visita.",
    ),
]

MENU_QR = [
    ("Free Menu QR Code Generator for Restaurants — InfoWeb", "Gerador gratuito de QR Code para ementa — InfoWeb"),
    (
        'content="Create a free QR code for your restaurant menu in seconds. Upload your PDF or image, customize colors, add your logo, and track leituras. No sign-up needed."',
        'content="Crie um QR Code grátis para a ementa em segundos. Carregue PDF ou imagem, personalize cores, adicione logótipo e acompanhe leituras. Sem registo."',
    ),
    (
        'content="Create a free QR code for your restaurant menu. Upload PDF, customize, add logo, track leituras. No sign-up."',
        'content="QR Code grátis para ementa. Carregue PDF, personalize, adicione logótipo, acompanhe leituras. Sem registo."',
    ),
    ('"name": "Free Menu QR Code Generator"', '"name": "Gerador de QR Code para ementa"'),
    (
        '"description": "Create a free QR code for your restaurant menu in seconds. Upload your PDF or image, customize colors, add your logo, and track leituras."',
        '"description": "Crie um QR Code grátis para a ementa em segundos. Carregue PDF ou imagem, personalize cores, adicione logótipo e acompanhe leituras."',
    ),
    ("Free Menu QR Code for Your Restaurant", "QR Code grátis para a ementa do restaurante"),
    (
        "Upload your menu PDF or image, customize your QR code with colors and logo, and start tracking leituras. Perfect for restaurants, cafés, and bars.",
        "Carregue o PDF ou imagem da ementa, personalize o QR com cores e logótipo e acompanhe leituras. Ideal para restaurantes, cafés e bares.",
    ),
    ("Your Menu", "A sua ementa"),
    ("Click to upload PDF or image", "Clique para carregar PDF ou imagem"),
    ("Max 10MB. PDF, JPG, or PNG.", "Máx. 10MB. PDF, JPG ou PNG."),
    ("Restaurant Name", "Nome do restaurante"),
    ("Live Preview", "Pré-visualização"),
    ("Scan to see example menu page", "Leia para ver página de ementa de exemplo"),
    ("Customize Your QR Code", "Personalizar o QR Code"),
    ("QR Color", "Cor do QR"),
    ("Dot Style", "Estilo dos pontos"),
    ("Frame Text (optional)", "Texto da moldura (opcional)"),
    ('placeholder="e.g., Scan for Menu"', 'placeholder="ex.: Leia para ver ementa"'),
    ("Generate Menu QR Code — It's Free", "Gerar QR da ementa — Grátis"),
    ("Generating your menu QR…", "A gerar o QR da ementa…"),
    ("Your Menu QR Code", "O seu QR da ementa"),
    ("Download QR Code", "Descarregar QR Code"),
    ("Generate a new one", "Gerar outro"),
    ("Is this really free?", "É mesmo grátis?"),
    ("Yes! Generate as many menu QR codes as you need. No credit card required.", "Sim! Gere quantos QR de ementa precisar. Sem cartão de crédito."),
]

BUSINESS_CARD = [
    ("Free Digital Business Card QR Generator — InfoWeb", "Gerador gratuito de cartão de visita digital em QR — InfoWeb"),
    (
        'content="Create a digital business card with QR code. Share your contact info instantly. No app needed. Free and easy to use."',
        'content="Crie um cartão de visita digital com QR Code. Partilhe contactos de imediato. Sem app. Grátis e fácil."',
    ),
    ('content="https://infoweb.sousadev.com/free-tools/business-card-qr/"', 'content="https://infoweb.sousadev.com/free-tools/pt/business-card-qr/"'),
    ('href="https://infoweb.sousadev.com/free-tools/business-card-qr/"', 'href="https://infoweb.sousadev.com/free-tools/pt/business-card-qr/"'),
    ('"name": "Free Digital Business Card QR Generator"', '"name": "Cartão de visita digital em QR"'),
    (
        '"description": "Create a digital business card with QR code. Share your contact info instantly. No app needed."',
        '"description": "Cartão de visita digital com QR Code. Partilhe contactos de imediato. Sem app."',
    ),
    ("Your Digital Business Card — With QR Code", "O seu cartão de visita digital — com QR Code"),
    (
        "Create a digital business card that anyone can save with one scan. No paper, no apps — just instant contact sharing.",
        "Crie um cartão de visita digital que qualquer pessoa guarda com uma leitura. Sem papel, sem apps — contactos na hora.",
    ),
    ("Full Name *", "Nome completo *"),
    ("Job Title", "Cargo"),
    ('placeholder="e.g., Restaurant Owner"', 'placeholder="ex.: Dono de restaurante"'),
    ("Company", "Empresa"),
    ("Phone", "Telefone"),
    ("Website", "Website"),
    ("Encodes your vCard after you generate", "Codifica o vCard depois de gerar"),
    ("Customize your QR", "Personalizar o QR"),
    ("QR color", "Cor do QR"),
    ("Generate Digital Card — It's Free", "Gerar cartão digital — Grátis"),
    ("Generating your digital card…", "A gerar o cartão digital…"),
    ("Your Digital Card", "O seu cartão digital"),
    ("Download vCard (.vcf)", "Descarregar vCard (.vcf)"),
    ("Create a new card", "Criar novo cartão"),
    ("How do people save my contact?", "Como guardam o meu contacto?"),
    (
        "They scan the QR with their phone camera. iPhone and Android open a contact card they can save in one tap.",
        "Leem o QR com a câmara. iPhone e Android abrem um cartão de contacto para guardar com um toque.",
    ),
    ("What is a vCard?", "O que é um vCard?"),
    (
        "A standard file format (.vcf) for contact information. It works across phones and email apps.",
        "Formato standard (.vcf) para contactos. Funciona em telemóveis e apps de email.",
    ),
]

WIFI_QR = [
    ("Wi‑Fi QR Code Generator for Your Business", "Gerador de QR Code Wi‑Fi para o seu negócio"),
    (
        "Guests scan once and join your Wi‑Fi — no typing passwords. Works on iPhone and Android. Raw Wi‑Fi QR (not a redirect link).",
        "Os clientes leem uma vez e ligam-se ao Wi‑Fi — sem escrever palavras-passe. Funciona em iPhone e Android. QR Wi‑Fi nativo (não é link de redirecionamento).",
    ),
    ('placeholder="Your Wi‑Fi password"', 'placeholder="A sua palavra-passe Wi‑Fi"'),
    (
        "Use type “text” so special characters paste correctly. Never share this page publicly with a sensitive password.",
        "Tipo «text» para caracteres especiais colarem bem. Não partilhe esta página publicamente com palavra-passe sensível.",
    ),
    ('placeholder="e.g. Scan for Wi‑Fi"', 'placeholder="ex.: Leia para Wi‑Fi"'),
    ("Generate Wi‑Fi QR — It’s Free", "Gerar QR Wi‑Fi — Grátis"),
]

MARKUP_MARGIN = [
    ("Free Markup vs Margin Calculator — InfoWeb", "Calculadora margem vs markup — InfoWeb"),
    (
        'content="Convert between markup % and margin %, or set a target margin and get your selling price from cost. Free calculator for shops, restaurants and freelancers."',
        'content="Converta entre markup % e margem %, ou defina margem alvo e obtenha preço de venda a partir do custo. Grátis para lojas, restaurantes e freelancers."',
    ),
    ('"name": "Free Markup vs Margin Calculator"', '"name": "Calculadora margem vs markup"'),
    ("Markup vs Margin Calculator", "Calculadora margem vs markup"),
    (
        "<strong class=\"text-slate-300\">Margin</strong> is profit ÷ selling price.\n        <strong class=\"text-slate-300\">Markup</strong> is profit ÷ cost.\n        Use this to price products, menus or services without mixing them up.",
        "<strong class=\"text-slate-300\">Margem</strong> é lucro ÷ preço de venda.\n        <strong class=\"text-slate-300\">Markup</strong> é lucro ÷ custo.\n        Use isto para definir preços de produtos, ementas ou serviços sem confundir.",
    ),
    ('class="sr-only">Inputs</h2>', 'class="sr-only">Entradas</h2>'),
    ("What do you know?", "O que sabe?"),
    ("Target margin %", "Margem alvo %"),
    ("I have cost and the margin I want on the sale.", "Tenho o custo e a margem que quero na venda."),
    ("Markup % on cost", "Markup % sobre o custo"),
    ("I add a percentage on top of my cost.", "Acrescento uma percentagem ao custo."),
    ("Selling price", "Preço de venda"),
    ("I already know what I charge — show me margin and markup.", "Já sei o que cobro — mostre margem e markup."),
    ("Cost (€)", "Custo (€)"),
    ("Enter a cost greater than zero.", "Introduza um custo superior a zero."),
    ("Target margin (%)", "Margem alvo (%)"),
    ('class="sr-only">Results</h2>', 'class="sr-only">Resultados</h2>'),
    (">Results</p>", ">Resultados</p>"),
    (">Cost</span>", ">Custo</span>"),
    (">Selling price</span>", ">Preço de venda</span>"),
    (">Gross profit</span>", ">Lucro bruto</span>"),
    (">Margin (of price)</span>", ">Margem (do preço)</span>"),
    (">Markup (on cost)</span>", ">Markup (sobre custo)</span>"),
    (
        "<strong class=\"text-slate-400\">Margin</strong> = (price − cost) ÷ price.\n          <strong class=\"text-slate-400\">Markup</strong> = (price − cost) ÷ cost.",
        "<strong class=\"text-slate-400\">Margem</strong> = (preço − custo) ÷ preço.\n          <strong class=\"text-slate-400\">Markup</strong> = (preço − custo) ÷ custo.",
    ),
    ("What is the difference between markup and margin?", "Qual é a diferença entre markup e margem?"),
    (
        "Both compare profit to something else. Markup compares profit to your cost. Margin compares profit to the final selling price. A 50% markup is not the same as a 50% margin.",
        "Ambos comparam lucro a algo diferente. Markup compara lucro ao custo. Margem compara lucro ao preço final. 50% de markup não é 50% de margem.",
    ),
    ("How do I get a selling price from a target margin?", "Como obtenho preço de venda a partir de margem alvo?"),
    (
        'Choose “Target margin %”, enter your cost and desired margin. We compute price as cost ÷ (1 − margin), which is the standard gross-margin pricing formula.',
        'Escolha «Margem alvo %», introduza custo e margem desejada. Calculamos preço = custo ÷ (1 − margem), a fórmula standard de margem bruta.',
    ),
    ("Does this include VAT or taxes?", "Inclui IVA ou impostos?"),
    (
        "No — enter cost and price consistently (both excluding VAT or both including VAT). For Portuguese IVA math, use our <a href=\"../vat-calculator-pt/\" class=\"text-amber-400 underline hover:text-amber-300\">IVA calculator (Portugal)</a>.",
        "Não — introduza custo e preço de forma consistente (com ou sem IVA). Para IVA em Portugal, use a nossa <a href=\"../vat-calculator-pt/\" class=\"text-amber-400 underline hover:text-amber-300\">calculadora de IVA</a>.",
    ),
    ("Is this financial advice?", "Isto é aconselhamento financeiro?"),
    (
        "This is a quick educational calculator. For tax, payroll and formal accounts, speak to a qualified accountant.",
        "Calculadora educativa rápida. Para impostos, salários e contas formais, fale com um contabilista certificado.",
    ),
]


def fix_hreflang_en_urls() -> None:
    """Ensure hreflang=en on PT pages points to EN tool URL, not PT."""
    for html in PT.glob("*/index.html"):
        text = html.read_text(encoding="utf-8")
        slug = html.parent.name
        wrong = f'hreflang="en" href="https://infoweb.sousadev.com/free-tools/pt/{slug}/"'
        right = f'hreflang="en" href="https://infoweb.sousadev.com/free-tools/{slug}/"'
        if wrong in text:
            text = text.replace(wrong, right)
            html.write_text(text, encoding="utf-8")
            print(f"fixed hreflang en: {html.relative_to(ROOT)}")


def fix_lost_hreflang() -> None:
    path = PT / "lost-customers-calculator" / "index.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '<link rel="alternate" hreflang="en" href="https://infoweb.sousadev.com/free-tools/pt/lost-customers-calculator/" />',
        '<link rel="alternate" hreflang="en" href="https://infoweb.sousadev.com/free-tools/lost-customers-calculator/" />',
    )
    path.write_text(text, encoding="utf-8")
    print("ok: lost-customers hreflang en")


def main() -> None:
    apply(PT / "lost-customers-calculator" / "index.html", LOST_FAQ_JSON, strict=False)
    apply(PT / "presence-score" / "index.html", PRESENCE_FAQ_JSON, strict=False)
    apply(PT / "google-review-generator" / "index.html", GOOGLE_REVIEW, strict=False)
    apply(PT / "menu-qr-generator" / "index.html", MENU_QR, strict=False)
    apply(PT / "business-card-qr" / "index.html", BUSINESS_CARD, strict=False)
    apply(PT / "wifi-qr-generator" / "index.html", WIFI_QR, strict=False)
    apply(PT / "markup-margin-calculator" / "index.html", MARKUP_MARGIN, strict=False)
    fix_lost_hreflang()
    fix_hreflang_en_urls()


if __name__ == "__main__":
    main()
