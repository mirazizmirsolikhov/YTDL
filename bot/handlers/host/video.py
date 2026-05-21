from aiogram import F, types
from aiogram.enums import ContentType
from aiogram.exceptions import TelegramForbiddenError

import captions
from bot.filters import IsHost
from loader import bot, db, dp, file_cache, status_store
from utils.transport import DownloadTask


@dp.message(IsHost(), F.content_type == ContentType.VIDEO)
async def on_host_video(message: types.Message) -> None:
    """Receive a successfully downloaded video from the host account.

    The video must physically pass through Telegram for the bot to obtain a
    file_id usable by the bot itself. The originating task travels in the
    caption as JSON (parsed safely via pydantic — no ast.literal_eval).
    """

    task: DownloadTask = DownloadTask.model_validate_json(message.caption)
    file_id: str = message.video.file_id

    # Cache the file_id so a repeated request is served without re-downloading.
    await file_cache.save(task.video_id, file_id)
    db.file_save(file_id=file_id, url=task.video_id)

    try:
        await bot.send_video(
            chat_id=task.chat_id,
            video=file_id,
            caption=captions.VIDEO_CAPTION,
        )
        db.increase_nod(user_id=task.user_id)
    except TelegramForbiddenError:
        db.set_active(user_id=task.user_id, is_active=0)
    finally:
        await status_store.clear(task.user_id)
