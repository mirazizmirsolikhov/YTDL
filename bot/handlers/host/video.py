from ast import literal_eval
from typing import Dict, Union

from aiogram import types
from aiogram.utils.exceptions import BotBlocked
from aiogram.utils.markdown import hlink, hbold

from bot.filters import IsHost
from loader import dp, db, bot


@dp.message_handler(IsHost(), content_types=types.ContentTypes.VIDEO)
async def host_video(message: types.Message) -> None:
    """
    Accepts video from host account.
    """

    file_id: str = message.video.file_id
    json_data: Dict[str, Union[str, int]] = literal_eval(message.caption)

    try:
        await bot.send_video(
            chat_id=json_data['id'],
            video=file_id,
            caption=f'''
{hbold('✅ Скачано с помощью ')}{hlink(title='YTDL | Скачать с Youtube/Youtube Shorts',
                                      url='https://t.me/yt_shorts_download_bot')}
💚 Спасибо за использование нашего бота!''',
            parse_mode=types.ParseMode.HTML
        )
        db.increase_nod(user_id=json_data['id'])
        db.file_save(file_id=file_id, url=json_data['file_name'])
    except BotBlocked:
        db.set_active(user_id=json_data['id'], is_active=0)
