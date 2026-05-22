from aiogram import F, types

import captions
from bot.filters import IsHost
from loader import dp


@dp.message(~IsHost(), F.chat.type == "private", F.text)
async def on_unrecognized(message: types.Message) -> None:
    """Reply when a private-chat message held no recognizable YouTube link.

    Registered last among the user handlers, so /start and valid links are
    claimed by their own handlers first. Scoped to private chats so the bot
    stays silent on unrelated messages when it is added to a group.
    """

    await message.reply(captions.LINK_NOT_FOUND)
