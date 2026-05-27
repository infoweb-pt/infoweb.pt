#!/usr/bin/env python3
"""Regenerate missing blog featured images and spread publish dates."""

from __future__ import annotations

import json
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from blog_featured_image import generate_from_metadata

REPO = Path(__file__).resolve().parents[1]
POSTS_DIR = REPO / "blog" / "posts"

# Topic pairs in publish order (oldest → newest). EN + PT share the same date.
TOPIC_PAIRS: list[tuple[str, str]] = [
    ("choosing-perfect-domain", "como-escolher-dominio-perfeito"),
    ("domain-name-checklist", "checklist-comprar-dominio"),
    ("small-business-website-cost", "quanto-custa-website-pequena-empresa"),
    ("cheap-websites-expensive-later", "websites-baratos-ficam-caros"),
    ("need-website-if-have-instagram", "precisa-website-se-tem-instagram"),
    ("small-business-homepage-checklist", "checklist-homepage-pequeno-negocio"),
    ("website-maintenance-checklist", "checklist-manutencao-website"),
    ("local-seo-checklist-small-business", "checklist-seo-local-pequenos-negocios"),
    ("optimize-google-business-profile", "otimizar-perfil-empresa-google"),
    ("get-more-google-reviews-small-business", "como-conseguir-mais-avaliacoes-google"),
    ("whatsapp-for-business-complete-guide", "whatsapp-para-negocios-guia-completo"),
    ("restaurant-menu-qr-code-guide", "guia-qr-code-menu-restaurante"),
    ("website-speed-small-business-guide", "guia-velocidade-website-pequenos-negocios"),
    ("when-to-redesign-small-business-website", "quando-redesenhar-website-pequeno-negocio"),
    ("seo-title-meta-description-guide", "guia-titulo-meta-description-seo"),
    ("online-presence-score-guide", "guia-score-presenca-online"),
    ("website-health-audit-small-business", "auditoria-saude-website-pequeno-negocio"),
    ("website-roi-calculator-guide", "guia-calculadora-roi-website"),
    ("smart-qr-codes-small-business", "qr-codes-inteligentes-pequenos-negocios"),
    ("restaurant-menu-pricing-guide", "guia-precos-ementa-restaurante"),
    ("iva-vat-portugal-small-business", "iva-portugal-guia-pequenos-negocios"),
    ("utm-campaign-tracking-guide", "guia-rastrear-campanhas-utm"),
]

# Irregular gaps (~weekly, not exact) from early January 2026
DAY_GAPS = [0, 6, 8, 5, 9, 7, 6, 10, 5, 8, 6, 9, 7, 5, 6, 8, 5, 7, 6, 9, 5, 8]


def build_publish_schedule() -> dict[str, str]:
    schedule: dict[str, str] = {}
    current = date(2026, 1, 6)
    for idx, (en_slug, pt_slug) in enumerate(TOPIC_PAIRS):
        if idx < len(DAY_GAPS):
            if idx > 0:
                current += timedelta(days=DAY_GAPS[idx])
        iso = current.isoformat()
        schedule[en_slug] = iso
        schedule[pt_slug] = iso
    return schedule


def update_index_html_dates(index_path: Path, iso_date: str) -> bool:
    text = index_path.read_text(encoding="utf-8")
    original = text

    text = re.sub(
        r'(<meta property="article:published_time" content=")[^"]+(")',
        rf"\g<1>{iso_date}T00:00:00Z\2",
        text,
        count=1,
    )
    text = re.sub(
        r'(<meta property="article:modified_time" content=")[^"]+(")',
        rf"\g<1>{iso_date}T00:00:00Z\2",
        text,
        count=1,
    )
    text = re.sub(r'("datePublished": ")[^"]+(")', rf"\g<1>{iso_date}\2", text, count=1)
    text = re.sub(r'("dateModified": ")[^"]+(")', rf"\g<1>{iso_date}\2", text, count=1)

    if text != original:
        index_path.write_text(text, encoding="utf-8")
        return True
    return False


def apply_schedule(schedule: dict[str, str]) -> None:
    index_entries: list[dict] = []

    for slug, iso_date in schedule.items():
        post_dir = POSTS_DIR / slug
        meta_path = post_dir / "metadata.json"
        if not meta_path.exists():
            print(f"skip missing metadata: {slug}")
            continue

        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        meta["dateCreated"] = iso_date
        meta["dateUpdated"] = iso_date
        meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        index_html = post_dir / "index.html"
        if index_html.exists():
            update_index_html_dates(index_html, iso_date)

        index_entries.append(
            {
                "slug": slug,
                "language": meta.get("language", "en"),
                "dateCreated": iso_date,
                "dateUpdated": iso_date,
            }
        )
        print(f"dated {slug} → {iso_date}")

    index_entries.sort(key=lambda e: (e["dateCreated"], e["slug"]), reverse=True)
    payload = {
        "posts": index_entries,
        "lastUpdated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }
    (POSTS_DIR / "metadata.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def regenerate_missing_featured() -> list[str]:
    created: list[str] = []
    for post_dir in sorted(POSTS_DIR.iterdir()):
        if not post_dir.is_dir():
            continue
        featured = post_dir / "assets" / "featured.png"
        if featured.exists():
            continue
        result = generate_from_metadata(post_dir)
        if result:
            created.append(post_dir.name)
            print(f"featured {post_dir.name}")
    return created


def main() -> None:
    created = regenerate_missing_featured()
    schedule = build_publish_schedule()
    apply_schedule(schedule)
    print(f"Done: {len(created)} featured images, {len(schedule)} dates updated")


if __name__ == "__main__":
    main()
