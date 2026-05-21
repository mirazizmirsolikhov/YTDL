import pytest
from fakeredis import FakeAsyncRedis

from utils.transport import (
    RESULTS_KEY,
    TASKS_KEY,
    DownloadResult,
    DownloadTask,
    FileCache,
    RedisQueue,
    StatusStore,
)


def _task(**overrides) -> DownloadTask:
    fields = dict(
        url='https://youtu.be/x', video_id='x', user_id=1,
        chat_id=1, status_message_id=1,
    )
    fields.update(overrides)
    return DownloadTask(**fields)


def test_task_json_round_trip():
    task = _task()
    assert DownloadTask.model_validate_json(task.model_dump_json()) == task


def test_result_json_round_trip():
    result = DownloadResult(task=_task(), success=False, error='boom')
    assert DownloadResult.model_validate_json(result.model_dump_json()) == result


@pytest.fixture
def redis() -> FakeAsyncRedis:
    return FakeAsyncRedis(decode_responses=True)


async def test_queue_preserves_fifo_order(redis):
    queue = RedisQueue(redis, TASKS_KEY, DownloadTask)
    first, second = _task(video_id='a'), _task(video_id='b')

    await queue.push(first)
    await queue.push(second)

    assert await queue.pop(timeout=1) == first
    assert await queue.pop(timeout=1) == second


async def test_queue_pop_returns_none_on_timeout(redis):
    queue = RedisQueue(redis, RESULTS_KEY, DownloadResult)
    assert await queue.pop(timeout=1) is None


async def test_status_store_set_and_clear(redis):
    store = StatusStore(redis)

    assert await store.is_busy(7) is False
    await store.set_busy(7)
    assert await store.is_busy(7) is True
    await store.clear(7)
    assert await store.is_busy(7) is False


async def test_file_cache_get_and_save(redis):
    cache = FileCache(redis)

    assert await cache.get('vid') is None
    await cache.save('vid', 'FILE_ID')
    assert await cache.get('vid') == 'FILE_ID'
