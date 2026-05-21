from typing import Optional

from pydantic import BaseModel


class DownloadTask(BaseModel):
    """A request for the userbot to download a video.

    Replaces the previous dict-serialised-as-text protocol. Carries everything
    the worker needs to do the job and everything the bot needs to deliver the
    result back to the right place — including ``status_message_id`` so the
    reply no longer relies on guessing ``message_id + 1``.
    """

    url: str
    video_id: str
    user_id: int
    chat_id: int
    status_message_id: int


class DownloadResult(BaseModel):
    """The outcome of a download, published back to the bot.

    The originating task is embedded so the bot knows where to deliver the
    video (or error) without keeping any local state between request and reply.
    """

    task: DownloadTask
    success: bool
    file_id: Optional[str] = None
    error: Optional[str] = None
