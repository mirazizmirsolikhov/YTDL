from typing import List, Optional, Tuple

from aiogram import types

import captions
from bot.services import user_service
from loader import bot, db, file_cache, status_store, task_queue
from utils.transport import DownloadTask

VIDEO_URL_TEMPLATE: str = 'https://www.youtube.com/watch?v={}'


async def _lookup_cache(video_id: str) -> Optional[str]:
    """Return a cached Telegram file_id for the video, if one exists.

    Redis is the fast path; the SQLite ``links`` table is a durable backup
    that also covers a flushed Redis (its fate is decided in stage 4.2).
    """

    cached: Optional[str] = await file_cache.get(video_id)
    if cached is not None:
        return cached

    row: Optional[Tuple[str]] = db.file_exists(url=video_id)
    return row[0] if row is not None else None


async def handle_download_request(message: types.Message, matches: List[str]) -> None:
    """Entry point for an incoming YouTube link.

    Decides between serving from cache, rejecting (busy / multiple links) and
    enqueueing a download task for the userbot worker.
    """

    user: types.User = message.from_user
    user_service.register_or_update(user)

    if len(matches) > 1:
        await message.reply(captions.MULTIPLE_LINKS)
        return

    if await status_store.is_busy(user.id):
        await message.reply(captions.WAIT)
        return

    video_id: str = matches[0]

    cached: Optional[str] = await _lookup_cache(video_id)
    if cached is not None:
        await bot.send_video(
            chat_id=message.chat.id,
            video=cached,
            caption=captions.VIDEO_CAPTION,
        )
        db.increase_nod(user_id=user.id)
        return

    # The reply's message_id is carried in the task so the worker's result can
    # be delivered to the exact message — no more guessing message_id + 1.
    status_message: types.Message = await message.reply(captions.DOWNLOADING_STARTED)
    await status_store.set_busy(user.id)

    task = DownloadTask(
        url=VIDEO_URL_TEMPLATE.format(video_id),
        video_id=video_id,
        user_id=user.id,
        chat_id=message.chat.id,
        status_message_id=status_message.message_id,
    )
    await task_queue.push(task)
