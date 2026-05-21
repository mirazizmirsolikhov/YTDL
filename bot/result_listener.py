import asyncio
import logging

import captions
from loader import bot, result_queue, status_store

logger = logging.getLogger(__name__)


async def listen_results() -> None:
    """Background task: deliver download failures back to users.

    Successful downloads arrive as video messages (handled by the host video
    handler); only failures travel through the result queue, because the queue
    cannot carry the video bytes or a bot-usable file_id.
    """

    logger.info('Result listener started')
    while True:
        try:
            result = await result_queue.pop(timeout=5)
        except Exception:
            logger.exception('Failed to read from the result queue')
            await asyncio.sleep(5)
            continue

        if result is None:
            continue

        task = result.task
        try:
            await bot.edit_message_text(
                chat_id=task.chat_id,
                message_id=task.status_message_id,
                text=result.error or captions.DOWNLOAD_FAILED,
            )
        except Exception:
            logger.exception('Failed to deliver a result to user %s', task.user_id)
        finally:
            await status_store.clear(task.user_id)
