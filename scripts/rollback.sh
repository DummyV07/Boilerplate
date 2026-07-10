#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

TARGET="${1:-}"

if [[ -z "$TARGET" ]]; then
  echo "Usage: $0 <git-tag-or-commit>"
  echo "Example: $0 v1.0.0"
  exit 1
fi

echo "==> [1/3] Checkout $TARGET"
git checkout "$TARGET"

echo "==> [2/3] Deploy backend"
"$PROJECT_ROOT/scripts/deploy-backend.sh"

echo "==> [3/3] Deploy frontend"
"$PROJECT_ROOT/scripts/deploy-frontend.sh"

echo "==> Rollback complete: $TARGET"
echo "    Remember to restart backend and reload nginx manually."
