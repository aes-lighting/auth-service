# Spec Kit Index — AES Auth Service

Navigation for the binding Spec Kit under `.specify/`. Conventions follow GitHub Spec Kit shapes plus the ontology program used in sibling AES / IV projects.

**Status legend:** **Implemented** | **Target** | **Roadmap** | **Deferred**

## Start here

| Artifact | Role | Status |
|----------|------|--------|
| [spec.md](./spec.md) | Binding agent & domain contract | Implemented |
| [memory/constitution.md](./memory/constitution.md) | Non-negotiable principles | Implemented |
| [memory/project-context.md](./memory/project-context.md) | Stack, deploy, integration baseline | Implemented |
| [ontology/](./ontology/) | OWL + SHACL auth domain (`auth:`) | Implemented |
| [specs/001-auth-service-baseline/](./specs/001-auth-service-baseline/) | Reverse-engineered baseline product spec | Implemented |
| [specs/001-auth-service-baseline/mvp-definition.md](./specs/001-auth-service-baseline/mvp-definition.md) | MVP success criteria | Deferred |

## Specs

| Spec | Title |
|------|-------|
| [001](./specs/001-auth-service-baseline/) | Auth service baseline (current codebase) |

## Operations

| Command | Purpose |
|---------|---------|
| `python3 .specify/scripts/validate_spec.py` | Three-gate ontology contract + SHACL + OWL-RL |
| `.specify/scripts/run_validate_spec.sh` | Same via local venv if present |
| `python3 .specify/scripts/extract_schema_snapshot.py` | Refresh schema snapshot from `app.py` |
| `python3 .specify/scripts/generate_ontology.py` | Regenerate generated TTL + role enums |

## Conventions

- **Implemented** — true of the live `app.py` / deploy config today.
- **Target** — intended hardening; not yet true in code.
- **Roadmap** — future product direction.
- **Deferred** — deliberately undefined (e.g. MVP) until owner update.

Human-readable architecture notes (non-binding): [`../spec-kit/`](../spec-kit/).
