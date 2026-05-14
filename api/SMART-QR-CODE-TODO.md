# Smart QR Code — Django App TODO

A new Django app (`smartqr`) under `api/` that issues short-link QR codes whose destination is **dynamic** (owner can change it later) and whose every scan is **logged with rich analytics** (device, OS, browser, geo, referrer, timestamp).

Used by every QR-producing free tool (WhatsApp, generic, vCard, menu, booking, click-to-call, …) and later as a paid product feature for InfoWeb customers.

---

## 1. Goals

1. **Short, brandable redirect URLs** — `https://infoweb.api.sousadev.com/q/<slug>` → 302 to the current target.
2. **Dynamic destinations** — owner edits the target URL at any time; printed QRs keep working.
3. **Per-scan analytics** — store every hit with device/OS/browser, country (best-effort from IP), referrer, UTM params, language, timestamp. NEVER store the raw IP after enrichment (GDPR).
4. **Owner dashboard** — list of QRs with totals, recent scans, top devices/countries/days. Export CSV.
5. **Anonymous / claim-later flow** — a free-tool user can create a QR without an account; a one-time `manage_token` is returned. They can later claim it by registering with the email tied to it.
6. **Abuse + safety** — rate-limit creation, block known phishing domains on target update, basic URL safe-browsing check (later).
7. **Optional features (later):** A/B target rotation, geo-based targeting, scheduled targets, password-protected QRs, expiry dates.

---

## 2. URL design

| Path | Purpose |
|---|---|
| `GET  /q/<slug>` | Public redirect endpoint. 302 → current target. Logs the scan. |
| `POST /smartqr/codes/` | Create a new smart QR (anonymous OK). Returns `{slug, short_url, manage_token}`. |
| `GET  /smartqr/codes/<slug>/` | Owner-scoped: code metadata + summary stats. Auth via `manage_token` header or session. |
| `PATCH /smartqr/codes/<slug>/` | Update target URL, label, or active flag. |
| `DELETE /smartqr/codes/<slug>/` | Soft-delete (sets `is_active=False`, keeps stats). |
| `GET  /smartqr/codes/<slug>/scans/` | Paginated raw scan log. |
| `GET  /smartqr/codes/<slug>/stats/` | Aggregates: totals, by day/device/country/browser/referrer. |
| `POST /smartqr/codes/<slug>/claim/` | Attach an authenticated user (or `email`) as the owner — consumes `manage_token`. |

**Redirect path is short on purpose** (`/q/<slug>`, not `/smartqr/q/<slug>`) — slugs are 6–8 chars, base62. Mount `smartqr.urls` at root for `/q/` and at `/smartqr/` for the management API.

---

## 3. Data model

### 3.1 `SmartQRCode`

| Field | Type | Notes |
|---|---|---|
| `id` | UUID PK | |
| `slug` | `CharField(8, unique, db_index)` | base62; collision-retry on create. |
| `target_url` | `URLField(2048)` | The current destination. Validated, scheme must be `http`/`https`/`tel`/`mailto`/`whatsapp`. |
| `label` | `CharField(120, blank)` | Owner-facing name ("Table 4 menu"). |
| `tool_source` | `CharField(64)` | Which free tool created it: `whatsapp_qr`, `menu_qr`, `vcard_qr`, `generic`, … |
| `owner_user` | `FK(User, null=True)` | Set after claim. |
| `owner_email` | `EmailField(null=True)` | Captured at create or claim, used for magic-link recovery. |
| `manage_token` | `CharField(48, unique)` | Secret, returned once at create; used to manage anonymously. Hashed at rest (`make_password` style). |
| `is_active` | `BooleanField(default=True)` | When False, redirect serves a friendly "this QR is no longer active" page (200, not 404, so phones don't show errors). |
| `password_hash` | `CharField(null=True)` | Optional gate. (Phase 2.) |
| `expires_at` | `DateTimeField(null=True)` | Optional. |
| `created_at` / `updated_at` | timestamps | |
| `created_ip_hash` | `CharField(64)` | sha256(ip + secret), for rate-limit + abuse only. Never the raw IP. |

Indexes: `slug`, `owner_user`, `tool_source`, `created_at`.

### 3.2 `SmartQRScan`

One row per scan (high write volume — keep it lean, no FKs beyond the code).

| Field | Type | Notes |
|---|---|---|
| `id` | BigAutoField | |
| `code` | `FK(SmartQRCode, on_delete=CASCADE, db_index)` | |
| `created_at` | `DateTimeField(auto_now_add, db_index)` | |
| `ip_hash` | `CharField(64)` | sha256(ip + daily-rotating salt) — enables "unique scans / day" without storing IPs. |
| `country` | `CharField(2, blank)` | ISO-3166-1 alpha-2, from GeoIP / Cloudflare `CF-IPCountry` header. |
| `city` | `CharField(120, blank)` | Optional, only with paid GeoIP. |
| `user_agent_raw` | `CharField(512)` | Truncated UA string. |
| `device_type` | `CharField(16)` | `mobile`, `tablet`, `desktop`, `bot`, `other`. |
| `os_family` | `CharField(32)` | `iOS`, `Android`, `Windows`, `macOS`, `Linux`, `other`. |
| `os_version` | `CharField(32, blank)` | |
| `browser_family` | `CharField(32)` | `Chrome`, `Safari`, `Firefox`, `Edge`, `Samsung Internet`, `WhatsApp`, … |
| `browser_version` | `CharField(32, blank)` | |
| `is_bot` | `BooleanField(default=False)` | UA-based heuristic. |
| `referrer` | `CharField(512, blank)` | `Referer` header. |
| `language` | `CharField(16, blank)` | Primary `Accept-Language`. |
| `utm_source` / `utm_medium` / `utm_campaign` | `CharField(64, blank)` | Lifted from query string before redirect. |

Partition mentally by `code_id + created_at`. If volume explodes, move to TimescaleDB or rollup tables (see §6).

### 3.3 `SmartQRDailyRollup` (phase 2)

Pre-aggregated rows per `(code, day, country, device_type, os_family, browser_family)` to keep dashboard queries cheap when raw scans pass ~1M.

---

## 4. Endpoints — request/response shapes

### `POST /smartqr/codes/`

```json
// Request
{
  "target_url": "https://wa.me/351912345678?text=Hi",
  "label": "Front-window QR",
  "tool_source": "whatsapp_qr",
  "owner_email": "owner@cafe.pt"   // optional
}

// Response 201
{
  "slug": "Ax9k2P",
  "short_url": "https://infoweb.api.sousadev.com/q/Ax9k2P",
  "manage_url": "https://infoweb.sousadev.com/free-tools/qr/manage/?slug=Ax9k2P&token=...",
  "manage_token": "<secret, show ONCE>",
  "qr_png_url": "https://infoweb.api.sousadev.com/q/Ax9k2P.png?size=512&logo=1"
}
```

### `GET /q/<slug>`

- 302 to `target_url` (with original query string merged, so UTMs from a campaign URL survive).
- Async-fires a scan log entry (`transaction.on_commit` + Django `Q`/Celery later, or just inline with `bulk_create` buffered).
- If `is_active=False` or `expires_at` past → 200 to a static "This QR is no longer active" page (with subtle InfoWeb upsell).
- If `password_hash` set → 200 to a small password-prompt page that POSTs back, then redirects.

### `GET /q/<slug>.png`

- Serves the QR PNG itself (so the static site doesn't have to bundle a QR lib for shareable URLs).
- Query params: `size` (px, 128–1024), `logo` (`0|1`), `ec` (error correction `L|M|Q|H`, default `M`; force `H` if logo overlay).
- Cache aggressively (immutable for 1 year, slug is permanent).

### `GET /smartqr/codes/<slug>/stats/?range=7d`

```json
{
  "totals": { "scans": 1284, "unique": 612 },
  "by_day":     [{ "date": "2026-05-07", "scans": 145, "unique": 80 }, …],
  "by_device":  [{ "key": "mobile",  "scans": 1100 }, { "key": "desktop", "scans": 184 }],
  "by_os":      [{ "key": "iOS",     "scans": 612 },  { "key": "Android", "scans": 488 }],
  "by_browser": [{ "key": "Safari",  "scans": 530 },  { "key": "Chrome",  "scans": 420 }],
  "by_country": [{ "key": "PT",      "scans": 1100 }, { "key": "ES",      "scans": 90  }],
  "by_referrer":[{ "key": "direct",  "scans": 900  }, { "key": "instagram.com", "scans": 200 }]
}
```

---

## 5. Implementation TODO

### Phase 1 — MVP (ship with WhatsApp QR migration)

- [ ] `python manage.py startapp smartqr` under `api/`.
- [ ] Add `'smartqr'` to `INSTALLED_APPS`.
- [ ] Models: `SmartQRCode`, `SmartQRScan` + initial migration.
- [ ] Slug generator (base62, 6 chars, retry on `IntegrityError`).
- [ ] `manage_token` generated with `secrets.token_urlsafe(32)`, hashed with `django.contrib.auth.hashers.make_password` before store.
- [ ] Add `qrcode[pil]` and `user-agents` to `requirements.txt`.
- [ ] DRF serializers + viewsets:
  - [ ] `SmartQRCodeCreateSerializer` — validates `target_url` scheme + length, `tool_source` in allowed set.
  - [ ] `SmartQRCodeUpdateSerializer` — `target_url`, `label`, `is_active` only.
  - [ ] `SmartQRScanSerializer` — read-only.
- [ ] Permissions: anonymous create allowed; manage requires `X-Manage-Token` header matching hash, OR authenticated owner.
- [ ] Public redirect view `GET /q/<slug>`:
  - [ ] Look up by slug (cache the row in Django cache for 60s — hot path).
  - [ ] Build scan record from request (UA parsing via `user_agents`, country from `CF-IPCountry` if present else GeoIP2).
  - [ ] Hash IP with daily salt (`HMAC-SHA256(daily_salt, ip)`).
  - [ ] Strip `utm_*` from incoming query, store on scan, forward the rest to target.
  - [ ] `transaction.on_commit(lambda: SmartQRScan.objects.create(...))` so a scan never blocks the redirect; if it errors, log + continue.
  - [ ] Return `HttpResponseRedirect` with `Cache-Control: no-store`.
- [ ] PNG view `GET /q/<slug>.png` with size/logo/ec params, served with `Cache-Control: public, max-age=31536000, immutable`.
- [ ] Stats endpoint with raw-SQL `GROUP BY` (Postgres `date_trunc` for `by_day`).
- [ ] Rate limit: max 10 creates / hour per `created_ip_hash` (DRF throttling).
- [ ] CORS: ensure `https://hc-sousa.github.io` (and the future custom domain) is in `CORS_ALLOWED_ORIGINS`.
- [ ] Admin: register both models, with inline scan preview (last 100) + scan totals on the code list.
- [ ] Tests:
  - [ ] Create code returns slug + token; token is single-use printable, not stored raw.
  - [ ] Redirect 302s and increments scan count.
  - [ ] UA parsing: iPhone Safari → `mobile / iOS / Safari`.
  - [ ] Bot UA → `is_bot=True`, **excluded** from `unique` counts.
  - [ ] Update target with valid token works; with wrong token → 401.
  - [ ] Inactive code returns the friendly 200 page, not a redirect.

### Phase 2 — Owner UX

- [ ] Static "Manage your QR" page under `free-tools/qr/manage/` — stores `manage_token` in `localStorage`, calls the management API.
- [ ] Magic-link claim by email (1-hour signed link via `django.core.signing`).
- [ ] CSV export of scan log.
- [ ] Owner dashboard chart (Chart.js, no SPA).

### Phase 3 — Power features

- [ ] Multiple targets per code (A/B 50/50, weighted, geo-based, scheduled).
- [ ] Password-protected QRs.
- [ ] Expiry dates.
- [ ] Custom slug (vanity URLs, paid).
- [ ] Custom domain (`qr.<owner-domain>` via CNAME, paid).
- [ ] Daily rollup table + cron + dashboards switch over once raw scans > 500k.
- [ ] Webhook on scan (paid).

---

## 6. Privacy & GDPR

- **Never persist raw IPs.** Hash with rotating daily salt; salt itself rotates and is not retained beyond 30 days, so re-identification becomes impossible.
- **Country only**, no precise geo unless paid plan opts in.
- Scan retention default: **180 days** for raw rows; aggregates kept indefinitely. Configurable per code.
- Provide a `DELETE /smartqr/codes/<slug>/scans/` endpoint to wipe scan history on owner request (right-to-erasure).
- Add a public `/smartqr/privacy` short notice describing what's logged.

---

## 7. Performance notes

- Redirect view is the hot path. Goals: **< 30 ms** server-side, single cached DB read.
- Use `select_related` nowhere on redirect — single column lookup `slug → (id, target_url, is_active, expires_at)`.
- Cache slug → row in Redis (`smartqr:slug:<slug>`, TTL 60s, busted on PATCH).
- Scan write is fire-and-forget via `on_commit` (Phase 1 inline create, Phase 2 batched via Celery + Redis queue if QPS justifies it).
- Add DB indexes: `(code_id, created_at)`, `(country)`, `(device_type)`.

---

## 8. Frontend integration contract (used by every QR free tool)

In each tool's `script.js`:

```js
const API = 'https://infoweb.api.sousadev.com';

async function createSmartQR({ target_url, label, tool_source, owner_email }) {
  const r = await fetch(`${API}/smartqr/codes/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ target_url, label, tool_source, owner_email })
  });
  if (!r.ok) throw new Error('smartqr_create_failed');
  return r.json(); // { slug, short_url, manage_url, manage_token, qr_png_url }
}
```

Tools then:

1. Build the **real** payload (e.g. `https://wa.me/351...?text=...`).
2. Call `createSmartQR({ target_url: payload, tool_source: 'whatsapp_qr', ... })`.
3. Render `<img src={qr_png_url}>` and a "Download PNG" link.
4. Show the `manage_url` + token to the user with copy-button + warning ("save this — it's the only way to edit your QR later without registering").
5. Encourage the user to drop their email so we send `manage_url` automatically (lead capture).

---

## 9. Migration: WhatsApp QR generator

- [ ] Replace client-side QR-of-`wa.me/...` with: POST to `/smartqr/codes/` first, then render QR of returned `short_url` (or use `qr_png_url` directly).
- [ ] Keep a "raw QR (no analytics)" toggle for users who explicitly don't want a backend redirect — defaults OFF.
- [ ] Show a tiny "📊 This QR includes free scan analytics — manage it here: [link]" line under the QR.
- [ ] Optional email field: "Email me the manage link" → also creates a `ToolContactLead` (existing model) with `source='whatsapp_qr_smartqr'`.
- [ ] Update `free-tools/whatsapp-qr-generator/index.html` copy + add manage-link UI.
- [ ] Update analytics: fire `smartqr_created` event in addition to existing ones.

---

*Spec v1 — owner: Sousa Dev. Build order: Phase 1 → migrate WhatsApp QR → roll out to other QR tools.*
