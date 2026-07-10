#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

DEPLOY_LOG="$PROJECT_ROOT/docs/DEPLOY_LOG.md"
COMMIT_HASH="$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
DEPLOY_TIME="$(date '+%Y-%m-%d %H:%M')"

echo "==> [1/5] Pull latest code"
git pull origin "$(git branch --show-current)"

echo "==> [2/5] Deploy backend"
"$PROJECT_ROOT/scripts/deploy-backend.sh"

echo "==> [3/5] Deploy frontend"
"$PROJECT_ROOT/scripts/deploy-frontend.sh"

echo "==> [4/5] Append deploy log"
cat >> "$DEPLOY_LOG" <<EOF

## ${DEPLOY_TIME} 部署记录

- **版本/分支**：$(git branch --show-current) @ ${COMMIT_HASH}
- **操作人**：$(whoami)
- **变更摘要**：（请手动补充）
- **数据库变更**：无
- **配置变更**：无
- **回滚方案**：./scripts/rollback.sh <previous-tag>
- **部署结果**：待验证
EOF

echo "==> [5/5] Health check"
"$PROJECT_ROOT/scripts/health-check.sh" || {
  echo "WARN: Health check failed — verify backend is running"
  exit 1
}

echo "==> Deploy complete: ${COMMIT_HASH} @ ${DEPLOY_TIME}"
