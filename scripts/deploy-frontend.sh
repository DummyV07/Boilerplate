#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT/frontend"

echo "==> [1/2] Install frontend dependencies"
npm ci

echo "==> [2/2] Build frontend"
npm run build

echo "    dist/ ready at: $PROJECT_ROOT/frontend/dist"
