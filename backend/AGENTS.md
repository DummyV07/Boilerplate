---
description: 适用于 FastAPI 后端开发的逻辑规范
globs: backend/**/*.py
alwaysApply: false
---

# FastAPI 开发规范

## 架构分层

- **Schemas**: 所有请求/响应模型在 `app/schemas/` 下定义，使用 Pydantic v2，`extra="forbid"`。
- **Services**: 业务逻辑在 `app/services/` 中，路由层只负责调用 Service。
- **Repositories**: 数据库 IO 封装在 `app/repositories/`。
- **Dependencies**: 数据库会话等通过 FastAPI `Depends` 注入（见 `app/api/deps.py`）。

## API 版本约定

- **新增路由**必须使用 `/api/v1/` 前缀（通过 `APIRouter(prefix="/v1")` 挂载）。
- 现有 `/api/items`、`/api/tasks` 为模版示例，保留不动。

## AI 流水线节点 (modules/)

- 节点放在 `app/modules/`，必须继承 `app/modules/base.py` 中的 `PipelineNode`。
- 实现 `process()` 方法；基类自动调用 `pipeline_trace.record_stage()` 记录 input/output。
- 日志必须携带 `trace_id` 与 `node` 字段。
- 新增节点后，在 `app/api/health_nodes.py` 的 `KNOWN_NODES` 中注册。

## 可观测性路由（不可删除）

| 文件 | 路由 | 说明 |
|------|------|------|
| `app/api/metrics.py` | `GET /metrics` | Prometheus 指标，可扩展不可移除 |
| `app/api/health_nodes.py` | `GET /health/{node}` | 节点健康检查 |
| `app/api/pipeline.py` | `GET /api/v1/pipeline/trace/{trace_id}` | 链路追踪查询 |

新增 AI 节点时，同步在 `metrics.py` 中注册对应 Counter/Histogram。

## 稳定性要求

- 每个 API 端点必须有 Pydantic 模型作为类型提示。
- 异步操作必须正确使用 `async/await`，禁止在协程中使用同步阻塞 IO。
- CPU 密集任务必须通过 `app/workers/task_pool.py` 提交，不得阻塞事件循环。

## 禁止事项

- 禁止在 `main.py` 中编写业务逻辑。
- 禁止删除 `pipeline_trace.py` 或 observability 相关路由文件。
- `tasks.py` 中的内联 Schema 仅为历史示例；新端点必须把模型放入 `app/schemas/`。
