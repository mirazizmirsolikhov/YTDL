from ast import literal_eval
from typing import Dict, Union

from aiogram import types
from aiogram.utils.markdown import hbold

from bot.filters import IsHost
from loader import dp, bot


@dp.message_handler(IsHost(), content_types=types.ContentTypes.TEXT)
async def host_text(message: types.Message) -> None:
    """
    Sends an error message to user in case any error occurs.
    """

    json_data: Dict[str, Union[str, int]] = literal_eval(message.text)
    await bot.edit_message_text(
        chat_id=json_data['id'],
        message_id=json_data['message_id'] + 1,
        parse_mode=types.ParseMode.HTML,
        text=f'''✋ {hbold("Упс, ссылка не найдена.")}'''
    )
