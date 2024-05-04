from ast import literal_eval
from os import remove, mkdir
from urllib.error import HTTPError

from pyrogram import Client, filters, types
from pytube import YouTube
from pytube.innertube import _default_clients

from config import Config
from database import Database

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

BOT_ID = Config.BOT_ID
SESSION_NAME = Config.SESSION_NAME
API_ID = Config.API_ID
API_HASH = Config.API_HASH
DATABASE_NAME = Config.DATABASE_NAME
DOWNLOADING_DIRECTORY = Config.DOWNLOADING_DIRECTORY

app = Client(
    name=SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH
)
db = Database(DATABASE_NAME)

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
    json_data = literal_eval(message.text)
    user_id = json_data['id']
    db.set_status(user_id=user_id, status=1)

    try:
        yt = YouTube(json_data['url'], use_oauth=True, allow_oauth_cache=True)
        video_stream = yt.streams.get_highest_resolution()
        if video_stream.filesize_gb > 2.0:
            raise ValueError('File size is too big')
        filename = f'{json_data["file_name"]}.mp4'

        video_stream.download(output_path=DOWNLOADING_DIRECTORY, filename=filename)
        await app.send_video(
            chat_id=BOT_ID,
            video=open(f'{DOWNLOADING_DIRECTORY}/{filename}', 'rb'),
            caption=message.text
        )
        remove(f'{DOWNLOADING_DIRECTORY}/{filename}')

        db.set_status(user_id=user_id, status=0)
    except (HTTPError, ValueError):
        await app.send_message(chat_id=BOT_ID, text=message.text)

        db.set_status(user_id=user_id, status=0)


app.run()
