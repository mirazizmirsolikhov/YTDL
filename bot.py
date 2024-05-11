from ast import literal_eval
from logging import INFO, basicConfig
from typing import Union, List, Tuple, Dict

from aiogram import Bot, Dispatcher, types, executor, filters
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils.exceptions import BotBlocked

import filters as custom_filters
from captions import *
from config import settings
from database import Database

TOKEN: str = settings.token
HOST_ID: int = settings.host_id
DATABASE_NAME: str = settings.database_name

bot: Bot = Bot(token=TOKEN)
dp: Dispatcher = Dispatcher(bot=bot)
db: Database = Database(DATABASE_NAME)

basicConfig(level=INFO)
dp.middleware.setup(LoggingMiddleware())


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

    await message.reply(text=START_MESSAGE, parse_mode=ParseMode.HTML)


@dp.message_handler(commands=['inform'])
async def admin_inform(message: types.Message) -> None:
    """
    Sends some text to all users.
    Admin status required.
    """

    user_id: int = message.from_user.id

    if message.chat.type == 'private':
        if 0 in db.is_admin(user_id):
            pass
        else:
            users: List[Tuple[int, int]] = db.get_users()
            for i in users:
                try:
                    await bot.send_message(chat_id=i[0], text=message.text.split(" ", 1)[1])
                    if int(i[1]) != 1:
                        db.set_active(user_id=i[0], is_active=1)
                except BotBlocked:
                    db.set_active(user_id=i[0], is_active=0)


@dp.message_handler(filters.IDFilter(chat_id=HOST_ID), content_types=types.ContentTypes.VIDEO)
async def host_video(message: types.Message) -> None:
    """
    Accepts video from host account.
    """

    file_id: str = message.video.file_id
    json_data: Dict[str, Union[str, int]] = literal_eval(message.caption)

    try:
        await bot.send_video(chat_id=json_data['id'], video=file_id, caption=VIDEO_CAPTION, parse_mode=ParseMode.HTML)
        db.increase_nod(user_id=json_data['id'])
        db.file_save(file_id=file_id, url=json_data['file_name'])
    except BotBlocked:
        db.set_active(user_id=json_data['id'], is_active=0)


@dp.message_handler(filters.IDFilter(chat_id=HOST_ID), content_types=types.ContentTypes.TEXT)
async def host_text(message: types.Message) -> None:
    """
    Sends an error message to user in case any error occurs.
    """

    json_data: Dict[str, Union[str, int]] = literal_eval(message.text)
    await bot.edit_message_text(
        chat_id=json_data['id'], message_id=json_data['message_id'] + 1, parse_mode=ParseMode.HTML,
        text=LINK_NOT_FOUND
    )


@dp.message_handler(custom_filters.IsCorrectLink())
async def url_determination(message: types.Message, matches: List[str]) -> None:
    """
    Validates urls using regex.
    """

    chat_id: int = message.chat.id
    message_id: int = message.message_id

    first_name: str = message.from_user.first_name
    username: str = message.from_user.username
    db.update_user(user_id=chat_id, first_name=first_name, username=username, is_active=1)

    status: Tuple[int] = db.see_status(chat_id)

    if 1 in status:
        await bot.send_message(chat_id=chat_id, text=WAIT, parse_mode=ParseMode.HTML)
    else:
        try:
            await bot.send_message(chat_id=chat_id, text=DOWNLOADING_STARTED, parse_mode=ParseMode.HTML)

            exists: Tuple[str] = db.file_exists(url=matches[0])
            if exists is not None:
                await bot.send_video(
                    chat_id=chat_id, video=exists[0], caption=VIDEO_CAPTION, parse_mode=ParseMode.HTML
                )
                db.increase_nod(user_id=chat_id)
            else:
                if len(matches) > 1:
                    await bot.send_message(chat_id=chat_id, parse_mode=ParseMode.HTML, text=MULTIPLE_LINKS)
                else:
                    file_name: str = matches[0]
                    url: str = f'https://www.youtube.com/watch?v={file_name}'

                    to_send: Dict[str, Union[str, int]] = {
                        "url": url,
                        "id": chat_id,
                        "message_id": message_id,
                        "file_name": file_name
                    }
                    await bot.send_message(chat_id=HOST_ID, text=f'{to_send}')
        except IndexError:
            await bot.edit_message_text(
                chat_id=chat_id, message_id=message.message_id + 1, text=LINK_NOT_FOUND, parse_mode=ParseMode.HTML
            )


if __name__ == '__main__':
    custom_filters.setup(dp)
    executor.start_polling(dp, skip_updates=True)
