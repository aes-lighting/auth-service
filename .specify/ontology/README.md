# Auth Domain Ontology — auth-service

Formal OWL/RDFS + SHACL package for the AES Auth Service. **Ontological maintenance is required** for domain changes — see [../spec.md](../spec.md).

**Status:** `0.1.0-baseline` (reverse-engineered from `app.py`).

## IRI namespace

| Prefix | IRI |
|--------|-----|
| `auth:` | `https://aes-lighting.com/ns/auth#` |

Open [auth_domain.ttl](./auth_domain.ttl) in Protégé. Prefer Turtle in Git.

## Files

| File | Maintainer | Purpose |
|------|------------|---------|
| [auth_domain.ttl](./auth_domain.ttl) | Thin catalog | `owl:imports` generated + axioms |
| [auth_domain.generated.ttl](./auth_domain.generated.ttl) | **Regenerated** | Classes/properties from schema snapshot |
| [auth_domain.axioms.ttl](./auth_domain.axioms.ttl) | Human | Surfaces, disjointness, agent must-nots |
| [auth_domain.shacl.ttl](./auth_domain.shacl.ttl) | Human | Instance shapes |
| [auth_domain.shacl.enums.ttl](./auth_domain.shacl.enums.ttl) | **Regenerated** | Role `sh:in` lists |
| [catalog-v001.xml](./catalog-v001.xml) | Protégé | Catalog |
| [fixtures/](./fixtures/) | Human | Valid + deliberate-reject graphs |
| [snapshots/](./snapshots/) | **Regenerated** | Schema extract + freshness hash |

Do **not** hand-edit `auth_domain.generated.ttl`, `auth_domain.shacl.enums.ttl`, or committed schema snapshots. Edit `app.py` DDL / curated axioms, then regenerate.

## Neurosymbolic ownership

| Layer | Owns | Does not own |
|-------|------|--------------|
| **OWL-RL** | TBox consistency | HTTP auth correctness |
| **SHACL** | Type, closed roles, fixtures | Password hashing, session crypto |
| **Flask + SQLite + Werkzeug** | Login, sessions, hashes, HTTP | Spec Kit graph conceptualization |
| **Agents** | Propose changes | Auto-deploy credential policy |
| **Human owner** | Acceptance, production secrets | — |

## Roles (closed)

`driver` | `pm` | `admin`

## Validate

```bash
pip install -r .specify/scripts/requirements.txt
python3 .specify/scripts/validate_spec.py
```
