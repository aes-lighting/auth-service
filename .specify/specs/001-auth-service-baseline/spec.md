# Spec 001 — Auth Service Baseline

**Feature Branch**: `main` (baseline reverse-engineering)  
**Created**: 2026-09-25  
**Status**: Implemented (as-built)  
**MVP**: [Deferred — see mvp-definition.md](./mvp-definition.md)

## Summary

Standalone authentication microservice for **AES Logistics**. Reverse-engineered from the live repository (`app.py`, `README.md`, Docker/Railway). Documents **as-built** behavior; does not invent an MVP.

## User scenarios

### US-1 Login (P1) — Implemented

Driver/PM/admin signs in with email + password and receives a session cookie plus JSON identity.

**Independent test:** `POST /api/auth/login` with valid credentials → 200 + `Set-Cookie`.

**Acceptance:**

1. **Given** a user row with matching password hash, **When** login with that email/password, **Then** 200 with `user_id`, `email`, `name`, `role` and `session["user_id"]` set.
2. **Given** bad credentials, **When** login, **Then** 401.

### US-2 Current user (P1) — Implemented

Authenticated client reads identity via session.

**Independent test:** `GET /api/auth/me` with session cookie.

### US-3 Logout (P2) — Implemented

Client clears session via `POST /api/auth/logout`.

### US-4 Session-admin user management (P1) — Implemented

Admin with session role `admin` registers users and lists users.

### US-5 Bearer-admin user management (P2) — Implemented (weak auth)

Microservice callers send `Authorization: Bearer …`. **Today only the Bearer prefix is checked** (Target: shared-secret validation).

### US-6 Health (P3) — Implemented

`GET /api/auth/health` → `{status: "healthy"}`.

### US-7 Token verify (P2) — Target / not Implemented

Module docstring lists `GET /api/auth/verify`; no route exists.

## Requirements

### Functional (Implemented)

- **FR-001**: Persist users in SQLite `users` table (email unique, role default `driver`).
- **FR-002**: Hash passwords with Werkzeug; never store plaintext.
- **FR-003**: Login sets permanent Flask session (`user_id`), lifetime 30 days.
- **FR-004**: Roles closed set: `driver`, `pm`, `admin`.
- **FR-005**: Session-admin routes require session + DB role `admin`.
- **FR-006**: Seed/refresh admin from `ADMIN_EMAIL` / `ADMIN_PASSWORD` on process init.
- **FR-007**: Expose health endpoint for deploy probes.

### Functional (Target)

- **FR-T01**: Validate Bearer token against a shared secret (or equivalent).
- **FR-T02**: Implement `GET /api/auth/verify` with defined semantics.
- **FR-T03**: Shared session store and/or Postgres for multi-instance.

### Non-goals (this baseline)

- OAuth/OIDC, MFA, password reset, email verification
- Defining MVP success metrics (Deferred)

## Key entities

- **User** — identity + role + password hash
- **SessionCredential** — Flask signed cookie holding `user_id`
- **Role** — closed enum individuals

## Success criteria

Baseline documentation success (this Spec Kit):

- **SC-DOC-001**: Spec Kit + ontology reflect as-built surfaces and pass `validate_spec.py`.

Product MVP success criteria: **Deferred** — see [mvp-definition.md](./mvp-definition.md).
