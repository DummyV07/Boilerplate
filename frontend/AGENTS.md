---
description: 适用于 Vue 3 组合式 API 开发规范
globs: frontend/**/*.{vue,ts}
alwaysApply: false
---

# Vue 3 开发规范

## 🧩 组件编写
- 必须使用 `<script setup>` 和 TypeScript。
- 复杂的业务状态必须抽离到 `src/stores/` (Pinia)。
- 所有的 API 请求必须引用 `frontend/src/api/` 下定义的 Service，禁止在组件内直接写 Axios 调用。

## ⚠️ 防错指令
- 修改 Props 时，必须先检查父组件的传递逻辑。
- 优化 CSS 时，严禁修改已经存在的 `data-testid` 或核心逻辑相关的 HTML 结构。