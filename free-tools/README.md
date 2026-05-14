# Free tools (InfoWeb)

Static marketing utilities under GitHub Pages: one folder per tool, shared branding and analytics.

| Doc | Purpose |
|-----|---------|
| [TEMPLATE.md](TEMPLATE.md) | Full build spec: SEO, layout, API patterns, **Smart QR** (§5.1c), **QRCustomizer** + logo rules (§5.1d), analytics, QA. |
| [TODO.md](TODO.md) | Roadmap and shipped tools (kept in sync with the hub). |
| [index.html](index.html) | Public hub — every new tool needs a card here before “done”. |

**Backend:** [`api/SMART-QR-CODE-TODO.md`](../api/SMART-QR-CODE-TODO.md) describes the Django `smartqr` app (short links, scans, manage token). Production API base: `https://infoweb.api.sousadev.com`.

**Shared QR UI:** [`../assets/js/qr-customizer.js`](../assets/js/qr-customizer.js) — canvas QR + optional centre logo; enforces density-aware logo limits so codes stay scannable.

**QR tools today:** `whatsapp-qr-generator/`, `menu-qr-generator/`, `business-card-qr/`, `google-review-generator/` (each loads `qr-customizer.js` + uses Smart QR where the product is a redirect URL). **Supporting:** `qr-manage/`, `qr-example/`.
