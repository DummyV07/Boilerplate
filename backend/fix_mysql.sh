#!/bin/bash

echo "=========================================="
echo "MySQL 认证修复脚本"
echo "=========================================="
echo ""
echo "这个脚本将帮助修复MySQL root用户的认证方式"
echo ""

# 检查MySQL是否运行
if ! pgrep -x "mysqld" > /dev/null; then
    echo "❌ MySQL服务未运行，请先启动MySQL"
    echo "   启动命令: brew services start mysql"
    exit 1
fi

echo "✅ MySQL服务正在运行"
echo ""
echo "请按照以下步骤操作："
echo ""
echo "1️⃣  打开新的终端窗口，执行："
echo "   sudo mysql -u root"
echo ""
echo "2️⃣  在MySQL命令行中执行以下SQL："
echo "   ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';"
echo "   FLUSH PRIVILEGES;"
echo "   EXIT;"
echo ""
echo "3️⃣  创建数据库（如果需要）："
echo "   mysql -u root -p123456 -e \"CREATE DATABASE IF NOT EXISTS chat_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\""
echo ""
echo "4️⃣  然后重新运行应用："
echo "   cd backend && uv run run.py"
echo ""
echo "=========================================="
