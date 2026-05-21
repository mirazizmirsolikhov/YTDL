import asyncio
import logging
import os

from pyrogram import idle

from config import config
from loader import app
from worker import run_worker

logging.basicConfig(level=logging.INFO)

os.makedirs(config.downloads_path, exist_ok=True)
os.makedirs(config.session_path, exist_ok=True)


async def main() -> None:
    """Run the pyrogram client alongside the task-queue worker."""

    await app.start()
    worker_task = asyncio.create_task(run_worker())
    try:
        await idle()
    finally:
        worker_task.cancel()
        await app.stop()


if __name__ == '__main__':
    asyncio.run(main())
