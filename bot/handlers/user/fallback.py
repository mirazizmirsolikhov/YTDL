from aiogram import F, types

import captions
from bot.filters import IsHost
from loader import dp


@dp.message(~IsHost(), F.text)
async def on_unrecognized(message: types.Message) -> None:
    """Reply when a regular user's message held no recognizable YouTube link.

    Registered last among the user handlers, so /start and valid links are
    claimed by their own handlers first; this catches every other text
    message from a non-host user instead of leaving it with silence.
    """

    await message.reply(captions.LINK_NOT_FOUND)
