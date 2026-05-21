from aiogram import types

import captions
from bot.services import user_service
from loader import dp


@dp.message_handler(commands=['start'])
async def on_start(message: types.Message) -> None:
    """Register the user (in private chats) and greet them."""

    if message.chat.type == 'private':
        user_service.register_or_update(message.from_user)

    await message.reply(captions.START_MESSAGE, parse_mode=types.ParseMode.HTML)
