# auth-service Constitution

**Version:** 1.0.0 | **Ratified:** 2026-09-25 | **Last Amended:** 2026-09-25

## Principles

1. Evidence before implementation — reverse-engineer and record before claiming Implemented.
2. Secrets stay outside Git — never commit passwords, session keys, or Bearer tokens.
3. Administrative routes must remain authenticated — session-admin via role check; Bearer-admin via a real shared secret (**Target** until Implemented).
4. Closed role vocabulary — only `driver`, `pm`, `admin` unless Spec Kit + ontology + code change together.
5. Ontology complements runtime — Flask + SQLite + Werkzeug own auth correctness; OWL/SHACL own vocabulary and surface law.
6. Domain-affecting schema/entity/role/surface changes must update `.specify/spec.md` + `.specify/ontology/` and pass `validate_spec.py` in the same change set.
7. Do not describe Target behavior as Implemented.
8. MVP remains Deferred until the owner writes [mvp-definition.md](../specs/001-auth-service-baseline/mvp-definition.md).
9. Each Spec Kit baseline must leave evidence suitable for future agents (`.specify/evidence/`).
10. Prefer small, reviewable auth changes over silent credential reseeding surprises in production.

## Required validation (implementation phases)

When changing auth behavior, record:

- Git status before and after
- Tests run (when present)
- Files changed
- Security impact
- Remaining risks

## Amendments

Changes to this constitution require a PR with rationale and a SemVer bump:

- **MAJOR** — principle removal or incompatible redefinition
- **MINOR** — new principle or material expansion
- **PATCH** — clarification only
