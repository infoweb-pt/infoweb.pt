#!/usr/bin/env python3
"""Apply common PT-PT string replacements to free-tools/pt/*/index.html (body copy)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PT = ROOT / "free-tools" / "pt"

# (English or mixed, Portuguese) — order matters for longer phrases first
REPLACEMENTS: list[tuple[str, str]] = [
    ("See Website Plans →", "Ver planos →"),
    ("See Website Plans", "Ver planos"),
    ("All free tools", "Todas as ferramentas"),
    ("Main site", "Site principal"),
    ("Frequently asked questions", "Perguntas frequentes"),
    ("Frequently Asked Questions", "Perguntas frequentes"),
    (
        "Something went wrong. Please try again in a moment.",
        "Algo correu mal. Tente novamente daqui a momentos.",
    ),
    ("Try again", "Tentar novamente"),
    ("Built by", "Criado por"),
    ("Helping local businesses grow online.", "A apoiar negócios locais a crescer online."),
    ("Free — No sign-up needed", "Grátis — sem registo"),
    ("Free · no sign-up", "Grátis · sem registo"),
    ("Liked how easy that was?", "Gostou da simplicidade?"),
    (
        "Your business website can work just as smoothly.",
        "O site do seu negócio pode ser igualmente simples.",
    ),
    (
        "InfoWeb builds, hosts and maintains your site for a flat monthly rate.",
        "A InfoWeb cria, aloja e mantém o seu site por uma mensalidade fixa.",
    ),
    (
        "InfoWeb builds simple, fast websites for local businesses — flat monthly fee.",
        "A InfoWeb cria sites simples e rápidos para negócios locais — mensalidade fixa.",
    ),
    ("Need a site that explains your pricing clearly?", "Precisa de um site que explique os seus preços com clareza?"),
    ("Copy to clipboard", "Copiar para a área de transferência"),
    ("Copy", "Copiar"),
    ("Calculate", "Calcular"),
    ("Generating your result…", "A gerar o resultado…"),
    ("Building your QR…", "A criar o QR…"),
    ("Your Result", "O seu resultado"),
    ("Tool Input", "Entrada"),
    ("Your result", "O seu resultado"),
    ("Notify me", "Avisem-me"),
    ("Sending…", "A enviar…"),
    ("Thanks — you’re on the list.", "Obrigado — fica na lista."),
    ("Please enter a valid email.", "Introduza um e-mail válido."),
    ("Could not save — try again shortly.", "Não foi possível guardar — tente daqui a pouco."),
    ("Please enter your email.", "Introduza o seu e-mail."),
    ("Leave your email", "Deixe o seu e-mail"),
    ("Scan with your camera to connect", "Leia com a câmara para ligar"),
    ("Print poster", "Imprimir poster"),
    ("Download PNG", "Descarregar PNG"),
    ("Copy payload", "Copiar payload"),
    ("Encoded payload", "Payload codificado"),
    ("Wi-Fi", "Wi‑Fi"),
    ("Customize QR", "Personalizar QR"),
    ("Live preview", "Pré-visualização"),
    ("Network name (SSID)", "Nome da rede (SSID)"),
    ("Password", "Palavra-passe"),
    ("Security type", "Tipo de segurança"),
    ("WPA / WPA2 personal", "WPA / WPA2 pessoal"),
    ("Open network (no password)", "Rede aberta (sem palavra-passe)"),
    ("Hidden network (SSID not broadcast)", "Rede oculta (SSID não anunciado)"),
    ("Show password on printable poster", "Mostrar palavra-passe no poster"),
    ("QR colour", "Cor do QR"),
    ("Background", "Fundo"),
    ("Dot style", "Estilo dos pontos"),
    ("Square", "Quadrado"),
    ("Rounded", "Arredondado"),
    ("Dots", "Pontos"),
    ("Logo (optional)", "Logótipo (opcional)"),
    ("Upload logo (PNG with transparency)", "Carregar logótipo (PNG com transparência)"),
    ("Frame text (optional)", "Texto da moldura (opcional)"),
    ("Generate Wi-Fi QR — It’s Free", "Gerar QR Wi‑Fi — é grátis"),
    (
        "Guests scan once and join your Wi-Fi — no typing passwords. Works on iPhone and Android. Raw Wi-Fi QR (not a redirect link).",
        "Os convidados leem uma vez e ligam-se ao Wi‑Fi — sem escrever palavras-passe. iPhone e Android. QR Wi‑Fi em texto cru (não é um link de redirecionamento).",
    ),
    (
        "Wi-Fi QR Code Generator for Your Business",
        "Gerador de QR Code Wi‑Fi para o seu negócio",
    ),
    (
        "Want a website that matches this polish?",
        "Quer um site com o mesmo nível de acabamento?",
    ),
    (
        "Leave your email — we’ll send occasional tips for local businesses. No spam.",
        "Deixe o seu e-mail — enviamos dicas pontuais para negócios locais. Sem spam.",
    ),
    (
        "This is the raw string inside the QR. Phones read it directly — it is <strong class=\"text-slate-300\">not</strong> a Smart QR short link (by design for Wi-Fi).",
        "É o texto cru dentro do QR. Os telemóveis leem diretamente — <strong class=\"text-slate-300\">não</strong> é um link curto Smart QR (por desenho, para Wi‑Fi).",
    ),
    ("InfoWeb home", "Início InfoWeb"),
    ("← Back to tools", "← Todas as ferramentas"),
    ("Loading your QR code stats...", "A carregar estatísticas do QR…"),
    ("Access Denied", "Acesso recusado"),
    ("Invalid or expired manage token.", "Token de gestão inválido ou expirado."),
    ("Your QR Code Stats", "Estatísticas do seu QR"),
    ("Track how many people scan your QR code", "Veja quantas pessoas leem o seu QR"),
    ("Active", "Ativo"),
    ("Total Scans", "Leituras totais"),
    ("Unique Visitors", "Visitantes únicos"),
    ("QR Code Details", "Detalhes do QR"),
    ("Short URL", "URL curto"),
    ("Target URL", "URL de destino"),
    ("Created", "Criado"),
    ("Last 7 days", "Últimos 7 dias"),
    ("Last 30 days", "Últimos 30 dias"),
    ("Last 90 days", "Últimos 90 dias"),
    ("Devices", "Dispositivos"),
    ("Top Countries", "Principais países"),
    ("Scans Over Time", "Leituras ao longo do tempo"),
    ("Loading...", "A carregar…"),
    ("No data yet", "Ainda sem dados"),
    (" scans", " leituras"),
]


def main() -> None:
    for p in sorted(PT.glob("*/index.html")):
        raw = p.read_text(encoding="utf-8")
        out = raw
        for en, pt in REPLACEMENTS:
            out = out.replace(en, pt)
        if out != raw:
            p.write_text(out, encoding="utf-8")
            print("bulk", p.parent.name)


if __name__ == "__main__":
    main()
