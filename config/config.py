from pathlib import Path

from pydantic_settings import BaseSettings

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent


class Config(BaseSettings):
    admin_id: int
    token: str
    bot_id: int
    host_id: int
    api_id: int
    api_hash: str
    database_name: str = 'users.db'
    session_name: str = 'my_account'
    session_folder: str = 'sessions'
    downloading_directory: str = 'downloads'
    minimal_resolution: str = '720'

    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 0

    @property
    def project_root(self) -> Path:
        return PROJECT_ROOT

    @property
    def database_path(self) -> Path:
        """Absolute path to the SQLite database, independent of CWD."""

        return PROJECT_ROOT / self.database_name

    @property
    def session_path(self) -> Path:
        """Absolute path to the pyrogram session folder."""

        return PROJECT_ROOT / self.session_folder

    @property
    def downloads_path(self) -> Path:
        """Absolute path to the directory for downloaded videos."""

        return PROJECT_ROOT / self.downloading_directory

    @property
    def redis_url(self) -> str:
        return f'redis://{self.redis_host}:{self.redis_port}/{self.redis_db}'


config = Config(_env_file=PROJECT_ROOT / '.env')
