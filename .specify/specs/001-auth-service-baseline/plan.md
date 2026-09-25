# Plan — Spec Kit + ontology baseline (001)

**Date**: 2026-09-25 | **Spec**: [spec.md](./spec.md)

## Summary

Stand up hybrid Spec Kit (GitHub Spec Kit shapes + OWL/SHACL ontology program) reverse-engineered from the current auth-service tree. No production behavior changes in `app.py`.

## Technical context

| Item | Value |
|------|-------|
| Language | Python 3.12 |
| Primary file | `app.py` |
| Ontology prefix | `auth:` `https://aes-lighting.com/ns/auth#` |
| Validation | `.specify/scripts/validate_spec.py` |

## Constitution check

- [x] Secrets stay out of Git
- [x] Admin auth gaps labeled Target where weak
- [x] Role vocab closed in ontology enums
- [x] `validate_spec.py` required for ontology baseline

## Design

1. Author `.specify/` binding contract, memory, templates, Spec 001 prose.
2. Author `auth:` ontology kit + extract/generate/validate scripts.
3. Snapshot `users` DDL from `app.py`; regenerate TTL/enums.
4. Green three gates; evidence file; signed commit.

## Out of scope

- Changing Bearer validation or adding `/verify`
- Defining MVP
- CI workflow
