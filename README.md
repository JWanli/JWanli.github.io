# Da Qiang Elo Rating

[简体中文](README.zh-CN.md)

An Elo-based rating and leaderboard website for traditional spear (大枪) competition. It turns recorded match results into an accessible view of player rankings, competitive form, and rating history.

<!-- TODO: Add the public site URL here. -->
<!-- TODO: Add one or two screenshots or a short demo GIF here. -->

## Highlights

- **Live leaderboard** — browse players by Elo rating, activity, region, grade, and rank movement.
- **Player profiles** — view team information, achievements, biography, peak rating, and Elo history charts.
- **Rating guide** — explains the Elo calculation model and the meaning of leaderboard indicators.
- **Responsive interface** — works across desktop and mobile layouts, with a light/dark theme toggle.
- **GitHub Pages deployment** — uses hash-based routing so page refreshes work without server-side rewrites.

## Technology

- Vue 3 and Vite
- Vue Router with hash history
- Element Plus and `@vueuse/core`
- Supabase
- ECharts through `vue-echarts`
- GitHub Actions and GitHub Pages

## Project layout

```text
.
├── src/
│   ├── assets/              # Project images
│   ├── router/index.js      # Application routes
│   ├── views/               # Home, leaderboard, information, and profile views
│   ├── App.vue              # Shared layout, navigation, and theme switch
│   ├── main.js              # Application entry point
│   └── supabase.js          # Supabase client configuration
├── python_files/
│   ├── asset/               # Historical Elo source data
│   ├── migrate_old_data.py  # Historical data import utility
│   ├── backfill_rank_change.py
│   └── reset_import.py      # Destructive database reset utility
├── .github/workflows/
│   └── deploy.yml           # GitHub Pages workflow
├── package.json
└── vite.config.js
```

## Local development

### Requirements

- Node.js 20 or later is recommended (the deployment workflow uses Node.js 20).
- Python 3.10 or later is recommended only when running the data-maintenance scripts.

### Install and run

```bash
npm install
npm run dev
```

### Build and preview

```bash
npm run build
npm run preview
```

## Supabase data

The web client reads player, team, player-team relationship, and Elo-history data from Supabase. The application expects tables equivalent to:

- `players`
- `teams`
- `player_teams`
- `elo_history`

### Security note

Browser code may use only a Supabase publishable/anonymous key protected by appropriate Row Level Security policies. Never expose a `service_role` key in frontend code, documentation, or a committed environment file.

For a production setup, configure the client using Vite environment variables, for example:

```bash
VITE_SUPABASE_URL=your-project-url
VITE_SUPABASE_ANON_KEY=your-publishable-key
```

<!-- TODO: Document the database schema, Row Level Security policies, and the approved frontend configuration process. -->

## Historical data maintenance

The `python_files/` directory contains utilities for importing historical Elo data and maintaining leaderboard fields.

Install the Python dependencies:

```bash
pip install supabase python-dotenv
```

Create an untracked `.env` file in the repository root or `python_files/` directory:

```bash
SUPABASE_URL=your-project-url
SUPABASE_KEY=your-server-side-key
```

Common commands:

```bash
python python_files/migrate_old_data.py
python python_files/backfill_rank_change.py
```

> Warning: `python python_files/reset_import.py` resets imported data. Review the script and back up the database before running it.

<!-- TODO: Describe the standard data-update process, required review, and backup location. -->

## Deployment

Pushing to the `main` branch triggers `.github/workflows/deploy.yml`. The workflow installs dependencies with `npm ci`, builds the Vite app, and deploys `dist/` to GitHub Pages.

The router uses hash history (`#/...`), which keeps direct navigation and refreshes compatible with static hosting.

<!-- TODO: Add the repository's GitHub Pages settings and custom-domain instructions, if applicable. -->

## TODO

<!-- TODO: Add the maintainer name and contact channel. -->
<!-- TODO: Add contribution guidelines or link to CONTRIBUTING.md. -->
<!-- TODO: Choose and add a license. -->
- [ ] **TODO:** Update the Python utilities to use incremental imports instead of a reset-and-reimport workflow.
- [ ] **TODO:** Add an external link and poster for the Da Qiang Map page.
