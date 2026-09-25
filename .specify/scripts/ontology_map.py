"""Explicit table/entity → OWL class allow-list for Spec Kit ontology.

INTENTIONAL: not auto-discovered. Adding a business table requires an entry here.
"""

from __future__ import annotations

# SQLite table name → auth: class local name (PascalCase).
ENTITY_OR_TABLE_TO_CLASS: dict[str, str] = {
    "users": "User",
}

# Closed role vocabulary (must match app.py register validation).
ROLE_CODES: tuple[str, ...] = ("driver", "pm", "admin")

# Extra generated classes not mapped from tables (session is cookie-side).
EXTRA_CLASSES: tuple[str, ...] = ("SessionCredential",)
