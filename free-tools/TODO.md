# Free Tools — Build Backlog

Pipeline of free tools for local/small businesses (restaurants, clinics, salons, shops, freelancers). Each one is a standalone static page under `free-tools/[slug]/`, follows `TEMPLATE.md`, and funnels to InfoWeb plans via UTM links.

Legend: 🔥 high SEO/lead potential · ⚡ quick build (< 3h) · 🧠 needs API/AI · 💎 premium gateable report · 📱 uses Smart QR backend

> **Smart QR rule:** every tool that produces a **redirect** QR code (WhatsApp, menu, review, booking, generic URL, etc.) MUST encode a short link served by our Django `smartqr` app — never the raw destination. **Exception:** payloads the OS must read verbatim (e.g. `WIFI:` for Wi-Fi join). Spec: [`api/SMART-QR-CODE-TODO.md`](../api/SMART-QR-CODE-TODO.md).

---

## ✅ Already shipped

- [x] **WhatsApp link & QR generator** — `whatsapp-qr-generator/` 📱 Creates a **Smart QR** short link via `POST https://infoweb.api.sousadev.com/smartqr/codes/` (`tool_source: whatsapp_qr`); printable QR encodes the short URL + optional centre logo. Optional email lead → `/leads/tool-contact/`.
- [x] **Menu QR generator** — `menu-qr-generator/` 📱 Menu PDF upload → public URL via API upload; Smart QR short link for the menu URL (`tool_source: menu_qr`); shared `QRCustomizer` + logo safety caps.
- [x] **Digital business card (vCard) QR** — `business-card-qr/` 📱 vCard payload in QR; centre logo via `QRCustomizer` (declare `uploadedLogo` in script state; strict mode).
- [x] **Google review link + QR** — `google-review-generator/` Smart QR + review URL flow; logo optional.
- [x] **Website ROI calculator** — `website-roi-calculator/` (no Smart QR — not a scan-to-redirect QR product).
- [x] **Local presence score** — `presence-score/`
- [x] **Lost customers calculator** — `lost-customers-calculator/`
- [x] **QR manage UI (static)** — `qr-manage/` — reads `slug` + `token` query params; calls Smart QR manage API with `X-Manage-Token` (see spec).
- [x] **QR example landing** — `qr-example/` — safe demo target for previews.
- [x] **Wi-Fi QR generator** — `wifi-qr-generator/` Raw `WIFI:` string in QR (phones auto-join) — **exception** to Smart QR rule; optional centre logo via `QRCustomizer`; optional email → `/leads/tool-contact/` (`wifi_qr_generator`).
- [x] **IVA / VAT calculator (PT)** — `vat-calculator-pt/` Continente / Madeira / Açores rates; add or remove IVA; client-side only.
- [x] **Markup vs margin calculator** — `markup-margin-calculator/` Cost + margin or markup or price → full breakdown; client-side only.

**Shared frontend:** `assets/js/qr-customizer.js` — canvas QR (qrcode-generator), error correction **H**, **density-aware logo cap** + module-aligned knockout so centre logos stay scannable across all tools.

**Deferred (no OpenAI in stack for now)**

- **Review response generator (AI)** — not shipped; requires hosted LLM. Revisit if/when we add an approved API path and budget.


---

## 🚀 Next up — high priority

### Lead-gen & ROI calculators (great for B2B funnel)

- [x] **Website ROI calculator** 🔥💎 — shipped as `website-roi-calculator/` (calculator only; not a Smart QR surface).
- [ ] **"How much is your downtime costing you?" calculator** 🔥💎 — for shops/restaurants without online presence; estimates monthly lost orders.
- [ ] **Cost-per-lead calculator** ⚡ — ad spend ÷ leads → CPL, with industry benchmarks.
- [ ] **Customer Lifetime Value (LTV) calculator** ⚡ — avg ticket × visits/year × retention years.
- [ ] **Break-even calculator for small business** ⚡ — fixed costs, variable cost, price → break-even units/€.
- [ ] **Freelancer hourly rate calculator** 🔥 — desired salary + expenses + billable hours → minimum rate.
- [x] **Markup vs margin calculator** ⚡ — shipped as `markup-margin-calculator/`.
- [x] **VAT / IVA calculator (PT/EU rates)** 🔥⚡ — shipped as `vat-calculator-pt/` (Continente / Madeira / Açores).

### Local SEO / Google Business

- [ ] **Google Business Profile audit** 🔥🧠💎 — input business name + city, scrape/check public profile, score completeness (photos, hours, posts, reviews). Email-gated full action plan.
- [ ] **NAP consistency checker** 🔥🧠 — paste name/address/phone, checks across major directories.
- [ ] **Review response generator (AI)** 🔥🧠 — **SKIP FOR NOW** (no OpenAI / server LLM). Paste review + tone → reply in PT/EN. Revisit when product approves model + spend.
- [x] **Google review link generator** ⚡ — shipped as `google-review-generator/` (Smart QR + optional logo).
- [ ] **Local keyword finder** 🧠 — niche + city → 20 long-tail keyword ideas with intent.
- [ ] **Schema.org local business generator** ⚡ — form → copy-paste JSON-LD snippet for `LocalBusiness`.

### WhatsApp / messaging utilities (extends existing tool family)

- [ ] **WhatsApp business hours auto-reply generator** ⚡ — form → ready-to-paste away-message text in PT/EN.
- [ ] **WhatsApp catalog link builder** ⚡ — products → formatted message with prices + emojis.
- [ ] **Click-to-call link + QR generator** ⚡📱 — phone → smart-QR short link wrapping `tel:`.
- [x] **vCard / contact card QR** ⚡📱 — shipped as `business-card-qr/` (vCard in QR; centre logo; destination is the encoded payload — swap “hosted vCard URL” later if product needs edit-in-place without reprint).
- [x] **Wi-Fi QR generator** 🔥⚡ — shipped as `wifi-qr-generator/` (`WIFI:` QR only; raw payload, not Smart QR).

### Restaurant / hospitality

- [x] **Menu QR generator** 🔥⚡📱 — shipped as `menu-qr-generator/` (upload + Smart QR short link).
- [ ] **Food cost / plate margin calculator** ⚡ — ingredients + price → margin %.
- [ ] **Reservation no-show cost calculator** 💎 — covers/week × avg ticket × no-show rate → annual loss.
- [ ] **Tip split calculator** ⚡ — bill + people + % → per-person split.

### Salons / clinics / personal services

- [ ] **Appointment cancellation cost calculator** 💎 — slots/week × fee × cancel rate → monthly bleed.
- [ ] **Booking link + QR generator** ⚡📱 — paste Calendly/Bookings link → smart-QR for window/posters (editable destination).
- [ ] **GDPR consent text generator (PT/EN)** 🔥⚡ — form fields used → ready-to-paste consent line for booking forms.

### Content & copy helpers (AI-powered)

- [ ] **Instagram bio generator for local businesses** 🔥🧠 — niche + city + USP → 5 bio options w/ emojis.
- [ ] **"About us" paragraph generator** 🧠 — questionnaire → polished About text in PT/EN.
- [ ] **Meta title + description generator** 🔥🧠 — page topic → 5 SEO-ready combos with character counts.
- [ ] **Slogan / tagline generator** 🧠 — business + tone → 10 options.
- [ ] **Email signature generator** ⚡ — form → HTML signature, copy-to-clipboard.

### Branding & design utilities

- [ ] **Brand colour palette extractor** ⚡ — upload logo → extract dominant colours + hex codes + Tailwind config snippet.
- [ ] **Favicon generator** ⚡ — upload PNG → multi-size favicon pack zip.
- [ ] **Logo contrast checker** ⚡ — upload logo → tells you if it works on dark/light backgrounds.
- [ ] **OG image generator** 🔥⚡ — title + subtitle + brand colour → 1200×630 PNG download. (Eat our own dog food.)

### Web/perf checks

- [ ] **Website speed snapshot** 🔥🧠💎 — paste URL → call PageSpeed Insights API, show 3 KPIs + fixes. Email-gated full report.
- [ ] **Mobile-friendly checker** 🧠 — URL → screenshot at 375px + checklist.
- [ ] **SSL / HTTPS checker** ⚡ — domain → cert validity + expiry warning.
- [ ] **Domain age & WHOIS lookup** 🧠 — domain → registration date + registrar.
- [ ] **Broken-link finder (single page)** 🧠 — URL → list of 4xx/5xx links.

### Social & sharing

- [ ] **Link-in-bio page generator** 🔥 — form → static HTML "linktree" they can host anywhere, with QR.
- [ ] **UTM link builder** 🔥⚡ — pre-filled with InfoWeb conventions; copy + shorten.
- [ ] **QR generator (generic with logo overlay)** ⚡📱 — any URL → smart-QR with centre logo, full scan analytics, swappable destination.

### Pricing & finance

- [ ] **Subscription pricing calculator** ⚡ — costs + target margin + churn → monthly price.
- [ ] **Discount / promo calculator** ⚡ — original price + % off → final + savings, copyable for posts.
- [ ] **Loan / financing simulator (PT rates)** 🔥 — amount + months + TAN → monthly + total cost.

### Productivity micro-tools (SEO long tail)

- [ ] **Slug generator** ⚡ — text → SEO-friendly slug.
- [ ] **Lorem-ipsum in Portuguese** ⚡ — paragraphs of pt-PT placeholder text.
- [ ] **Character / word counter** ⚡ — for meta descriptions, tweets, etc.
- [ ] **Image compressor (client-side)** ⚡ — drag image → smaller version, no upload.
- [ ] **Colour contrast checker (WCAG)** ⚡ — fg + bg → AA/AAA pass/fail.

---

## Backlog — nice to have

- [ ] Invoice number generator (sequential, with prefix)
- [ ] PT NIF validator
- [ ] IBAN validator + bank lookup (PT)
- [ ] CAE (Portuguese activity code) lookup
- [ ] Easy holiday calculator for PT (next bank holidays for planning campaigns)
- [ ] "When to post on Instagram" — best-time suggester by industry
- [ ] Ad budget allocator (Meta vs Google split based on goal)
- [ ] Domain name brainstormer (AI) — niche → 20 available `.pt` / `.com` ideas

---

## Build order suggestion

0. **Smart QR backend (`api/smartqr` Django app)** — live. Spec: [`api/SMART-QR-CODE-TODO.md`](../api/SMART-QR-CODE-TODO.md). Public redirect: `GET https://infoweb.api.sousadev.com/q/<slug>` (or path under configured public base).
1. **WhatsApp / menu / review / vCard tools** — wired to Smart QR + shared `QRCustomizer`; keep new QR tools consistent (see `TEMPLATE.md` §5.1c–5.1d).
2. **Wi-Fi QR generator** — trivial build, massive search volume, perfect cousin to existing WhatsApp QR. (Stays raw, no backend.)
3. **VAT calculator (PT)** — huge organic traffic in PT, 1h build.
4. **Generic smart-QR generator** — once backend is up, this is the flagship lead magnet (analytics dashboard preview = upsell).
5. **Review response generator (AI)** — high-value, showcases AI, killer demo for restaurant/clinic owners.
6. **Website speed snapshot (gated)** — best lead-magnet of the bunch.
7. **Google Business Profile audit (gated)** — second lead magnet, pairs with `presence-score`.
