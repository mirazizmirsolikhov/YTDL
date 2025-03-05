from pydantic_settings import BaseSettings


class Config(BaseSettings):
    admin_id: int
    token: str
    bot_id: int
    host_id: int
    api_id: int
    api_hash: str
    database_name: str = 'users.db'
    session_name: str = 'my_account'
    downloading_directory: str = '../downloads'
    minimal_resolution: str = '720'


config = Config(_env_file='../.env')
