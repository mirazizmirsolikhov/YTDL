from typing import Union

from aiogram import types
from aiogram.utils.markdown import hbold

from loader import dp, db


@dp.message_handler(commands=['start'])
async def on_start(message: types.Message) -> None:
    """
    Registers user if one does not exist in database.
    """

    user_id: int = message.from_user.id
    first_name: str = message.from_user.first_name
    username: Union[str, None] = message.from_user.username

    if message.chat.type == 'private':
        if not db.user_exists(user_id):
            db.create_user(user_id=user_id, first_name=first_name, username=username)
        db.update_user(user_id=user_id, first_name=first_name, username=username, is_active=1)

    await message.reply(
        text=f"""👋 {hbold('Вас приветствует бот для загрузки видео.')}
\nИмеется возможность загрузки из следующих источников:
❤ {hbold('YouTube')}
❤ {hbold('YouTube Shorts')}""",
        parse_mode=types.ParseMode.HTML
    )
