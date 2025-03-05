from logging import INFO, basicConfig

from aiogram import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import handlers
from bot import filters
from loader import dp

basicConfig(level=INFO)
dp.middleware.setup(LoggingMiddleware())
filters.setup(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
