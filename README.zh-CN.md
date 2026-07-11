# 大枪等级分

[English](README.md)

这是一个面向传统大枪竞技的 Elo 等级分与排行榜网站。项目将记录的对抗或比赛结果转化为易于浏览的选手排名、竞技状态与等级分历史。

<!-- TODO: 在此补充线上站点地址。 -->
<!-- TODO: 在此补充一至两张项目截图或简短演示 GIF。 -->

## 项目亮点

- **实时排行榜**：按 Elo 分数、活跃度、地区、等级与排名变化浏览选手。
- **选手档案**：展示团体、荣誉、简介、最高分与 Elo 历史曲线。
- **等级分说明**：介绍 Elo 计算模型及排行榜标识的含义。
- **响应式界面**：适配桌面端与移动端，并支持浅色/深色主题切换。
- **GitHub Pages 部署**：使用 Hash 路由，无需服务器重写规则也可正常刷新页面。

## 技术栈

- Vue 3 与 Vite
- Vue Router（Hash History）
- Element Plus 与 `@vueuse/core`
- Supabase
- ECharts（通过 `vue-echarts` 集成）
- GitHub Actions 与 GitHub Pages

## 项目结构

```text
.
├── src/
│   ├── assets/              # 项目图片资源
│   ├── router/index.js      # 路由配置
│   ├── views/               # 首页、排行榜、信息页与选手详情页
│   ├── App.vue              # 公共布局、导航与主题切换
│   ├── main.js              # 应用入口
│   └── supabase.js          # Supabase 客户端配置
├── python_files/
│   ├── asset/               # 历史 Elo 原始数据
│   ├── migrate_old_data.py  # 历史数据导入工具
│   ├── backfill_rank_change.py
│   └── reset_import.py      # 会清空数据的重置工具
├── .github/workflows/
│   └── deploy.yml           # GitHub Pages 自动部署工作流
├── package.json
└── vite.config.js
```

## 本地开发

### 环境要求

- 建议使用 Node.js 20 或更高版本（部署工作流使用 Node.js 20）。
- 仅在运行数据维护脚本时，建议安装 Python 3.10 或更高版本。

### 安装与启动

```bash
npm install
npm run dev
```

### 构建与预览

```bash
npm run build
npm run preview
```

## Supabase 数据

网站通过 Supabase 读取选手、团体、选手与团体关系以及 Elo 历史数据。应用所需的数据表包括：

- `players`
- `teams`
- `player_teams`
- `elo_history`

### 安全说明

浏览器端只能使用 Supabase 的 publishable/anonymous key，并应配合正确的 Row Level Security（RLS）策略。不要将 `service_role` key 写入前端代码、README 或任何被提交的环境文件。

生产环境建议通过 Vite 环境变量配置客户端，例如：

```bash
VITE_SUPABASE_URL=your-project-url
VITE_SUPABASE_ANON_KEY=your-publishable-key
```

<!-- TODO: 补充数据库结构、RLS 策略和前端配置的正式流程。 -->

## 历史数据维护

`python_files/` 提供历史 Elo 数据导入及排行榜字段维护工具。

安装 Python 依赖：

```bash
pip install supabase python-dotenv
```

在仓库根目录或 `python_files/` 中创建不提交到 Git 的 `.env` 文件：

```bash
SUPABASE_URL=your-project-url
SUPABASE_KEY=your-server-side-key
```

常用命令：

```bash
python python_files/migrate_old_data.py
python python_files/backfill_rank_change.py
```

> 注意：`python python_files/reset_import.py` 会重置已导入的数据。执行前请审查脚本内容并完成数据库备份。

<!-- TODO: 补充日常数据更新、审核要求与备份位置。 -->

## 部署

向 `main` 分支推送代码会触发 `.github/workflows/deploy.yml`。该工作流会使用 `npm ci` 安装依赖、构建 Vite 应用，并将 `dist/` 部署到 GitHub Pages。

项目使用 Hash 路由（`#/...`），因此可以兼容静态托管环境中的直接访问与刷新。

<!-- TODO: 如适用，请补充 GitHub Pages 设置及自定义域名配置。 -->

## TODO

<!-- TODO: 补充维护者名称与联系方式。 -->
<!-- TODO: 补充贡献说明，或链接至 CONTRIBUTING.md。 -->
<!-- TODO: 选择并补充开源许可证。 -->
- [ ] **TODO：**将 Python 脚本改为增量更新，不再采用“清空后重新写入”的流程。
- [ ] **TODO：**增加“大枪地图”页面的外链与海报。
