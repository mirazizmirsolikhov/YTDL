from aiogram import Bot, Dispatcher
from pyrogram import Client

from config import config
from utils.db import Database

bot = Bot(token=config.token)
dp = Dispatcher(bot)
db = Database(f'../{config.database_name}')

app = Client(
    name=config.session_name,
    api_id=config.api_id,
    api_hash=config.api_hash,
    workdir=config.session_folder,
    plugins=dict(root='plugins')
)
