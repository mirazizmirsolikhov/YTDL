from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    ADMIN_ID: int = int(getenv('ADMIN_ID'))
    TOKEN: str = getenv('TOKEN')
    BOT_ID: int = int(getenv('BOT_ID'))
    HOST_ID: int = int(getenv('HOST_ID'))
    API_ID: int = int(getenv('API_ID'))
    API_HASH: str = getenv('API_HASH')
    DATABASE_NAME: str = getenv('DATABASE_NAME', default='users.db')
    SESSION_NAME: str = getenv('SESSION_NAME', default='my_account')
    DOWNLOADING_DIRECTORY: str = getenv('DOWNLOADING_DIRECTORY', default='downloads')
