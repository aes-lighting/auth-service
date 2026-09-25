#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VENV="$ROOT/.specify/scripts/.venv"
if [[ -x "$VENV/bin/python" ]]; then
  exec "$VENV/bin/python" "$ROOT/.specify/scripts/validate_spec.py"
fi
exec python3 "$ROOT/.specify/scripts/validate_spec.py"
