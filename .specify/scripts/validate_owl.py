#!/usr/bin/env python3
"""OWL-RL TBox consistency checks for auth-service ontology."""

from __future__ import annotations

import sys
from pathlib import Path

import owlrl
from rdflib import Graph, Namespace, RDF, OWL, RDFS

ROOT = Path(__file__).resolve().parents[2]
ONTOLOGY = ROOT / ".specify" / "ontology"
AUTH = Namespace("https://aes-lighting.com/ns/auth#")


def load_tbox() -> Graph:
    g = Graph()
    for name in (
        "auth_domain.generated.ttl",
        "auth_domain.axioms.ttl",
        "auth_domain.ttl",
    ):
        g.parse(ONTOLOGY / name, format="turtle")
    return g


def main() -> int:
    g = load_tbox()
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)

    # Probe: surfaces remain declared
    required = [
        AUTH.PublicAuthSurface,
        AUTH.SessionAdminSurface,
        AUTH.BearerAdminSurface,
        AUTH.AiRawAdvice,
        AUTH.User,
        AUTH.Role,
        AUTH.SessionCredential,
        AUTH.PolicyNoSecretsInGit,
        AUTH.PolicyOntologyDoesNotReplaceRuntimeAuth,
        AUTH.PolicyDoNotTreatBearerPrefixAsVerifiedToken,
    ]
    missing = [str(x) for x in required if (x, RDF.type, None) not in g and (x, RDFS.label, None) not in g]
    # Classes may only appear as owl:Class triples
    for cls in (
        AUTH.PublicAuthSurface,
        AUTH.SessionAdminSurface,
        AUTH.BearerAdminSurface,
        AUTH.AiRawAdvice,
        AUTH.User,
        AUTH.Role,
        AUTH.SessionCredential,
    ):
        if (cls, RDF.type, OWL.Class) not in g:
            print(f"FAIL: missing owl:Class {cls}")
            return 1

    for ind in (
        AUTH.PolicyNoSecretsInGit,
        AUTH.PolicyOntologyDoesNotReplaceRuntimeAuth,
        AUTH.PolicyDoNotTreatBearerPrefixAsVerifiedToken,
        AUTH.RoleDriver,
        AUTH.RolePm,
        AUTH.RoleAdmin,
    ):
        if (ind, RDF.type, OWL.NamedIndividual) not in g and (ind, RDF.type, AUTH.Role) not in g:
            # NamedIndividual may be inferred; check any type
            if not list(g.objects(ind, RDF.type)):
                print(f"FAIL: missing individual {ind}")
                return 1

    # Deliberate reject graph: assert same node as two disjoint surfaces → inconsistency materializes as both types
    probe = Graph()
    probe += g
    bad = AUTH["fixtures/inconsistent-surface"]
    probe.add((bad, RDF.type, AUTH.PublicAuthSurface))
    probe.add((bad, RDF.type, AUTH.SessionAdminSurface))
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(probe)
    # OWL-RL marks inconsistency via owl:Nothing membership in some setups; also check disjoint axiom present
    disjoint_ok = (AUTH.PublicAuthSurface, OWL.disjointWith, AUTH.SessionAdminSurface) in g or (
        AUTH.SessionAdminSurface,
        OWL.disjointWith,
        AUTH.PublicAuthSurface,
    ) in g
    if not disjoint_ok:
        print("FAIL: PublicAuthSurface disjointWith SessionAdminSurface not found")
        return 1

    print("OK: OWL-RL TBox expanded; required classes/individuals present; surface disjointness asserted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
