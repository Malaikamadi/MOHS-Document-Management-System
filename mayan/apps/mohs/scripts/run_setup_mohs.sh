#!/usr/bin/env bash
# Run from anywhere: MoHS bootstrap against your local Mayan DB.
# Stop `runserver` (or anything using mayan/media/db.sqlite3) first, or use
# `lsof mayan/media/db.sqlite3` and quit those processes.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
export DYLD_LIBRARY_PATH="/opt/homebrew/opt/libmagic/lib:${DYLD_LIBRARY_PATH:-}"
exec "${ROOT}/venv/bin/python" manage.py setup_mohs "$@"
