# Agent & Domain Contract — auth-service

> **Binding.** This document is the universal Spec Kit contract for **every** human and AI agent working on this repository (Cursor agents, CI bots, and future workers). Informal prompts do not override it.

**Incorporation by reference (normative):**

| Artifact | Role |
|----------|------|
| [ontology/auth_domain.ttl](./ontology/auth_domain.ttl) | OWL catalog (`owl:imports` generated structure + curated axioms) |
| [ontology/auth_domain.generated.ttl](./ontology/auth_domain.generated.ttl) | Regenerated structural TBox from live schema snapshot |
| [ontology/auth_domain.axioms.ttl](./ontology/auth_domain.axioms.ttl) | Curated OWL constraints (disjoint surfaces, agent must-nots) |
| [ontology/auth_domain.shacl.ttl](./ontology/auth_domain.shacl.ttl) | SHACL shapes for projected instance / fixture validation |
| [ontology/auth_domain.shacl.enums.ttl](./ontology/auth_domain.shacl.enums.ttl) | Regenerated blocking role `sh:in` lists |
| [memory/constitution.md](./memory/constitution.md) | Non-negotiable project principles |
| [memory/project-context.md](./memory/project-context.md) | Stack and deployment baseline |
| [specs/001-auth-service-baseline/](./specs/001-auth-service-baseline/) | Reverse-engineered product baseline |

## 1. Purpose

**AES Auth Service** is the standalone authentication microservice for **AES Logistics**. It owns user identity storage, email/password login, Flask session cookies, and role-based access (`driver`, `pm`, `admin`).

Runtime authority for passwords, sessions, and HTTP behavior remains **Flask + SQLite + Werkzeug** in [`app.py`](../app.py). The Spec Kit ontology complements that authority; it does **not** replace it.

## 2. Surfaces (must not collapse)

| Surface | Auth mode (Implemented) | Routes |
|---------|-------------------------|--------|
| Public / session auth | None or session cookie | `/login`, `/logout`, `/me`, `/health` |
| Session admin | Session + DB role `admin` | `/register`, `/users` |
| Bearer admin | `Authorization: Bearer …` **prefix only** (Target: real secret) | `/admin/*` |

Documented but **not Implemented:** `GET /api/auth/verify`.

Agents must label Bearer-prefix-only behavior as **Target / risk** until code validates a shared secret or equivalent.

## 3. Ontology maintenance

Domain-affecting schema, entity, role, or surface changes must update this Spec Kit (`.specify/spec.md` + `.specify/ontology/`) and pass `python3 .specify/scripts/validate_spec.py` in the **same change set**.

## 4. Agent must-nots

1. Do not commit secrets (`FLASK_SECRET_KEY`, `ADMIN_PASSWORD`, `SHARED_PASSWORD`, `.env`).
2. Do not invent auth bypasses or weaken session/admin checks without an explicit Target spec and owner approval.
3. Do not treat ontology / SHACL success as proof of secure HTTP auth.
4. Do not auto-deploy production credential or auth-policy changes from unreviewed AI output.
5. Do not redefine MVP success criteria in code comments — update [mvp-definition.md](./specs/001-auth-service-baseline/mvp-definition.md) when the owner defines it.

## 5. IRI prefix

| Prefix | IRI |
|--------|-----|
| `auth:` | `https://aes-lighting.com/ns/auth#` |

## 6. Validation

```bash
python3 .specify/scripts/validate_spec.py
# or
.specify/scripts/run_validate_spec.sh
```

Three gates (all required): contract → SHACL instances → OWL-RL TBox.
