from pathlib import Path
from typing import Optional

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
    # Optional yt-dlp cookies file (Netscape format), relative to the project
    # root. Needed when YouTube blocks the server IP and demands sign-in.
    cookies_file: str = ''
    # Base URL of the bgutil PO-token provider. When set, yt-dlp fetches
    # YouTube proof-of-origin tokens from it; empty disables the integration.
    pot_provider_url: str = ''

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
    def cookies_path(self) -> Optional[Path]:
        """Absolute path to the yt-dlp cookies file, or None if not configured."""

        return PROJECT_ROOT / self.cookies_file if self.cookies_file else None

    @property
    def redis_url(self) -> str:
        return f'redis://{self.redis_host}:{self.redis_port}/{self.redis_db}'


config = Config(_env_file=PROJECT_ROOT / '.env')
