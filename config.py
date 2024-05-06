from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(
            self,
            admin_id: int,
            token: str,
            bot_id: int,
            host_id: int,
            api_id: int,
            api_hash: str,
            database_name: str,
            session_name: str,
            downloading_directory: str,
    ):
        self.admin_id = admin_id
        self.token = token
        self.bot_id = bot_id
        self.host_id = host_id
        self.api_id = api_id
        self.api_hash = api_hash
        self.database_name = database_name
        self.session_name = session_name
        self.downloading_directory = downloading_directory


settings = Config(
    admin_id=int(getenv('ADMIN_ID')),
    token=getenv('TOKEN'),
    bot_id=int(getenv('BOT_ID')),
    host_id=int(getenv('HOST_ID')),
    api_id=int(getenv('API_ID')),
    api_hash=getenv('API_HASH'),
    database_name=getenv('DATABASE_NAME', default='users.db'),
    session_name=getenv('SESSION_NAME', default='my_account'),
    downloading_directory=getenv('DOWNLOADING_DIRECTORY', default='downloads'),
)
