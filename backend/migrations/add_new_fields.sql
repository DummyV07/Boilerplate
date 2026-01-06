-- 数据库迁移脚本：添加新字段和表
-- 执行此脚本来更新数据库结构

-- 1. 为users表添加is_admin字段
ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT FALSE NOT NULL COMMENT '是否为管理员';

-- 2. 为attachments表添加source和is_shared字段
ALTER TABLE attachments ADD COLUMN source VARCHAR(50) DEFAULT 'direct_upload' NOT NULL COMMENT '文件来源：chat, admin, api, direct_upload';
ALTER TABLE attachments ADD COLUMN is_shared INTEGER DEFAULT 0 NOT NULL COMMENT '是否共享：0-不共享，1-共享';

-- 3. 创建feedbacks表
CREATE TABLE IF NOT EXISTS feedbacks (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户反馈表';
