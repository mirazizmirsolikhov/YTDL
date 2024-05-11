import re
from typing import Union, Dict, List

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsCorrectLink(BoundFilter):
    """
    Checks if the YouTube link is correct.
    """
    key: str = 'is_correct_link'

    async def check(self, message: types.Message) -> Union[bool, Dict[str, List[str]]]:
        pattern1: str = r'(?:https?://)?(?:www\.)?youtube\.com/shorts/([A-Za-z0-9_-]+)(?:\?si=[A-Za-z0-9_-]+)?'
        matches1: List[str] = re.findall(pattern1, message.text)
        pattern2: str = r'(?:youtu\.be/|youtube\.com/watch\?v=)([A-Za-z0-9_-]+)'
        matches2: List[str] = re.findall(pattern2, message.text)
        matches: List[str] = matches1 + matches2
        if len(matches) == 0:
            return False
        else:
            return {'matches': matches}
