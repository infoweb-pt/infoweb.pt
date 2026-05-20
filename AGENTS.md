# AGENTS.md

## Cursor Cloud specific instructions

### Architecture

- **Frontend**: Static HTML/CSS/JS site (vanilla + Tailwind CDN) served by `server.js` (Node.js, port 5000)
- **Backend**: Django REST API in `api/` (port 8001) with two apps: `leads` (email capture) and `smartqr` (dynamic QR codes)
- The Node server proxies `/api/*` requests to Django at `localhost:8001`

### Running services

```bash
# Django API (from repo root)
cd api && /workspace/.venv/bin/python manage.py runserver 8001

# Static frontend + API proxy
node server.js
```

Visit `http://localhost:5000` for full site, `http://localhost:8001/admin/` for Django admin.

### Testing

```bash
# All Django tests (44 tests, runs in ~13s)
cd api && /workspace/.venv/bin/python manage.py test
```

### Key details

- No linter is configured in this project. `python manage.py check` is the closest system validation.
- Django defaults to SQLite (`api/db.sqlite3`) when `DATABASE_URL` is not set — no Postgres needed for dev.
- The `pyproject.toml` at root manages core Python deps via `uv sync`, but `api/requirements.txt` has additional runtime deps (`whitenoise`, `qrcode[pil]`, `user-agents`, `gunicorn`) that must also be installed.
- The Node.js `server.js` has zero npm dependencies — just run `node server.js`.
