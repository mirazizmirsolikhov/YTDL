from typing import List, Tuple

from aiogram import types
from aiogram.utils.exceptions import BotBlocked

from bot.filters import IsAdmin
from loader import dp, db, bot


@dp.message_handler(IsAdmin(), commands=['inform'])
async def admin_inform(message: types.Message) -> None:
    """
    Sends some text to all users.
    """

    if message.chat.type == 'private':
        users: List[Tuple[int, int]] = db.get_users()
        for i in users:
            try:
                await bot.send_message(chat_id=i[0], text=message.text.split(" ", 1)[1])
                if int(i[1]) != 1:
                    db.set_active(user_id=i[0], is_active=1)
            except BotBlocked:
                db.set_active(user_id=i[0], is_active=0)
