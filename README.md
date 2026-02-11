# Da Qiang Elo Rating (大枪等级分)

[中文说明](README.zh-CN.md)

A Vue 3 + Vite web app that displays an Elo-based ranking system for traditional spear (大枪) competitive results.

It includes a real-time leaderboard, per-player profile pages (with Elo history charts and achievements), a simple activity timeline, and a dark mode toggle.

## Features

- **Leaderboard**: sortable table, rank-change indicators (↑ / ↓ / +), mobile-friendly layout.
- **Player profiles**: team tags, achievements, bio, and an **Elo history line chart**.
- **Dark mode**: uses Element Plus dark variables + `@vueuse/core`.
- **GitHub Pages friendly routing**: uses hash history (`#/...`) so it works without server rewrites.

## Tech Stack

- Vue 3 + Vite
- Vue Router (hash history)
- Element Plus
- Supabase (`@supabase/supabase-js`)
- ECharts via `vue-echarts`

## Project Structure

```
.
├─ index.html
├─ src/
│  ├─ main.js              # App entry
│  ├─ App.vue              # Layout + navbar + dark mode toggle
│  ├─ supabase.js          # Supabase client
│  ├─ router/index.js      # Routes
│  └─ views/
│     ├─ Home.vue
│     ├─ Leaderboard.vue
│     ├─ Profile.vue
│     └─ Activity.vue
├─ asset/elo.txt           # Historical data source for migration scripts
└─ python_files/           # Admin/migration utilities (Supabase service key)
```

## Getting Started

### Prerequisites

- Node.js 18+ (recommended)

### Install

```bash
npm install
```

### Development

```bash
npm run dev
```

### Build

```bash
npm run build
```

### Preview the production build

```bash
npm run preview
```

## Supabase Configuration

The app reads data from Supabase tables such as:

- `players` (id, name, nick_name, region, current_elo, max_elo, avatar_url, activity, grade, rank_change, achievements (JSON), bio, ...)
- `teams`
- `player_teams`
- `elo_history`

### Frontend key (public)

The frontend Supabase client is currently configured in `src/supabase.js` using a **publishable/anon key**.

- This key is intended to be used in browsers.
- Do **NOT** put your Supabase `service_role` key in the frontend.

Recommended improvement (optional): move the frontend config to Vite env variables:

1. Create `.env.local`:

	```bash
	VITE_SUPABASE_URL=...
	VITE_SUPABASE_ANON_KEY=...
	```

2. Update `src/supabase.js` to read from `import.meta.env`.

## Data Import / Admin Utilities (Python)

This repo includes scripts under `python_files/` to migrate historical data from `asset/elo.txt` into Supabase.

### Prerequisites

- Python 3.10+ recommended

Install dependencies:

```bash
pip install supabase python-dotenv
```

Create a `.env` file (in the repo root or inside `python_files/`) with:

```bash
SUPABASE_URL=...
SUPABASE_KEY=...
```

Notes:

- `SUPABASE_KEY` here is typically a **service role key** for admin scripts. Keep it secret and never commit it.

### Migration workflow

- (Optional) Reset tables (DANGEROUS): `python python_files/reset_import.py`
- Import historical data: `python python_files/migrate_old_data.py`
- Backfill rank change field: `python python_files/backfill_rank_change.py`

## Deployment Notes (GitHub Pages)

- Routing uses `createWebHashHistory()` so direct refresh works on GitHub Pages.
- If you deploy under a sub-path (e.g. `https://user.github.io/repo/`), you may need to set Vite `base` in `vite.config.js`.

## License

No license specified yet.
