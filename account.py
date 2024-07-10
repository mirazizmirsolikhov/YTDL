from ast import literal_eval
from os import remove, mkdir
from typing import Dict, Union
from urllib.error import HTTPError

from pyrogram import Client, filters, types
from pytube import YouTube, Stream
from pytube.exceptions import VideoUnavailable
from pytube.innertube import _default_clients

from config import settings
from database import Database
from utils import load_proxies

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

BOT_ID: int = settings.bot_id
SESSION_NAME: str = settings.session_name
API_ID: int = settings.api_id
API_HASH: str = settings.api_hash
DATABASE_NAME: str = settings.database_name
DOWNLOADING_DIRECTORY: str = settings.downloading_directory

app: Client = Client(
    name=SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH
)
db: Database = Database(DATABASE_NAME)

try:
    mkdir(DOWNLOADING_DIRECTORY)
except FileExistsError:
    pass


@app.on_message(filters.user(BOT_ID))
async def download(client: Client, message: types.Message) -> None:
    """
    Checks file size. If it is bigger than 2.0 GB, it raises an error.
    Otherwise, the video downloading starts.
    """
    json_data: Dict[str, Union[str, int]] = literal_eval(message.text)
    user_id: int = json_data['id']
    db.set_status(user_id=user_id, status=1)

    try:
        if settings.use_proxies:
            yt: YouTube = YouTube(json_data['url'], use_oauth=True, allow_oauth_cache=True, proxies=load_proxies())
        else:
            yt: YouTube = YouTube(json_data['url'], use_oauth=True, allow_oauth_cache=True)
        video_stream: Stream = yt.streams.get_highest_resolution()
        if video_stream.filesize_gb > 2.0:
            raise ValueError('File size is too big')
        filename: str = f'{json_data["file_name"]}.mp4'

        video_stream.download(output_path=DOWNLOADING_DIRECTORY, filename=filename)
        await app.send_video(
            chat_id=BOT_ID,
            video=open(f'{DOWNLOADING_DIRECTORY}/{filename}', 'rb'),
            caption=message.text
        )
        remove(f'{DOWNLOADING_DIRECTORY}/{filename}')

        db.set_status(user_id=user_id, status=0)
    except (HTTPError, ValueError, VideoUnavailable) as e:
        print(str(e))
        await app.send_message(chat_id=BOT_ID, text=message.text)

        db.set_status(user_id=user_id, status=0)


app.run()
