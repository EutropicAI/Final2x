# AGENTS.md

Guidance for AI coding agents working in this repository. The commands below are the ones CI actually runs (`.github/workflows/CI-test.yml`, `CI-build.yml`, `CI-test-core.yml`); treat them as the source of truth.

## What this is

Final2x is an Electron + Vue 3 desktop app (image upscaler) with a Python core:

- `src/main` — Electron main process (IPC handlers, core process management, e.g. `getCorePath.ts`, `runCommand.ts`).
- `src/preload` — preload bridge.
- `src/renderer/src` — Vue 3 + Naive UI frontend; UI copy lives in `src/renderer/src/locales/*.ts` (`en`, `zh`, `ja`, `fr`, `tr`) — keep locale keys in sync across all five when adding strings.
- `src/shared` — types and constants shared between main and renderer.
- `core/` — the Python package `Final2x_core` (upscaling pipeline; entry point `Final2x-core`, main modules `SRclass.py`, `SRqueue.py`, `config.py`), managed with `uv` (`core/pyproject.toml`).
- `resources/Final2x-core` — where the packaged Python core lands for local runs.

## Commands

Frontend (CI runs pnpm with `node@24`, lockfile required):

```sh
pnpm install                 # setup (postinstall runs electron-builder install-app-deps)
pnpm run lint                # eslint .
pnpm run typecheck           # tsc (node config) + vue-tsc (web config)
pnpm run test                # vitest run --coverage (tests in test/)
pnpm run dev                 # electron-vite dev
pnpm run build               # electron-vite build
pnpm run build:mac-arm64     # also :mac-x64 / :win-x64 / :win-arm64 / :linux-x64 / :linux-arm64
```

Python core (uv):

```sh
uv sync --project core --locked              # runtime deps
uv sync --project core --locked --group dev  # with dev tooling (what CI uses to build)
python scripts/check_version.py              # version consistency check (CI runs this first)
```

CI (`CI-test.yml`) gates a PR on `check_version.py` → `lint` → `typecheck` → `test`, plus the core test job in `CI-test-core.yml`. Run those four before pushing.

## Conventions

- PRs follow the repo templates (`.github/ISSUE_TEMPLATE`); issue tracker is English-first with Chinese/Japanese welcome text — reply in the language of the thread.
- Frontend style: Vue SFC + `<script setup>`; eslint (`eslint.config.js`, flat config) is the arbiter, run `pnpm run lint:fix` rather than reformatting by hand.
- Core style: the pre-commit config in `core/.pre-commit-config.yaml` applies to the Python package.
- Version bumps: `package.json`, the installer metadata, and core version are cross-checked by `scripts/check_version.py` — bump them together.
