#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

BACKEND_URL="${BACKEND_URL:-http://127.0.0.1:8000}"
FRONTEND_URL="${FRONTEND_URL:-http://127.0.0.1:3000}"

echo "==> Health check: backend $BACKEND_URL"

echo "    GET /health"
curl -sf "$BACKEND_URL/health" | grep -q '"status"' || {
  echo "ERROR: /health failed"
  exit 1
}

echo "    GET /metrics"
curl -sf "$BACKEND_URL/metrics" | grep -q 'pipeline_node_total' || {
  echo "ERROR: /metrics missing pipeline metrics"
  exit 1
}

echo "    GET /health/asr"
curl -sf "$BACKEND_URL/health/asr" | grep -q '"node"' || {
  echo "ERROR: /health/asr failed"
  exit 1
}

echo "==> Health check: frontend $FRONTEND_URL"
if curl -sf --max-time 5 "$FRONTEND_URL" > /dev/null 2>&1; then
  echo "    Frontend reachable"
else
  echo "    WARN: Frontend not reachable (skip if not started)"
fi

echo "==> All health checks passed"
