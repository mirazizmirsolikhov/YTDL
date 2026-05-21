from aiogram import Dispatcher

from .is_admin import IsAdmin
from .is_host import IsHost
from .link import IsCorrectLink


def setup(dp: Dispatcher) -> None:
    """
    Adds extra filters to the dispatcher.
    """

    dp.filters_factory.bind(IsCorrectLink)
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsHost)
