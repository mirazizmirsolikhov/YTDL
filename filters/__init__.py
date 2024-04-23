from aiogram import Dispatcher

from .filters import IsCorrectLink


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsCorrectLink)
