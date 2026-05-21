import os

from config import config
from loader import app

os.makedirs(config.downloads_path, exist_ok=True)
os.makedirs(config.session_path, exist_ok=True)

app.run()
