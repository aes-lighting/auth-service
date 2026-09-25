#!/usr/bin/env python3
"""SHACL instance validation for auth-service Spec Kit ontology."""

from __future__ import annotations

import sys
from pathlib import Path

from rdflib import Graph
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[2]
ONTOLOGY = ROOT / ".specify" / "ontology"


def load_shapes() -> Graph:
    g = Graph()
    for name in (
        "auth_domain.generated.ttl",
        "auth_domain.shacl.enums.ttl",
        "auth_domain.shacl.ttl",
    ):
        g.parse(ONTOLOGY / name, format="turtle")
    return g


def main() -> int:
    shapes = load_shapes()
    ok = True

    valid_path = ONTOLOGY / "fixtures" / "valid-user.ttl"
    data = Graph()
    data.parse(valid_path, format="turtle")
    conforms, _, results_text = validate(
        data_graph=data,
        shacl_graph=shapes,
        inference="rdfs",
        abort_on_first=False,
        meta_shacl=False,
        advanced=True,
        inplace=False,
    )
    if not conforms:
        print("FAIL: valid-user.ttl should conform")
        print(results_text)
        ok = False
    else:
        print("OK: fixtures/valid-user.ttl conforms")

    reject_path = ONTOLOGY / "fixtures" / "reject-bad-role.ttl"
    bad = Graph()
    bad.parse(reject_path, format="turtle")
    # Bind role shape: validate User nodes against UserShape which references RoleCodeEnumShape
    conforms_bad, _, results_bad = validate(
        data_graph=bad,
        shacl_graph=shapes,
        inference="rdfs",
        abort_on_first=False,
        meta_shacl=False,
        advanced=True,
        inplace=False,
    )
    if conforms_bad:
        print("FAIL: reject-bad-role.ttl should NOT conform")
        print(results_bad)
        ok = False
    else:
        print("OK: fixtures/reject-bad-role.ttl correctly rejected")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
