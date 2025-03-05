from typing import List, Tuple, Dict, Union

from aiogram import types
from aiogram.utils.markdown import hbold, hlink

from bot.filters import IsCorrectLink, IsHost
from config import config
from loader import dp, db, bot


@dp.message_handler(IsCorrectLink(), ~IsHost())
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
        await bot.send_message(
            chat_id=chat_id,
            text=f"""🛑 {hbold('Пожалуйста, дождитесь пока загрузится предыдущее видео.')}""",
            parse_mode=types.ParseMode.HTML
        )
    else:
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=f'''✔ {hbold("Отлично, загрузка видео началась.")}''',
                parse_mode=types.ParseMode.HTML
            )

            exists: Tuple[str] = db.file_exists(url=matches[0])
            if exists is not None:
                await bot.send_video(
                    chat_id=chat_id,
                    video=exists[0],
                    caption=f'''
{hbold('✅ Скачано с помощью ')}{hlink(title='YTDL | Скачать с Youtube/Youtube Shorts',
                                      url='https://t.me/yt_shorts_download_bot')}
💚 Спасибо за использование нашего бота!''',
                    parse_mode=types.ParseMode.HTML
                )
                db.increase_nod(user_id=chat_id)
            else:
                if len(matches) > 1:
                    await bot.send_message(
                        chat_id=chat_id,
                        parse_mode=types.ParseMode.HTML,
                        text=f'''🛑 {hbold("Пожалуйста. отправьте ссылку только на одно видео.")}'''
                    )
                else:
                    file_name: str = matches[0]
                    url: str = f'https://www.youtube.com/watch?v={file_name}'

                    to_send: Dict[str, Union[str, int]] = {
                        "url": url,
                        "id": chat_id,
                        "message_id": message_id,
                        "file_name": file_name
                    }
                    await bot.send_message(chat_id=config.host_id, text=f'{to_send}')
        except IndexError:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message.message_id + 1,
                text=f'''✋ {hbold("Упс, ссылка не найдена.")}''',
                parse_mode=types.ParseMode.HTML
            )
