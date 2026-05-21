from redis.asyncio import Redis

STATUS_PREFIX: str = 'ytdl:status:'
# A "busy" flag expires on its own, so a crashed worker cannot leave a user
# locked forever — the previous SQLite `status` column had exactly that bug.
STATUS_TTL: int = 600


class StatusStore:
    """Tracks whether a user currently has a download in progress.

    Backed by Redis keys with a TTL: the flag clears itself if the worker dies
    mid-job, replacing the non-recoverable SQLite `status` column.
    """

    def __init__(self, redis: Redis, ttl: int = STATUS_TTL) -> None:
        self._redis = redis
        self._ttl = ttl

    @staticmethod
    def _key(user_id: int) -> str:
        return f'{STATUS_PREFIX}{user_id}'

    async def set_busy(self, user_id: int) -> None:
        await self._redis.set(self._key(user_id), '1', ex=self._ttl)

    async def clear(self, user_id: int) -> None:
        await self._redis.delete(self._key(user_id))

    async def is_busy(self, user_id: int) -> bool:
        return await self._redis.exists(self._key(user_id)) == 1
