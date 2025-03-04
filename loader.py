import os

from aiogram import Bot, Dispatcher

from config import config
from utils.db import Database

DOTENV = os.path.join(os.getcwd(), '.env')

bot = Bot(token=config.token)
dp = Dispatcher(bot)
db = Database(config.database_name)
