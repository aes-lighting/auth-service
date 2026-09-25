# Ontology baseline evidence — auth-service

**Date:** 2026-09-25  
**Version:** `auth:` 0.1.0-baseline  
**Status:** Baseline reverse-engineering closed

## What was reverse-engineered

| Source | Captured into |
|--------|----------------|
| `app.py` users DDL + routes + decorators | Spec 001 data-model, api-contract, security; schema snapshot |
| `README.md` | Product purpose, env vars, consumer notes |
| `Dockerfile` / `railway.json` | project-context + architecture |
| Role literals `driver`/`pm`/`admin` | ontology enums + axioms Role individuals |

## Surfaces recorded

- PublicAuthSurface / SessionAdminSurface / BearerAdminSurface (disjoint)
- Bearer prefix-only labeled Target / risk (not verified token auth)
- `GET /verify` documented as Target (not Implemented)
- MVP explicitly Deferred in `mvp-definition.md`

## Gates

Run:

```bash
python3 .specify/scripts/extract_schema_snapshot.py
python3 .specify/scripts/generate_ontology.py
python3 .specify/scripts/validate_spec.py
```

Expected: `ALL GATES PASSED` (contract + SHACL + OWL-RL).

## Neurosymbolic boundary

Ontology complements Flask + SQLite + Werkzeug; it does not replace password hashing, session crypto, or HTTP authorization decisions.
