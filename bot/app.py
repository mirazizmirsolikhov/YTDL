from logging import INFO, basicConfig

from aiogram import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from bot import filters
from loader import dp

basicConfig(level=INFO)
dp.middleware.setup(LoggingMiddleware())

if __name__ == '__main__':
    filters.setup(dp)
    executor.start_polling(dp, skip_updates=True)
