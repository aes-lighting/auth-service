# Security — Auth Service Baseline

## Surfaces

| Surface | Control (Implemented) | Risk / Target |
|---------|----------------------|---------------|
| Public login | Password hash verify | Brute force / rate limit not Implemented |
| Session cookie | Signed Flask session, HttpOnly, Secure, SameSite=Lax | Needs HTTPS; no shared store |
| Session admin | Session + `role == admin` | Relies on session integrity |
| Bearer admin | Prefix `Bearer ` only | **Critical Target:** validate shared secret |
| Admin seed | Env-based recreate | Default password `aes` if env weak; deletes prior admin row |

## Secrets

Never commit: `FLASK_SECRET_KEY`, `ADMIN_PASSWORD`, `SHARED_PASSWORD`, Railway env, local `.env`.

`python-dotenv` is listed in `requirements.txt` but **not used** in `app.py` (note only).

## Password handling

- Store only Werkzeug hashes
- Do not return `password_hash` from list/me endpoints (Implemented)

## Gaps to track

1. Bearer admin authorization is not a real token check.
2. `/verify` absent despite docstring.
3. Logout logging uses `session["email"]` which login never sets.
4. Multi-worker gunicorn + cookie sessions without affinity/shared store.
5. SQLite durability on ephemeral containers.

## Agent rules

Per constitution: do not weaken auth in code without Target labeling and owner approval; do not commit secrets; update ontology when role/surface/schema changes.
