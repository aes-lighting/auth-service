# Project context — auth-service

## Identity

| Field | Value |
|-------|-------|
| Repository | `aes-lighting/auth-service` |
| Product | AES Auth Service (AES Logistics) |
| Language | Python 3.12 |
| Framework | Flask 2.3.3 + Flask-CORS |
| WSGI | gunicorn (Docker) |
| Database | SQLite (`DATABASE_URL`, default `auth.db`) |
| Passwords | Werkzeug PBKDF2 |
| Sessions | Flask signed cookie (`user_id`), 30-day permanent |
| Deploy | Docker → Railway (`railway.json`) |

## Layout

| Path | Role |
|------|------|
| `app.py` | Entire application (routes, DB, decorators) |
| `requirements.txt` | Runtime deps |
| `Dockerfile` | Production image |
| `railway.json` | Railway builder config |
| `README.md` | Human setup / API overview |
| `.specify/` | Binding Spec Kit + ontology |
| `spec-kit/` | Non-binding human architecture notes |

## Environment

| Variable | Notes |
|----------|-------|
| `FLASK_SECRET_KEY` | Required in prod; random hex if unset (sessions break on restart) |
| `DATABASE_URL` | SQLite path |
| `ADMIN_EMAIL` / `ADMIN_PASSWORD` | Seed/refresh admin on startup |
| `SHARED_PASSWORD` | Default password for Bearer admin register when body omits password |
| `PORT` | Default `5000` |

## Consumer integration

Downstream apps call this service (e.g. `AUTH_SERVICE_URL`) for login; session cookies require credentialed CORS and HTTPS for `Secure` cookies.

## Known gaps (Target / Roadmap)

- `GET /api/auth/verify` documented, not Implemented
- Bearer admin routes check prefix only (no shared-secret compare)
- SQLite + in-memory Flask sessions are multi-instance fragile
- Admin seed deletes/recreates admin by email on every process init
