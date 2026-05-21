from aiogram import Bot, Dispatcher
from pyrogram import Client
from redis.asyncio import Redis

from config import config
from utils.db import Database
from utils.transport import (
    RESULTS_KEY,
    TASKS_KEY,
    DownloadResult,
    DownloadTask,
    FileCache,
    RedisQueue,
    StatusStore,
)

bot = Bot(token=config.token)
dp = Dispatcher(bot)
db = Database(str(config.database_path))

app = Client(
    name=config.session_name,
    api_id=config.api_id,
    api_hash=config.api_hash,
    workdir=str(config.session_path),
)

# Shared transport between the bot and the userbot. The connection is lazy —
# established on the first command — so creating the client at import is safe.
redis_client = Redis.from_url(config.redis_url, decode_responses=True)

task_queue: RedisQueue[DownloadTask] = RedisQueue(redis_client, TASKS_KEY, DownloadTask)
result_queue: RedisQueue[DownloadResult] = RedisQueue(redis_client, RESULTS_KEY, DownloadResult)
status_store = StatusStore(redis_client)
file_cache = FileCache(redis_client)
