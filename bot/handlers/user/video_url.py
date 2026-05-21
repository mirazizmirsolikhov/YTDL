from typing import List

from aiogram import types

from bot.filters import IsCorrectLink, IsHost
from bot.services import download_service
from loader import dp


@dp.message_handler(IsCorrectLink(), ~IsHost())
async def on_video_url(message: types.Message, matches: List[str]) -> None:
    """Handle a YouTube link from a regular user."""

    await download_service.handle_download_request(message, matches)
