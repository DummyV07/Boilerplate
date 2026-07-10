# UI 草图目录

将项目 UI 设计资产存放在此目录，供 Cursor 开发时 `@` 引用。

## 存放规范

| 类型 | 命名建议 | 示例 |
| :--- | :--- | :--- |
| 手绘草图照片 | `wireframe_{页面}.png` | `wireframe_home.png` |
| Figma/原型导出 | `mockup_{页面}.png` | `mockup_detail.png` |
| 竞品参考截图 | `ref_{来源}.png` | `ref_competitor_chat.png` |

## 使用方式

在 Cursor 新对话中引用：

```
@AGENTS.md @ARCH_LOG.md @docs/ui/wireframe_home.png
我要开发首页，请根据 UI 图给出实现计划。
```

## 最低要求

项目启动前至少准备三个状态的草图：**首页**、**列表**、**详情**。
