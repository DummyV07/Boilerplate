# AI Chat 全栈应用

一个基于 FastAPI 和 Vue 3 的全栈 AI 对话应用，使用 Ollama 本地模型进行对话。

## 项目结构

```
my-awesome-project/
├── backend/                 # Python 后端代码 (FastAPI)
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
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml      # 一键启动全栈环境的编排文件
├── .gitignore
└── README.md
```

## 技术栈

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

## 环境搭建

### 前置要求

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose（可选）
- Ollama（需要单独安装）

### 安装 Ollama

访问 [Ollama 官网](https://ollama.ai/) 下载并安装。

安装后，拉取模型：
```bash
ollama pull llama2
```

### 方式一：Docker Compose（推荐）

1. 克隆项目
```bash
git clone <repository-url>
cd Boilerplate
```

2. 配置环境变量
```bash
cp backend/.env.example backend/.env
# 编辑 backend/.env，修改 SECRET_KEY 等配置
```

3. 启动服务
```bash
docker-compose up -d
```

4. 访问应用
- 前端: http://localhost:5173
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs

### 方式二：本地开发

#### 后端

1. 进入后端目录
```bash
cd backend
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件
```

5. 启动服务
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端

1. 进入前端目录
```bash
cd frontend
```

2. 安装依赖
```bash
npm install
```

3. 启动开发服务器
```bash
npm run dev
```

4. 访问 http://localhost:5173

## API 文档

启动后端后，访问 http://localhost:8000/docs 查看 Swagger API 文档。

### 主要 API 端点

#### 认证
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息

#### 对话
- `GET /api/conversations` - 获取所有对话
- `POST /api/conversations` - 创建新对话
- `GET /api/conversations/{id}` - 获取对话详情

#### 消息
- `POST /api/conversations/{id}/messages` - 发送消息（返回 202 和 task_id）

#### 任务
- `GET /api/tasks/{task_id}` - 获取任务状态（用于轮询）

## 使用指南

1. **注册账号**: 访问注册页面，创建新账号
2. **登录**: 使用用户名/邮箱和密码登录
3. **创建对话**: 点击"新建对话"按钮
4. **发送消息**: 在输入框输入消息，按 Ctrl+Enter 或点击发送按钮
5. **查看回复**: AI 回复会通过轮询自动获取并显示

## 开发规范

### 后端

1. **异步编程**: 必须使用 `async def` 定义路由
2. **长任务处理**: 处理时间超过 2 秒的任务必须返回 202，后台异步处理
3. **日志**: 使用 `logging` 库，禁止使用 `print`
4. **错误处理**: 统一异常处理中间件，记录 ERROR 级别日志

### 前端

1. **组件化**: 复用组件放在 `components/` 目录
2. **状态管理**: 使用 Pinia 管理全局状态
3. **API 封装**: 所有 API 调用通过 `api/` 目录下的文件
4. **类型安全**: 使用 TypeScript 确保类型安全

## 日志配置

日志文件位置：
- 应用日志: `backend/logs/app.log`
- 错误日志: `backend/logs/error.log`

日志轮转配置：
- 最大文件大小: 10MB
- 备份文件数: 5
- 日志级别: INFO

## 故障排查

### Ollama 连接失败

1. 确保 Ollama 服务正在运行
```bash
ollama serve
```

2. 检查 Ollama API 地址配置（`backend/.env` 中的 `OLLAMA_API_URL`）

3. 测试 Ollama API
```bash
curl http://localhost:11434/api/tags
```

### 数据库错误

1. 确保数据库文件有写入权限
2. 检查 `DATABASE_URL` 配置
3. 删除 `chat.db` 文件重新初始化

### 前端无法连接后端

1. 检查后端服务是否运行（http://localhost:8000/health）
2. 检查 CORS 配置
3. 检查前端代理配置（`vite.config.ts`）

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
