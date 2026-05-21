from typing import Optional

from redis.asyncio import Redis

CACHE_PREFIX: str = 'ytdl:fileid:'


class FileCache:
    """Maps a YouTube video id to the Telegram ``file_id`` of an already
    uploaded video, so a repeated request is served instantly without
    re-downloading.
    """

    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    @staticmethod
    def _key(video_id: str) -> str:
        return f'{CACHE_PREFIX}{video_id}'

    async def get(self, video_id: str) -> Optional[str]:
        return await self._redis.get(self._key(video_id))

    async def save(self, video_id: str, file_id: str) -> None:
        await self._redis.set(self._key(video_id), file_id)
