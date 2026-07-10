# 架构变更日志 (ARCH_LOG)

> 每次架构级变更（新增模块、改分层、换通信方式、改数据库）必须在此追加一条记录。
> AI 开发新功能前应先阅读本文件最新条目。

---

## 2026-07-10 — 模版骨架初始化

**类型**：骨架占位

**技术栈**
- 后端：FastAPI + SQLAlchemy (async) + SQLite + uv + Gunicorn
- 前端：Vue 3 + TypeScript + Pinia + Vite + Tailwind CSS
- 部署：Docker Compose + Nginx 反代

**分层约定**
```
api/ → services/ → repositories/ → models/
schemas/ — Pydantic 请求/响应（extra=forbid）
```

**占位目录（不可删除，只可扩展）**
| 路径 | 用途 |
| :--- | :--- |
| `backend/app/modules/` | AI 流水线节点（ASR / LLM / TTS） |
| `backend/app/core/pipeline_trace.py` | 链路追踪（trace_id） |
| `backend/app/api/metrics.py` | Prometheus 指标（对接 Grafana） |
| `backend/app/api/pipeline.py` | 链路查询 API |
| `scripts/` | 部署与健康检查脚本 |
| `docs/ui/` | UI 草图存放 |
| `docs/DEPLOY_LOG.md` | 部署更新记录 |

**示例业务**
- Item CRUD（`/api/items`）— 演示分层与 Schema First
- TaskPool CPU 任务（`/api/tasks/compute`）— 演示多进程任务隔离

**可观测性**
- `GET /health` — 服务存活
- `GET /health/{node}` — AI 节点状态（asr / llm / tts）
- `GET /metrics` — Prometheus 格式指标
- `GET /api/v1/pipeline/trace/{trace_id}` — 链路追踪查询

**未内置（扩展方向）**
- WebSocket 双通道
- Celery + Redis 异步队列
- JWT 认证

---

<!-- 在此下方追加新的架构变更记录 -->
