# 个人全栈项目开发之路


# 1月29日记
这是一份为您定制的 **《一人公司：Cursor 全栈开发实战 SOP》**。

这份指南总结了我们之前的讨论，旨在解决你“后期 AI 变笨”、“逻辑被破坏”以及“想法被阉割”的核心痛点。

请记住：**你不再是单纯的程序员（Coder），你是产品经理 + 架构师 + 验收测试员。Cursor 是你手下那个“打字极快、懂所有语言、但记性只有 7 秒的实习生”。**

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
* **架构**：FastAPI (后端) + Vue3 (前端) + 双通道 WS。
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
* 不要写具体功能。先写一个简单的 WS 接口，前端发一个“Ping”，后端回一个“Pong”。
* **目的**：验证前后端连接、跨域配置、环境依赖（Python/Node）是否正常。



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

### 🚀 你的第一步行动清单

1. [ ] **创建 `AGENTS.md**`：复制我们定稿的 Markdown 内容进去。
2. [ ] **创建 `ARCH_LOG.md**`：新建一个空文件。
3. [ ] **画图**：在纸上画出 UI 草图，拍照，存入电脑。
4. [ ] **开工**：打开 Cursor，输入：
> “你好，我是你的首席架构师。请读取 @AGENTS.md 和 @ARCH_LOG.md。我们现在的目标是初始化项目结构。请根据文档，为我生成创建 backend 和 frontend 目录的脚本。”



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

### 项目结构

```
my-awesome-project/
├── backend/                # Python 后端代码 (FastAPI)
│   ├── app/
│   │   ├── api/            # 接口路由层
│   │   ├── core/           # 全局配置、常量、安全设置
│   │   ├── models/         # 数据库模型层 (SQLAlchemy)
│   │   ├── schemas/        # 数据验证层 (Pydantic)
│   │   ├── services/       # 核心业务逻辑层
│   │   └── main.py         # 声明入口
│   ├── run.py/             # 点火器
│   ├── tests/              # 单元测试与集成测试
│   ├── requirements.txt    # 依赖管理
│   └── .env                # 环境变量
├── frontend/               # Vue.js 前端代码 (Vue 3 + Vite)
│   ├── src/
│   │   ├── api/            # 封装 Axios 请求
│   │   ├── assets/         # 静态资源
│   │   ├── components/     # 复用组件
│   │   ├── views/          # 页面级组件
│   │   ├── store/          # 状态管理 (Pinia)
│   │   ├── router/         # 路由配置
│   │   └── utils/          # 工具函数
│   ├── package.json        # 前端依赖管理
│   └── vite.config.ts      # Vite 配置文件
├── docker-compose.yml      # 一键启动全栈环境的编排文件
├── .gitignore
└── README.md
```


## 💾 数据库配置（MySQL）

项目已配置为使用 **MySQL** 数据库（替代 SQLite）。

### 1. 安装 MySQL

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

### 2. 创建数据库

登录 MySQL 并创建数据库：

```bash
mysql -u root -p
```

在 MySQL 命令行中执行：

```sql
CREATE DATABASE chat_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 3. 配置环境变量

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

### 4. 安装依赖

确保已安装 MySQL 异步驱动：

```bash
cd backend
uv sync  # 或 pip install -r requirements.txt
```

依赖已在 `pyproject.toml` 中配置：
- `asyncmy>=0.2.9` - MySQL 异步驱动

### 5. 初始化数据库表

启动后端服务时，数据库表会自动创建（通过 `init_db()` 函数）。

或者手动初始化：

```python
# 在 Python 交互式环境中
from app.core.database import init_db
import asyncio

asyncio.run(init_db())
```

### 6. 数据库连接池配置

在 `.env` 文件中可以配置连接池参数：

```bash
DB_POOL_SIZE=10          # 连接池大小
DB_MAX_OVERFLOW=20       # 最大溢出连接数
DB_POOL_RECYCLE=3600     # 连接回收时间（秒）
DB_ECHO=False            # 是否打印 SQL（开发时可设为 True）
```

### 7. 验证连接

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

## 🎨 第三部分：VUE 前端开发

1. **环境变量隔离**：区分 `development` 和 `production` 环境的 API 地址。
2. **状态管理规范**：
   - 简单的组件传参用 `props`。
   - 跨页面、跨组件的全局数据（如用户信息、Token）必须存入 **Pinia**。
3. **请求封装**：统一封装 Axios 拦截器，全局处理 401（登录过期）、500（服务器错误）等状态码。
   
frontend/
├── package.json          # 项目配置（类似 requirements.txt）
├── vite.config.ts        # 构建工具配置
├── index.html            # 入口 HTML（类似传统 HTML 的 <body>）
└── src/
    ├── main.ts           # 应用入口（类似传统 JS 的入口文件）
    ├── App.vue           # 根组件（类似传统 HTML 的 <body> 容器）
    │
    ├── views/            # 页面级组件（类似传统的一个完整 HTML 页面）
    │   ├── Login.vue     # 登录页
    │   ├── Register.vue  # 注册页
    │   └── Chat.vue      # 聊天页
    │
    ├── components/       # 可复用组件（类似传统的小功能块）
    │   ├── ChatInput.vue      # 聊天输入框
    │   ├── MessageBubble.vue  # 消息气泡
    │   └── LoadingSpinner.vue  # 加载动画
    │
    ├── router/           # 路由配置（类似传统网站的页面跳转）
    │   └── index.ts      # 定义哪些 URL 对应哪个页面
    │
    ├── store/            # 状态管理（类似全局变量，但更强大）
    │   ├── auth.ts       # 用户登录状态
    │   └── conversations.ts  # 对话数据
    │
    ├── api/              # API 请求封装（类似传统 JS 的 fetch/axios 调用）
    │   ├── auth.ts       # 登录/注册接口
    │   ├── conversations.ts
    │   └── messages.ts
    │
    └── utils/            # 工具函数（类似传统 JS 的工具函数）
        ├── request.ts    # 统一的 HTTP 请求封装
        └── polling.ts    # 轮询工具



目录/文件	作用	类比传统开发
views/	完整页面（如登录页、聊天页）	一个完整的 HTML 页面
components/	可复用的小组件（如按钮、输入框）	HTML 中的 <div> 片段，可在多处使用
router/	定义 URL 和页面的对应关系	传统网站的页面跳转逻辑
store/	全局状态（如用户信息、对话列表）	全局变量，但更安全、可追踪
api/	封装后端接口调用	传统 JS 中的 fetch() 或 axios.get()
utils/	工具函数	传统 JS 中的辅助函数



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

## AI-chats技术栈

### 后端
- **FastAPI**: 异步 Web 框架
- **SQLAlchemy**: 异步 ORM
- **Pydantic**: 数据验证
- **python-jose**: JWT 认证
- **aiohttp**: 异步 HTTP 客户端（调用 Ollama）
- **SQLite**: 数据库（开发环境）

### 前端
- **Vue 3**: 前端框架（Composition API）
- **Vite**: 构建工具
- **Pinia**: 状态管理
- **Axios**: HTTP 客户端
- **Vue Router**: 路由管理
- **Element Plus**: UI 组件库

### AI 服务
- **Ollama**: 本地 AI 模型服务

## 核心特性

1. **异步编程**: 所有路由使用 `async def`，数据库操作使用 `await`
2. **长任务处理**: 消息发送接口立即返回 202，后台异步处理，前端轮询获取结果
3. **日志系统**: 使用 `RotatingFileHandler`，按大小轮转，INFO/ERROR 分级
4. **JWT 认证**: 安全的用户认证机制
5. **实时对话**: 支持多轮对话，保存对话历史



