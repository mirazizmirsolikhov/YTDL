from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from redis.asyncio import Redis

# Redis keys for the two queues that connect the bot and the userbot.
TASKS_KEY: str = 'ytdl:tasks'
RESULTS_KEY: str = 'ytdl:results'

M = TypeVar('M', bound=BaseModel)


class RedisQueue(Generic[M]):
    """A reliable FIFO queue of pydantic models backed by a Redis list.

    Unlike pub/sub, items survive a consumer being offline: they wait in the
    list until something pops them. ``LPUSH`` + ``BRPOP`` give FIFO ordering.
    """

    def __init__(self, redis: Redis, key: str, model: type[M]) -> None:
        self._redis = redis
        self._key = key
        self._model = model

    async def push(self, item: M) -> None:
        """Append an item to the head of the queue."""

        await self._redis.lpush(self._key, item.model_dump_json())

    async def pop(self, timeout: int = 0) -> Optional[M]:
        """Block until an item is available, then return it.

        ``timeout`` is in seconds; ``0`` blocks indefinitely. Returns ``None``
        only when a non-zero timeout elapses with the queue still empty.
        """

        entry = await self._redis.brpop(self._key, timeout=timeout)
        if entry is None:
            return None
        _key, payload = entry
        return self._model.model_validate_json(payload)
