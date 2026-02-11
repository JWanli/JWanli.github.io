# 大枪等级分（Da Qiang Elo Rating）

这是一个基于 **Vue 3 + Vite** 的前端站点，用来展示大枪（长枪）竞技对抗的 **Elo 等级分**与数据看板。

站点包含综合排行榜、选手详情页（Elo 历史曲线、荣誉、团体等）、近期活动页，并支持暗黑模式。路由采用 Hash 模式，适合部署到 GitHub Pages。

## 功能概览

- **综合排行榜**：表格展示实时排名，可排序；支持升降标记（↑ / ↓ / +）；移动端适配。
- **选手详情页**：展示团体、荣誉、简介与 **Elo 历史折线图**。
- **暗黑模式**：基于 Element Plus 暗色变量 + `@vueuse/core`。
- **GitHub Pages 友好路由**：使用 `#/...` 的 Hash History，无需服务器重写规则。

## 技术栈

- Vue 3 + Vite
- Vue Router（Hash History）
- Element Plus
- Supabase（`@supabase/supabase-js`）
- ECharts（`vue-echarts`）

## 目录结构

```
.
├─ index.html
├─ src/
│  ├─ main.js              # 应用入口
│  ├─ App.vue              # 整体布局 + 顶部导航 + 暗黑开关
│  ├─ supabase.js          # Supabase 前端客户端
│  ├─ router/index.js      # 路由配置
│  └─ views/
│     ├─ Home.vue          # 主页
│     ├─ Leaderboard.vue   # 排行榜
│     ├─ Profile.vue       # 选手详情
│     └─ Activity.vue      # 活动页
├─ asset/elo.txt           # 历史数据源（供迁移脚本使用）
+└─ python_files/           # 管理/迁移脚本（使用 Supabase 管理密钥）
```

## 本地开发

### 环境要求

- 建议 Node.js 18+

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

### 构建

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

## Supabase 配置说明

前端通过 Supabase 读取数据（典型表包括）：

- `players`（id、name、nick_name、region、current_elo、max_elo、avatar_url、activity、grade、rank_change、achievements(JSON)、bio 等）
- `teams`
- `player_teams`
- `elo_history`

### 前端 Key（公开）

前端的 Supabase 客户端目前写在 `src/supabase.js`，使用 **publishable/anon key**。

- 这是允许在浏览器中使用的 key。
- **不要**把 `service_role`（服务角色密钥）放进前端代码。

推荐改进（可选）：改为 Vite 环境变量（便于多环境/避免硬编码）

1. 新建 `.env.local`：

   ```bash
   VITE_SUPABASE_URL=...
   VITE_SUPABASE_ANON_KEY=...
   ```

2. 将 `src/supabase.js` 改为读取 `import.meta.env`。

## 数据迁移/管理脚本（Python）

仓库的 `python_files/` 下提供了将 `asset/elo.txt` 导入 Supabase 的脚本。

### 环境要求

- 建议 Python 3.10+

安装依赖：

```bash
pip install supabase python-dotenv
```

在仓库根目录（或 `python_files/` 目录）创建 `.env`：

```bash
SUPABASE_URL=...
SUPABASE_KEY=...
```

说明：

- 这里的 `SUPABASE_KEY` 通常是 **service role key**，仅用于管理脚本；务必保密且不要提交到仓库。

### 常用流程

- （可选，危险）清空表后重导：`python python_files/reset_import.py`
- 导入历史数据：`python python_files/migrate_old_data.py`
- 回填升降字段：`python python_files/backfill_rank_change.py`

## 部署（GitHub Pages）

- 路由使用 `createWebHashHistory()`，因此 GitHub Pages 上直接刷新页面也能正常访问。
- 若部署在子路径（例如 `https://user.github.io/repo/`），可能需要在 `vite.config.js` 设置 `base`。

## 许可证

当前未指定 License。
