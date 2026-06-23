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

## 稳定性要求

- 每个 API 端点必须有 Pydantic 模型作为类型提示。
- 异步操作必须正确使用 `async/await`，禁止在协程中使用同步阻塞 IO。
- CPU 密集任务必须通过 `app/workers/task_pool.py` 提交，不得阻塞事件循环。
