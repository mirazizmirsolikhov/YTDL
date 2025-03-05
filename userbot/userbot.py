import os

from config import config
from loader import app

os.makedirs(config.downloading_directory, exist_ok=True)
os.makedirs(config.session_folder, exist_ok=True)

app.run()
