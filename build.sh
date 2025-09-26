#!/usr/bin/env bash
set -euo pipefail

# Render already provides uv. Just sync dependencies.
uv sync

if ! psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f database.sql; then
  echo "Database schema initialization failed" >&2
  exit 1
fi
