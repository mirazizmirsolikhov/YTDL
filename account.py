from __future__ import unicode_literals

from ast import literal_eval
from os import remove, mkdir, getcwd
from pprint import pprint
from typing import Dict, Union

from pyrogram import Client, filters, types
from youtube_dl import YoutubeDL

from config import settings
from database import Database

BOT_ID: int = settings.bot_id
SESSION_NAME: str = settings.session_name
API_ID: int = settings.api_id
API_HASH: str = settings.api_hash
DATABASE_NAME: str = settings.database_name
DOWNLOADING_DIRECTORY: str = settings.downloading_directory
MINIMAL_RESOLUTION: str = settings.minimal_resolution

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
        ytdl = YoutubeDL()
        info = ytdl.extract_info(json_data['url'], download=False)
        formats = info['formats']
        for vd in formats:
            if vd['ext'] == 'mp4' and vd['height'] == int(MINIMAL_RESOLUTION):
                if vd['filesize'] * 0.000001 > 2000:
                    raise ValueError('File size is too big')

        filename: str = f'{json_data["file_name"]}.mp4'
        ydl_opts = {
            'format': f'mp4[format_id=398]+[ext=mp4]',
            'outtmpl': f'{getcwd()}/{DOWNLOADING_DIRECTORY}/{filename}',
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([json_data['url']])

        await app.send_video(
            chat_id=BOT_ID,
            video=open(f'{DOWNLOADING_DIRECTORY}/{filename}', 'rb'),
            caption=message.text
        )
        remove(f'{DOWNLOADING_DIRECTORY}/{filename}')

        db.set_status(user_id=user_id, status=0)
    except Exception as e:
        print(str(e))
        await app.send_message(chat_id=BOT_ID, text=message.text)

        db.set_status(user_id=user_id, status=0)


app.run()
