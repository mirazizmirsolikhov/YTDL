# CLAUDE.md

Guidance for Claude Code working on this project.

## Project

YTDL — a Telegram bot that downloads YouTube / YouTube Shorts videos. It runs
as **two processes coordinated through Redis**:

- `bot/` — Aiogram bot: receives links, serves cached videos, enqueues download
  tasks, delivers results.
- `userbot/` — Pyrogram worker on a second Telegram account: pulls tasks off the
  queue, downloads with yt-dlp, uploads the video to the bot (this is how the
  bot file-size limit is bypassed).

Redis carries the task queue, the result queue, per-user "busy" status (with a
TTL), and the `file_id` cache. SQLite (`users.db`) holds users and a durable
`file_id` backup.

See `README.md` for setup and `REFACTORING.md` for architecture history.

## Git

- Commit only as the user (Miraziz Mirsolikhov). Do NOT add a
  `Co-Authored-By: Claude` trailer or any Claude attribution.
- Work on `dev`; `main` is updated via pull request.

## Running

- Local: `uv sync`, run Redis, then `uv run python bot/app.py` and
  `uv run python userbot/userbot.py`.
- Docker: `docker compose up -d --build`. All persistent state lives in `./data`
  (bind-mounted): `data/users.db`, `data/sessions/`, `data/downloads/`,
  `data/cookies.txt`.
- Tests: `uv run pytest`.

## Key gotchas

- **Python is pinned to 3.11** (`pyproject.toml`) — aiogram 2.25.1 needs
  aiohttp 3.8.x, which has no wheels for 3.12+.
- **Pyrogram session** — the userbot needs `data/sessions/my_account.session`.
  `docker compose up` has no TTY for the interactive first login; create the
  session with `docker compose run --rm userbot`, or copy an existing session
  file in. Never run the same session on two machines at once.
- **YouTube on a VPS** — datacenter IPs hit "Sign in to confirm you're not a
  bot". Fix: provide `data/cookies.txt` (Netscape format, exported from a
  logged-in browser). yt-dlp also needs a JS runtime — `deno` (in the Docker
  image) plus the `yt-dlp-ejs` package.
- **Dependency management is uv** — `pyproject.toml` + `uv.lock`, no
  `requirements.txt` or pip.
- Entry points (`bot/app.py`, `userbot/userbot.py`) bootstrap the project root
  onto `sys.path`, so they run from their own folders without `PYTHONPATH`.
- Importing `utils.transport` is kept independent of `utils.db`/`config` —
  don't make `utils/__init__.py` eagerly import submodules.

## Deployment

Runs on a VPS via `docker compose` (from the `main` branch), with
`restart: unless-stopped`. The bot and userbot share `./data`; YouTube cookies
expire periodically and need re-exporting into `data/cookies.txt`.

Auto-deploy: a push to `main` triggers `.github/workflows/deploy.yml` — it runs
`pytest`, then SSHes into the VPS and runs `deploy.sh`. `deploy.sh` pulls
`origin/main`, rebuilds, restarts, and rolls back to the previous commit if the
build fails or a container does not come up. It is also safe to run by hand on
the VPS.
