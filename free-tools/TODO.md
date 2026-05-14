# Free Tools — Build Backlog

Pipeline of free tools for local/small businesses (restaurants, clinics, salons, shops, freelancers). Each one is a standalone static page under `free-tools/[slug]/`, follows `TEMPLATE.md`, and funnels to InfoWeb plans via UTM links.

Legend: 🔥 high SEO/lead potential · ⚡ quick build (< 3h) · 🧠 needs API/AI · 💎 premium gateable report · 📱 uses Smart QR backend

> **Smart QR rule:** every tool that produces a QR code (WhatsApp, Wi-Fi, menu, vCard, booking, generic, etc.) MUST encode a short link served by our Django `smartqr` app — never the raw destination. This gives us scan analytics + the ability for the user to later edit the destination URL without reprinting. Spec: [`api/SMART-QR-CODE-TODO.md`](../api/SMART-QR-CODE-TODO.md).

---

## ✅ Already shipped

- [x] **WhatsApp link & QR generator** — `whatsapp-qr-generator/` &nbsp;⚠️ **needs migration to Smart QR backend** 📱
- [x] **Local presence score** — `presence-score/`
- [x] **Lost customers calculator** — `lost-customers-calculator/`

---

## 🚀 Next up — high priority

### Lead-gen & ROI calculators (great for B2B funnel)

- [ ] **Website ROI calculator** 🔥💎 — input avg. ticket + monthly visitors → projected extra revenue from having a proper site. Email-gated full PDF report.
- [ ] **"How much is your downtime costing you?" calculator** 🔥💎 — for shops/restaurants without online presence; estimates monthly lost orders.
- [ ] **Cost-per-lead calculator** ⚡ — ad spend ÷ leads → CPL, with industry benchmarks.
- [ ] **Customer Lifetime Value (LTV) calculator** ⚡ — avg ticket × visits/year × retention years.
- [ ] **Break-even calculator for small business** ⚡ — fixed costs, variable cost, price → break-even units/€.
- [ ] **Freelancer hourly rate calculator** 🔥 — desired salary + expenses + billable hours → minimum rate.
- [ ] **Markup vs margin calculator** ⚡ — converts between the two, shows final price.
- [ ] **VAT / IVA calculator (PT/EU rates)** 🔥⚡ — add/remove VAT at 6/13/23%. Massive search volume in PT.

### Local SEO / Google Business

- [ ] **Google Business Profile audit** 🔥🧠💎 — input business name + city, scrape/check public profile, score completeness (photos, hours, posts, reviews). Email-gated full action plan.
- [ ] **NAP consistency checker** 🔥🧠 — paste name/address/phone, checks across major directories.
- [ ] **Review response generator (AI)** 🔥🧠 — paste review text + tone → ready-to-post reply in PT/EN. Top funnel tool for restaurants/clinics.
- [ ] **Google review link generator** ⚡ — paste Place ID or business name → short shareable review link + QR.
- [ ] **Local keyword finder** 🧠 — niche + city → 20 long-tail keyword ideas with intent.
- [ ] **Schema.org local business generator** ⚡ — form → copy-paste JSON-LD snippet for `LocalBusiness`.

### WhatsApp / messaging utilities (extends existing tool family)

- [ ] **WhatsApp business hours auto-reply generator** ⚡ — form → ready-to-paste away-message text in PT/EN.
- [ ] **WhatsApp catalog link builder** ⚡ — products → formatted message with prices + emojis.
- [ ] **Click-to-call link + QR generator** ⚡📱 — phone → smart-QR short link wrapping `tel:`.
- [ ] **vCard / contact card QR** ⚡📱 — name, phone, email, web → smart-QR resolving to a hosted vCard download (editable later).
- [ ] **Wi-Fi QR generator** 🔥⚡ — SSID + password → standard `WIFI:` QR (cannot be a redirect, must stay raw so phones auto-join).

### Restaurant / hospitality

- [ ] **Menu QR generator** 🔥⚡📱 — paste menu URL (or upload PDF we host) → smart-QR for tables. Owner can swap the menu later without reprinting.
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

0. **Smart QR backend (`api/smartqr` Django app)** — prerequisite for every QR-based tool. See `api/SMART-QR-CODE-TODO.md`.
1. **Migrate WhatsApp QR generator** to smart-QR backend (replace raw `wa.me/...` payload with `https://infoweb.api.sousadev.com/q/<slug>`).
2. **Wi-Fi QR generator** — trivial build, massive search volume, perfect cousin to existing WhatsApp QR. (Stays raw, no backend.)
3. **VAT calculator (PT)** — huge organic traffic in PT, 1h build.
4. **Generic smart-QR generator** — once backend is up, this is the flagship lead magnet (analytics dashboard preview = upsell).
5. **Review response generator (AI)** — high-value, showcases AI, killer demo for restaurant/clinic owners.
6. **Website speed snapshot (gated)** — best lead-magnet of the bunch.
7. **Google Business Profile audit (gated)** — second lead magnet, pairs with `presence-score`.
