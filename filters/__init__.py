from aiogram import Dispatcher

from .link import IsCorrectLink


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsCorrectLink)
