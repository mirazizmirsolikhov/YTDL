import asyncio
import logging
import os

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

import captions
from config import config
from loader import app, result_queue, task_queue
from utils.transport import DownloadResult, DownloadTask

logger = logging.getLogger(__name__)

BOT_ID: int = config.bot_id
# Upload ceiling for the host account; videos larger than this are rejected
# instead of failing mid-upload.
MAX_FILE_SIZE_MB: int = 2000


def _download(task: DownloadTask) -> None:
    """Download the video with yt-dlp. Blocking — call via an executor."""

    resolution: str = config.minimal_resolution
    ydl_opts = {
        # Cap the height at the configured resolution and prefer mp4.
        'format': (
            f'bestvideo[height<={resolution}][ext=mp4]+bestaudio[ext=m4a]/'
            f'best[height<={resolution}][ext=mp4]/best'
        ),
        'outtmpl': str(config.downloads_path / f'{task.video_id}.%(ext)s'),
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([task.url])


async def _process(task: DownloadTask) -> None:
    """Download one video and hand it to the bot, or report a failure."""

    path = config.downloads_path / f'{task.video_id}.mp4'
    try:
        await asyncio.get_running_loop().run_in_executor(None, _download, task)

        size_mb: float = os.path.getsize(path) / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            await result_queue.push(
                DownloadResult(task=task, success=False, error=captions.FILE_TOO_BIG)
            )
            return

        # The video must travel through Telegram so the bot can obtain its own
        # file_id; the task rides along in the caption as JSON.
        await app.send_video(
            chat_id=BOT_ID, video=str(path), caption=task.model_dump_json()
        )
    except DownloadError as error:
        logger.warning('Download failed for %s: %s', task.url, error)
        await result_queue.push(
            DownloadResult(task=task, success=False, error=captions.VIDEO_UNAVAILABLE)
        )
    except Exception:
        logger.exception('Unexpected error while processing %s', task.url)
        await result_queue.push(
            DownloadResult(task=task, success=False, error=captions.DOWNLOAD_FAILED)
        )
    finally:
        if path.exists():
            os.remove(path)


async def run_worker() -> None:
    """Consume download tasks from the queue until cancelled."""

    logger.info('Worker started, waiting for tasks')
    while True:
        try:
            task = await task_queue.pop(timeout=5)
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception('Failed to read from the task queue')
            await asyncio.sleep(5)
            continue

        if task is not None:
            await _process(task)
