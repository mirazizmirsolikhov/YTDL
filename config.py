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


def get_env_variable(var: str, default: str | None = None):
    env = getenv(var)

    if env is None:
        if default is None:
            raise ValueError(f"Missing environment variable: {var}")
        return default
    return env


settings = Config(
    admin_id=int(get_env_variable(var='ADMIN_ID')),
    token=get_env_variable(var='TOKEN'),
    bot_id=int(get_env_variable(var='BOT_ID')),
    host_id=int(get_env_variable(var='HOST_ID')),
    api_id=int(get_env_variable(var='API_ID')),
    api_hash=get_env_variable(var='API_HASH'),
    database_name=get_env_variable(var='DATABASE_NAME', default='users.db'),
    session_name=get_env_variable(var='SESSION_NAME', default='my_account'),
    downloading_directory=get_env_variable(var='DOWNLOADING_DIRECTORY', default='downloads'),
)
