# API contract — Auth Service Baseline

Base path: `/api/auth`  
**Implemented** unless marked otherwise.

## Public / session

| Method | Path | Auth | Request | Success |
|--------|------|------|---------|---------|
| POST | `/login` | None | `{email, password}` | 200: `{user_id, email, name, role}` + session |
| POST | `/logout` | Optional session | — | 200: `{message}` |
| GET | `/me` | Session | — | 200: `{user_id, email, name, role}` |
| GET | `/health` | None | — | 200: `{status: "healthy"}` |

Errors: 400 missing fields; 401 bad credentials / not authenticated; 404 user missing on `/me`.

## Session admin

| Method | Path | Auth | Request | Success |
|--------|------|------|---------|---------|
| POST | `/register` | Session + role `admin` | `{name, email, password, role?}` | 201 user; 409 duplicate email |
| GET | `/users` | Session + role `admin` | — | 200: `{users: [...]}` (no password hashes) |

Role must be `driver` | `pm` | `admin`.

## Bearer admin (microservices)

| Method | Path | Auth (Implemented) | Notes |
|--------|------|--------------------|-------|
| POST | `/admin/register_user` | Header starts with `Bearer ` | Password optional → `SHARED_PASSWORD` or `"aes"` |
| GET | `/admin/users` | Same | List users |
| DELETE | `/admin/users/<user_id>` | Same | Delete user |

**Target:** compare Bearer token to a configured secret. **Risk:** any non-empty Bearer prefix currently passes.

## Documented but missing

| Method | Path | Status |
|--------|------|--------|
| GET | `/verify` | Target — listed in `app.py` docstring only |

## Consumer example

See root `README.md` (`curl` / `requests` against `AUTH_SERVICE_URL`).
