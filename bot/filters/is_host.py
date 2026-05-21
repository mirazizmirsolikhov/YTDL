from aiogram import types
from aiogram.filters import BaseFilter

from config import config


class IsHost(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id == config.host_id
