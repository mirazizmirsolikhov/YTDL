import asyncio
from logging import INFO, basicConfig

from aiogram import Dispatcher, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import handlers
from bot import filters
from loader import dp
from result_listener import listen_results

basicConfig(level=INFO)
dp.middleware.setup(LoggingMiddleware())
filters.setup(dp)


async def on_startup(_: Dispatcher) -> None:
    """Start the background task that delivers download failures to users."""

    asyncio.create_task(listen_results())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
