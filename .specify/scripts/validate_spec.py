#!/usr/bin/env python3
"""Spec Kit ontology validation for auth-service.

Three labeled gates (all required):

  1. Spec Kit ontology contract validation — deps, files, markers, Turtle parse,
     schema snapshot freshness, generated TTL + enums, mapped class stubs
  2. SHACL instance validation — fixtures (valid + deliberate reject)
  3. OWL-RL TBox consistency — expansion + required probes
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ontology_map import ENTITY_OR_TABLE_TO_CLASS, ROLE_CODES  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SPECIFY = ROOT / ".specify"
ONTOLOGY = SPECIFY / "ontology"
APP = ROOT / "app.py"
SNAPSHOT = ONTOLOGY / "snapshots" / "schema.snapshot.json"
GENERATE = SCRIPTS / "generate_ontology.py"
EXTRACT = SCRIPTS / "extract_schema_snapshot.py"

REQUIRED_FILES = [
    SPECIFY / "spec.md",
    SPECIFY / "README.md",
    SPECIFY / "memory" / "constitution.md",
    SPECIFY / "memory" / "project-context.md",
    SPECIFY / "specs" / "001-auth-service-baseline" / "spec.md",
    SPECIFY / "specs" / "001-auth-service-baseline" / "data-model.md",
    SPECIFY / "specs" / "001-auth-service-baseline" / "api-contract.md",
    SPECIFY / "specs" / "001-auth-service-baseline" / "security.md",
    SPECIFY / "specs" / "001-auth-service-baseline" / "mvp-definition.md",
    ONTOLOGY / "README.md",
    ONTOLOGY / "auth_domain.ttl",
    ONTOLOGY / "auth_domain.generated.ttl",
    ONTOLOGY / "auth_domain.axioms.ttl",
    ONTOLOGY / "auth_domain.shacl.ttl",
    ONTOLOGY / "auth_domain.shacl.enums.ttl",
    ONTOLOGY / "catalog-v001.xml",
    ONTOLOGY / "fixtures" / "valid-user.ttl",
    ONTOLOGY / "fixtures" / "reject-bad-role.ttl",
    SNAPSHOT,
    SCRIPTS / "requirements.txt",
    SCRIPTS / "ontology_map.py",
    SCRIPTS / "extract_schema_snapshot.py",
    SCRIPTS / "generate_ontology.py",
    SCRIPTS / "validate_spec.py",
    SCRIPTS / "validate_instances.py",
    SCRIPTS / "validate_owl.py",
    SPECIFY / "evidence" / "ontology-baseline-2026-09-25.md",
]

REQUIRED_AXIOM_SNIPPETS = [
    "auth:PublicAuthSurface",
    "auth:SessionAdminSurface",
    "auth:BearerAdminSurface",
    "auth:AiRawAdvice",
    "owl:disjointWith",
    "auth:PolicyNoSecretsInGit",
    "auth:PolicyOntologyDoesNotReplaceRuntimeAuth",
    "auth:PolicyDoNotTreatBearerPrefixAsVerifiedToken",
    "auth:PolicyMvpDeferred",
    "auth:RoleDriver",
    "auth:RolePm",
    "auth:RoleAdmin",
]

REQUIRED_SPEC_SNIPPETS = [
    "Deferred",
    "TBD",
    "do not invent success criteria",
]


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def gate1_contract() -> None:
    print("=== Gate 1: Spec Kit ontology contract ===")
    missing = [str(p.relative_to(ROOT)) for p in REQUIRED_FILES if not p.exists()]
    if missing:
        fail("missing required files:\n  - " + "\n  - ".join(missing))

    try:
        import rdflib  # noqa: F401
        import pyshacl  # noqa: F401
        import owlrl  # noqa: F401
    except ImportError as exc:
        fail(f"ontology deps missing ({exc}); pip install -r .specify/scripts/requirements.txt")

    axioms = (ONTOLOGY / "auth_domain.axioms.ttl").read_text(encoding="utf-8")
    for snippet in REQUIRED_AXIOM_SNIPPETS:
        if snippet not in axioms:
            fail(f"axioms missing required snippet: {snippet}")

    mvp = (SPECIFY / "specs" / "001-auth-service-baseline" / "mvp-definition.md").read_text(
        encoding="utf-8"
    )
    for snippet in REQUIRED_SPEC_SNIPPETS:
        if snippet not in mvp:
            fail(f"mvp-definition.md missing required snippet: {snippet}")

    # Freshness: snapshot sha must match app.py
    app_sha = hashlib.sha256(APP.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
    snap = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    if snap.get("sourceSha256") != app_sha:
        fail(
            "schema snapshot stale vs app.py — run extract_schema_snapshot.py && generate_ontology.py"
        )
    if "AUTO-GENERATED" not in snap.get("$schemaComment", ""):
        fail("schema snapshot missing AUTO-GENERATED marker")

    if set(snap.get("roles") or []) != set(ROLE_CODES):
        fail(f"snapshot roles {snap.get('roles')} != ontology_map.ROLE_CODES {ROLE_CODES}")

    for table, cls in ENTITY_OR_TABLE_TO_CLASS.items():
        if table not in snap.get("tables", {}):
            fail(f"mapped table {table} missing from snapshot")
        if snap["tables"][table].get("class") != cls:
            fail(f"snapshot class for {table} != {cls}")

    generated = (ONTOLOGY / "auth_domain.generated.ttl").read_text(encoding="utf-8")
    if "AUTO-GENERATED" not in generated:
        fail("generated TTL missing AUTO-GENERATED marker")
    if app_sha[:12] not in generated and snap["sourceSha256"] not in generated:
        fail("generated TTL does not reference sourceSha256")
    for cls in ENTITY_OR_TABLE_TO_CLASS.values():
        if f"auth:{cls}" not in generated:
            fail(f"generated TTL missing class auth:{cls}")

    enums = (ONTOLOGY / "auth_domain.shacl.enums.ttl").read_text(encoding="utf-8")
    if "AUTO-GENERATED" not in enums:
        fail("enums TTL missing AUTO-GENERATED marker")
    for role in ROLE_CODES:
        if f'"{role}"' not in enums:
            fail(f"enums missing role {role}")

    # Turtle parse all ontology files
    from rdflib import Graph

    for name in (
        "auth_domain.ttl",
        "auth_domain.generated.ttl",
        "auth_domain.axioms.ttl",
        "auth_domain.shacl.ttl",
        "auth_domain.shacl.enums.ttl",
        "fixtures/valid-user.ttl",
        "fixtures/reject-bad-role.ttl",
    ):
        g = Graph()
        try:
            g.parse(ONTOLOGY / name, format="turtle")
        except Exception as exc:  # noqa: BLE001
            fail(f"Turtle parse failed for {name}: {exc}")

    print("OK: contract files, freshness, markers, Turtle parse")


def gate2_shacl() -> None:
    print("=== Gate 2: SHACL instances ===")
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "validate_instances.py")],
        cwd=ROOT,
        check=False,
    )
    if proc.returncode != 0:
        fail("validate_instances.py failed")
    print("OK: SHACL gate")


def gate3_owl() -> None:
    print("=== Gate 3: OWL-RL TBox ===")
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "validate_owl.py")],
        cwd=ROOT,
        check=False,
    )
    if proc.returncode != 0:
        fail("validate_owl.py failed")
    print("OK: OWL-RL gate")


def main() -> int:
    gate1_contract()
    gate2_shacl()
    gate3_owl()
    print("\nALL GATES PASSED")
    return 0


if __name__ == "__main__":
    # Avoid unused import warning for EXTRACT/GENERATE in static checkers
    _ = (EXTRACT, GENERATE)
    sys.exit(main())
