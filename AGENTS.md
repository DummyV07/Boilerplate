# 全栈项目模版 - 开发指南

## 运行环境

- 后端采用 `backend/app/` 布局，使用 **uv** 管理 Python 依赖。
- 开发启动：`cd backend && uv run python run.py`
- 生产启动：`cd backend && uv run gunicorn app.main:app -c gunicorn_conf.py`
- IDE 请将 `backend/app` 标记为 Sources Root。

## 执行规范

- 优先使用根目录 `Makefile` 中的命令，不要重复发明脚本。
- `.env` 文件仅在首次启动前检查一次，业务脚本内禁止重复校验环境变量。
- 没有明确指令时，禁止修改 `README.md`。

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
```

服务拓扑：
- `backend`：Gunicorn + UvicornWorker，挂载 `data/` 与 `logs/`
- `frontend`：Nginx 托管静态资源，反代 `/api` 到 backend

## 项目结构

```
Boilerplate/
├── AGENTS.md              # 本文件
├── Makefile
├── docker-compose.yml
├── backend/
│   ├── app/
│   │   ├── api/           # REST 路由
│   │   ├── core/          # 配置、数据库、日志
│   │   ├── models/        # SQLAlchemy 模型
│   │   ├── schemas/       # Pydantic 模型
│   │   ├── services/      # 业务逻辑
│   │   ├── repositories/  # 数据访问
│   │   └── workers/       # multiprocessing 任务池
│   ├── Dockerfile
│   ├── gunicorn_conf.py
│   └── pyproject.toml
└── frontend/
    ├── AGENTS.md          # Vue 3 开发规范（保留原文）
    ├── Dockerfile
    └── src/
        ├── api/           # Axios Service 层
        ├── stores/        # Pinia 状态
        └── views/         # 页面组件
```
