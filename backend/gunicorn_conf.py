# gunicorn_conf.py
import multiprocessing

# 1. 监听地址与端口
bind = "127.0.0.1:8000"

# 2. 工作进程数
# 公式：CPU核心数 * 2 + 1 (这是业界通用平衡点)
workers = multiprocessing.cpu_count() * 2 + 1

# 3. 指定工作模式：必须使用 uvicorn 提供的 worker 类
worker_class = "uvicorn.workers.UvicornWorker"

# 4. 超时设置：防止某个请求处理时间过长被强行杀死
timeout = 120

# 5. 日志配置
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"