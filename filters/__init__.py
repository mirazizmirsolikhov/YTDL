from aiogram import Dispatcher

from .link import IsCorrectLink


def setup(dp: Dispatcher) -> None:
    """
    Adds extra filters to the dispatcher.
    """
    dp.filters_factory.bind(IsCorrectLink)
