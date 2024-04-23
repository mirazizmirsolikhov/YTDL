import re

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsCorrectLink(BoundFilter):
    """
    Checks if the YouTube link is correct.
    """
    key = 'is_correct_link'

    async def check(self, message: types.Message):
        pattern1 = r'(?:https?://)?(?:www\.)?youtube\.com/shorts/([A-Za-z0-9_-]+)(?:\?si=[A-Za-z0-9_-]+)?'
        matches1 = re.findall(pattern1, message.text)
        pattern2 = r'(?:youtu\.be/|youtube\.com/watch\?v=)([A-Za-z0-9_-]+)'
        matches2 = re.findall(pattern2, message.text)
        matches = matches1 + matches2
        if len(matches) == 0:
            return False
        else:
            return {'matches': matches}
