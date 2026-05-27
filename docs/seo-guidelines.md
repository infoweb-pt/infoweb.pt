# SEO Guidelines — InfoWeb

Patterns and checklist for maintaining SEO quality when adding or updating pages.

## Canonical URL

Always use production domain:

```
https://infoweb.sousadev.com/
```

Never use GitHub Pages URLs in canonical, Open Graph, hreflang, or structured data.

## Meta description formula

- **Length:** 150–160 characters (max 165)
- **Structure:** Primary keyword in first 50 chars + value proposition + optional CTA
- **Language:** Match page language (PT pages get PT descriptions, not English)

```html
<meta name="description" content="Primary keyword here. Benefit statement and call to action if space allows." />
```

## Hreflang (bilingual pages)

For EN/PT page pairs, add after canonical:

```html
<link rel="alternate" hreflang="en" href="https://infoweb.sousadev.com/path/en/" />
<link rel="alternate" hreflang="pt" href="https://infoweb.sousadev.com/path/pt/" />
<link rel="alternate" hreflang="x-default" href="https://infoweb.sousadev.com/path/en/" />
```

For client-side i18n pages (homepage, affiliates) on a single URL:

```html
<link rel="alternate" hreflang="en" href="https://infoweb.sousadev.com/page/" />
<link rel="alternate" hreflang="pt" href="https://infoweb.sousadev.com/page/" />
<link rel="alternate" hreflang="x-default" href="https://infoweb.sousadev.com/page/" />
```

## Structured data (JSON-LD)

### Blog posts

Include `BlogPosting` + `BreadcrumbList`:

```
Home → Blog → Post Title
```

### Free tools

Include `WebApplication` + `BreadcrumbList`:

```
Home → Free Tools → Tool Name
```

Add `FAQPage` only when the page has visible question/answer content.

### Homepage

Use `@type: ["ProfessionalService", "LocalBusiness"]` with `addressCountry: "PT"`.

## Heading hierarchy

- Exactly **one `<h1>`** per page, matching the page topic
- Do not skip levels (H1 → H2 → H3, not H1 → H3)
- Blog posts: static `<h1 id="postTitle">` in HTML for crawlers; `post-loader.js` strips duplicate H1 from markdown

## Image alt text

Format: **context — subject — action/state**

```html
<!-- Good -->
<img alt="InfoWeb logo — managed websites for small businesses" />
<img alt="Henrique Sousa — InfoWeb founder and full-stack developer" />

<!-- Decorative only -->
<img alt="" role="presentation" />
```

## Internal linking

Each blog post and tool page should link to:

1. **3+ related pages** (thematically relevant posts or tools)
2. **Hub page** (`/blog/` or `/free-tools/`)
3. **Homepage pricing** where appropriate

Use descriptive anchor text, not "click here".

## New blog post checklist

- [ ] `metadata.json` with title, description, `alternateLanguage`
- [ ] Static H1 in `index.html` matching title
- [ ] Canonical + hreflang to language pair
- [ ] `BlogPosting` + `BreadcrumbList` JSON-LD
- [ ] Meta description 150–160 chars
- [ ] Featured image with descriptive `og:image:alt`
- [ ] **`assets/featured.png` generated** — run `python3 scripts/blog_featured_image.py blog/posts/[slug]/` before commit
- [ ] Related reading section with 3 internal links
- [ ] Add URL to `sitemap.xml`

## New free tool checklist

- [ ] EN and PT versions with bidirectional hreflang
- [ ] Canonical on `infoweb.sousadev.com`
- [ ] `WebApplication` + `BreadcrumbList` JSON-LD
- [ ] FAQ schema if page has FAQ section
- [ ] Related tools section in footer area
- [ ] One H1, mobile-friendly inputs (16px+ font on forms)
- [ ] Add both URLs to `sitemap.xml`

## Mobile usability

- Viewport meta on every page: `width=device-width, initial-scale=1.0`
- Touch targets minimum 44×44px
- Form inputs 16px+ font size (prevents iOS zoom)
- No horizontal scroll at 320px width
- Test with Chrome DevTools responsive mode before shipping

## Validation before deploy

1. [Google Rich Results Test](https://search.google.com/test/rich-results) on changed pages
2. Verify hreflang reciprocity on language pairs
3. Confirm no `hc-sousa.github.io` URLs remain
4. Check meta description length and uniqueness

## Automation

Run `python3 scripts/apply-seo-improvements.py` after bulk HTML changes to re-apply:

- Domain normalization
- Breadcrumb injection
- Related links blocks
- Alt text improvements
