from aiogram import types
from aiogram.filters import Command

import captions
from bot.services import user_service
from loader import dp


@dp.message(Command('start'))
async def on_start(message: types.Message) -> None:
    """Register the user (in private chats) and greet them."""

    if message.chat.type == 'private':
        user_service.register_or_update(message.from_user)

    await message.reply(captions.START_MESSAGE)
