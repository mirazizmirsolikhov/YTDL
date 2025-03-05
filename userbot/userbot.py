from os import mkdir

from config import config
from loader import app

DOWNLOADING_DIRECTORY: str = config.downloading_directory

try:
    mkdir(DOWNLOADING_DIRECTORY)
except FileExistsError:
    pass

app.run()
