#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT/backend"

echo "==> [1/2] Install backend dependencies"
uv sync --no-dev

echo "==> [2/2] Backend ready"
echo "    Start with: cd backend && uv run gunicorn app.main:app -c gunicorn_conf.py"
echo "    Or dev mode: make dev-backend"
