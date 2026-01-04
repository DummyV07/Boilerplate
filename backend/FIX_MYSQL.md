# 修复MySQL认证问题

## 问题
错误 `(1698, "Access denied for user 'root'@'localhost'")` 表示MySQL root用户使用了socket认证而不是密码认证。

## 解决方案

### 方案1：修改root用户认证方式（推荐）

1. 使用sudo登录MySQL：
```bash
sudo mysql -u root
```

2. 在MySQL中执行以下命令：
```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '你的密码';
FLUSH PRIVILEGES;
```

3. 退出MySQL：
```sql
EXIT;
```

4. 更新 `.env` 文件中的 `DATABASE_URL`，使用你设置的密码。

### 方案2：创建新的MySQL用户（更安全）

1. 使用sudo登录MySQL：
```bash
sudo mysql -u root
```

2. 创建新用户和数据库：
```sql
CREATE DATABASE IF NOT EXISTS chat_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON chat_db.* TO 'app_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

3. 创建 `.env` 文件并更新配置：
```bash
cd backend
cp .env.example .env
# 然后编辑 .env 文件，将 DATABASE_URL 改为：
# DATABASE_URL=mysql+asyncmy://app_user:your_secure_password@localhost:3306/chat_db
```

### 方案3：使用环境变量（临时解决）

在运行应用前设置环境变量：
```bash
export DATABASE_URL="mysql+asyncmy://root:你的密码@localhost:3306/chat_db"
uv run run.py
```

## 验证连接

测试MySQL连接：
```bash
mysql -u root -p
# 或
mysql -u app_user -p
```

## 注意事项

- 生产环境请使用强密码
- 建议使用方案2创建专用应用用户
- 确保数据库 `chat_db` 已创建
