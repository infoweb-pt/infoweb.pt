# InfoWeb

A professional landing page for a "Website as a Service" business targeting small businesses in Portugal and internationally. Offers managed website plans with hosting, maintenance, and updates on a monthly billing cycle.

## Run & Operate

- **Start server:** `node server.js`
- **Port:** 5000
- **Verify GA4 is present on all HTML pages:** `bash scripts/check-html-ga.sh` (checks gtag + `assets/js/analytics.js`)
- **GA4 key events (admin):** see `docs/GA4-key-events.md`

## Stack

- Vanilla HTML5, CSS3, JavaScript
- Tailwind CSS (CDN)
- Custom i18n via `assets/js/scripts.js` + `locales/` JSON files
- Node.js static file server (`server.js`)

## Where things live

- `index.html` — Main landing page
- `assets/css/` — Custom stylesheets
- `assets/js/analytics.js` — shared `trackEvent`, scroll depth, `data-track` auto-binding
- `locales/en.json`, `locales/pt.json` — Translations
- `assets/images/` — Brand and decorative images
- `vendor/` — Bootstrap, jQuery and plugins
- `server.js` — Static file server for Replit

## Architecture decisions

- Pure static site — no build step required; served with a minimal Node.js HTTP server
- Multi-language (EN/PT) handled client-side by fetching locale JSON and swapping `data-i18n` attributes
- Tailwind loaded via CDN to avoid a build pipeline
- Deployment configured as `static` pointing to project root

## Product

- Landing page with pricing plans, payback ROI simulator, testimonials, FAQ
- Supports English and Portuguese via language toggle
- Early Bird promotional offer integration

## User preferences

_Populate as you build_

## Gotchas

- All static assets must be served from the project root
- Locale JSON files are fetched at runtime — ensure they are accessible from the server

## Pointers

- Tailwind CDN: https://cdn.tailwindcss.com
- FontAwesome via CDN in index.html
