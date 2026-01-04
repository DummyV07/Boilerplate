#!/bin/bash

# 创建环境变量文件脚本

# 开发环境
cat > .env.development << 'EOF'
# 开发环境配置
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_ENV=development
EOF

# 测试环境
# cat > .env.test << 'EOF'
# # 测试环境配置
# VITE_API_BASE_URL=https://test-api.example.com
# VITE_APP_ENV=test
# EOF

# 生产环境
cat > .env.production << 'EOF'
# 生产环境配置
VITE_API_BASE_URL=https://api.example.com
VITE_APP_ENV=production
EOF

echo "✅ 环境变量文件创建成功！"
echo "📁 已创建："
echo "   - .env.development"
echo "   - .env.production"
echo ""
echo "⚠️  请记得修改 .env.test 和 .env.production 中的 API 地址为实际地址"
