from ast import literal_eval
from logging import INFO, basicConfig
from os import getenv
from re import findall

from aiogram import Bot, Dispatcher, types, filters
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils.exceptions import BotBlocked
from dotenv import load_dotenv

from captions import *
from database import Database

load_dotenv()
TOKEN = getenv('TOKEN')
HOST_ID = getenv('HOST_ID')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
db = Database('users.db')

basicConfig(level=INFO)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    """
    Start command handler.
    Registers user if one does not exist in database.
    """
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username

    if message.chat.type == 'private':
        if not db.user_exists(user_id):
            db.create_user(user_id=user_id, first_name=first_name, username=username)
        db.update_user(user_id=user_id, first_name=first_name, username=username, is_active=1)

    await message.reply(text=START_MESSAGE, parse_mode=ParseMode.HTML)


@dp.message_handler(commands=['inform'])
async def admin_inform(message: types.Message):
    """
    Sends some text to all users.
    Admin status required.
    """
    user_id = message.from_user.id

    if message.chat.type == 'private':
        if 0 in db.is_admin(user_id):
            pass
        else:
            users = db.get_users()
            for i in users:
                try:
                    await bot.send_message(chat_id=i[0], text=message.text.split(" ", 1)[1])
                    if int(i[1]) != 1:
                        db.set_active(user_id=i[0], is_active=1)
                except BotBlocked:
                    db.set_active(user_id=i[0], is_active=0)


@dp.message_handler(filters.IDFilter(chat_id=int(HOST_ID)), content_types=types.ContentTypes.VIDEO)
async def host_video(message: types.Message):
    """
    Accepts video from host account.
    """
    file_id = message.video.file_id
    json_data = literal_eval(message.caption)

    try:
        await bot.send_video(chat_id=json_data['id'], video=file_id, caption=VIDEO_CAPTION, parse_mode=ParseMode.HTML)
        db.increase_nod(user_id=json_data['id'])
        db.file_save(file_id=file_id, url=json_data['file_name'])
    except BotBlocked:
        db.set_active(user_id=json_data['id'], is_active=0)


@dp.message_handler(filters.IDFilter(chat_id=int(HOST_ID)), content_types=types.ContentTypes.TEXT)
async def host_text(message: types.Message):
    """
    Sends an error message to user in case any error occurs.
    """
    json_data = literal_eval(message.text)

    await bot.edit_message_text(
        chat_id=json_data['id'], message_id=json_data['message_id'] + 1, parse_mode=ParseMode.HTML,
        text=LINK_NOT_FOUND
    )


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def url_determination(message: types.Message):
    """
    Validates urls using regex.
    """
    chat_id = message.chat.id
    message_id = message.message_id

    first_name = message.from_user.first_name
    username = message.from_user.username
    db.update_user(user_id=chat_id, first_name=first_name, username=username, is_active=1)

    status = db.see_status(chat_id)

    if 1 in status:
        await bot.send_message(chat_id=chat_id, text=WAIT, parse_mode=ParseMode.HTML)
    else:
        try:
            await bot.send_message(chat_id=chat_id, text=DOWNLOADING_STARTED, parse_mode=ParseMode.HTML)

            pattern1 = r'(?:https?://)?(?:www\.)?youtube\.com/shorts/([A-Za-z0-9_-]+)(?:\?si=[A-Za-z0-9_-]+)?'
            matches1 = findall(pattern1, message.text)
            pattern2 = r'(?:youtu\.be/|youtube\.com/watch\?v=)([A-Za-z0-9_-]+)'
            matches2 = findall(pattern2, message.text)

            matches = matches1 + matches2

            exists = db.file_exists(url=matches[0])
            if exists is not None:
                await bot.send_video(
                    chat_id=chat_id, video=exists[0], caption=VIDEO_CAPTION, parse_mode=ParseMode.HTML
                )
                db.increase_nod(user_id=chat_id)
            else:
                if len(matches) > 1:
                    await bot.send_message(chat_id=chat_id, parse_mode=ParseMode.HTML, text=MULTIPLE_LINKS)
                else:
                    file_name = matches[0]
                    url = f'https://www.youtube.com/watch?v={file_name}'

                    to_send = {
                        "url": url,
                        "id": chat_id,
                        "message_id": message_id,
                        "file_name": file_name
                    }
                    await bot.send_message(chat_id=int(HOST_ID), text=f'{to_send}')
        except IndexError:
            await bot.edit_message_text(
                chat_id=chat_id, message_id=message.message_id + 1, text=LINK_NOT_FOUND, parse_mode=ParseMode.HTML
            )


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
