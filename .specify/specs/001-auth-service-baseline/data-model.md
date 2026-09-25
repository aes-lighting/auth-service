# Data model — Auth Service Baseline

**Source of truth (runtime):** [`app.py`](../../../app.py) `init_db()`  
**Ontology map:** `.specify/scripts/ontology_map.py` → `users` → `User`

## Table: `users`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Exposed as `user_id` in JSON |
| `email` | TEXT | UNIQUE NOT NULL | Normalized to lowercase on write/login |
| `name` | TEXT | NOT NULL | Display name |
| `password_hash` | TEXT | NOT NULL | Werkzeug hash; never returned in list/me JSON |
| `role` | TEXT | NOT NULL DEFAULT `'driver'` | Closed: `driver`, `pm`, `admin` |
| `created_at` | TEXT | NOT NULL | ISO timestamp string |
| `updated_at` | TEXT | NOT NULL | ISO timestamp string |

## Session model (not a DB table)

| Key | Storage | Notes |
|-----|---------|-------|
| `user_id` | Flask session cookie | Set on login; required by `login_required` / `admin_required` |
| `email` | — | **Not** set on login; logout log may show `"unknown"` |

Cookie flags: `SameSite=Lax`, `HttpOnly=True`, `Secure=True`, permanent lifetime 30 days.

## Admin seed behavior

On init, if `ADMIN_EMAIL` / `ADMIN_PASSWORD` are set (defaults exist), existing row with that email is **deleted** and a new `admin` user is inserted. Document as operational risk for production.

## Target persistence

- Managed Postgres instead of SQLite
- Shared session store (e.g. Redis) for multi-worker / multi-instance
