#!/usr/bin/env python3
"""Generate InfoWeb blog featured.png OG images (1200x630)."""

from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CATEGORY_ACCENTS = {
    "domains-hosting": "#d7b46a",
    "web-design": "#d7b46a",
    "seo": "#38bdf8",
    "digital-marketing": "#22c55e",
    "small-business": "#f97316",
    "tutorials": "#a78bfa",
    "case-studies": "#fb7185",
    "company-news": "#94a3b8",
}

DEFAULT_ACCENT = "#d7b46a"
FONT_BOLD_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
]
FONT_REGULAR_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/TTF/DejaVuSans.ttf",
]


def static_title(title: str) -> str:
    return title.replace("{{CURRENT_YEAR}}", "2026")


def accent_for_category(category: str | None, slug: str = "") -> str:
    if category and category in CATEGORY_ACCENTS:
        base = CATEGORY_ACCENTS[category]
    else:
        base = DEFAULT_ACCENT
    if not slug:
        return base
    # Slight variation per slug while staying on-brand
    variants = ["#d7b46a", "#fbbf24", "#38bdf8", "#22c55e", "#f97316"]
    return variants[sum(ord(c) for c in slug) % len(variants)]


def load_font(candidates: list[str], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def generate_featured_image(
    path: Path,
    title: str,
    accent: str | None = None,
    *,
    category: str | None = None,
    slug: str = "",
) -> Path:
    """Render featured.png and return the output path."""
    if accent is None:
        accent = accent_for_category(category, slug)

    width, height = 1200, 630
    img = Image.new("RGB", (width, height), "#020617")
    draw = ImageDraw.Draw(img)

    for i in range(height):
        ratio = i / height
        r = int(2 + (15 - 2) * ratio)
        g = int(6 + (23 - 6) * ratio)
        b = int(23 + (42 - 23) * ratio)
        draw.line([(0, i), (width, i)], fill=(r, g, b))

    draw.ellipse((820, -80, 1180, 260), fill=(40, 35, 20))
    draw.rounded_rectangle((70, 120, 620, 520), radius=28, outline=accent, width=4, fill=(15, 23, 42))
    draw.rounded_rectangle((110, 170, 580, 250), radius=12, fill=accent)
    draw.rounded_rectangle((110, 280, 520, 320), radius=8, fill=(51, 65, 85))
    draw.rounded_rectangle((110, 340, 480, 380), radius=8, fill=(51, 65, 85))
    draw.rounded_rectangle((110, 400, 400, 440), radius=8, fill=(51, 65, 85))

    font = load_font(FONT_BOLD_CANDIDATES, 34)
    small = load_font(FONT_REGULAR_CANDIDATES, 22)

    draw.text((110, 188), "InfoWeb Blog", fill="#020617", font=small)
    lines = textwrap.wrap(static_title(title), width=28)
    y = 290
    for line in lines[:3]:
        draw.text((110, y), line, fill="#e2e8f0", font=font)
        y += 42

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG", optimize=True)
    return path


def generate_from_metadata(post_dir: Path, *, force: bool = False) -> Path | None:
    meta_path = post_dir / "metadata.json"
    if not meta_path.exists():
        return None
    out = post_dir / "assets" / "featured.png"
    if out.exists() and not force:
        return None

    import json

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    title = meta.get("title", post_dir.name.replace("-", " ").title())
    category = meta.get("category")
    generate_featured_image(
        out,
        title,
        category=category,
        slug=post_dir.name,
    )
    return out


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate blog featured.png OG images")
    parser.add_argument(
        "paths",
        nargs="*",
        help="Post directory or repo root (default: regenerate all missing under blog/posts/)",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing featured.png")
    args = parser.parse_args()

    if not args.paths:
        roots = [Path(__file__).resolve().parents[1] / "blog" / "posts"]
    else:
        roots = [Path(p) for p in args.paths]

    count = 0
    for root in roots:
        if (root / "metadata.json").exists():
            out = root / "assets" / "featured.png"
            if out.exists() and not args.force:
                continue
            generate_from_metadata(root, force=True)
            print(out)
            count += 1
            continue
        for post_dir in sorted(root.glob("*/")):
            if not (post_dir / "metadata.json").exists():
                continue
            featured = post_dir / "assets" / "featured.png"
            if featured.exists() and not args.force:
                continue
            result = generate_from_metadata(post_dir, force=args.force)
            if result:
                print(result)
                count += 1
    print(f"Generated {count} featured image(s)")
