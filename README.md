# YTDL - YouTube Downloader

Telegram bot based on Aiogram, Pyrogram and yt-dlp that allows to download any kind of videos from YouTube.
Bot requires an extra Telegram account for bypassing file limits for bots.

<div style="text-align: center;">
    <img alt="YouTube" src="https://img.shields.io/badge/YouTube-red?style=for-the-badge&logo=youtube&logoColor=white"/>
    <img alt="Telegram" src="https://img.shields.io/badge/Telegram-blue?&style=for-the-badge&logoColor=white&logo=telegram"/>
    <img alt="Python" src="https://img.shields.io/badge/python-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/>
    <img alt="Redis" src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white"/>
    <img alt="SQLite" src="https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white"/>
</div>

## Architecture

The project runs as **two processes** that coordinate through **Redis**:

- **bot** (`bot/`) — Aiogram bot: receives links, serves cached videos, enqueues download tasks.
- **userbot** (`userbot/`) — Pyrogram worker on an extra account: downloads videos and bypasses the bot file-size limit.

Redis carries the task queue, the result queue, per-user status flags and the `file_id` cache.

## Requirements

- **ffmpeg** — required by yt-dlp for muxing video/audio.
- **Redis** — message transport between the two processes.
- **[uv](https://docs.astral.sh/uv/)** — dependency manager (replaces pip).

```shell
sudo apt update && sudo apt upgrade -y
sudo apt install ffmpeg redis-server -y
```

## Configuring Environments

Copy `.env_example` to `.env` and fill it in:

- `ADMIN_ID` : Your account`s Telegram ID.
- `TOKEN`: Bot`s token, can be obtained here - https://t.me/BotFather.
- `BOT_ID`: Bot`s Telegram ID.
- `HOST_ID`: Telegram ID of an account that will be used to bypass the 2 GB file restriction.
- `API_ID`: Can be obtained here - https://my.telegram.org.
- `API_HASH`: Can be obtained here - https://my.telegram.org.
- `REDIS_HOST` / `REDIS_PORT` / `REDIS_DB`: Redis connection (defaults: `localhost` / `6379` / `0`).

The SQLite database is created automatically on first run.

## Running

### Docker Compose (recommended)

All persistent state (database, session, downloads) lives in `./data`, created
automatically. Before the first run, place the host account's Pyrogram session
there so the userbot starts without an interactive login:

```shell
mkdir -p data/sessions
# copy my_account.session into data/sessions/
docker compose up -d --build
```

### Manually

```shell
uv sync                       # install dependencies from uv.lock
redis-server &                # if not already running

cd bot && uv run python app.py
cd userbot && uv run python userbot.py
```

## Tests

```shell
uv run pytest
```

### Show some ❤️ and ⭐ the repo to support the project!
