from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    admin_id: int
    token: str
    bot_id: int
    host_id: int
    api_id: int
    api_hash: str
    database_name: str = 'users.db'
    session_name: str = 'my_account'
    downloading_directory: str = 'downloads'
    use_proxies: bool = False
