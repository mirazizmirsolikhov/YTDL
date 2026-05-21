import sys
from pathlib import Path

# Ensure the project root is importable when run as a script from this folder.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
from logging import INFO, basicConfig

import handlers  # noqa: F401 — importing registers the handlers on `dp`
from loader import bot, dp
from result_listener import listen_results

basicConfig(level=INFO)


async def main() -> None:
    """Start the result listener and begin long-polling."""

    listener = asyncio.create_task(listen_results())
    # Drop updates accumulated while the bot was down (old `skip_updates`).
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        listener.cancel()


if __name__ == '__main__':
    asyncio.run(main())
