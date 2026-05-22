from aiogram import F, types

from bot.filters import IsHost
from config import config
from loader import bot, dp


@dp.message(IsHost(), F.text)
async def on_host_alert(message: types.Message) -> None:
    """Relay an operational alert from the userbot worker to the admin.

    The userbot account can reliably message the bot but not necessarily the
    admin, so worker alerts (e.g. expired YouTube cookies) travel
    host -> bot -> admin. The host account otherwise only sends videos here,
    so any plain text from it is treated as an alert and forwarded verbatim.
    """

    await bot.send_message(chat_id=config.admin_id, text=message.text)
