# InfoWeb Lead Capture API

Minimal Django REST API that stores email leads from the free tools on the InfoWeb site.

## Endpoints

| Method | Path | Tool | Payload |
|--------|------|------|---------|
| POST | `/leads/lost-customers/` | Lost Customers Calculator | `{email, weekly_loss, monthly_loss}` |
| POST | `/leads/presence-score/` | Online Presence Score | `{email, score, answers}` |
| POST | `/leads/website-health-scorecard/` | Website Health Scorecard | `{email, url, score, checks, fixes}` |
| POST | `/leads/competitor-visibility-gap/` | Competitor Visibility Gap | `{email, score, answers}` |
| POST | `/leads/tool-contact/` | Free-tool contact CTA | `{email, source}` — `source` ∈ `whatsapp_qr_generator`, `wifi_qr_generator` |

Deployed base URL: **`https://infoweb.api.sousadev.com`** — e.g. `https://infoweb.api.sousadev.com/leads/lost-customers/`.

Returns `200 OK` on success, `400 Bad Request` with validation errors on failure.

## Setup

From the `api/` directory:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Apply database migrations
python manage.py migrate

# 3. Create an admin user to access /admin/
python manage.py createsuperuser

# 4. Start the dev server (port 8001 to avoid conflict with the front-end on 5000)
python manage.py runserver 8001
```

The admin panel is at **http://localhost:8001/admin/** — log in with the superuser credentials to view and search all leads.

## Configuration

Set these environment variables (or create a `.env` file in `api/`) before deploying:

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | insecure dev key | Django secret key — **must change in production** |
| `DEBUG` | `True` | Set to `False` in production |
| `ALLOWED_HOSTS` | `*` | Comma-separated list of allowed hostnames |
| `CORS_ALLOW_ALL_ORIGINS` | `True` | Set to `False` and configure `CORS_ALLOWED_ORIGINS` in production |

## Wiring the front-end

Production: set **`API_ENDPOINT`** at the top of each tool script to the full HTTPS URL (GitHub Pages needs an absolute URL for browser `fetch`):

- [`free-tools/lost-customers-calculator/script.js`](../free-tools/lost-customers-calculator/script.js) → `https://infoweb.api.sousadev.com/leads/lost-customers/`
- [`free-tools/presence-score/script.js`](../free-tools/presence-score/script.js) → `https://infoweb.api.sousadev.com/leads/presence-score/`
- [`free-tools/website-health-scorecard/script.js`](../free-tools/website-health-scorecard/script.js) → `https://infoweb.api.sousadev.com/leads/website-health-scorecard/`
- [`free-tools/competitor-visibility-gap/script.js`](../free-tools/competitor-visibility-gap/script.js) → `https://infoweb.api.sousadev.com/leads/competitor-visibility-gap/`
- [`free-tools/whatsapp-qr-generator/script.js`](../free-tools/whatsapp-qr-generator/script.js) → `https://infoweb.api.sousadev.com/leads/tool-contact/` (`source: whatsapp_qr_generator`)
- [`free-tools/wifi-qr-generator/script.js`](../free-tools/wifi-qr-generator/script.js) → `https://infoweb.api.sousadev.com/leads/tool-contact/` (`source: wifi_qr_generator`)

Local dev: swap to `http://localhost:8001/leads/.../` when running `python manage.py runserver 8001` from `api/`.
