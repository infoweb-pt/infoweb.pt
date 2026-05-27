#!/usr/bin/env python3
"""Scaffold five bilingual blog post pairs for InfoWeb."""

from __future__ import annotations

import json
import textwrap
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[1]
POSTS_DIR = REPO / "blog" / "posts"
BASE_URL = "https://infoweb.sousadev.com"
DATE = "2026-05-27"
DATE_DISPLAY_EN = "27 May 2026"
DATE_DISPLAY_PT = "27 maio 2026"

CATEGORY_SECTION = {
    "seo": {"en": "SEO", "pt": "SEO"},
    "digital-marketing": {"en": "Digital Marketing", "pt": "Marketing Digital"},
    "small-business": {"en": "Small Business", "pt": "Pequenos Negócios"},
    "web-design": {"en": "Web Design", "pt": "Web Design"},
}

POSTS = [
    {
        "en_slug": "get-more-google-reviews-small-business",
        "pt_slug": "como-conseguir-mais-avaliacoes-google",
        "category": "digital-marketing",
        "read_time": 8,
        "accent": "#fbbf24",
        "en": {
            "title": "How to Get More Google Reviews for Your Small Business",
            "description": "Get more Google reviews with ethical ask workflows, QR links, follow-up timing, and GBP settings that turn happy customers into social proof.",
            "keywords": "google reviews, small business reviews, get more reviews, google business profile reviews",
            "image_alt": "Small business owner collecting Google reviews from happy customers on a phone",
            "image_scene": "five-star review cards and a smartphone showing a review request screen",
            "related": [
                ("Optimize your Google Business Profile", "/blog/posts/optimize-google-business-profile/"),
                ("Local SEO checklist for small businesses", "/blog/posts/local-seo-checklist-small-business/"),
                ("Google review link generator", "/free-tools/google-review-generator/"),
            ],
            "content": textwrap.dedent(
                """
                # How to Get More Google Reviews for Your Small Business

                Google reviews influence whether someone calls you, visits your shop, or chooses a competitor. For local businesses, reviews are not vanity metrics — they are conversion assets that show up in the map pack, in branded search, and in word-of-mouth referrals.

                This guide covers ethical ways to get more Google reviews without buying fake feedback or spamming customers.

                ## Why Google reviews matter more than ever

                Reviews affect three things at once:

                - **Trust:** new customers use star ratings as a quick quality filter.
                - **Visibility:** active review profiles often perform better in local search.
                - **Conversion:** a strong rating next to your business name increases calls and direction requests.

                One extra review will not change your business overnight. A steady flow of recent, detailed reviews will.

                {{CTA:tools}}

                ## Start with a review-friendly customer experience

                You cannot market your way out of a bad experience. Before asking for reviews, make sure the basics are solid:

                1. Clear pricing or quote process
                2. On-time delivery or appointments
                3. Easy ways to contact you
                4. A simple fix when something goes wrong

                The best review strategy is still excellent service with a clear moment to ask.

                ## Ask at the right moment

                Timing beats volume. Ask when the customer is happiest:

                - Right after a successful installation or treatment
                - When they compliment your team
                - After a repeat purchase
                - When they message you thanks on WhatsApp or email

                Avoid asking while they are waiting, frustrated, or mid-problem.

                ### Scripts that work

                Keep it personal and short:

                - "If we made this easy for you, a quick Google review helps other customers find us."
                - "Would you mind sharing your experience on Google? It takes about 30 seconds."

                Do not offer payment or discounts in exchange for reviews — that violates Google's policies and can get reviews removed.

                ## Make leaving a review effortless

                Friction kills response rates. Remove every extra step:

                1. Create a direct Google review link for your business profile.
                2. Shorten it or turn it into a QR code for receipts, counters, and follow-up messages.
                3. Test the link on mobile before sharing it.

                Use our [Google review link generator](https://infoweb.sousadev.com/free-tools/google-review-generator/) to build a clean link and QR code in seconds.

                {{CTA}}

                ## Use QR codes and follow-up channels wisely

                Place review requests where customers already engage:

                - Printed card after service
                - Email signature for completed projects
                - WhatsApp follow-up with the direct link
                - Table tent in a café or salon

                QR codes work well because the customer scans once and lands on the review form immediately.

                ## Reply to every review

                Replying shows you are active and professional:

                - **Positive reviews:** thank them and mention something specific they praised.
                - **Negative reviews:** respond calmly, take responsibility where fair, and invite offline resolution.

                Prospects read your replies as much as the reviews themselves.

                ## What not to do

                - Do not buy reviews or use review farms.
                - Do not ask employees to review the business from fake accounts.
                - Do not gate reviews by sending only happy customers to Google and unhappy ones elsewhere.
                - Do not copy-paste the same review request to hundreds of people without context.

                Google removes suspicious patterns. Short-term tricks create long-term damage.

                ## Track progress monthly

                Pick three metrics and review them every month:

                1. Total review count
                2. Average rating
                3. Reviews in the last 30 days

                If recent reviews stall, fix the ask timing and the link before trying new tactics.

                {{CTA:contact}}

                ## Final takeaway

                More Google reviews come from consistent service, well-timed asks, and a frictionless review link. Build the habit into your delivery process and reviews become a reliable growth channel instead of a random bonus.
                """
            ).strip(),
        },
        "pt": {
            "title": "Como Conseguir Mais Avaliações Google para o Seu Negócio",
            "description": "Consiga mais avaliações Google com pedidos éticos, links QR, timing certo e definições no Perfil da Empresa que transformam clientes satisfeitos em prova social.",
            "keywords": "avaliações google, reviews google negócio local, conseguir avaliações, perfil empresa google",
            "image_alt": "Dono de pequeno negócio a pedir avaliações Google a clientes satisfeitos no telemóvel",
            "image_scene": "cartões de cinco estrelas e telemóvel com ecrã de pedido de avaliação",
            "related": [
                ("Otimizar o Perfil da Empresa no Google", "/blog/posts/otimizar-perfil-empresa-google/"),
                ("Checklist SEO local para pequenos negócios", "/blog/posts/checklist-seo-local-pequenos-negocios/"),
                ("Gerador de link para avaliações Google", "/free-tools/pt/google-review-generator/"),
            ],
            "content": textwrap.dedent(
                """
                # Como Conseguir Mais Avaliações Google para o Seu Negócio

                As avaliações Google influenciam se alguém liga, visita a loja ou escolhe a concorrência. Para negócios locais em Portugal, as reviews não são métricas de vaidade — são ativos de conversão visíveis no mapa, na pesquisa de marca e no passa-palavra.

                Este guia explica formas éticas de conseguir mais avaliações Google sem comprar feedback falso ou spammar clientes.

                ## Porque as avaliações Google importam

                As reviews afetam três áreas ao mesmo tempo:

                - **Confiança:** novos clientes usam estrelas como filtro rápido de qualidade.
                - **Visibilidade:** perfis com avaliações recentes tendem a performar melhor em pesquisa local.
                - **Conversão:** uma boa classificação junto ao nome aumenta chamadas e pedidos de direções.

                Uma avaliação extra não muda o negócio da noite para o dia. Um fluxo constante de reviews recentes e detalhadas, sim.

                {{CTA:tools}}

                ## Comece por uma experiência que merece avaliação

                Não há marketing que compense uma má experiência. Antes de pedir reviews, confirme o básico:

                1. Preços ou orçamentos claros
                2. Entregas ou marcações pontuais
                3. Formas fáceis de contacto
                4. Resolução rápida quando algo corre mal

                A melhor estratégia continua a ser bom serviço com um momento claro para pedir feedback.

                ## Peça no momento certo

                O timing vence o volume. Peça quando o cliente está mais satisfeito:

                - Logo após uma instalação ou tratamento bem-sucedido
                - Quando elogia a equipa
                - Depois de uma compra repetida
                - Quando agradece por WhatsApp ou email

                Evite pedir enquanto espera, está frustrado ou ainda há um problema por resolver.

                ### Frases que funcionam

                Seja pessoal e breve:

                - "Se corrermos tudo bem, uma avaliação rápida no Google ajuda outros clientes a encontrar-nos."
                - "Importa-se de partilhar a experiência no Google? Demora cerca de 30 segundos."

                Não ofereça pagamento ou descontos em troca de avaliações — viola as políticas Google e pode levar a remoções.

                ## Torne o processo simples

                Fricção mata taxas de resposta. Remova passos extra:

                1. Crie um link direto para avaliar o Perfil da Empresa Google.
                2. Encurte o link ou transforme-o em QR code para talões, balcão e follow-ups.
                3. Teste o link no telemóvel antes de partilhar.

                Use o nosso [gerador de link para avaliações Google](https://infoweb.sousadev.com/free-tools/pt/google-review-generator/) para criar link e QR code em segundos.

                {{CTA}}

                ## QR codes e follow-up nos canais certos

                Coloque pedidos onde os clientes já interagem:

                - Cartão impresso após o serviço
                - Assinatura de email em projetos concluídos
                - Follow-up WhatsApp com link direto
                - Display na mesa de café, salão ou clínica

                QR codes funcionam bem porque o cliente scannea uma vez e cai direto no formulário de avaliação.

                ## Responda a todas as avaliações

                Responder mostra profissionalismo:

                - **Positivas:** agradeça e mencione algo específico que elogiaram.
                - **Negativas:** responda com calma, assuma responsabilidade quando justo e convide a resolver offline.

                Prospects leem as respostas tanto quanto as reviews.

                ## O que não fazer

                - Não compre avaliações ou use farms de reviews.
                - Não peça a colaboradores para avaliar com contas falsas.
                - Não envie só clientes felizes para o Google e insatisfeitos para outro sítio.
                - Não copie o mesmo pedido em massa sem contexto.

                A Google remove padrões suspeitos. Atalhos criam dano a longo prazo.

                ## Acompanhe o progresso mensalmente

                Escolha três métricas e reveja-as todos os meses:

                1. Total de avaliações
                2. Classificação média
                3. Avaliações nos últimos 30 dias

                Se as reviews recentes estagnarem, corrija timing e link antes de testar novas táticas.

                {{CTA:contact}}

                ## Conclusão

                Mais avaliações Google vêm de serviço consistente, pedidos bem timed e um link sem fricção. Integre o hábito no processo de entrega e as reviews tornam-se canal de crescimento fiável em vez de bónus aleatório.
                """
            ).strip(),
        },
    },
    {
        "en_slug": "whatsapp-for-business-complete-guide",
        "pt_slug": "whatsapp-para-negocios-guia-completo",
        "category": "digital-marketing",
        "read_time": 9,
        "accent": "#22c55e",
        "en": {
            "title": "WhatsApp for Business: Complete Guide for Small Teams",
            "description": "WhatsApp for business explained: Business vs Business API, click-to-chat links, QR codes, templates, and workflows that convert chats into sales.",
            "keywords": "whatsapp for business, whatsapp business guide, click to chat, whatsapp qr code business",
            "image_alt": "Small business team managing WhatsApp customer conversations on mobile and laptop",
            "image_scene": "WhatsApp-style chat bubbles and a QR code on a shop counter",
            "related": [
                ("Do you need a website if you have Instagram?", "/blog/posts/need-website-if-have-instagram/"),
                ("Small business homepage checklist", "/blog/posts/small-business-homepage-checklist/"),
                ("WhatsApp QR code generator", "/free-tools/whatsapp-qr-generator/"),
            ],
            "content": textwrap.dedent(
                """
                # WhatsApp for Business: Complete Guide for Small Teams

                WhatsApp is often the highest-intent channel for small businesses. Customers message when they want a quote, a booking, or a quick answer — not when they feel like browsing a feed.

                This guide explains how to use WhatsApp professionally without turning your personal number into a 24/7 chaos inbox.

                ## WhatsApp, WhatsApp Business, and the API

                Most small businesses should start with **WhatsApp Business** (the free app):

                - Business profile with hours, address, and description
                - Quick replies and labels
                - Catalog for simple product lists
                - Away messages and greeting templates

                The **WhatsApp Business API** is for larger teams that need multiple agents, CRM integrations, and automated flows. It has setup cost and provider fees. Do not jump to the API until the free app is clearly limiting you.

                {{CTA:tools}}

                ## Set up a professional presence

                Before promoting your number, complete the basics:

                1. Use a dedicated business number when possible
                2. Add logo, category, and service area
                3. Write a clear description with what you sell and response times
                4. Set business hours and an away message

                Customers decide whether to message you based on how complete and trustworthy the profile looks.

                ## Click-to-chat links and QR codes

                Make starting a conversation one tap away:

                - Add a WhatsApp button on your website header or contact page
                - Put a QR code on business cards, flyers, and packaging
                - Include a prefilled message for common intents ("Hi, I'd like a quote for…")

                Generate a branded QR code with our [WhatsApp QR generator](https://infoweb.sousadev.com/free-tools/whatsapp-qr-generator/).

                ## Message workflows that save time

                ### Quick replies

                Save answers you repeat daily: pricing ranges, service area, opening hours, parking, payment methods.

                ### Labels

                Tag chats as **New lead**, **Quote sent**, **Booked**, or **Follow up** so nothing disappears in the scroll.

                ### Templates for follow-up

                After a quote, send a structured follow-up within 24–48 hours. Short, helpful, not pushy.

                {{CTA}}

                ## Connect WhatsApp to your website

                WhatsApp works best as part of a simple digital stack:

                - Website explains what you do and builds trust
                - WhatsApp handles fast questions and bookings
                - Google Business Profile sends local discovery traffic

                If you only have WhatsApp and no site, you lose search visibility and look less established for higher-ticket services.

                ## Privacy, consent, and boundaries

                - Only message people who opted in or contacted you first
                - Avoid bulk promotional broadcasts unless you use approved API templates
                - Set response windows so customers know when you are available
                - Never share customer chats publicly without permission

                ## Measure what matters

                Track weekly:

                1. Inbound chats
                2. Chats that become quotes
                3. Quotes that become sales
                4. Average response time

                If response time slips, add quick replies or assign one person as primary inbox owner during business hours.

                {{CTA:contact}}

                ## Final takeaway

                WhatsApp for business is not about being always online. It is about making it easy to start a conversation, answering fast with systems, and connecting chat to a website and local presence that builds trust before the first message.
                """
            ).strip(),
        },
        "pt": {
            "title": "WhatsApp para Negócios: Guia Completo para Pequenas Equipas",
            "description": "WhatsApp para negócios explicado: Business vs API, links click-to-chat, QR codes, respostas rápidas e fluxos que convertem conversas em vendas.",
            "keywords": "whatsapp negócios, whatsapp business portugal, click to chat, qr code whatsapp empresa",
            "image_alt": "Equipa de pequeno negócio a gerir conversas WhatsApp no telemóvel e portátil",
            "image_scene": "balões de conversa estilo WhatsApp e QR code no balcão de loja",
            "related": [
                ("Precisa de website se tem Instagram?", "/blog/posts/precisa-website-se-tem-instagram/"),
                ("Checklist homepage para pequeno negócio", "/blog/posts/checklist-homepage-pequeno-negocio/"),
                ("Gerador QR code WhatsApp", "/free-tools/pt/whatsapp-qr-generator/"),
            ],
            "content": textwrap.dedent(
                """
                # WhatsApp para Negócios: Guia Completo para Pequenas Equipas

                O WhatsApp é muitas vezes o canal de maior intenção para pequenos negócios em Portugal. Os clientes escrevem quando querem orçamento, marcação ou resposta rápida — não quando têm vontade de scrollar um feed.

                Este guia explica como usar WhatsApp de forma profissional sem transformar o número pessoal numa caixa de entrada 24/7.

                ## WhatsApp, WhatsApp Business e API

                A maioria deve começar com **WhatsApp Business** (app gratuita):

                - Perfil com horário, morada e descrição
                - Respostas rápidas e etiquetas
                - Catálogo para listas simples de produtos
                - Mensagens de ausência e saudação

                A **WhatsApp Business API** serve equipas maiores com vários agentes, integrações CRM e fluxos automáticos. Tem custos de setup e fornecedor. Não avance para a API enquanto a app gratuita não for claramente insuficiente.

                {{CTA:tools}}

                ## Configure uma presença profissional

                Antes de divulgar o número, complete o básico:

                1. Use número dedicado ao negócio quando possível
                2. Adicione logo, categoria e zona de serviço
                3. Escreva descrição clara com o que vende e tempos de resposta
                4. Defina horário e mensagem de ausência

                Os clientes decidem se escrevem com base no quão completo e fiável o perfil parece.

                ## Links click-to-chat e QR codes

                Torne o início da conversa um toque:

                - Botão WhatsApp no header ou página de contacto do website
                - QR code em cartões, flyers e embalagens
                - Mensagem pré-preenchida para intenções comuns ("Olá, gostava de orçamento para…")

                Gere QR code com o nosso [gerador WhatsApp QR](https://infoweb.sousadev.com/free-tools/pt/whatsapp-qr-generator/).

                ## Fluxos que poupam tempo

                ### Respostas rápidas

                Guarde respostas repetidas: preços indicativos, zona, horário, estacionamento, métodos de pagamento.

                ### Etiquetas

                Marque conversas como **Lead novo**, **Orçamento enviado**, **Marcado** ou **Follow-up** para nada se perder no scroll.

                ### Follow-up estruturado

                Depois de um orçamento, envie follow-up em 24–48 horas. Curto, útil, sem pressão.

                {{CTA}}

                ## Ligue WhatsApp ao website

                WhatsApp funciona melhor num stack digital simples:

                - Website explica o serviço e cria confiança
                - WhatsApp trata perguntas rápidas e marcações
                - Perfil Google traz descoberta local

                Só com WhatsApp e sem site perde visibilidade na pesquisa e parece menos estabelecido em serviços de ticket mais alto.

                ## Privacidade, consentimento e limites

                - Só contacte quem deu opt-in ou escreveu primeiro
                - Evite broadcasts promocionais em massa sem templates aprovados da API
                - Defina janelas de resposta para gerir expectativas
                - Nunca partilhe conversas publicamente sem autorização

                ## Meça o que importa

                Acompanhe semanalmente:

                1. Conversas recebidas
                2. Conversas que viram orçamento
                3. Orçamentos que viram venda
                4. Tempo médio de resposta

                Se o tempo de resposta aumentar, reforce respostas rápidas ou designe um responsável pelo inbox em horário comercial.

                {{CTA:contact}}

                ## Conclusão

                WhatsApp para negócios não é estar sempre online. É facilitar o primeiro contacto, responder rápido com sistemas e ligar chat a website e presença local que constróem confiança antes da primeira mensagem.
                """
            ).strip(),
        },
    },
    {
        "en_slug": "restaurant-menu-qr-code-guide",
        "pt_slug": "guia-qr-code-menu-restaurante",
        "category": "small-business",
        "read_time": 7,
        "accent": "#f97316",
        "en": {
            "title": "Restaurant Menu QR Codes: Setup Guide for {{CURRENT_YEAR}}",
            "description": "Restaurant menu QR code guide: PDF vs digital menus, table placement, accessibility, updates, and hygiene-friendly setups customers actually scan.",
            "keywords": "restaurant menu qr code, digital menu qr, qr code menu, hospitality menu",
            "image_alt": "Restaurant table tent with menu QR code scanned by a customer on a phone",
            "image_scene": "restaurant table with QR tent card and phone scanning a menu",
            "related": [
                ("WhatsApp for business complete guide", "/blog/posts/whatsapp-for-business-complete-guide/"),
                ("Small business homepage checklist", "/blog/posts/small-business-homepage-checklist/"),
                ("Menu QR code generator", "/free-tools/menu-qr-generator/"),
            ],
            "content": textwrap.dedent(
                """
                # Restaurant Menu QR Codes: Setup Guide for {{CURRENT_YEAR}}

                QR menus went from pandemic workaround to standard hospitality tooling. Done well, they reduce print costs, speed up updates, and keep menus accurate. Done poorly, they frustrate guests and hurt the experience.

                Here is a practical setup guide for cafés, restaurants, and bars that want QR menus customers will actually use.

                ## Choose the right menu format

                ### PDF menu

                Fast to launch if you already have a designed PDF. Weakness: PDFs are hard to read on small phones and painful to update frequently.

                ### Mobile-friendly web menu

                Best long-term option. Responsive text, photos, allergens, and daily specials without reprinting. Updates go live instantly.

                ### Hybrid

                Keep a short printed menu for bestsellers and a QR for the full list, wine pairings, or seasonal items.

                {{CTA:tools}}

                ## Generate a reliable QR code

                Use a high-contrast QR code that links directly to the menu URL — not a redirect chain that breaks later.

                Test scans on:

                - iPhone camera
                - Android camera
                - Low light at a corner table

                Build one with our [menu QR code generator](https://infoweb.sousadev.com/free-tools/menu-qr-generator/).

                ## Placement and signage

                Guests should understand what to scan without asking staff:

                - Table tent with "Scan for full menu"
                - One QR at the bar and one per section in large venues
                - Laminated card sized at least 8×8 cm for easy scanning

                Avoid tiny QR codes on busy posters or reflective surfaces.

                ## Accessibility matters

                Not every guest prefers QR:

                - Keep a few printed menus available
                - Train staff to offer help without making guests feel awkward
                - Ensure the web menu works without installing an app
                - Use readable font sizes (16px+ body text)

                {{CTA}}

                ## Keep menus accurate

                QR menus fail when prices or dishes are outdated. Assign one person to own updates:

                1. Sold-out items removed same day
                2. Seasonal menus swapped on schedule
                3. Allergen info reviewed when recipes change

                An accurate QR menu beats a beautiful printed menu with wrong prices.

                ## Connect QR to reservations and reviews

                Your menu page can also link to:

                - Online booking
                - WhatsApp for large groups
                - Google review link after a great meal

                Small links at the bottom of the menu page increase repeat visits and reviews without cluttering the dining room.

                {{CTA:contact}}

                ## Final takeaway

                Restaurant menu QR codes work when the destination is mobile-friendly, signage is clear, and updates are owned by someone on the team. Treat the QR as part of service operations — not a one-time print job.
                """
            ).strip(),
        },
        "pt": {
            "title": "QR Code para Ementa de Restaurante: Guia Prático {{CURRENT_YEAR}}",
            "description": "Guia QR code ementa restaurante: PDF vs ementa digital, colocação na mesa, acessibilidade, atualizações e setups higiénicos que clientes scanneiam.",
            "keywords": "qr code ementa restaurante, ementa digital qr, menu digital restaurante, qr code menu portugal",
            "image_alt": "Mesa de restaurante com QR code de ementa scanneado por cliente no telemóvel",
            "image_scene": "mesa de restaurante com display QR e telemóvel a abrir ementa digital",
            "related": [
                ("WhatsApp para negócios guia completo", "/blog/posts/whatsapp-para-negocios-guia-completo/"),
                ("Checklist homepage pequeno negócio", "/blog/posts/checklist-homepage-pequeno-negocio/"),
                ("Gerador QR code para ementa", "/free-tools/pt/menu-qr-generator/"),
            ],
            "content": textwrap.dedent(
                """
                # QR Code para Ementa de Restaurante: Guia Prático {{CURRENT_YEAR}}

                Ementas QR deixaram de ser solução de emergência e passaram a ferramenta normal na restauração. Bem feitas, reduzem impressão, aceleram atualizações e mantêm preços corretos. Mal feitas, frustram clientes.

                Guia prático para cafés, restaurantes e bares em Portugal que querem QR codes que clientes usam de facto.

                ## Escolha o formato certo

                ### PDF

                Rápido se já tem PDF desenhado. Fraqueza: difícil de ler no telemóvel e chato de atualizar.

                ### Ementa web mobile-friendly

                Melhor opção a longo prazo. Texto responsivo, fotos, alergénios e pratos do dia sem reimprimir.

                ### Híbrido

                Ementa curta impressa com bestsellers e QR para lista completa, vinhos ou sazonal.

                {{CTA:tools}}

                ## Gere QR code fiável

                Use QR de alto contraste ligado direto ao URL da ementa — não cadeias de redirect que partem depois.

                Teste scans em:

                - Câmara iPhone
                - Câmara Android
                - Luz baixa numa mesa de canto

                Crie um com o nosso [gerador QR para ementa](https://infoweb.sousadev.com/free-tools/pt/menu-qr-generator/).

                ## Colocação e sinalética

                Clientes devem perceber o que scanear sem perguntar:

                - Display na mesa com "Scan para ementa completa"
                - Um QR no bar e um por secção em espaços grandes
                - Cartão laminado mínimo 8×8 cm

                Evite QR minúsculos em posters reflexivos.

                ## Acessibilidade importa

                Nem todos preferem QR:

                - Mantenha algumas ementas impressas
                - Forme equipa para ajudar sem constranger
                - Ementa web sem instalar app
                - Texto legível (16px+ corpo)

                {{CTA}}

                ## Mantenha a ementa correta

                QR falha quando preços ou pratos estão desatualizados. Designe um responsável:

                1. Esgotados removidos no mesmo dia
                2. Ementas sazonais trocadas a tempo
                3. Alergénios revistos quando receitas mudam

                Ementa QR correta vence ementa bonita com preços errados.

                ## Ligue QR a reservas e avaliações

                A página da ementa pode linkar para:

                - Reserva online
                - WhatsApp para grupos
                - Avaliação Google após boa refeição

                Links discretos no rodapé aumentam revisitas e reviews sem poluir a sala.

                {{CTA:contact}}

                ## Conclusão

                QR code para ementa funciona quando o destino é mobile-friendly, a sinalética é clara e alguém na equipa gere atualizações. Trate o QR como operação de serviço — não como impressão única.
                """
            ).strip(),
        },
    },
    {
        "en_slug": "website-speed-small-business-guide",
        "pt_slug": "guia-velocidade-website-pequenos-negocios",
        "category": "seo",
        "read_time": 8,
        "accent": "#38bdf8",
        "en": {
            "title": "Website Speed for Small Business: Practical {{CURRENT_YEAR}} Guide",
            "description": "Improve small business website speed: Core Web Vitals, image compression, hosting, caching, and fixes that help Google rankings and conversions.",
            "keywords": "website speed small business, core web vitals, fast website, page speed seo",
            "image_alt": "Website speed metrics dashboard on laptop showing improved Core Web Vitals scores",
            "image_scene": "speed gauge and performance chart on dark navy dashboard",
            "related": [
                ("Website maintenance checklist", "/blog/posts/website-maintenance-checklist/"),
                ("Local SEO checklist for small businesses", "/blog/posts/local-seo-checklist-small-business/"),
                ("Website health scorecard", "/free-tools/website-health-scorecard/"),
            ],
            "content": textwrap.dedent(
                """
                # Website Speed for Small Business: Practical {{CURRENT_YEAR}} Guide

                Slow websites lose leads quietly. A local customer on mobile will not wait five seconds for your services page to load — they tap back and call someone else.

                Speed also feeds SEO through Core Web Vitals, Google's user experience metrics. You do not need a massive engineering team to fix the basics.

                ## What Core Web Vitals mean in plain language

                Google tracks three signals:

                - **LCP (Largest Contentful Paint):** how fast the main content appears
                - **INP (Interaction to Next Paint):** how responsive the page feels when tapped
                - **CLS (Cumulative Layout Shift):** whether buttons jump while loading

                You want green scores on mobile for local business sites. Start with Google's PageSpeed Insights and test your homepage plus top service pages.

                {{CTA:tools}}

                ## Fix images first

                Images are the most common speed killer for small business sites:

                1. Resize photos before upload (max 1600px wide for heroes)
                2. Use WebP or compressed JPG
                3. Lazy-load below-the-fold images
                4. Do not upload 5MB phone photos directly

                One optimized hero image can shave seconds off load time.

                ## Reduce plugin and script bloat

                Page builders and plugins stack JavaScript quickly. Audit what loads on every page:

                - Remove unused chat widgets on pages that do not need them
                - Defer non-critical scripts
                - Avoid loading three different font families

                Faster sites often have fewer moving parts, not more optimization tricks.

                ## Choose hosting that matches traffic

                Cheap shared hosting can work for brochure sites, but slow TTFB (time to first byte) hurts everyone. Look for:

                - SSL included
                - Daily backups
                - CDN or edge caching for static assets
                - Support that understands small business sites

                {{CTA}}

                ## Mobile-first testing

                Most local traffic is mobile. Test on real phones over 4G, not just office Wi‑Fi:

                - Tap phone number links
                - Scroll contact forms
                - Open maps directions
                - Check hero text readability without zoom

                If mobile feels slow, desktop speed scores do not matter much.

                ## Speed and conversions

                Treat speed as a sales metric:

                - Compare bounce rate before and after image fixes
                - Track form submissions on key pages
                - Watch call clicks from mobile

                A one-second improvement on a high-intent page can pay for hosting upgrades quickly.

                {{CTA:contact}}

                ## Final takeaway

                Website speed for small business is mostly discipline: lighter images, cleaner scripts, solid hosting, and mobile testing. Fix those four and you will beat many local competitors who never look at performance.
                """
            ).strip(),
        },
        "pt": {
            "title": "Velocidade de Website para Pequenos Negócios: Guia {{CURRENT_YEAR}}",
            "description": "Melhore a velocidade do website: Core Web Vitals, compressão de imagens, hosting, cache e correções que ajudam SEO Google e conversões.",
            "keywords": "velocidade website, core web vitals, site rápido pequena empresa, page speed seo",
            "image_alt": "Dashboard de velocidade de website no portátil com Core Web Vitals melhorados",
            "image_scene": "medidor de velocidade e gráfico de performance em dashboard navy",
            "related": [
                ("Checklist manutenção website", "/blog/posts/checklist-manutencao-website/"),
                ("Checklist SEO local pequenos negócios", "/blog/posts/checklist-seo-local-pequenos-negocios/"),
                ("Website health scorecard", "/free-tools/website-health-scorecard/"),
            ],
            "content": textwrap.dedent(
                """
                # Velocidade de Website para Pequenos Negócios: Guia {{CURRENT_YEAR}}

                Websites lentos perdem leads em silêncio. Um cliente local no telemóvel não espera cinco segundos pela página de serviços — volta atrás e liga à concorrência.

                Velocidade também alimenta SEO via Core Web Vitals, métricas de experiência Google. Não precisa de equipa de engenharia para corrigir o básico.

                ## O que Core Web Vitals significam

                A Google mede três sinais:

                - **LCP:** quão rápido o conteúdo principal aparece
                - **INP:** quão responsiva a página é ao toque
                - **CLS:** se botões saltam durante carregamento

                Quer scores verdes no mobile para sites locais. Comece com PageSpeed Insights na homepage e páginas de serviço principais.

                {{CTA:tools}}

                ## Corrija imagens primeiro

                Imagens são o assassino de velocidade mais comum:

                1. Redimensione antes de upload (máx. 1600px largura em heroes)
                2. Use WebP ou JPG comprimido
                3. Lazy-load abaixo da dobra
                4. Não faça upload direto de fotos 5MB do telemóvel

                Uma hero otimizada pode poupar segundos.

                ## Reduza bloat de plugins e scripts

                Page builders acumulam JavaScript. Audite o que carrega em cada página:

                - Remova chat widgets onde não precisa
                - Adie scripts não críticos
                - Evite três famílias de fontes diferentes

                Sites rápidos têm menos peças, não mais truques.

                ## Escolha hosting adequado

                Hosting barato pode servir sites simples, mas TTFB lento prejudica todos. Procure:

                - SSL incluído
                - Backups diários
                - CDN ou cache para assets estáticos
                - Suporte que entende sites de pequenos negócios

                {{CTA}}

                ## Teste mobile-first

                Tráfego local é maioritariamente mobile. Teste em telemóvel real em 4G:

                - Links click-to-call
                - Formulários de contacto
                - Direções no Maps
                - Legibilidade do hero sem zoom

                Se mobile parece lento, scores desktop importam pouco.

                ## Velocidade e conversões

                Trate velocidade como métrica de vendas:

                - Compare bounce rate antes/depois de otimizar imagens
                - Acompanhe submissões de formulário
                - Veja cliques para ligar no mobile

                Um segundo a menos numa página de intenção alta paga upgrades de hosting rapidamente.

                {{CTA:contact}}

                ## Conclusão

                Velocidade de website para pequenos negócios é sobretudo disciplina: imagens leves, scripts limpos, hosting sólido e testes mobile. Corrija estes quatro e fica à frente de muitos concorrentes locais.
                """
            ).strip(),
        },
    },
    {
        "en_slug": "when-to-redesign-small-business-website",
        "pt_slug": "quando-redesenhar-website-pequeno-negocio",
        "category": "web-design",
        "read_time": 7,
        "accent": "#d7b46a",
        "en": {
            "title": "When to Redesign Your Small Business Website",
            "description": "Signs you need a small business website redesign: outdated design, mobile issues, poor SEO, slow speed, and how to plan a refresh without downtime.",
            "keywords": "website redesign small business, when to redesign website, refresh business website",
            "image_alt": "Before and after website redesign mockups for a small business on a designer screen",
            "image_scene": "split before/after browser windows showing modern website refresh",
            "related": [
                ("Cheap websites get expensive later", "/blog/posts/cheap-websites-expensive-later/"),
                ("How much does a small business website cost?", "/blog/posts/small-business-website-cost/"),
                ("Website maintenance checklist", "/blog/posts/website-maintenance-checklist/"),
            ],
            "content": textwrap.dedent(
                """
                # When to Redesign Your Small Business Website

                A website is not a one-time project. Markets change, services evolve, and design standards move fast on mobile. Keeping an outdated site often costs more in lost leads than a thoughtful redesign.

                Here are clear signs it is time to refresh — and how to plan without breaking search visibility or daily operations.

                ## Sign 1: Mobile experience is painful

                If you have to pinch-zoom, buttons overlap, or forms fail on phones, you are losing local customers daily. Mobile-first design is non-negotiable in {{CURRENT_YEAR}}.

                ## Sign 2: Your offer outgrew the site

                Common mismatches:

                - Site lists old services you no longer sell
                - New locations or hours are missing
                - Pricing pages reflect 2022 packages
                - Team page shows staff who left years ago

                When sales conversations start with "your website is wrong," redesign becomes a revenue fix, not a cosmetic one.

                {{CTA}}

                ## Sign 3: SEO basics were never implemented

                Check quickly:

                - Unique titles and meta descriptions per page
                - Proper H1/H2 structure
                - Local keywords on service pages
                - XML sitemap submitted in Search Console
                - Google Business Profile linked to the site

                A redesign is the right moment to rebuild information architecture for search intent, not just prettier graphics.

                ## Sign 4: Speed and security red flags

                Redesign triggers:

                - No SSL or browser warnings
                - Load times over 4 seconds on mobile
                - Broken plugins or unmaintained CMS
                - Contact forms that silently fail

                See our [website maintenance checklist](https://infoweb.sousadev.com/blog/posts/website-maintenance-checklist/) for ongoing tasks after launch.

                ## Sign 5: Brand upgraded, site did not

                If you refreshed logo, photography, or positioning but the site still looks like the old business, trust drops. Visual inconsistency makes you look smaller than you are.

                {{CTA:tools}}

                ## How to plan a redesign without chaos

                1. **Audit current pages** — keep URLs that rank when possible
                2. **List must-have pages** — services, about, contact, booking
                3. **Collect proof** — reviews, case studies, certifications
                4. **Set one primary CTA** — call, book, or quote
                5. **Plan redirects** — map old URLs to new ones
                6. **Launch checklist** — forms, analytics, Search Console

                A phased launch beats a six-month perfect project that never ships.

                ## Redesign vs refresh

                Not every project needs a full rebuild:

                - **Refresh:** new visuals, updated copy, same structure
                - **Redesign:** new structure, navigation, and page strategy

                Choose refresh when analytics show good traffic but poor conversion. Choose redesign when traffic and trust are both weak.

                {{CTA:contact}}

                ## Final takeaway

                Redesign when mobile, messaging, SEO, or trust clearly hurt sales — not because a competitor launched something flashy. Plan redirects, protect rankings, and launch with working forms and analytics on day one.
                """
            ).strip(),
        },
        "pt": {
            "title": "Quando Redesenhar o Website do Seu Pequeno Negócio",
            "description": "Sinais de que precisa de redesenhar o website: design desatualizado, mobile fraco, SEO pobre, lentidão e como planear refresh sem parar o negócio.",
            "keywords": "redesenhar website, quando atualizar site, refresh website pequena empresa",
            "image_alt": "Mockups antes e depois de redesenho de website para pequeno negócio no ecrã",
            "image_scene": "janelas de browser antes/depois com refresh moderno de website",
            "related": [
                ("Websites baratos ficam caros", "/blog/posts/websites-baratos-ficam-caros/"),
                ("Quanto custa website pequena empresa", "/blog/posts/quanto-custa-website-pequena-empresa/"),
                ("Checklist manutenção website", "/blog/posts/checklist-manutencao-website/"),
            ],
            "content": textwrap.dedent(
                """
                # Quando Redesenhar o Website do Seu Pequeno Negócio

                Um website não é projeto único. Mercados mudam, serviços evoluem e standards mobile avançam rápido. Manter site desatualizado custa mais em leads perdidos do que um redesenho bem planeado.

                Sinais claros de que é hora de refrescar — e como planear sem partir SEO ou operações diárias.

                ## Sinal 1: Experiência mobile dolorosa

                Se precisa de zoom, botões sobrepõem-se ou formulários falham no telemóvel, perde clientes locais todos os dias. Design mobile-first é obrigatório em {{CURRENT_YEAR}}.

                ## Sinal 2: A oferta cresceu, o site não

                Desalinhamentos comuns:

                - Serviços antigos ainda listados
                - Novas lojas ou horários em falta
                - Preços de pacotes desatualizados
                - Equipa com pessoas que já saíram

                Quando vendas começam com "o site está errado," redesenho é correção de receita, não cosmética.

                {{CTA}}

                ## Sinal 3: SEO básico nunca foi feito

                Verifique rapidamente:

                - Títulos e meta descriptions únicos por página
                - Estrutura H1/H2 correta
                - Keywords locais nas páginas de serviço
                - Sitemap XML na Search Console
                - Perfil Google ligado ao site

                Redesenho é momento certo para reconstruir arquitetura de informação para intenção de pesquisa.

                ## Sinal 4: Velocidade e segurança em alerta

                Gatilhos de redesenho:

                - Sem SSL ou avisos no browser
                - Carregamento acima de 4 segundos no mobile
                - Plugins partidos ou CMS abandonado
                - Formulários que falham em silêncio

                Veja o nosso [checklist de manutenção](https://infoweb.sousadev.com/blog/posts/checklist-manutencao-website/) para tarefas pós-lançamento.

                ## Sinal 5: Marca evoluiu, site ficou atrás

                Se renovou logo, fotografia ou posicionamento mas o site parece o negócio antigo, confiança cai. Inconsistência visual faz parecer mais pequeno do que é.

                {{CTA:tools}}

                ## Como planear sem caos

                1. **Audite páginas atuais** — mantenha URLs que rankeiam quando possível
                2. **Liste páginas essenciais** — serviços, sobre, contacto, marcações
                3. **Recolha prova social** — avaliações, casos, certificações
                4. **Defina CTA principal** — ligar, marcar ou pedir orçamento
                5. **Planeie redirects** — mapeie URLs antigas para novas
                6. **Checklist de lançamento** — formulários, analytics, Search Console

                Lançamento faseado vence projeto perfeito de seis meses que nunca sai.

                ## Redesenho vs refresh

                Nem tudo precisa rebuild total:

                - **Refresh:** novos visuais, copy atualizada, mesma estrutura
                - **Redesenho:** nova estrutura, navegação e estratégia de páginas

                Escolha refresh quando tráfego é bom mas conversão fraca. Escolha redesenho quando tráfego e confiança estão fracos.

                {{CTA:contact}}

                ## Conclusão

                Redesenhe quando mobile, mensagem, SEO ou confiança claramente prejudicam vendas — não porque concorrente lançou algo bonito. Proteja rankings com redirects e lance com formulários e analytics a funcionar no dia um.
                """
            ).strip(),
        },
    },
]


def static_title(title: str) -> str:
    return title.replace("{{CURRENT_YEAR}}", "2026")


def write_metadata(slug: str, lang: str, data: dict, alt_slug: str, category: str, read_time: int) -> None:
    alt_key = "pt" if lang == "en" else "en"
    payload = {
        "slug": slug,
        "language": lang,
        "title": data["title"],
        "description": data["description"],
        "author": "InfoWeb",
        "dateCreated": DATE,
        "dateUpdated": DATE,
        "category": category,
        "tags": data["keywords"].split(", ")[:4],
        "image": "./assets/featured.png",
        "imageAlt": data["image_alt"],
        "readTime": read_time,
        "featured": False,
        "published": True,
        "alternateLanguage": {alt_key: alt_slug},
    }
    path = POSTS_DIR / slug / "metadata.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_image_prompt(slug: str, lang: str, data: dict) -> None:
    title = static_title(data["title"])
    content = textwrap.dedent(
        f"""
        # Image generation prompt

        Create a 1200x630 hero image for an InfoWeb blog post titled "{title}".

        Style: modern editorial illustration, premium small-business SaaS/agency aesthetic, dark navy/slate background (#020617), subtle gold accents (#d7b46a), clean high-contrast composition.

        Scene: {data.get('image_scene', data['image_alt'])}. {"Use Portuguese/local business context where relevant." if lang == "pt" else "Use international small-business context."}

        Brand cues: professional, trustworthy, not corporate stock photography. InfoWeb navy/gold palette. No third-party logos, no brand screenshots, no watermarks.

        Composition: 16:9 Open Graph layout, safe negative space upper-left, readable at small preview size.

        Avoid: tiny unreadable text, fake UI clutter, distorted typography, watermarks.

        Output: `featured.png` at 1200x630, optimized under 250KB if possible.
        """
    ).strip() + "\n"
    (POSTS_DIR / slug / "image-prompt.md").write_text(content, encoding="utf-8")


def related_html(related: list[tuple[str, str]]) -> str:
    items = "\n".join(
        f'        <li><a href="{BASE_URL}{path}" class="hover:text-signal transition">{label}</a></li>'
        for label, path in related
    )
    hub = f"{BASE_URL}/blog/" if "pt/" not in related[0][1] else f"{BASE_URL}/blog/"
    tools = f"{BASE_URL}/free-tools/pt/" if "/pt/" in related[-1][1] else f"{BASE_URL}/free-tools/"
    hub_label = "Blog" if "/pt/" not in tools else "Blog"
    tools_label = "Free tools" if "/pt/" not in tools else "Ferramentas gratuitas"
    return (
        f"{items}\n"
        f'        <li><a href="{hub}" class="hover:text-signal transition">{hub_label}</a></li>\n'
        f'        <li><a href="{tools}" class="hover:text-signal transition">{tools_label}</a></li>'
    )


def write_index_html(slug: str, lang: str, data: dict, alt_slug: str, category: str, read_time: int) -> None:
    title = static_title(data["title"])
    section = CATEGORY_SECTION[category][lang]
    date_display = DATE_DISPLAY_PT if lang == "pt" else DATE_DISPLAY_EN
    read_label = "min leitura" if lang == "pt" else "min read"
    blog_back = "← Voltar ao blog" if lang == "pt" else "← Back to blog"
    blog_nav = "← Blog" if lang == "pt" else "← Blog"
    plans = "Planos" if lang == "pt" else "Plans"
    related_heading = "Leitura relacionada" if lang == "pt" else "Related reading"
    share_label = "Partilhar este artigo:" if lang == "pt" else "Share this article:"
    copy_label = "Copiar link" if lang == "pt" else "Copy link"
    loading = "A carregar artigo..." if lang == "pt" else "Loading article..."
    author_bio = (
        "Soluções completas de websites para pequenos negócios. Domínio, hosting, design e manutenção incluídos."
        if lang == "pt"
        else "Complete website solutions for small businesses. Domain, hosting, design, and maintenance included."
    )
    author_cta = "Conhecer os planos →" if lang == "pt" else "See plans →"
    footer_blog = "Blog"
    footer_tools = "Ferramentas Grátis" if lang == "pt" else "Free Tools"
    footer_plans = "Planos" if lang == "pt" else "Plans"
    copyright = (
        "© 2026 InfoWeb by Sousa Dev. Todos os direitos reservados."
        if lang == "pt"
        else "© 2026 InfoWeb by Sousa Dev. All rights reserved."
    )
    lang_switch_href = f"../{alt_slug}/"
    lang_switch_label = "🇬🇧 EN" if lang == "pt" else "🇵🇹 PT"
    lang_switch_target = "en" if lang == "pt" else "pt"
    og_locale = "pt_PT" if lang == "pt" else "en_GB"
    og_alt = "en_GB" if lang == "pt" else "pt_PT"
    canonical = f"{BASE_URL}/blog/posts/{slug}/"
    alt_canonical = f"{BASE_URL}/blog/posts/{alt_slug}/"
    x_default = alt_canonical if lang == "pt" else canonical
    hreflang_self = lang
    hreflang_alt = "en" if lang == "pt" else "pt"
    in_language = "pt-PT" if lang == "pt" else "en-GB"
    page_title_suffix = "InfoWeb Blog"

    html = f"""<!DOCTYPE html>
<html lang="{lang}" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXQSMBERJM"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag() {{
      dataLayer.push(arguments);
    }}
    gtag("js", new Date());
    gtag("config", "G-XXQSMBERJM");
  </script>
  <script src="../../../assets/js/analytics.js" defer></script>

  <title>{title} — {page_title_suffix}</title>
  <meta name="description" content="{data['description']}" />
  <meta name="keywords" content="{data['keywords']}" />
  <meta name="author" content="InfoWeb" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
  <link rel="canonical" href="{canonical}" />

  <link rel="alternate" hreflang="{hreflang_self}" href="{canonical}" />
  <link rel="alternate" hreflang="{hreflang_alt}" href="{alt_canonical}" />
  <link rel="alternate" hreflang="x-default" href="{x_default}" />

  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="InfoWeb" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{data['description']}" />
  <meta property="og:image" content="{BASE_URL}/blog/posts/{slug}/assets/featured.png" />
  <meta property="og:image:type" content="image/png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{data['image_alt']}" />
  <meta property="og:locale" content="{og_locale}" />
  <meta property="og:locale:alternate" content="{og_alt}" />
  <meta property="article:published_time" content="{DATE}T00:00:00Z" />
  <meta property="article:modified_time" content="{DATE}T00:00:00Z" />
  <meta property="article:author" content="InfoWeb" />
  <meta property="article:section" content="{section}" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{data['description']}" />
  <meta name="twitter:image" content="{BASE_URL}/blog/posts/{slug}/assets/featured.png" />
  <meta name="twitter:image:alt" content="{data['image_alt']}" />

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{title}",
    "description": "{data['description']}",
    "image": "{BASE_URL}/blog/posts/{slug}/assets/featured.png",
    "author": {{ "@type": "Organization", "name": "InfoWeb" }},
    "publisher": {{
      "@type": "Organization",
      "name": "InfoWeb",
      "logo": {{
        "@type": "ImageObject",
        "url": "{BASE_URL}/assets/images/infoweb-logo.png"
      }}
    }},
    "datePublished": "{DATE}",
    "dateModified": "{DATE}",
    "mainEntityOfPage": "{canonical}",
    "inLanguage": "{in_language}"
  }}
  </script>

  <link rel="icon" type="image/png" href="../../../favicon_io/favicon-32x32.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;600;700;800&display=swap" rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/marked@15.0.12/marked.min.js"></script>
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
  <link rel="stylesheet" href="../../post.css" />

  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "{BASE_URL}/"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "Blog",
      "item": "{BASE_URL}/blog/"
    }},
    {{
      "@type": "ListItem",
      "position": 3,
      "name": "{title}",
      "item": "{canonical}"
    }}
  ]
}}
  </script>
</head>
<body class="bg-slate-950 text-white font-sans antialiased min-h-screen flex flex-col bg-[radial-gradient(circle_at_top,_rgba(215,180,106,0.22),_transparent_42%),radial-gradient(circle_at_80%_18%,_rgba(56,189,248,0.18),_transparent_36%),linear-gradient(180deg,_#020617_0%,_#020617_70%,_#0f172a_100%)]">
  <header class="border-b border-slate-800/60 bg-slate-950/70 backdrop-blur-xl sticky top-0 z-20">
    <div class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between gap-3">
      <a href="../../../" class="inline-flex items-center gap-2 text-white" aria-label="InfoWeb home" data-track="nav_click" data-track-location="header" data-track-target="/">
        <img src="../../../assets/images/infoweb-logo.png" alt="InfoWeb — managed websites for small businesses" class="h-9 w-auto" width="120" height="36" />
      </a>
      <div class="flex items-center gap-4">
        <a href="../../" class="text-sm font-semibold text-slate-300 hover:text-white transition" data-track="nav_click" data-track-location="header" data-track-target="/blog/">{blog_nav}</a>
        <a href="{lang_switch_href}" class="text-xs px-3 py-1.5 rounded-full border border-slate-600 text-slate-300 hover:border-signal hover:text-signal transition" data-track="language_switch" data-track-target="{lang_switch_target}">{lang_switch_label}</a>
        <a href="../../../#pricing" class="text-sm font-semibold border border-slate-600 rounded-full px-4 py-1.5 hover:border-white text-slate-300 transition" data-track="cta_click" data-track-location="blog_post" data-track-target="/#pricing">{plans}</a>
      </div>
    </div>
  </header>
  <main class="max-w-4xl mx-auto px-4 py-14 sm:py-16 flex-1 w-full">
    <div class="mb-8">
      <a href="../../" class="inline-flex items-center text-sm text-slate-400 hover:text-signal transition mb-4">{blog_back}</a>
      <div class="flex items-center gap-3 text-sm text-slate-400 mb-4">
        <span id="postCategory" class="px-3 py-1 rounded-full bg-slate-800/50 border border-slate-700 text-signal font-semibold"></span>
        <span id="postDate">{date_display}</span>
        <span>•</span>
        <span id="postReadTime">{read_time} {read_label}</span>
      </div>
    </div>
    <h1 class="text-3xl sm:text-4xl font-extrabold text-white mb-6 leading-tight" id="postTitle">{title}</h1>
    <article class="blog-content" id="postContent">
      <div class="text-center py-20">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-signal"></div>
        <p class="text-slate-400 mt-4">{loading}</p>
      </div>
    </article>
    <div class="mt-12 p-6 rounded-2xl bg-slate-900/50 border border-slate-800">
      <div class="flex items-start gap-4">
        <img src="../../../favicon_io/apple-touch-icon.png" alt="InfoWeb logo — website as a service for small businesses" class="w-16 h-16 rounded-xl object-contain shrink-0" width="64" height="64" />
        <div>
          <h3 class="text-white font-bold text-lg mb-1">InfoWeb</h3>
          <p class="text-slate-400 text-sm mb-3">{author_bio}</p>
          <a href="../../../#pricing" class="text-signal font-semibold text-sm hover:opacity-80 transition" data-track="cta_click" data-track-location="author_box" data-track-target="/#pricing">{author_cta}</a>
        </div>
      </div>
    </div>

    <section class="related-resources mt-10 pt-8 border-t border-slate-800" aria-labelledby="related-reading-heading">
      <h2 id="related-reading-heading" class="text-lg font-bold text-white mb-4">{related_heading}</h2>
      <ul class="space-y-2 text-slate-300">
{related_html(data['related'])}
      </ul>
    </section>
<div id="postTags" class="mt-8 flex flex-wrap gap-2"></div>
    <div class="mt-8 pt-8 border-t border-slate-800">
      <p class="text-slate-400 text-sm mb-3">{share_label}</p>
      <div class="flex gap-3 flex-wrap">
        <a href="#" id="shareTwitter" class="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-sm font-semibold transition" target="_blank" rel="noopener" data-track="share_click" data-track-platform="twitter">Twitter</a>
        <a href="#" id="shareFacebook" class="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-sm font-semibold transition" target="_blank" rel="noopener" data-track="share_click" data-track-platform="facebook">Facebook</a>
        <a href="#" id="shareLinkedIn" class="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-sm font-semibold transition" target="_blank" rel="noopener" data-track="share_click" data-track-platform="linkedin">LinkedIn</a>
        <button id="copyLink" class="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-sm font-semibold transition" data-track="share_click" data-track-platform="copy">{copy_label}</button>
      </div>
    </div>
  </main>
  <footer class="border-t border-slate-800 py-8 text-center">
    <div class="max-w-6xl mx-auto px-4">
      <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
        <a href="../../../" class="text-slate-400 hover:text-white transition" data-track="nav_click" data-track-location="footer" data-track-target="/">InfoWeb home</a>
        <div class="flex gap-6 text-sm text-slate-500">
          <a href="../../" class="hover:text-white transition">{footer_blog}</a>
          <a href="../../../free-tools/" class="hover:text-white transition">{footer_tools}</a>
          <a href="../../../#pricing" class="hover:text-white transition">{footer_plans}</a>
        </div>
      </div>
      <p class="text-slate-500 text-sm mt-4">{copyright}</p>
    </div>
  </footer>
  <script src="../../blog-i18n.js"></script>
  <script src="../../post-loader.js"></script>
</body>
</html>
"""
    (POSTS_DIR / slug / "index.html").write_text(html, encoding="utf-8")


def generate_featured_image(path: Path, title: str, accent: str) -> None:
    width, height = 1200, 630
    img = Image.new("RGB", (width, height), "#020617")
    draw = ImageDraw.Draw(img)

    for i in range(height):
        ratio = i / height
        r = int(2 + (15 - 2) * ratio)
        g = int(6 + (23 - 6) * ratio)
        b = int(23 + (42 - 23) * ratio)
        draw.line([(0, i), (width, i)], fill=(r, g, b))

    draw.ellipse((820, -80, 1180, 260), fill=(215, 180, 106, 40) if img.mode == "RGBA" else (40, 35, 20))
    draw.rounded_rectangle((70, 120, 620, 520), radius=28, outline=accent, width=4, fill=(15, 23, 42))
    draw.rounded_rectangle((110, 170, 580, 250), radius=12, fill=accent)
    draw.rounded_rectangle((110, 280, 520, 320), radius=8, fill=(51, 65, 85))
    draw.rounded_rectangle((110, 340, 480, 380), radius=8, fill=(51, 65, 85))
    draw.rounded_rectangle((110, 400, 400, 440), radius=8, fill=(51, 65, 85))

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 34)
        small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
        small = font

    draw.text((110, 188), "InfoWeb Blog", fill="#020617", font=small)
    lines = textwrap.wrap(title.replace("{{CURRENT_YEAR}}", "2026"), width=28)
    y = 290
    for line in lines[:3]:
        draw.text((110, y), line, fill="#e2e8f0", font=font)
        y += 42

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG", optimize=True)


def update_posts_index() -> None:
    index_path = POSTS_DIR / "metadata.json"
    existing = json.loads(index_path.read_text(encoding="utf-8"))
    seen = set()
    posts = []
    for entry in existing.get("posts", []):
        key = (entry["slug"], entry.get("language", "en"))
        if key in seen:
            continue
        seen.add(key)
        posts.append(entry)

    for spec in POSTS:
        for slug, lang in ((spec["en_slug"], "en"), (spec["pt_slug"], "pt")):
            key = (slug, lang)
            if key in seen:
                continue
            posts.append(
                {
                    "slug": slug,
                    "language": lang,
                    "dateCreated": DATE,
                    "dateUpdated": DATE,
                }
            )
            seen.add(key)

    posts.sort(key=lambda p: (p["dateCreated"], p["slug"]), reverse=True)
    payload = {
        "posts": posts,
        "lastUpdated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }
    index_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def append_blog_to_sitemap() -> None:
    sitemap = REPO / "sitemap.xml"
    text = sitemap.read_text(encoding="utf-8")
    if "blog/posts/get-more-google-reviews" in text:
        return
    block = ["  <!-- Blog -->", "  <url>", f"    <loc>{BASE_URL}/blog/</loc>", "    <changefreq>weekly</changefreq>", "    <priority>0.9</priority>", "  </url>"]
    for spec in POSTS:
        for slug in (spec["en_slug"], spec["pt_slug"]):
            block.extend(
                [
                    "  <url>",
                    f"    <loc>{BASE_URL}/blog/posts/{slug}/</loc>",
                    "    <changefreq>monthly</changefreq>",
                    "    <priority>0.7</priority>",
                    "  </url>",
                ]
            )
    # Also add all existing blog posts from filesystem
    for meta_path in sorted(POSTS_DIR.glob("*/metadata.json")):
        if meta_path.parent.name == "metadata.json":
            continue
        slug = meta_path.parent.name
        url = f"{BASE_URL}/blog/posts/{slug}/"
        if url in text or url in "\n".join(block):
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
    insertion = "\n".join(block) + "\n"
    text = text.replace("</urlset>", insertion + "</urlset>")
    sitemap.write_text(text, encoding="utf-8")


def main() -> None:
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
            write_metadata(slug, lang, data, alt_slug, category, read_time)
            write_image_prompt(slug, lang, data)
            write_index_html(slug, lang, data, alt_slug, category, read_time)
            generate_featured_image(assets / "featured.png", data["title"], accent)
            print(f"Created {slug}")

    update_posts_index()
    append_blog_to_sitemap()
    print("Updated posts/metadata.json and sitemap.xml")


if __name__ == "__main__":
    main()
