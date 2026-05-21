from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from config import config


class IsHost(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.from_user.id == config.host_id
