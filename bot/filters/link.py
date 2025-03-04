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
        pattern1: str = r'(?:https?://)?(?:www\.)?youtube\.com/shorts/([\w\-]+)'
        pattern1_matches: List[str] = re.findall(pattern1, message.text)

        pattern2: str = r'(?:youtu\.be/|youtube\.com/watch\?v=)([\w\-]+)'
        pattern2_matches: List[str] = re.findall(pattern2, message.text)

        matches: List[str] = pattern1_matches + pattern2_matches
        if len(matches) == 0:
            return False
        else:
            return {'matches': matches}
