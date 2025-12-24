# 个人全栈项目开发之路

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

## 🐍 第二部分：Python 后端开发

这里的python开发使用fastapi


一、 接口阻塞的架构级解决方案
接口响应慢通常有两种情况：I/O 密集型（等数据库、等第三方 API）和 计算密集型（处理图片、运行 AI 模型）。

1. 异步框架选型（FastAPI）
如果你还在用 Flask/Django 的同步模式，建议切换到 FastAPI。

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



