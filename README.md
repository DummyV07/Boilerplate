# 个人全栈项目开发之路


# 1月29日记
这是一份为您定制的 **《一人公司：Cursor 全栈开发实战 SOP》**。

这份指南总结了我们之前的讨论，旨在解决你“后期 AI 变笨”、“逻辑被破坏”以及“想法被阉割”的核心痛点。

请记住：**你不再是单纯的程序员（Coder），你是产品经理 + 架构师 + 验收测试员。Cursor 是你手下那个“打字极快、懂所有语言、但记性只有 7 秒的实习生”。**

---

## 💡 一人全栈 + AI 的现实：接受失控，分层掌控

> *7 月 8 日感悟*

一个人扛全栈项目，再叠加 AI 提效，代码量会膨胀得很快——**失控几乎是不可避免的**。这不是能力问题，而是工作方式的必然结果：你不可能像传统团队那样，对每个 PR 做逐行 Code Review。

因此需要接受一个现实：**除开关键节点和核心逻辑，你大概率只能关注“浮在表面”的东西**——整体架构是否合理、模块边界是否清晰、API 接口分布是否顺眼、前后端契约（Schema）有没有跑偏。至于某个组件里多写了一个 `if`、某段工具函数是否最优，很多时候根本没有精力细看。

这听起来像妥协，但换个角度想，**这恰恰是你作为“一人公司”应该专注的层级**：

| 审查深度 | 关注什么 | 为什么 |
| :--- | :--- | :--- |
| **必须深挖** | 核心业务逻辑、数据流、鉴权/支付等关键路径、状态机、数据库 Schema 变更 | 这里出错 = 产品翻车 |
| **表面扫一眼** | 目录结构、API 路由分布、模块职责划分、`schemas/` 与 `api/` 的对应关系、**运行日志**、**部署更新记录** | 骨架对了，血肉即使有点乱也不致命；出问题时有迹可循 |
| **放心交给 AI** | UI 样式微调、重复性 CRUD、工具函数、测试用例骨架 | 出问题容易发现，修复成本低 |

**实操口诀：抓骨架，放血肉。**

- **骨架**：`AGENTS.md` 里的分层约定、`schemas/` 定义的数据契约、`api/` 下的接口分布、`ARCH_LOG.md` 里的架构变更记录——这些是你必须亲自盯住的。
- **血肉**：具体实现细节、某个 Vue 组件的内部状态写法、某段 Service 里的异常处理分支——功能跑通、测试过了，不必强求全懂。
- **救生绳**：当你没法逐行审查代码时，**日志（Logs）** 和 **部署更新记录** 是你唯一能依赖的"黑盒透视"手段——它们帮你在失控状态下快速定位"什么时候、改了什么、挂了在哪里"。
- **链路透视**：AI 多节点项目里，**Grafana 指标 + 链路 Trace** 帮你定位"偏差从哪个节点开始"——最终输出错了，别只盯最后一个环节。

这也是为什么本 SOP 反复强调 **Schema First**、**小步提交**、**精准投喂 2-3 个文件**——它们不是为了让你审更多代码，而是让你在**有限的注意力**里，始终盯住那些真正决定项目生死的节点。

**失控不可怕，可怕的是在失控中失去了对骨架的感知。**

---

### 第一阶段：谋定而后动 (70% 的时间)

*解决痛点：想法被阉割、后期逻辑混乱*

在打开 Cursor 写第一行代码之前，你必须先完成“图纸”。

1. **绘制 UI 草图 (Visual Specs)**
* **做什么**：不要空想。用笔在纸上画，或者用 iPad/Figma 画出 `首页`、`列表`、`详情` 三个界面。
* **为什么**：图片是信息密度最高的指令。把 UI 图喂给 Cursor，它能瞬间理解布局、层级和交互逻辑，比你说 1000 句 Prompt 都管用。
* **存哪里**：存入 `docs/ui/` 目录。


2. **确立“宪法” (`AGENTS.md`)**
* **做什么**：把我们之前商定的 `AGENTS.md` 放入根目录。
* **核心内容**：
* **身份**：你是一个全栈专家。
* **架构**：FastAPI (后端) + Vue3 (前端) + REST API（WebSocket 为扩展方向）。
* **铁律**：先写测试、先写文档、禁止破坏性重构。
* **审计**：强制维护 `ARCH_LOG.md`。




3. **定义数据结构 (Schema First)**
* **做什么**：明确 SQLite 的表结构（Product 表有哪些字段）和前后端交互的 JSON 格式。
* **技巧**：让 Cursor 先写 `types/api.ts` (前端) 和 `app/schemas/` (后端)。这是前后端的“契约”，契约定了，逻辑就不容易跑偏。



---

### 第二阶段：搭建骨架 (Skeleton Phase)

*解决痛点：项目太复杂导致 AI 变笨*

不要一上来就写业务，先搭架子。

1. **初始化目录 (Modular Setup)**
* 让 Cursor 按照 `AGENTS.md` 里的规范，建立 `frontend/` 和 `backend/` 文件夹。
* **关键动作**：确保 `backend/app/modules/` (ASR/LLM/TTS) 的文件夹结构存在。此时里面可以是空的，但“坑”要先挖好。


2. **跑通“Hello World”全链路**
* 不要写具体功能。先验证前后端连通：`curl localhost:8000/health` + 前端页面能打开。
* **目的**：验证前后端连接、跨域配置、环境依赖（Python/Node）是否正常。
* **扩展方向**：如需 WebSocket 双通道，模版未内置，可在 `backend/app/api/` 新增 WS 路由后按同样方式验证 Ping/Pong。

---

### 第三阶段：增量开发循环 (The Loop)

*解决痛点：上下文过载、代码不可控*

这是你每天的日常工作流，必须严格遵守 **“小步快跑”** 原则。

#### 1. 开启新任务 (New Feature)

* **动作**：永远不要在一个聊了 50 轮的对话框里继续。**Ctrl+L (Command+L)** 开启新对话。
* **起手式**：
> “@AGENTS.md @ARCH_LOG.md 我要开始开发‘商品详情页点击跳转’功能。请阅读 UI 图 @ui_detail.png，并给出实现计划。”



#### 2. 精准投喂 (Context Pruning)

* **动作**：不要直接问。
* **错误**：“帮我改一下那个跳转逻辑。”（Cursor 会懵，或者瞎改）
* **正确**：“@frontend/src/views/Detail.vue @backend/websocket/control_handler.py 当用户点击商品时，前端发送 `UPDATE_CONTEXT` 事件，后端需要更新 Session 状态。请只修改这两个文件。”
* **原则**：**只喂跟当前任务最相关的 2-3 个文件。**

#### 3. 审计与测试 (Review & Verify)

* **动作**：Cursor 写完代码后，不要直接信。
* **口诀**：**“先看 Log，再看 Diff，最后 Run。”**
* 看它有没有更新 `ARCH_LOG.md`？
* 看它的代码变更有没有删掉你之前的注释？
* 运行项目，手动点一下，看报错没。



#### 4. 提交代码 (Commit)

* **动作**：功能跑通一个，就 Git Commit 一个。千万不要堆积一天的代码再提交。

---

### 第四阶段：防崩坏锦囊 (Maintenance)

*解决痛点：AI 突然胡言乱语*

当你发现 Cursor 开始写 Bug、遗忘之前的逻辑时，请执行以下操作：

1. **清空上下文 (Reset Context)**：
* 它变笨是因为对话历史太长，噪声太多。
* **操作**：把当前代码 Commit，然后**重启 Cursor** 或开启一个全新的 Chat 窗口。


2. **更新文档 (Docs Sync)**：
* 如果项目逻辑变了（比如从 HTTP 改成了 WS），**必须手动更新 `AGENTS.md**`。
* Cursor 是看着文档干活的，文档旧了，活就干坏了。


3. **人类介入 (Human Intervention)**：
* 对于极度复杂的重构（比如把整个数据库层换掉），**不要让 AI 自动做**。
* 你自己手动调整文件夹结构、文件名，然后再让 Cursor 去填里面的代码内容。**“人做骨架，AI 做血肉”。**



---

## 📋 Git 工作流与贡献规范

### 分支命名

| 分支 | 用途 |
| :--- | :--- |
| **main** | 主分支，用于生产环境部署，必须保持稳定。通常由 `release` 或 `hotfix` 分支合并更新，**禁止直接修改代码**。 |
| **develop** | 主开发分支，包含最新已完成的功能与 Bug 修复，用于前后端联调。所有新功能分支应从此分支创建。 |
| **feature** | 新功能开发分支，基于 `develop` 创建。命名格式：`feature/` + 模块名，如 `feature/user_module`、`feature/cart_module`。 |
| **test** | 测试环境分支，外部用户不可访问，专供测试团队使用，代码相对稳定。 |
| **release** | 预发布（Staging）分支，用于 UAT（用户验收测试）。通常由 `test` 或 `hotfix` 分支合并，**不建议直接修改代码**。 |
| **hotfix** | 紧急生产 Bug 修复分支，从 `main` 分支创建。修复完成后必须同时合并到 `main` 和 `develop`。 |

### 分支与环境对应关系

| 分支 | 功能 | 环境 | 是否可访问 |
| :--- | :--- | :--- | :--- |
| **main** | 主分支，稳定版本 | PRO（生产环境） | 是 |
| **develop** | 开发分支，最新版本 | DEV（开发环境） | 是 |
| **feature** | 开发分支，新功能 | — | 否 |
| **test** | 测试分支，功能测试 | FAT（功能验收测试） | 是 |
| **release** | 预发布分支，发布新版本 | UAT（用户验收测试） | 是 |
| **hotfix** | 紧急修复分支，修复生产 Bug | — | 否 |

**环境说明：**

- **DEV**：供开发人员调试使用。
- **FAT**：功能验收测试（Functional Acceptance Test）环境。
- **UAT**：用户验收测试（User Acceptance Test）环境，用于类生产环境验证。
- **PRO**：生产环境（Production）。

### Commit 提交信息规范

提交信息使用标准化前缀，格式为 `<type>: <description>`：

| 前缀 | 含义 |
| :--- | :--- |
| **feat** | 新功能 |
| **fix** | Bug 修复 |
| **docs** | 仅文档变更 |
| **style** | 不影响代码含义的变更（空格、格式化、分号等） |
| **refactor** | 既不修复 Bug 也不新增功能的代码重构 |
| **perf** | 性能优化 |
| **test** | 添加或修正测试 |
| **chore** | 构建流程或辅助工具、库的变更（如文档生成） |

**示例：**

```
feat: 添加用户登录接口
fix: 修复购物车数量计算错误
docs: 更新 API 文档
```

### 单次提交注意事项

1. **类别统一**：单次提交中的变更必须属于同一类别（例如不要在一个 commit 中同时包含 `feat` 和 `fix`）。
2. **控制范围**：单次提交不要包含超过 3 个问题/任务。
3. **修正信息**：若发现提交信息不符合规范，使用 `git commit --amend` 修正。
4. **重新提交**：对于"新建"的提交信息，或在执行 `git reset --hard HEAD` 之后，需重新提交一次。

---

## 从模版 Fork 启动新项目

> **双文档分工**：`README.md` 给人类读（流程、感悟、部署）；`AGENTS.md` 给 AI 读（架构铁律、目录约定）。开发时两个都要 `@`。

### 启动步骤

1. **Fork / Clone** 本仓库，修改项目名与远程地址。
2. **配置环境**：`cp backend/.env.example backend/.env`（模版默认 SQLite，无需额外安装数据库）。
3. **安装依赖**：`make install-dev`
4. **初始化架构日志**：在 [`ARCH_LOG.md`](ARCH_LOG.md) 追加第一条项目专属记录。
5. **准备 UI 资产**：在纸上画出首页/列表/详情草图，拍照存入 [`docs/ui/`](docs/ui/)。
6. **启动开发**：
   ```bash
   make dev-backend   # 终端 1：后端 :8000
   make dev-frontend  # 终端 2：前端 :3000
   ```
7. **验证骨架**：
   ```bash
   curl localhost:8000/health
   curl localhost:8000/metrics
   curl localhost:8000/health/llm
   make health-check  # 服务启动后
   ```
8. **第一个 Cursor 对话**：
   > `@AGENTS.md @ARCH_LOG.md @docs/ui/wireframe_home.png`
   > 我要开发首页，请根据 UI 图给出实现计划。

### 模版已内置的骨架

| 能力 | 路径 / 命令 | 状态 |
| :--- | :--- | :--- |
| 分层 CRUD 示例 | `/api/items` | 可运行 |
| CPU 任务池示例 | `/api/tasks/compute` | 可运行 |
| AI 节点占位 | `backend/app/modules/` | 待填充业务 |
| Grafana 指标 | `GET /metrics` | 已预留 |
| 链路追踪 | `GET /api/v1/pipeline/trace/{id}` | 已预留 |
| 部署脚本 | `make deploy` / `scripts/` | 已就绪 |
| 部署记录 | `docs/DEPLOY_LOG.md` | 模板已建 |

### 模版未内置（扩展方向）

- WebSocket 双通道通信（README 第二阶段提及，需自行扩展）
- Celery + Redis 异步队列（README 后端章节提及，模版使用 TaskPool）
- JWT 认证模块
- Grafana / Prometheus 实际部署（已预留 `/metrics` 接口）

---

### 🚀 你的第一步行动清单（Fork 后）

1. [x] **`AGENTS.md`**：模版已内置，Fork 后直接 `@` 使用。
2. [x] **`ARCH_LOG.md`**：模版已内置初始记录，追加项目专属条目。
3. [x] **骨架目录**：`modules/`、`scripts/`、`docs/` 已就位。
4. [ ] **配置 `.env`**：`cp backend/.env.example backend/.env`
5. [ ] **画图**：UI 草图拍照，存入 `docs/ui/`。
6. [ ] **开工**：打开 Cursor，输入：
> `@AGENTS.md @ARCH_LOG.md 我要开发 [你的第一个功能]。请阅读 UI 图 @docs/ui/xxx.png，并给出实现计划。`

层级一：手绘草图 (Wireframe)
在纸上画出三个状态（首页、列表、详情）的方框分布。
拍张照丢给 Cursor。
作用：确定功能组件的占位和跳转逻辑。

层级二：简单的 Figma/蓝湖原形
定义好主色调（商场导购可能是高级白或温暖色）、圆角大小、按钮位置。
作用：定死 UI 风格，防止 AI 生成那种 90 年代的网页感。

层级三：竞品截图（最快的方法）
如果你觉得“AI 小智”或其他导购应用的界面好，直接截屏。
告诉 Cursor：“参考这张图的布局，但左侧对话框改为透明磨砂效果，右侧商品卡片按我们的 SQLite 结构展示。”



技术栈 FASTAPI + VUE3 + Nginx + Gunicorn

## 🏗️ 第一部分：系统架构

1. **前后端分离原则**：前端（Vue）仅负责 UI 渲染与交互逻辑，后端（Python）仅负责数据处理与业务逻辑。两者通过 **RESTful API** 进行 JSON 交互。
2. **Schema 为先 (Schema-First)**：在写具体的业务逻辑前，先定义好后端的数据结构（Pydantic Models），确保前端联调时有明确的数据契约。
3. **单一职责原则**：一个接口只做一件事。复杂的长耗时操作必须与即时响应接口分离。
4. **可观测性预留 (Observability-Ready)**：从项目骨架阶段就预留 **Grafana** 对齐接口和 **链路监控** 埋点，尤其 AI 多节点流水线（ASR → LLM → TTS 等）必须在每个节点输出可采集的指标，而不是只盯最终结果。

### 可观测性预留：Grafana 与 AI 链路监控

> *针对 AI 项目的核心痛点：最终输出错了，往往不是最后一个节点的问题，而是前几个节点就已经开始偏移，误差逐级放大。*

传统 Web 项目出 Bug，看最后一层接口的 500 日志通常就够。但 AI 项目是一条**多节点处理链**——语音识别错了，LLM 再强也救不回来；Prompt 模板偏了，TTS 读出来的就是歪的。**你看到的"最后结果不对"，根因可能在链路最前端。**

因此，监控的重点不是"最终接口返没返回"，而是**每个节点的输入/输出质量与耗时**。

#### 必须预留的接口

| 接口 | 路径建议 | 用途 | 对接方 |
| :--- | :--- | :--- | :--- |
| 健康检查 | `GET /health` | 服务存活（已有） | 部署脚本、负载均衡 |
| **Metrics 指标** | `GET /metrics` | Prometheus 格式指标导出 | **Grafana**（通过 Prometheus 数据源） |
| 节点健康 | `GET /health/{node}` | 单个 AI 节点状态（如 `asr`、`llm`、`tts`） | Grafana 面板、告警规则 |
| 链路追踪 | `GET /api/v1/pipeline/trace/{trace_id}` | 按请求 ID 查询全链路各节点输入/输出摘要 | 链路检测插件、人工排查 |

**`/metrics` 是后期对接 Grafana 的入口**——项目初期哪怕只暴露几个 Counter（请求数、错误数），也比上线后再补埋点省事得多。Grafana 侧配置 Prometheus 抓取 `/metrics`，即可做时序图表和告警。

#### 每个 AI 节点应记录的指标

在每个处理节点（`backend/app/modules/` 下的 ASR、LLM、TTS 等）统一埋点，指标命名建议带节点前缀：

```
# 耗时
pipeline_node_duration_seconds{node="asr", status="success"}
pipeline_node_duration_seconds{node="llm", status="error"}

# 质量（按业务定义）
pipeline_node_output_confidence{node="asr"}          # ASR 置信度
pipeline_node_token_count{node="llm"}                  # LLM 输出 token 数
pipeline_node_retry_total{node="tts"}                  # TTS 重试次数

# 链路贯通
pipeline_request_total{trace_id="xxx", final_status="degraded"}  # 最终结果降级
```

**关键原则：每个节点既记"成功/失败"，也记"质量指标"**——ASR 置信度从 0.95 悄悄降到 0.6，接口不会 500，但最终回答已经开始偏了。

#### 链路追踪（Trace ID）贯通

一次用户请求从进入到输出，全链路共享同一个 `trace_id`：

```
用户请求 → [trace_id: abc123]
  ├─ ASR 节点    input: 音频流  → output: "今天天气怎么样"  (耗时 320ms, 置信度 0.91)
  ├─ LLM 节点    input: 上述文本 → output: "今天北京晴..."   (耗时 1200ms, tokens 85)
  └─ TTS 节点    input: 上述文本 → output: 音频流          (耗时 450ms)
```

- 在日志中，每条记录携带 `trace_id` + `node` + `stage`（input/output）。
- 链路检测插件（或 Grafana Loki + Trace 面板）按 `trace_id` 串联，一眼看出**偏差从哪个节点开始**。
- 后期可升级为 OpenTelemetry，但初期用 **结构化日志 + `/metrics`** 就够落地。

#### 与 Grafana / 链路检测插件的对齐节奏

| 阶段 | 做什么 | 不做什么 |
| :--- | :--- | :--- |
| **骨架期（现在）** | 预留 `/metrics`、`/health/{node}` 路由；定义指标命名规范；日志带 `trace_id` | 不急着搭完整 Grafana 集群 |
| **联调期** | 每个 AI 节点接入埋点；本地用 `curl /metrics` 验证指标输出 | 不要求面板好看 |
| **上线期** | Prometheus 抓取 + Grafana Dashboard；配置关键节点延迟/错误率告警 | — |
| **运维期** | 接入链路检测插件，按 `trace_id` 做端到端巡检；定期回顾"降级请求"占比 | — |

#### 实操口诀：查链路，不猜结果。

- 最终输出错了 → 先拿 `trace_id` 查链路 → 看**最早出现异常指标的节点**，而不是直接改 Prompt 或换模型。
- 搭建骨架时就把 `app/api/metrics.py` 和 `app/core/pipeline_trace.py` 的"坑"挖好，后期接入 Grafana 和链路插件只需填实现，不用改路由结构。

### 项目结构

```
my-awesome-project/
├── AGENTS.md               # AI 开发宪法（Cursor 必须 @）
├── ARCH_LOG.md             # 架构变更日志
├── Makefile                # 统一命令入口
├── scripts/                # 部署与健康检查脚本
│   ├── deploy.sh
│   ├── deploy-backend.sh
│   ├── deploy-frontend.sh
│   ├── rollback.sh
│   └── health-check.sh
├── docs/
│   ├── DEPLOY_LOG.md       # 部署更新记录
│   └── ui/                 # UI 草图存放
├── backend/                # Python 后端 (FastAPI)
│   ├── app/
│   │   ├── api/            # 路由层（含 metrics、pipeline）
│   │   ├── core/           # 配置、数据库、日志、pipeline_trace
│   │   ├── models/         # SQLAlchemy 模型
│   │   ├── schemas/        # Pydantic 模型
│   │   ├── services/       # 业务逻辑
│   │   ├── repositories/   # 数据访问
│   │   ├── modules/        # AI 流水线节点（ASR/LLM/TTS）
│   │   ├── workers/        # TaskPool 多进程任务
│   │   └── main.py         # 应用入口
│   ├── run.py              # 开发启动
│   ├── pyproject.toml      # uv 依赖管理
│   └── .env                # 环境变量
├── frontend/               # Vue 3 + Vite
│   ├── AGENTS.md           # 前端开发规范
│   └── src/
│       ├── api/            # Axios Service 层
│       ├── components/     # 可复用组件
│       ├── views/          # 页面组件
│       ├── stores/         # Pinia 状态
│       └── router/         # 路由配置
├── docker-compose.yml
└── README.md               # 人类 SOP（本文件）
```

## 💾 数据库配置

**模版默认使用 SQLite**（零配置，开箱即用）。以下 MySQL 配置为**生产环境可选方案**。

### 默认：SQLite（开发推荐）

模版已配置 SQLite，无需额外安装数据库：

```bash
# backend/.env（默认值）
DATABASE_URL=sqlite+aiosqlite:///./data/template.db
```

启动后端时自动创建 `backend/data/template.db` 和数据表。

---

### 可选：MySQL（生产环境）

如需切换到 MySQL，按以下步骤操作：

#### 1. 安装 MySQL

**macOS (使用 Homebrew):**
```bash
brew install mysql
brew services start mysql
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo systemctl start mysql
```

#### 2. 创建数据库

登录 MySQL 并创建数据库：

```bash
mysql -u root -p
```

在 MySQL 命令行中执行：

```sql
CREATE DATABASE chat_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

#### 3. 配置环境变量

复制 `.env.example` 并修改数据库连接信息：

```bash
cd backend
cp .env.example .env
```

编辑 `.env` 文件，修改 `DATABASE_URL`：

```bash
# 格式: mysql+asyncmy://用户名:密码@主机:端口/数据库名
DATABASE_URL=mysql+asyncmy://root:你的密码@localhost:3306/chat_db
```

**示例：**
```bash
DATABASE_URL=mysql+asyncmy://root:mypassword@localhost:3306/chat_db
```

#### 4. 安装依赖

切换 MySQL 时需先添加驱动：

```bash
cd backend
uv add asyncmy
uv sync
```

#### 5. 初始化数据库表

启动后端服务时，数据库表会通过 `main.py` lifespan 自动创建（`Base.metadata.create_all`）。

#### 6. 数据库连接池配置（可选）

SQLAlchemy 连接池可在 `database.py` 中按需调整，或通过环境变量扩展 `Settings`。
当前模版未内置 `DB_POOL_*` 环境变量。

#### 7. 验证连接

启动后端服务，检查日志是否显示 "Database initialized"：

```bash
cd backend
uv run python run.py
```

如果看到数据库初始化成功的日志，说明连接正常。

### 📝 注意事项

1. **字符集**：数据库使用 `utf8mb4` 字符集，支持 emoji 和特殊字符
2. **时区**：确保 MySQL 时区设置正确（建议使用 UTC）
3. **权限**：确保数据库用户有创建表的权限
4. **连接池**：生产环境建议调整连接池大小以适应并发需求

## 🐍 第二部分：Python 后端开发

这里的python开发使用fastapi


一、 接口阻塞的架构级解决方案
接口响应慢通常有两种情况：I/O 密集型（等数据库、等第三方 API）和 计算密集型（处理图片、运行 AI 模型）。

1. 异步框架选型（FastAPI）

非阻塞 I/O：使用 async def 定义接口，配合 await 处理数据库操作。这样当一个请求在等待时，Python 进程可以去处理另一个请求。

代码示例：

Python

@app.get("/slow-data")
async def get_data():
    data = await database.fetch_all() # 异步等待，不阻塞进程
    return data
2. 耗时任务：生产者-消费者模型 (Celery + Redis)
对于需要几秒甚至几分钟才能完成的任务（比如 AI 推理、发送大批量邮件），绝对不能在 Web 接口里同步等待。

方案：接口立即返回一个 task_id，告诉前端“任务已收到，正在处理”。实际运算交给后台 Worker 进程。

架构：FastAPI (接收请求) -> Redis (消息队列) -> Celery (后台异步执行)。

> **模版现状**：当前使用 `TaskPool`（multiprocessing）处理 CPU 密集任务（见 `POST /api/tasks/compute`）。Celery + Redis 为扩展方向，适合更长耗时的 AI 推理场景。

2. 接口分层与版本控制
版本号：所有 API 必须以 /api/v1/xxx 开头，方便后续无缝升级。

拆分逻辑：按业务模块拆分文件（如 user.py, order.py, ai_process.py），利用 FastAPI 的 APIRouter 进行挂载。

1. **异步编程常态化**：
   - 必须使用 `async def` 定义路由。
   - 所有 I/O 操作（数据库读写、外部 API 调用）必须使用 `await` 挂起，严禁在主流程中使用 `time.sleep()`。
2. **长耗时任务处理**：
   - 处理时间超过 2 秒的任务（如 AI 生成、大文件处理），**禁止同步等待**。
   - **规则**：接口立即返回 `202 Accepted` 和任务 ID，由后台进程处理，前端通过轮询或 WebSocket 获取结果。
3. **日志三原则**：
   - **弃用 print**：统一使用 `loguru` 或 `logging` 库。
   - **分级存储**：`INFO` 记录关键路径，`ERROR` 记录异常堆栈。
   - **日志滚动**：必须配置按天或按大小切分日志（Rotation），防止撑爆硬盘。
4. **可观测性接口预留**：
   - 骨架阶段预留 `GET /metrics`（Prometheus 格式），后期无缝对接 **Grafana**。
   - AI 流水线每个节点（ASR / LLM / TTS）日志必须携带 `trace_id`，记录 input/output 摘要与耗时。
   - 最终输出异常时，按 `trace_id` 回溯链路，定位**最早出现偏差的节点**——详见上文「可观测性预留：Grafana 与 AI 链路监控」。

## 🎨 第三部分：VUE 前端开发

1. **环境变量隔离**：区分 `development` 和 `production` 环境的 API 地址。
2. **状态管理规范**：
   - 简单的组件传参用 `props`。
   - 跨页面、跨组件的全局数据（如用户信息、Token）必须存入 **Pinia**。
3. **请求封装**：API 请求统一走 `frontend/src/api/client.ts`；401/500 拦截器可按业务扩展。

```
frontend/src/
├── api/            # Axios Service 层（client.ts + 业务 API）
├── components/     # 可复用组件
├── views/          # 页面组件（模版示例：Home.vue）
├── stores/         # Pinia 状态（模版示例：app.ts）
├── router/         # 路由配置
└── styles/         # 全局样式（Tailwind CSS）
```

## 🚀 第四部分：生产环境部署 (Gunicorn + Nginx)

### Gunicorn
1. **拒绝 `nohup`**：
   - 生产环境必须使用 **Gunicorn** 作为进程管理器（Master）。
   - 配置 `workers = (2 * CPU核数) + 1` 以最大化利用多核性能。
   -  我们使用 `uv` 驱动 `gunicorn`，通过多进程模式运行后端。
```
uv run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000
```

2. **如何看输出（验证）**

- **终端输出**：应显示 `[INFO] Starting gunicorn 23.x.x` 及 `Listening at: http://127.0.0.1:8000`。
- **进程验证**：执行 `ps aux | grep gunicorn`。
- **正常标志**：看到 1 个 Master 进程和 4 个 Worker 进程。
- **端口验证**：执行 `lsof -i :8000`。
- **正常标志**：显示 `COMMAND: Python` 正在 `LISTEN`。

### Nginx

1. **动静分离**：
   - **Nginx** 直接托管 Vue 编译后的静态文件（`dist` 目录），不经过后端进程。
   - **Nginx** 仅作为反向代理，将 `/api` 请求转发给后端的 Gunicorn。

将源代码转换为 Nginx 能够理解的静态资源。

1. 执行命令

进入 frontend 目录执行：

Bash

```
npm run build
```

**2. 如何看输出（验证）**

- **文件验证**：检查是否生成了 `dist/` 文件夹。
- **内容验证**：`dist/` 内应包含 `index.html` 和 `assets/` 文件夹。
- **记住路径**：记录 `dist` 的**绝对路径**（如 `/Users/dummy/project/dist`），下一步要用。

将前端静态文件和后端 API 接口统一到一个入口（80 端口）。

1. 修改权限（关键步骤）

编辑 /opt/homebrew/etc/nginx/nginx.conf，将首行的 user nobody; 改为：

Nginx

```
user dummy staff; # dummy 换成你的 Mac 用户名
```

2. 编写项目配置

在 /opt/homebrew/etc/nginx/servers/ 下创建 my_app.conf：

Nginx

```
server {
    listen 80;
    server_name localhost;

    location / {
        root /你的/dist/绝对路径;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }
}
```

**3. 启动与重载**

Bash

```
sudo nginx -t            # 检查语法是否 ok
sudo nginx -s reload     # 重新加载配置
# 如果 nginx 没启动，改用：sudo nginx
```

------

1. **进程守护**：
   - 必须将 Gunicorn 注册为 **Systemd 服务**。
   - 配置 `Restart=always`，确保系统重启或进程崩溃后能自动拉起服务。

### 日志与部署记录：失控后的救生绳

代码细节审不过来时，**日志**和**部署更新记录**是你最重要的兜底手段。它们回答三个现场必问的问题：**挂了没？挂在哪？上次上了什么？**

#### 1. 运行日志（Runtime Logs）

项目已配置分层日志，部署后应定期扫一眼，而不是等用户反馈：

| 日志文件 | 位置 | 用途 |
| :--- | :--- | :--- |
| 应用日志 | `backend/logs/app.log` | 业务关键路径、异常堆栈 |
| Gunicorn 访问日志 | `backend/logs/access.log` | 请求是否到达后端 |
| Gunicorn 错误日志 | `backend/logs/error.log` | Worker 崩溃、启动失败 |
| Nginx 错误日志 | `/opt/homebrew/var/log/nginx/error.log`（macOS） | 403/502 等反向代理问题 |

**现场排查口诀：**

```bash
# 后端：看最近 50 行错误
tail -n 50 backend/logs/app.log

# Nginx：看最近报错
tail -n 20 /opt/homebrew/var/log/nginx/error.log
```

日志的价值不在于开发时逐行阅读，而在于**上线后快速定位**：你不用懂每一行实现，但能从时间戳和堆栈判断"是数据库连不上"还是"某个接口 500"。

#### 2. 部署更新记录（Deploy Changelog）

每次上线前，写清楚本次变更——不用长篇大论，几条 bullet 即可：

```
## 2026-07-10 部署记录
- 版本/分支：release/v1.2.0
- 变更摘要：新增用户模块 API；前端购物车页重构
- 数据库变更：无 / 需执行 migrate_xxx.sql
- 配置变更：.env 新增 OLLAMA_BASE_URL
- 回滚方案：git checkout <上一版本 tag> && ./scripts/deploy.sh rollback
```

建议维护在 `docs/DEPLOY_LOG.md` 或每次部署时追加到 Git Tag 的 Release Notes。**部署记录和 Git Commit 是两回事**——Commit 给开发者看，部署记录给"三个月后的自己"在服务器上看。

#### 3. 用 Shell 脚本固化部署流程

现场部署最怕的不是技术难，而是**人为输入出错**：路径打错、漏了 `cd`、环境变量没 export、前后端启动顺序搞反、手抖多敲了一个空格。这些问题在本地开发时不会出现，一到客户服务器就容易踩坑。

**原则：所有部署操作写成 `.sh` 脚本，现场只执行脚本，不手敲命令。**

建议脚本目录结构：

```
scripts/
├── deploy.sh          # 一键部署（拉代码 → 装依赖 → 构建 → 重启）
├── deploy-backend.sh  # 仅更新后端
├── deploy-frontend.sh # 仅构建并同步前端 dist
├── rollback.sh        # 回滚到上一版本
└── health-check.sh    # 部署后自动验证（端口、HTTP 200、日志无 ERROR）
```

**`deploy.sh` 应固化的事项：**

1. **路径写死**：项目根目录、虚拟环境、`dist` 输出路径全部在脚本顶部用变量定义，现场零输入。
2. **步骤可回滚**：每步 echo 当前动作；关键步骤失败时 `exit 1`，不要带着半成品继续跑。
3. **环境检查前置**：部署前检查 `uv`、`node`、`nginx`、`mysql` 是否可用，缺什么直接报错退出。
4. **自动写部署记录**：脚本末尾把本次 Git commit hash、时间、操作人设写入 `docs/DEPLOY_LOG.md`。
5. **部署后自检**：调用 `health-check.sh`，确认 8000/80 端口正常、首页和 `/api/health` 返回 200。

**示例骨架：**

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "==> [1/5] 拉取最新代码"
git pull origin main

echo "==> [2/5] 安装后端依赖"
cd backend && uv sync --no-dev

echo "==> [3/5] 构建前端"
cd "$PROJECT_ROOT/frontend" && npm ci && npm run build

echo "==> [4/5] 重启后端"
# systemctl restart myapp  或 kill + 启动 gunicorn

echo "==> [5/5] 重载 Nginx"
sudo nginx -t && sudo nginx -s reload

echo "==> 部署完成: $(git rev-parse --short HEAD) @ $(date '+%Y-%m-%d %H:%M')"
```

**记住：脚本在本地写好、测通，再带到现场执行。** 现场是修问题的地方，不是试命令的地方。

---

### 🚨 常见问题排查手册 (SOP)

- **看到 403 Forbidden**：
  - **原因**：Nginx 用户权限不足或 `dist` 路径权限过高。
  - **解决**：检查 `nginx.conf` 里的 `user` 设定；执行 `chmod +x` 你的用户目录。
- **看到 502 Bad Gateway**：
  - **原因**：Nginx 活着的，但后端 Gunicorn 挂了。
  - **解决**：重新执行第一阶段的启动命令。
- **修改了代码没生效**：
  - **原因**：前端需要重新 `build`，后端需要重新启动（或开启 Gunicorn 的 `--reload` 模式）。

## 运维常用指令集

| **任务**             | **命令**                                           |
| -------------------- | -------------------------------------------------- |
| **检查 Nginx 配置**  | `sudo nginx -t`                                    |
| **热重载 Nginx**     | `sudo nginx -s reload`                             |
| **查看进程树**       | `pstree -p <Master_PID>`                           |
| **强制停止 Nginx**   | `sudo pkill -9 nginx`                              |
| **查看最新错误日志** | `tail -n 20 /opt/homebrew/var/log/nginx/error.log` |

## 技术栈速查

### 后端
- **FastAPI** + **Uvicorn** / **Gunicorn**
- **SQLAlchemy**（async）+ **SQLite**（默认，可换 MySQL）
- **Pydantic v2** + **loguru**

### 前端
- **Vue 3** + **TypeScript** + **Vite**
- **Pinia** + **Vue Router** + **Axios** + **Tailwind CSS**

### 模版骨架（待扩展）
- AI 流水线节点：`backend/app/modules/`（ASR / LLM / TTS）
- 可观测性：`/metrics`、`/health/{node}`、链路追踪 API
- CPU 任务池：TaskPool（`POST /api/tasks/compute`）

## 核心特性

1. **异步编程**：路由使用 `async def`，数据库操作使用 `await`
2. **分层架构**：`api → services → repositories → models`
3. **日志系统**：loguru，按大小轮转（100MB / 10 天）
4. **可观测性预留**：Prometheus 指标 + trace_id 链路追踪
5. **部署脚本**：`make deploy` / `make health-check`

