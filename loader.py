from aiogram import Bot, Dispatcher

from config import config
from utils.db import Database

bot = Bot(token=config.token)
dp = Dispatcher(bot)
db = Database(f'../{config.database_name}')
