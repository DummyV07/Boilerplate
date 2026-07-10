# 全栈项目模版 - 开发指南（AI 宪法）

> **本文件是 AI 辅助开发的唯一权威约束。** 人类工作流见 [README.md](README.md)。

## 模版定位

本仓库是**全栈项目起点**，不是成品应用。包含：

- 可运行的最小示例（Item CRUD + TaskPool CPU 任务）
- AI 流水线骨架（`modules/` ASR / LLM / TTS 占位）
- 可观测性接口（`/metrics`、`/health/{node}`、链路追踪）
- 部署脚本与文档模板

业务逻辑在既有分层上扩展，**禁止推倒重来**。

## AI 工作流

1. **新任务起手**：`@AGENTS.md` + `@ARCH_LOG.md`，必要时 `@docs/ui/` 下的 UI 图。
2. **小步修改**：每次对话只改与任务最相关的 **2-3 个文件**。
3. **架构变更**：修改分层、通信方式、数据库前，先更新 [ARCH_LOG.md](ARCH_LOG.md)。
4. **禁止破坏性重构**：不要一次性重写多个模块或更换整体架构。

## 运行环境

- 后端采用 `backend/app/` 布局，使用 **uv** 管理 Python 依赖。
- 开发启动：`cd backend && uv run python run.py`
- 生产启动：`cd backend && uv run gunicorn app.main:app -c gunicorn_conf.py`
- IDE 请将 `backend/app` 标记为 Sources Root。

## 执行规范

- 优先使用根目录 `Makefile` 中的命令，不要重复发明脚本。
- `.env` 文件仅在首次启动前检查一次，业务脚本内禁止重复校验环境变量。
- **没有明确指令时，禁止修改 `README.md`。**
- **禁止修改 `frontend/AGENTS.md` 内容。**

## 依赖管理

```bash
uv add <package>           # 添加运行时依赖
uv add <package> --dev     # 添加开发依赖（使用 --extra dev）
uv remove <package>        # 移除依赖
make install               # 安装运行时依赖
make install-dev           # 安装全部依赖（含前端）
```

默认 Python 解释器：`.venv/bin/python`（由 uv 自动管理）。

## 代码质量

```bash
make check    # ruff check + ruff format --check + mypy（只检查不修改）
make fix      # ruff --fix + ruff format（自动修复）
make test     # pytest 后端测试
```

## 前端控制台 (frontend/)

- **技术栈**：Vue 3 + TypeScript + Pinia + Vite + Tailwind CSS
- `make web-dev` — 启动开发服务器（端口 3000）
- `make web-build` — 生产构建
- `make web-check` — 构建检查
- 所有 API 请求必须通过 `frontend/src/api/` 下的 Service 层发起。
- 前端开发规范见 [frontend/AGENTS.md](frontend/AGENTS.md)（禁止修改该文件内容）。

## 后端分层约定

```
api/ → services/ → repositories/ → models/
schemas/  — Pydantic 请求/响应模型（extra=forbid）
```

- 路由层（`app/api/`）只负责参数校验与调用 Service。
- 禁止在 `main.py` 中编写业务逻辑。
- **新增 API 路由使用 `/api/v1/` 前缀**；现有 `/api/items`、`/api/tasks` 保留作示例。

## AI 流水线节点 (modules/)

- 所有 AI 处理节点放在 `backend/app/modules/`，继承 `PipelineNode` 基类。
- 每个节点必须携带 `trace_id`，通过 `pipeline_trace.record_stage()` 记录 input/output 摘要。
- 节点命名：`asr`、`llm`、`tts`（可扩展，需同步更新 `/health/{node}`）。

## 可观测性铁律

以下路由为模版骨架，**不可删除，只可扩展**：

| 路由 | 用途 |
| :--- | :--- |
| `GET /health` | 服务存活 |
| `GET /health/{node}` | AI 节点状态 |
| `GET /metrics` | Prometheus 指标（对接 Grafana） |
| `GET /api/v1/pipeline/trace/{trace_id}` | 链路追踪查询 |

新增 AI 节点时，同步在 `metrics` 中暴露耗时与质量指标。

## 多进程约定

本项目包含两层多进程能力，职责不同：

| 层级 | 配置 | 用途 |
|------|------|------|
| Gunicorn workers | `gunicorn_conf.py` | 水平扩展 HTTP 请求处理 |
| TaskPool | `app/workers/task_pool.py` | 应用内 CPU 密集任务隔离 |

TaskPool 使用 `multiprocessing.Process / Manager / Queue`，在 `main.py` lifespan 中启动/关闭。
CPU 任务通过 `POST /api/tasks/compute` 提交，API 层使用 `run_in_executor` 避免阻塞事件循环。

## Docker 部署

```bash
make docker-build    # 构建镜像
make docker-up       # 启动服务（backend:8000, frontend:3000）
make docker-down     # 停止服务
make deploy          # 本地/服务器一键部署脚本
make health-check    # 部署后健康检查
```

服务拓扑：
- `backend`：Gunicorn + UvicornWorker，挂载 `data/` 与 `logs/`
- `frontend`：Nginx 托管静态资源，反代 `/api` 到 backend

## 骨架目录（不可删除）

```
Boilerplate/
├── AGENTS.md                  # 本文件（AI 宪法）
├── ARCH_LOG.md                # 架构变更日志
├── Makefile
├── docker-compose.yml
├── scripts/                   # 部署与健康检查脚本
│   ├── deploy.sh
│   ├── deploy-backend.sh
│   ├── deploy-frontend.sh
│   ├── rollback.sh
│   └── health-check.sh
├── docs/
│   ├── DEPLOY_LOG.md          # 部署更新记录
│   └── ui/                    # UI 草图存放
├── backend/
│   ├── app/
│   │   ├── api/               # REST 路由（含 metrics、pipeline）
│   │   ├── core/              # 配置、数据库、日志、pipeline_trace
│   │   ├── models/            # SQLAlchemy 模型
│   │   ├── schemas/           # Pydantic 模型
│   │   ├── services/          # 业务逻辑
│   │   ├── repositories/      # 数据访问
│   │   ├── modules/           # AI 流水线节点（ASR/LLM/TTS）
│   │   └── workers/           # multiprocessing 任务池
│   ├── Dockerfile
│   ├── gunicorn_conf.py
│   └── pyproject.toml
└── frontend/
    ├── AGENTS.md              # Vue 3 开发规范（禁止修改）
    ├── Dockerfile
    └── src/
        ├── api/               # Axios Service 层
        ├── components/        # 可复用组件
        ├── stores/            # Pinia 状态
        └── views/             # 页面组件
```

## 从模版 Fork 新项目

1. Fork / Clone 本仓库，修改项目名。
2. `cp backend/.env.example backend/.env` 并按需修改。
3. 在 `ARCH_LOG.md` 追加第一条项目专属架构记录。
4. `make install-dev` → 分别启动 `make dev-backend` 与 `make dev-frontend`。
5. UI 草图存入 `docs/ui/`。
6. 在 Cursor 开启新对话：`@AGENTS.md @ARCH_LOG.md`，描述第一个功能需求。

详细人类 SOP 见 [README.md](README.md) 中「从模版 Fork 启动新项目」章节。

## 模版未内置（扩展方向）

- WebSocket 双通道通信
- Celery + Redis 异步任务队列
- JWT 认证模块
- Grafana / Prometheus 实际部署（已预留 `/metrics` 接口）
