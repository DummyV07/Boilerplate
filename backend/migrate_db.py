"""
数据库迁移脚本
用于添加新字段和表到现有数据库
运行方式: uv run migrate_db.py
"""
import asyncio
from sqlalchemy import text
from app.core.database import engine


async def migrate_database():
    """执行数据库迁移"""
    print("开始数据库迁移...")
    
    async with engine.begin() as conn:
        # 1. 添加users.is_admin字段
        try:
            result = await conn.execute(text("""
                SELECT COUNT(*) as count 
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'users' 
                AND COLUMN_NAME = 'is_admin'
            """))
            row = result.fetchone()
            if row and row[0] == 0:
                await conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN is_admin BOOLEAN DEFAULT FALSE NOT NULL COMMENT '是否为管理员'
                """))
                print("✓ 已添加 users.is_admin 字段")
            else:
                print("✓ users.is_admin 字段已存在，跳过")
        except Exception as e:
            print(f"处理 users.is_admin 时出错: {e}")
        
        # 2. 添加attachments.source字段
        try:
            result = await conn.execute(text("""
                SELECT COUNT(*) as count 
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'attachments' 
                AND COLUMN_NAME = 'source'
            """))
            row = result.fetchone()
            if row and row[0] == 0:
                await conn.execute(text("""
                    ALTER TABLE attachments 
                    ADD COLUMN source VARCHAR(50) DEFAULT 'direct_upload' NOT NULL COMMENT '文件来源：chat, admin, api, direct_upload'
                """))
                print("✓ 已添加 attachments.source 字段")
            else:
                print("✓ attachments.source 字段已存在，跳过")
        except Exception as e:
            print(f"处理 attachments.source 时出错: {e}")
        
        # 3. 添加attachments.is_shared字段
        try:
            result = await conn.execute(text("""
                SELECT COUNT(*) as count 
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'attachments' 
                AND COLUMN_NAME = 'is_shared'
            """))
            row = result.fetchone()
            if row and row[0] == 0:
                await conn.execute(text("""
                    ALTER TABLE attachments 
                    ADD COLUMN is_shared INTEGER DEFAULT 0 NOT NULL COMMENT '是否共享：0-不共享，1-共享'
                """))
                print("✓ 已添加 attachments.is_shared 字段")
            else:
                print("✓ attachments.is_shared 字段已存在，跳过")
        except Exception as e:
            print(f"处理 attachments.is_shared 时出错: {e}")
        
        # 4. 创建feedbacks表
        try:
            result = await conn.execute(text("""
                SELECT COUNT(*) as count 
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'feedbacks'
            """))
            row = result.fetchone()
            if row and row[0] == 0:
                await conn.execute(text("""
                    CREATE TABLE feedbacks (
                        id INTEGER PRIMARY KEY AUTO_INCREMENT,
                        user_id INTEGER NOT NULL,
                        feedback_type VARCHAR(50) NOT NULL COMMENT '反馈类型：bug, feature, complaint, other',
                        content TEXT NOT NULL COMMENT '反馈内容',
                        status VARCHAR(20) DEFAULT 'pending' NOT NULL COMMENT '处理状态：pending, processing, resolved, closed',
                        admin_comment TEXT NULL COMMENT '管理员回复',
                        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                        INDEX idx_user_id (user_id),
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户反馈表'
                """))
                print("✓ 已创建 feedbacks 表")
            else:
                print("✓ feedbacks 表已存在，跳过")
        except Exception as e:
            print(f"处理 feedbacks 表时出错: {e}")
    
    print("\n数据库迁移完成！")


if __name__ == "__main__":
    asyncio.run(migrate_database())
