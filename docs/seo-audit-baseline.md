# SEO Audit Baseline — InfoWeb (2026-05-20)

Baseline inventory before implementing `docs/plans/2026-05-20-001-feat-comprehensive-seo-improvements-plan.md`.

**Source:** SEOptimer report for `infoweb.sousadev.com` (Grade B, 68%)

| Category | Grade | Notes |
|----------|-------|-------|
| On-Page SEO | A- | Strong meta tags, canonical URLs on main pages |
| Links | A- | Good footer navigation |
| Usability | F | SEOptimer score unreliable; manual mobile review recommended |
| Performance | A | Static site, CDN assets |
| Social | A+ | Open Graph and Twitter cards present |

## Page inventory

| Section | Pages | Language variants |
|---------|-------|-------------------|
| Homepage | 1 | EN/PT via client-side i18n (single URL) |
| Blog hub | 1 | PT primary |
| Blog posts | 8 | 4 EN + 4 PT pairs |
| Free tools hub | 2 | EN + PT |
| Free tools | 34 | 17 EN + 17 PT (excl. qr-example demo) |
| Affiliates | 1 | EN/PT via client-side i18n |

## Gaps identified (pre-implementation)

### Critical
- **Mixed canonical domain:** 37 free-tool pages used `hc-sousa.github.io/infoweb` instead of `infoweb.sousadev.com`
- **Missing hreflang:** `index.html`, `blog/index.html`, `affiliates/index.html`
- **Missing static H1:** All 8 blog posts (content loaded via JavaScript only)
- **No breadcrumb schema:** Blog posts and free tools

### Moderate
- **LocalBusiness schema:** Homepage had `ProfessionalService` only; no `addressCountry: PT`
- **Meta descriptions too long:** `free-tools/index.html`, PT hub, lost-customers, website-health-scorecard
- **PT meta in English:** `free-tools/pt/lost-customers-calculator/` description was English
- **Internal linking:** No related content sections on blog posts or tools
- **Generic alt text:** Logo images used bare `"InfoWeb"` without context

### Already good
- `robots.txt` allows crawling, references sitemap
- `sitemap.xml` lists all public URLs on `infoweb.sousadev.com`
- Blog post pairs have bidirectional hreflang
- Most free-tool pairs have hreflang
- FAQ schema on tools with visible FAQ sections (WhatsApp QR, Wi-Fi QR, VAT, etc.)
- All images had alt attributes (quality varied)

## Heading hierarchy

| Page type | H1 status (pre-fix) |
|-----------|---------------------|
| Homepage | 1 H1 ✓ |
| Blog hub | 1 H1 ✓ |
| Blog posts | 0 H1 (JS-rendered from markdown `#` heading) |
| Free tools | 1 H1 each ✓ |

## Implementation tracking

See commit implementing this plan for resolved items. Post-implementation validation:

- [ ] Google Rich Results Test on homepage structured data
- [ ] Hreflang validator on bilingual page pairs
- [ ] Mobile Lighthouse usability check
- [ ] Re-run SEOptimer after deploy
